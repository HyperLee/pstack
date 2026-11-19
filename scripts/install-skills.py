#!/usr/bin/env python3
"""Install pstack without replacing user-owned files. Python 3.9+, POSIX."""
import argparse
from pathlib import Path
import os
import shutil

PAYLOAD = ("README.md", "LICENSE", "skills", "docs", "automations", "scripts", "assets", "tests", "requirements-dev.txt")
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


def install(source, *, project=None, user_home=None, dry_run=False):
    source = Path(source).resolve()
    skills = sorted(p for p in (source / "skills").iterdir() if (p / "SKILL.md").is_file())
    if not skills or not (source / "LICENSE").is_file():
        raise InstallConflict("Source is not a complete pstack suite")
    if project is not None and user_home is not None:
        raise InstallConflict("Choose user or project scope, not both")
    home = Path(user_home) if user_home is not None else Path.home()
    target = Path(project).resolve() if project is not None else home.resolve()
    destination = target / ".agents/skills"
    bundle = target / ".codex/pstack" if project is not None else source
    expected = payload_files(source)
    problems = []
    for directory in (target, target / ".agents", destination):
        if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
            problems.append(str(directory))
    if project is not None:
        parent = target / ".codex"
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            problems.append(str(parent))
        if bundle.is_symlink() or (bundle.exists() and
                                   (not bundle.is_dir() or files_under(bundle) != expected)):
            problems.append(str(bundle))
    links = []
    for skill in skills:
        link = destination / skill.name
        actual = bundle / "skills" / skill.name
        if link.is_symlink() and link.resolve() == actual.resolve():
            continue
        if link.is_symlink() or link.exists():
            problems.append(str(link))
        else:
            links.append((link, actual))
    if problems:
        raise InstallConflict("Existing content differs; nothing changed:\n" + "\n".join(problems))
    if dry_run:
        return [str(link) for link, _ in links]
    if project is not None and not bundle.exists():
        bundle.mkdir(parents=True)
        for relative, data in expected.items():
            output = bundle / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
            output.chmod((source / relative).stat().st_mode & 0o777)
    destination.mkdir(parents=True, exist_ok=True)
    for link, actual in links:
        path = os.path.relpath(actual, link.parent) if project is not None else str(actual)
        link.symlink_to(path, target_is_directory=True)
    return [str(link) for link, _ in links]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--user", action="store_true", help="Link to this clone in ~/.agents/skills")
    scope.add_argument("--project", type=Path, help="Vendor the full suite in a project")
    parser.add_argument("--dry-run", action="store_true", help="Check conflicts and list links without writes")
    args = parser.parse_args()
    try:
        links = install(Path(__file__).resolve().parents[1], project=args.project, dry_run=args.dry_run)
    except (InstallConflict, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print(("Would create" if args.dry_run else "Created") + f" {len(links)} skill links")
    for link in links:
        print(link)
    if args.user:
        print("Keep the source clone at its current location. Re-run to check an existing install.")
    else:
        print("Commit .codex/pstack and .agents/skills together for a portable project install.")


if __name__ == "__main__":
    main()
