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
    "provides utilities for",
    "对应的领域职责",
    "对应的自动化",
    "实现“",
    "仓库支持文件，用于",
    "提供所属包需要的局部实现",
    "完成“所属模块”流程中的内部步骤",
)

HAN_RE = re.compile(r"[\u3400-\u9fff]")
ENGLISH_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z-]{2,}\b")
VALID_SYMBOL_KINDS = {"函数", "方法", "类型", "接口", "类", "变量", "常量", "声明"}
VALID_RELATIONS = {"直接参与", "支撑", "验证", "说明", "不直接参与"}
VALID_TABLE_ACCESS = {"读取", "写入", "读写", "定义", "迁移"}

REQUIRED_DRAWER_LABELS = (
    "这个文件主要做什么",
    "个主要功能中的作用",
    "主要函数、类型和变量",
    "直接涉及的数据表",
    "注册的 HTTP 路由",
    "为什么要使用其他模块",
    "源码设计说明",
    "主要测试场景",
)

REQUIRED_SHELL_MARKERS = (
    'data-atlas-template="codebase-understanding-atlas/v3"',
    'id="atlas-topbar"',
    'id="repository-head"',
    'id="top-directory"',
    'id="content-panel"',
    'id="detail-drawer"',
    'id="search"',
    'id="search-results"',
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def chinese_explanation(value: object, *, min_han: int = 6, max_chars: int = 300) -> bool:
    if not isinstance(value, str) or not value.strip() or len(value) > max_chars:
        return False
    han = len(HAN_RE.findall(value))
    english_words = len(ENGLISH_WORD_RE.findall(value))
    return han >= min_han and english_words <= max(4, han // 2)


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
    if not isinstance(capabilities, list) or not 1 <= len(capabilities) <= 5:
        fail(errors, "capability count must be between 1 and 5")
        capabilities = []
    else:
        for capability in capabilities:
            if not (
                isinstance(capability, dict)
                and isinstance(capability.get("id"), str)
                and capability["id"].strip()
                and all(chinese_explanation(capability.get(key), min_han=3, max_chars=240) for key in ("name", "trigger", "outcome"))
            ):
                fail(errors, "every capability requires a Chinese name, trigger, and outcome")
                break

    for marker in REQUIRED_SHELL_MARKERS:
        if marker not in html:
            fail(errors, f"missing mandatory atlas shell marker: {marker}")
    for label in REQUIRED_DRAWER_LABELS:
        if label not in html:
            fail(errors, f"missing mandatory Chinese drawer section: {label}")
    visual_tokens = ("--bg:#f6f8fa", ".repo-head{", ".layout{", ".summary{", ".filebox{", ".row{")
    for token in visual_tokens:
        if token not in html:
            fail(errors, f"missing mandatory GitHub-style visual token: {token}")
    if 'class="hero"' in html or 'id="capability-hero"' in html:
        fail(errors, "oversized capability hero is not part of the primary repository-browser shell")

    counts = data.get("counts")
    embedded_dirs = {path for path, item in entries.items() if isinstance(item, dict) and item.get("kind") == "dir"}
    counted_dirs = embedded_dirs - {"", "."}
    if not isinstance(counts, dict) or counts.get("files") != len(files) or counts.get("dirs") != len(counted_dirs):
        fail(errors, "embedded file/directory counts do not match entries")

    for path in sorted(embedded_dirs):
        description = entries[path].get("description")
        if not chinese_explanation(description, min_han=4, max_chars=360):
            fail(errors, f"directory description is empty, English-heavy, or not concise Chinese: {path or '/'}")

    role_counts: set[int] = set()
    for path in sorted(files):
        item = entries[path]
        description = item.get("description")
        if not chinese_explanation(description, min_han=8, max_chars=420):
            fail(errors, f"file description is empty, English-heavy, or not concise Chinese: {path}")
            continue
        lowered = description.lower()
        for phrase in VAGUE_PATTERNS:
            if phrase.lower() in lowered:
                fail(errors, f"vague description phrase {phrase!r}: {path}")

        purpose = item.get("purpose")
        if not isinstance(purpose, dict) or not all(
            chinese_explanation(purpose.get(key), min_han=6, max_chars=240)
            for key in ("summary", "when", "effect")
        ):
            fail(errors, f"missing or non-Chinese structured purpose: {path}")

        roles = item.get("coreRoles")
        if not isinstance(roles, list) or not roles:
            fail(errors, f"missing core capability roles: {path}")
        else:
            role_counts.add(len(roles))
            if capabilities and len(roles) != len(capabilities):
                fail(errors, f"capability-card count does not match discovered capabilities: {path}")
            for role in roles:
                if not (
                    isinstance(role, dict)
                    and isinstance(role.get("name"), str)
                    and role["name"].strip()
                    and role.get("relation") in VALID_RELATIONS
                    and chinese_explanation(role.get("description"), min_han=5, max_chars=280)
                ):
                    fail(errors, f"incomplete, English-heavy, or invalid core role: {path}")
                    break

        dependencies = item.get("dependencies", [])
        if not isinstance(dependencies, list):
            fail(errors, f"dependencies is not a list: {path}")
        else:
            for dependency in dependencies:
                if not (
                    isinstance(dependency, dict)
                    and dependency.get("name")
                    and chinese_explanation(dependency.get("purpose"), min_han=5, max_chars=240)
                ):
                    fail(errors, f"dependency without concise Chinese purpose explanation: {path}")
                    break

        details = item.get("symbolDetails", [])
        if not isinstance(details, list):
            fail(errors, f"symbolDetails is not a list: {path}")
        else:
            if item.get("symbols") and not details:
                fail(errors, f"declarations were detected but no main function/type/variable was explained: {path}")
            for detail in details:
                if not (
                    isinstance(detail, dict)
                    and detail.get("name")
                    and detail.get("kind") in VALID_SYMBOL_KINDS
                    and chinese_explanation(detail.get("description"), min_han=4, max_chars=240)
                ):
                    fail(errors, f"displayed declaration lacks kind or concise Chinese explanation: {path}")
                    break

        tables = item.get("tables")
        if not isinstance(tables, list):
            fail(errors, f"tables is not a list: {path}")
        else:
            for table in tables:
                if not (
                    isinstance(table, dict)
                    and table.get("name")
                    and chinese_explanation(table.get("display"), min_han=2, max_chars=80)
                    and table.get("access") in VALID_TABLE_ACCESS
                    and chinese_explanation(table.get("purpose"), min_han=4, max_chars=200)
                ):
                    fail(errors, f"table lacks Chinese fact name, access mode, or purpose: {path}")
                    break

        routes = item.get("routes")
        if not isinstance(routes, list):
            fail(errors, f"routes is not a list: {path}")
        else:
            for route in routes:
                if not (
                    isinstance(route, dict)
                    and route.get("method")
                    and route.get("path")
                    and chinese_explanation(route.get("description"), min_han=4, max_chars=200)
                ):
                    fail(errors, f"route lacks a concise Chinese explanation: {path}")
                    break

        tests = item.get("tests")
        if not isinstance(tests, list):
            fail(errors, f"tests is not a list: {path}")
        else:
            for test in tests:
                if not (
                    isinstance(test, dict)
                    and test.get("name")
                    and chinese_explanation(test.get("description"), min_han=4, max_chars=240)
                ):
                    fail(errors, f"test lacks a concise Chinese behavior explanation: {path}")
                    break

        design_notes = item.get("designNotes")
        if not isinstance(design_notes, list):
            fail(errors, f"designNotes is not a list: {path}")
        else:
            for note in design_notes:
                if not chinese_explanation(note, min_han=5, max_chars=280):
                    fail(errors, f"source design note is English-heavy or not concise Chinese: {path}")
                    break
        if item.get("sourceComment") and not design_notes:
            fail(errors, f"source comment exists but has no Chinese designNotes translation: {path}")

    if len(role_counts) > 1:
        fail(errors, f"files have inconsistent capability-card counts: {sorted(role_counts)}")
    if role_counts and not 1 <= next(iter(role_counts)) <= 5:
        fail(errors, "each file must have 1–5 capability cards")

    glossary = data.get("glossary", [])
    if not isinstance(glossary, list):
        fail(errors, "glossary is not a list")
    else:
        for term in glossary:
            if not (
                isinstance(term, dict)
                and (term.get("code") or term.get("name"))
                and chinese_explanation(term.get("meaning") or term.get("description"), min_han=3, max_chars=240)
            ):
                fail(errors, "glossary term lacks a concise Chinese explanation")
                break

    modules = data.get("modules", {})
    if not isinstance(modules, dict):
        fail(errors, "modules is not an object")
    else:
        for code_name, module in modules.items():
            if not isinstance(module, dict) or not all(
                chinese_explanation(module.get(key), min_han=3, max_chars=500)
                for key in ("name", "owns", "usedFor", "doesNotOwn")
            ):
                fail(errors, f"incomplete or English-heavy module glossary entry: {code_name}")

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
