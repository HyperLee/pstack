#!/usr/bin/env python3
"""Locate the complete suite from a copied or symlinked SKILL.md."""
import argparse
import json
from pathlib import Path


def locate(skill):
    folder = Path(skill).resolve()
    if folder.is_file():
        folder = folder.parent
    marker = folder / ".pstack-suite.json"
    if marker.exists():
        relative = json.loads(marker.read_text(encoding="utf-8-sig"))["suite"]
        if not isinstance(relative, str) or Path(relative).is_absolute():
            raise ValueError("Suite marker must contain a relative path")
        suite = (folder / relative).resolve()
    else:
        suite = folder.parents[1]
    if not (suite / "LICENSE").is_file() or not (suite / "skills" / folder.name / "SKILL.md").is_file():
        raise ValueError(f"Incomplete pstack suite at {suite}")
    return suite


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", type=Path)
    args = parser.parse_args()
    try:
        print(locate(args.skill))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, str(error) + "\n")
