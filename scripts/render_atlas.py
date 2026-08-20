#!/usr/bin/env python3
"""Render atlas evidence JSON with the mandatory Codebase Understanding Atlas shell."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MARKER = "__ATLAS_JSON__"


def die(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def validate(data: object) -> dict:
    if not isinstance(data, dict):
        die("atlas data must be a JSON object")
    entries = data.get("entries")
    capabilities = data.get("capabilities")
    if not isinstance(entries, dict) or not entries:
        die("atlas data must contain a non-empty entries object")
    if not isinstance(capabilities, list) or not 1 <= len(capabilities) <= 5:
        die("atlas data must contain 1–5 capabilities")
    if not any(isinstance(item, dict) and item.get("kind") == "dir" for item in entries.values()):
        die("entries must contain at least one directory")
    if not any(isinstance(item, dict) and item.get("kind") == "file" for item in entries.values()):
        die("entries must contain at least one file")

    for capability in capabilities:
        if not isinstance(capability, dict) or not all(
            isinstance(capability.get(key), str) and capability[key].strip()
            for key in ("id", "name", "trigger", "outcome")
        ):
            die("every capability requires id, name, trigger, and outcome")
        capability.setdefault("summary", capability["outcome"])

    files = 0
    dirs = 0
    for path, item in entries.items():
        if not isinstance(path, str) or not isinstance(item, dict):
            die("every entry must map a string path to an object")
        item.setdefault("path", path)
        if item.get("kind") == "file":
            files += 1
        elif item.get("kind") == "dir":
            if path not in ("", "."):
                dirs += 1
        else:
            die(f"entry has invalid kind: {path}")
    data["counts"] = {**(data.get("counts") or {}), "files": files, "dirs": dirs}
    data.setdefault("repository", {})
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path, help="atlas evidence JSON")
    parser.add_argument("--output", required=True, type=Path, help="standalone HTML output")
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "templates" / "atlas-shell.html",
    )
    args = parser.parse_args()

    try:
        data = validate(json.loads(args.data.read_text(encoding="utf-8")))
        template = args.template.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if template.count(MARKER) != 1:
        die(f"template must contain exactly one {MARKER} marker")

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Prevent an embedded filename or comment from terminating the JSON script node.
    payload = payload.replace("</", "<\\/").replace("<!--", "<\\!--")
    output = template.replace(MARKER, payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(json.dumps({"output": str(args.output), "files": data["counts"]["files"], "dirs": data["counts"]["dirs"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
