#!/usr/bin/env python3
"""Validate manual Benny source coordinates. Does not contact Slack or post."""
import argparse
import json
from pathlib import Path
import re


def validate(source, expected_channel):
    if not isinstance(source, dict) or not isinstance(expected_channel, str) or not expected_channel:
        raise ValueError("Supply source coordinates and a configured source channel")
    if source.get("channel_id") != expected_channel:
        raise ValueError("source.channel_id does not match the configured source channel")
    for field in ("thread_ts", "message_ts"):
        value = source.get(field)
        if not isinstance(value, str) or re.fullmatch(r"\d+\.\d+", value) is None:
            raise ValueError("source." + field + " must be a Slack timestamp string")
    if "permalink" in source and not isinstance(source["permalink"], str):
        raise ValueError("source.permalink must be a string")
    return dict(source)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--channel", required=True)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.file.read_text(encoding="utf-8-sig")), args.channel)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
