#!/usr/bin/env python3
"""Check that a pull request body contains the protocol review contract."""

from __future__ import annotations

import json
import re
import sys


REQUIRED_SECTIONS = (
    "Objective",
    "Scope",
    "Security",
    "Structure and abstraction",
    "Implementation",
    "Verification",
    "Not in scope",
)


def _sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    in_fence = False

    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            heading = re.fullmatch(r"##\s+(.+?)\s*", line.strip())
            if heading:
                current = heading.group(1)
                sections.setdefault(current, [])
                continue
        if current is not None:
            sections[current].append(line)

    return {name: "\n".join(lines) for name, lines in sections.items()}


def _meaningful(text: str) -> bool:
    without_comments = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    without_checkboxes = re.sub(r"^\s*-\s*\[[ xX]\]\s*$", "", without_comments, flags=re.MULTILINE)
    return bool(without_checkboxes.strip())


def missing_sections(body: str) -> list[str]:
    sections = _sections(body)
    return [name for name in REQUIRED_SECTIONS if not _meaningful(sections.get(name, ""))]


def main() -> int:
    missing = missing_sections(sys.stdin.read())
    print(json.dumps(missing, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
