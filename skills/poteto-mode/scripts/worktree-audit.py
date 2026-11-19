#!/usr/bin/env python3
"""Read local worktree facts without fetching refs, reading private chats or deleting files."""
import argparse
from pathlib import Path
import json
import shutil
import subprocess
import time


def command(args, cwd):
    try:
        return subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    except OSError as error:
        return subprocess.CompletedProcess(args, 2, stdout="", stderr=str(error))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-b", "--base")
    parser.add_argument("--offline", action="store_true", help="Do not query PR state")
    parser.add_argument("repo", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    listing = command(["git", "worktree", "list", "--porcelain", "-z"], repo)
    if listing.returncode:
        parser.exit(1, listing.stderr)
    base = args.base
    if base is None:
        symbolic = command(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"], repo)
        for candidate in (symbolic.stdout.strip(), "origin/main", "origin/master"):
            if candidate and command(["git", "rev-parse", "--verify", candidate+"^{commit}"], repo).returncode == 0:
                base = candidate
                break
    if not base or command(["git", "rev-parse", "--verify", base+"^{commit}"], repo).returncode:
        parser.exit(1, "No valid local base ref. Pass --base REF; this audit never fetches.\n")
    prs = []
    if not args.offline and shutil.which("gh"):
        response = command(["gh", "pr", "list", "--state", "all", "--limit", "1000", "--json", "number,state,headRefName"], repo)
        if response.returncode == 0:
            try:
                prs = json.loads(response.stdout)
            except ValueError:
                pass
    print("# Local refs only; merge/PR facts are inventory, never deletion permission. Base: " + base)
    print("SIZE\tAGE\tMERGED\tDIRTY\tPR\tACTIVITY\tBUCKET\tWORKTREE")
    for block in listing.stdout.split("\0\0"):
        fields = dict(item.split(" ", 1) for item in block.split("\0") if " " in item)
        if "worktree" not in fields:
            continue
        worktree = Path(fields["worktree"])
        status = command(["git", "status", "--porcelain"], worktree)
        dirty = "unknown" if status.returncode else ("dirty" if status.stdout else "clean")
        merge_code = command(["git", "merge-base", "--is-ancestor", fields.get("HEAD", "HEAD"), base], repo).returncode
        merged = {0: "yes", 1: "no"}.get(merge_code, "unknown")
        stamp = command(["git", "log", "-1", "--format=%ct"], worktree).stdout.strip()
        age = str(max(0, int((time.time()-int(stamp))/86400)))+"d" if stamp.isdigit() else "unknown"
        size = (command(["du", "-sh", str(worktree)], repo).stdout.split("\t", 1)[0].strip() if shutil.which("du") else "") or "unknown"
        branch = fields.get("branch", "").removeprefix("refs/heads/")
        pr = next(("#"+str(p["number"])+"/"+p["state"] for p in prs if p.get("headRefName")==branch), "unknown")
        bucket = "hold-unavailable" if dirty == "unknown" else "hold-wip" if dirty != "clean" else "manual-review"
        print("\t".join((size,age,merged,dirty,pr,"unknown",bucket,str(worktree))))


if __name__ == "__main__":
    main()
