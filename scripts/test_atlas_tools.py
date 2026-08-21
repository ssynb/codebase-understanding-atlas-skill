#!/usr/bin/env python3
"""Behavior tests for the mandatory atlas renderer and content audit."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RENDER = ROOT / "scripts" / "render_atlas.py"
AUDIT = ROOT / "scripts" / "audit_atlas.py"
DRAWER_LABELS = (
    "这个文件主要做什么",
    "主要函数、类型和变量",
    "直接涉及的数据表",
    "源码设计说明",
)


def role(relation: str, description: str) -> dict:
    return {"id": "run", "name": "运行示例任务", "relation": relation, "description": description}


def fixture_data() -> dict:
    empty_lists = {"tables": [], "routes": [], "dependencies": [], "designNotes": [], "tests": []}
    return {
        "repository": {"name": "fixture", "fullName": "example/fixture", "title": "示例仓库", "branch": "main"},
        "revision": "1234567890",
        "capabilities": [{
            "id": "run",
            "name": "运行示例任务",
            "trigger": "用户启动示例程序并提交一项任务。",
            "outcome": "程序完成任务并向用户返回明确结果。",
        }],
        "modules": {"app": {
            "name": "app（示例程序）",
            "owns": "负责执行示例任务并返回运行结果。",
            "usedFor": "其他入口使用它获得统一的任务执行能力。",
            "doesNotOwn": "不负责保存用户资料或管理外部系统。",
        }},
        "glossary": [],
        "entries": {
            "": {
                "kind": "dir", "name": "fixture", "display": "fixture（示例仓库）",
                "description": "用于验证代码库地图渲染与中文内容审计。", "children": ["src", "README.md"],
            },
            "src": {
                "kind": "dir", "name": "src", "display": "src（程序源码）",
                "description": "保存示例程序真正执行任务的源代码。", "children": ["src/main.py"],
            },
            "README.md": {
                "kind": "file", "name": "README.md", "display": "README.md（使用说明）",
                "description": "向新成员说明示例仓库的用途和基本运行方式。",
                "purpose": {
                    "summary": "帮助第一次接触仓库的人快速知道项目用途。",
                    "when": "新成员开始阅读代码或准备运行项目时查看。",
                    "effect": "读者打开文档后获得项目定位和最短使用步骤。",
                },
                "coreRoles": [role("说明", "只解释任务如何启动，不参与程序的实际执行。")],
                "symbols": [], "symbolDetails": [], **empty_lists, "ext": ".md", "size": 9, "lines": 1,
            },
            "src/main.py": {
                "kind": "file", "name": "main.py", "display": "main.py（程序入口）",
                "description": "接收启动命令，执行示例任务并把结果打印给用户。",
                "purpose": {
                    "summary": "作为示例程序的唯一启动入口，组织一次完整执行。",
                    "when": "用户从命令行启动程序并要求执行示例任务时使用。",
                    "effect": "接收启动动作，运行任务，最后向标准输出写出成功结果。",
                },
                "coreRoles": [role("直接参与", "负责启动任务、执行主步骤并返回用户能看到的结果。")],
                "symbols": ["main"],
                "symbolDetails": [{
                    "name": "main", "kind": "函数",
                    "description": "启动示例任务，完成后把明确结果打印到标准输出。",
                }],
                "tables": [{
                    "name": "task_run", "display": "任务运行记录", "access": "读写",
                    "purpose": "任务开始时保存输入，结束后写回状态和结果。",
                }],
                "routes": [{
                    "method": "POST", "path": "/tasks",
                    "description": "接收用户提交的新任务并返回任务编号。",
                }],
                "dependencies": [],
                "designNotes": ["入口保持单一职责，只负责串起任务执行和结果输出。"],
                "tests": [{
                    "name": "test_main_prints_result",
                    "description": "验证任务完成后会向用户输出明确结果。",
                }],
                "ext": ".py", "size": 28, "lines": 2,
            },
        },
    }


class AtlasToolsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        (self.repo / "src").mkdir()
        (self.repo / "README.md").write_text("# 示例\n", encoding="utf-8")
        (self.repo / "src/main.py").write_text('def main():\n    print("ok")\n', encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "add", "README.md", "src/main.py"], check=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def render(self, data: dict) -> Path:
        data_path = self.repo / "atlas-data.json"
        html_path = self.repo / "repository-browser.html"
        data_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        subprocess.run(["python3", str(RENDER), "--data", str(data_path), "--output", str(html_path)], check=True)
        return html_path

    def audit(self, html: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(AUDIT), "--repo", str(self.repo), "--html", str(html)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def test_renderer_keeps_mandatory_chinese_drawer(self) -> None:
        html = self.render(fixture_data())
        result = self.audit(html)
        self.assertEqual(result.returncode, 0, result.stderr)
        source = html.read_text(encoding="utf-8")
        for label in DRAWER_LABELS:
            self.assertIn(label, source)

    def test_audit_rejects_english_heavy_explanation(self) -> None:
        data = fixture_data()
        data["entries"]["src/main.py"]["description"] = (
            "文档说明。This module handles application orchestration, runtime dispatch, "
            "dependency management, and execution state transitions."
        )
        html = self.render(data)
        result = self.audit(html)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("English-heavy", result.stderr)


if __name__ == "__main__":
    unittest.main()
