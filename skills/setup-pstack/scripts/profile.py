#!/usr/bin/env python3
"""Validate a pstack profile or load the project/personal profile. No writes."""
import argparse
import json
from pathlib import Path

PANELS = {"arena runners", "arena cross-judge pool", "interrogate reviewers"}
ROLES = PANELS | {"feature, refactoring", "bug-fix", "perf-issue", "hillclimb",
                  "judgment and prose", "swarm workers"}
EFFORTS = {"inherit", "low", "medium", "high", "xhigh"}


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("Profile must be a JSON object")
    unknown = set(data) - {"schema_version", "budget", "max_workers", "roles"}
    if unknown:
        raise ValueError("Unknown profile fields: " + ", ".join(sorted(unknown)))
    result = {"schema_version": 1, "budget": "inherit", "max_workers": 3, "roles": {}}
    result.update(data)
    if type(result["schema_version"]) is not int or result["schema_version"] != 1:
        raise ValueError("schema_version must be 1")
    if result["budget"] not in ("inherit", "small", "medium", "large"):
        raise ValueError("budget must be inherit, small, medium or large")
    if type(result["max_workers"]) is not int or result["max_workers"] < 1:
        raise ValueError("max_workers must be a positive integer")
    roles = result["roles"]
    if not isinstance(roles, dict) or set(roles) - ROLES:
        raise ValueError("roles must map known pstack role names to settings")
    for role, value in roles.items():
        choices = value if role in PANELS else [value]
        if not isinstance(choices, list) or not choices:
            raise ValueError(role + " requires a nonempty list")
        for choice in choices:
            if not isinstance(choice, dict) or set(choice) - {"model", "reasoning_effort"}:
                raise ValueError(role + " requires model/reasoning_effort objects")
            model = choice.get("model", "inherit-parent")
            if not isinstance(model, str) or not model.strip():
                raise ValueError(role + ": model must be a nonempty string")
            effort = choice.get("reasoning_effort", "inherit")
            if not isinstance(effort, str) or effort not in EFFORTS:
                raise ValueError(role + ": unsupported reasoning_effort")
    return result


def load(project, personal=None):
    paths = [Path(project) / ".codex/pstack.json",
             Path(personal) if personal is not None else Path.home() / ".codex/pstack.json"]
    for path in paths:
        if path.exists():
            try:
                return validate(json.loads(path.read_text(encoding="utf-8-sig"))), path
            except (ValueError, OSError) as error:
                raise ValueError(str(path) + ": " + str(error)) from error
    return validate({}), None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        if args.file:
            result = validate(json.loads(args.file.read_text(encoding="utf-8-sig")))
        else:
            result, _ = load(args.project)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
