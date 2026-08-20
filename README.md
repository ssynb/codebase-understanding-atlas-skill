# Codebase Understanding Atlas Skill

An [Agent Skills](https://agentskills.io/) compatible workflow for turning an unfamiliar software repository into an evidence-based, interactive HTML atlas.

It helps coding agents explain a system from user-visible capabilities down to modules, files, declarations, dependencies, routes, storage, and tests—without reducing descriptions to paraphrased filenames or unexplained technical names.

[中文说明](#中文说明) · [English](#english)

## 中文说明

### 解决什么问题

面对陌生代码库时，普通文件树通常只能告诉你“文件叫什么”，不能告诉你：

- 项目最重要的用户功能是什么
- 一个文件在完整用户流程中位于哪一步
- 为什么要依赖另一个模块
- 英文模块名、函数名和数据表分别代表什么
- 哪些文件是生产执行、公共支撑、自动化验证或文档说明

这个 Skill 指导 Agent 基于源码证据生成一个可离线打开的 HTML 代码库地图。

### 核心能力

- 自动识别项目最重要的 3–5 个用户可见功能
- 覆盖 Git 中全部 tracked files
- 为模块、目录和文件生成通俗职责说明
- 把技术标识显示为“代码名（通俗含义）”
- 解释依赖另一个模块的具体目的
- 展示路由、数据表、主要声明、测试和源码注释
- 从每个核心功能视角说明文件是直接参与、公共支撑、验证、说明或不参与
- 生成无需服务器即可通过 `file://` 打开的交互式 HTML
- 附带自动审计脚本，检查覆盖率、空泛描述和功能卡片完整性

### 安装

安装到跨 Agent 通用的全局 Skill 目录：

```bash
git clone https://github.com/ssynb/codebase-understanding-atlas-skill.git \
  ~/.agents/skills/codebase-understanding-atlas
```

Pi 用户安装后执行：

```text
/reload
/skill:codebase-understanding-atlas
```

其他兼容 Agent Skills 标准的工具会从其支持的 Skill 目录发现 `SKILL.md`。

### 使用示例

```text
使用 codebase-understanding-atlas 分析当前代码库，生成一个面向新成员的交互式 HTML 项目地图。
```

```text
重新生成代码库地图，重点检查每个依赖是否解释了调用目的，并确认所有 tracked files 都被覆盖。
```

### 校验生成结果

```bash
python3 scripts/audit_atlas.py \
  --repo /path/to/repository \
  --html /path/to/repository-browser.html
```

## English

### What it solves

A normal file tree tells readers what files are named, but rarely explains:

- the repository's most important user-visible capabilities
- where a file participates in an end-to-end flow
- why it depends on another module
- what technical module, declaration, and storage names mean
- whether a file executes production behavior, supports it, verifies it, or only documents it

This skill guides an agent through source-grounded investigation and generation of a standalone interactive HTML atlas.

### Highlights

- Discovers 3–5 core user-visible capabilities from repository evidence
- Covers every Git-tracked file
- Produces plain-language module, directory, and file responsibilities
- Explains displayed technical identifiers instead of listing bare names
- Explains the purpose of cross-module dependencies
- Surfaces routes, storage facts, declarations, tests, and useful source comments
- Maps every file to each core capability as Direct, Support, Verification, Documentation, or Not involved
- Generates a self-contained `file://`-compatible HTML browser
- Includes an audit script for coverage and description quality

### Installation

```bash
git clone https://github.com/ssynb/codebase-understanding-atlas-skill.git \
  ~/.agents/skills/codebase-understanding-atlas
```

For Pi:

```text
/reload
/skill:codebase-understanding-atlas
```

### Repository contents

```text
.
├── SKILL.md
├── references/
│   ├── output-contract.md
│   └── quality-standard.md
└── scripts/
    └── audit_atlas.py
```

## Design principles

- Evidence before inference
- User flows before infrastructure lists
- Plain language before unexplained identifiers
- File-level roles instead of blindly copied module-level roles
- Explicit uncertainty instead of fabricated explanations
- Systemic generator fixes instead of one-off wording patches

## Security

Skills can instruct agents to read files and execute commands. Review `SKILL.md` and helper scripts before use, and run agents with permissions appropriate for the repository being analyzed.

## License

MIT
