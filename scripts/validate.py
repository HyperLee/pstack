#!/usr/bin/env python3
"""Validate the complete Codex suite, metadata, local links and retired dependencies."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

try:
    import yaml
except ImportError:
    raise SystemExit("Install the developer requirements first: python3 -m pip install -r requirements-dev.txt")

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    operational = sorted((root / "automations/benny/skills").glob("*/SKILL.md"))
    if len(skills) != 58 or len(operational) != 3:
        errors.append("Expected 58 discoverable skills and 3 direct-read Benny operational files")
    if len(list((root / "skills").glob("principle-*/SKILL.md"))) != 24:
        errors.append("Expected 24 principle skills")
    if len(list((root / "skills/poteto-mode/playbooks").glob("*.md"))) != 22:
        errors.append("Expected 22 playbooks")
    for p in skills + operational:
        label = str(p.relative_to(root))
        try:
            parts = p.read_text().split("---", 2)
            assert len(parts) == 3 and not parts[0].strip(), "missing frontmatter"
            fm = yaml.safe_load(parts[1])
            assert isinstance(fm, dict), "frontmatter must be a map"
            assert not set(fm) - {"name", "description", "metadata", "license", "allowed-tools"}, "unsupported frontmatter"
            assert fm.get("name") == p.parent.name, "name/folder mismatch"
            assert re.fullmatch(r"[a-z0-9-]{1,64}", fm["name"]), "invalid name"
            assert isinstance(fm.get("description"), str) and 0 < len(fm["description"]) <= 1024, "invalid description"
            if p in skills:
                ui = yaml.safe_load((p.parent / "agents/openai.yaml").read_text())
                interface = ui["interface"]
                assert interface.get("display_name"), "missing display_name"
                assert 25 <= len(interface["short_description"]) <= 64, "short_description must be 25–64 characters"
                assert "$" + fm["name"] in interface["default_prompt"], "prompt must mention its skill"
                assert ui["policy"]["allow_implicit_invocation"] == (fm["name"] == "setup-pstack"), "invocation policy drift"
        except (AssertionError, KeyError, OSError, ValueError, TypeError, yaml.YAMLError) as error:
            errors.append(label + ": " + str(error))
    files = [root / "README.md"]
    for directory in ("skills", "docs", "automations"):
        files.extend(p for p in (root / directory).rglob("*.md")
                     if "corpus" not in p.parts and "node_modules" not in p.parts)
    banned = ("~/.cursor/", ".cursor/skills/", ".cursor/settings.json", "api2.cursor.sh",
              "subagent_type:", "run_in_background:", "SendToUser", "update_state")
    for p in files:
        text = p.read_text()
        for token in banned:
            if token in text:
                errors.append(str(p.relative_to(root)) + ": retired dependency " + token)
        prose = re.sub(r"```[\s\S]*?```", "", text)
        for match in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)\)", prose):
            ref = unquote(match[1].strip("<>"))
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", ref) or "{{" in ref:
                continue
            file_part, _, anchor = ref.partition("#")
            target = (p.parent / file_part).resolve() if file_part else p
            if not target.exists():
                errors.append(str(p.relative_to(root)) + ": missing link " + ref)
            elif anchor and target.is_file() and target.suffix == ".md":
                headings = set()
                for title in re.findall(r"^#{1,6}\s+(.+)$", target.read_text(), re.M):
                    headings.add(re.sub(r"[^\w\-\s]", "", title.lower()).replace(" ", "-"))
                if anchor not in headings:
                    errors.append(str(p.relative_to(root)) + ": missing heading " + ref)
    for path in ("plugin.json", ".cursor-plugin/plugin.json", "docs/harness/claude-code.md"):
        if (root / path).exists():
            errors.append("Retired entry point remains: " + path)
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("Validated 58 Codex skills, 3 Benny files, 22 playbooks, UI policies and local references")
