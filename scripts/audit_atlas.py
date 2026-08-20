#!/usr/bin/env python3
"""Audit a generated codebase-understanding atlas against its source repository."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DATA_RE = re.compile(
    r'<script\s+id=["\']data["\']\s+type=["\']application/json["\']>(.*?)</script>',
    re.DOTALL,
)
VAGUE_PATTERNS = (
    "implements the responsibility corresponding to",
    "automation for",
    "handles the corresponding domain responsibility",
    "对应的领域职责",
    "对应的自动化",
    "实现“",
    "仓库支持文件，用于",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def tracked_files(repo: Path) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "-z"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("Git tracked-file inventory is unavailable") from exc
    return {item.decode("utf-8", "surrogateescape") for item in result.stdout.split(b"\0") if item}


def load_data(html_path: Path) -> tuple[str, dict]:
    html = html_path.read_text(encoding="utf-8")
    match = DATA_RE.search(html)
    if not match:
        raise RuntimeError('Missing <script id="data" type="application/json"> block')
    return html, json.loads(match.group(1))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--html", required=True, type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    try:
        expected = tracked_files(args.repo.resolve())
        html, data = load_data(args.html.resolve())
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    entries = data.get("entries")
    if not isinstance(entries, dict):
        print("ERROR: embedded data has no entries object", file=sys.stderr)
        return 2

    files = {path for path, item in entries.items() if isinstance(item, dict) and item.get("kind") == "file"}
    missing = sorted(expected - files)
    extra = sorted(files - expected)
    if missing:
        fail(errors, f"{len(missing)} tracked files are missing; first: {missing[:5]}")
    if extra:
        fail(errors, f"{len(extra)} embedded files are not tracked; first: {extra[:5]}")

    capabilities = data.get("capabilities")
    if capabilities is not None and not 1 <= len(capabilities) <= 5:
        fail(errors, "capability count must be between 1 and 5")

    role_counts: set[int] = set()
    for path in sorted(files):
        item = entries[path]
        description = item.get("description")
        if not isinstance(description, str) or not description.strip():
            fail(errors, f"empty file description: {path}")
            continue
        lowered = description.lower()
        for phrase in VAGUE_PATTERNS:
            if phrase.lower() in lowered:
                fail(errors, f"vague description phrase {phrase!r}: {path}")

        roles = item.get("coreRoles")
        if not isinstance(roles, list) or not roles:
            fail(errors, f"missing core capability roles: {path}")
        else:
            role_counts.add(len(roles))
            for role in roles:
                if not all(isinstance(role.get(key), str) and role[key].strip() for key in ("name", "relation", "description")):
                    fail(errors, f"incomplete core role: {path}")
                    break

        details = item.get("symbolDetails", [])
        if not isinstance(details, list):
            fail(errors, f"symbolDetails is not a list: {path}")
        else:
            for detail in details:
                if not isinstance(detail, dict) or not detail.get("name") or not detail.get("description"):
                    fail(errors, f"unexplained displayed declaration: {path}")
                    break

    if len(role_counts) > 1:
        fail(errors, f"files have inconsistent capability-card counts: {sorted(role_counts)}")
    if role_counts and not 1 <= next(iter(role_counts)) <= 5:
        fail(errors, "each file must have 1–5 capability cards")

    if re.search(r">\s*(?:Full path|完整路径)\s*<", html, re.IGNORECASE):
        fail(errors, "a redundant full-path section is present")

    if errors:
        print("Atlas audit failed:", file=sys.stderr)
        for error in errors[:100]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 100:
            print(f"- ... and {len(errors) - 100} more", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "tracked_files": len(expected),
                "embedded_files": len(files),
                "capability_cards_per_file": next(iter(role_counts), 0),
                "status": "ok",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
