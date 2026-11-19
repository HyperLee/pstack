#!/usr/bin/env python3
"""Append one safe UTF-8 TSV decision row. Artifacts are never removed."""
import argparse
from datetime import datetime, timezone
from pathlib import Path


def clean(value):
    value = value.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    return "'" + value if value.startswith(("=", "+", "-", "@")) else value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logfile", type=Path)
    for column in ("phase", "decision", "why", "evidence", "result"):
        parser.add_argument(column)
    args = parser.parse_args()
    args.logfile.parent.mkdir(parents=True, exist_ok=True)
    header = not args.logfile.exists() or args.logfile.stat().st_size == 0
    with args.logfile.open("a", encoding="utf-8", newline="") as stream:
        if header:
            stream.write("ts\tphase\tdecision\twhy\tevidence\tresult\n")
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        stream.write("\t".join([stamp] + [clean(getattr(args, name)) for name in
                                         ("phase", "decision", "why", "evidence", "result")]) + "\n")


if __name__ == "__main__":
    main()
