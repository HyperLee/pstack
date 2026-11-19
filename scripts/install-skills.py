#!/usr/bin/env python3
"""Install pstack without replacing user-owned files. Python 3.9+, Windows/POSIX."""
import argparse
from pathlib import Path
import os
import json
import stat

PAYLOAD = ("README.md", "LICENSE", ".gitattributes", "skills", "docs", "automations", "scripts", "assets", "tests", "requirements-dev.txt")
IGNORED = {"node_modules", "__pycache__", ".DS_Store"}


class InstallConflict(RuntimeError):
    pass


def files_under(root):
    return {p.relative_to(root): p.read_bytes() for p in root.rglob("*")
            if p.is_file() and not any(part in IGNORED for part in p.relative_to(root).parts)
            and not p.name.endswith((".log", ".pyc"))}


def payload_files(source):
    result = {}
    for name in PAYLOAD:
        item = source / name
        if item.is_dir():
            result.update({Path(name) / rel: data for rel, data in files_under(item).items()})
        elif item.is_file():
            result[Path(name)] = item.read_bytes()
    return result


def is_link(path):
    if path.is_symlink() or getattr(os.path, "isjunction", lambda p: False)(path):
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def marker_bytes(skill, bundle):
    return (json.dumps({"suite": Path(os.path.relpath(bundle, skill)).as_posix()},
                       ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def install(source, *, project=None, user_home=None, dry_run=False, mode=None):
    mode = mode or ("copy" if os.name == "nt" else "symlink")
    if mode not in ("copy", "symlink"):
        raise InstallConflict("Mode must be copy or symlink")
    source = Path(source).resolve()
    skills = sorted(p for p in (source / "skills").iterdir() if (p / "SKILL.md").is_file())
    if not skills or not (source / "LICENSE").is_file():
        raise InstallConflict("Source is not a complete pstack suite")
    if project is not None and user_home is not None:
        raise InstallConflict("Choose user or project scope, not both")
    home = Path(user_home) if user_home is not None else Path.home()
    target = Path(project).resolve() if project is not None else home.resolve()
    destination = target / ".agents/skills"
    bundled = project is not None or mode == "copy"
    bundle = target / ".codex/pstack" if bundled else source
    expected = payload_files(source)
    problems = []
    for directory in (target, target / ".agents", destination):
        if is_link(directory) or (directory.exists() and not directory.is_dir()):
            problems.append(str(directory))
    if bundled:
        parent = target / ".codex"
        if is_link(parent) or (parent.exists() and not parent.is_dir()):
            problems.append(str(parent))
        if is_link(bundle) or (bundle.exists() and
                                   (not bundle.is_dir() or files_under(bundle) != expected)):
            problems.append(str(bundle))
    links = []
    for skill in skills:
        link = destination / skill.name
        actual = bundle / "skills" / skill.name
        copied = files_under(skill)
        copied[Path(".pstack-suite.json")] = marker_bytes(link, bundle)
        copied[Path(".gitattributes")] = b"* text=auto eol=lf\n"
        if mode == "copy" and not is_link(link) and link.is_dir() and files_under(link) == copied:
            continue
        if mode == "symlink" and link.is_symlink() and link.resolve() == actual.resolve():
            continue
        if is_link(link) or link.exists():
            problems.append(str(link))
        else:
            links.append((link, actual))
    if problems:
        raise InstallConflict("Existing content differs; nothing changed:\n" + "\n".join(problems))
    if dry_run:
        return [str(link) for link, _ in links]
    if bundled and not bundle.exists():
        try:
            bundle.mkdir(parents=True)
            for relative, data in expected.items():
                output = bundle / relative
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(data)
                if os.name != "nt":
                    output.chmod((source / relative).stat().st_mode & 0o777)
        except OSError as error:
            raise InstallConflict(f"Bundle write stopped: {error}. Artifacts retained in {bundle}; "
                                  "inspect before retrying; no cleanup was performed.") from error
    destination.mkdir(parents=True, exist_ok=True)
    for link, actual in links:
        try:
            if mode == "copy":
                for relative, data in files_under(actual).items():
                    output = link / relative
                    output.parent.mkdir(parents=True, exist_ok=True)
                    output.write_bytes(data)
                    if os.name != "nt":
                        output.chmod((actual / relative).stat().st_mode & 0o777)
                (link / ".pstack-suite.json").write_bytes(marker_bytes(link, bundle))
                (link / ".gitattributes").write_bytes(b"* text=auto eol=lf\n")
            else:
                path = os.path.relpath(actual, link.parent) if project is not None else str(actual)
                link.symlink_to(path, target_is_directory=True)
        except OSError as error:
            raise InstallConflict(f"Install stopped at {link}: {error}. "
                                  f"Existing artifacts retained in {destination} and {bundle}; "
                                  "inspect them before retrying. On Windows prefer --mode copy.") from error
    return [str(link) for link, _ in links]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--user", action="store_true", help="Link to this clone in ~/.agents/skills")
    scope.add_argument("--project", type=Path, help="Vendor the full suite in a project")
    parser.add_argument("--dry-run", action="store_true", help="Check conflicts and list links without writes")
    parser.add_argument("--mode", choices=("copy", "symlink"),
                        default="copy" if os.name == "nt" else "symlink",
                        help="Windows defaults to physical copies; POSIX defaults to links")
    args = parser.parse_args()
    try:
        links = install(Path(__file__).resolve().parents[1], project=args.project,
                        dry_run=args.dry_run, mode=args.mode)
    except (InstallConflict, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print(("Would create" if args.dry_run else "Created") + f" {len(links)} skill entries ({args.mode})")
    for link in links:
        print(link)
    if args.user and args.mode == "symlink":
        print("Keep the source clone at its current location. Re-run to check an existing install.")
    else:
        print("Commit .codex/pstack and .agents/skills together for a portable project install.")


if __name__ == "__main__":
    main()
