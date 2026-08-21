# Atlas Quality Standard

## Evidence ranking

Use evidence in this order:

1. Executable behavior tests and contracts
2. Production call sites and state transitions
3. Public routes and request/response types
4. Database queries, schemas, and migrations
5. Adjacent source comments
6. Build/deploy/config consumers
7. Stable identifier semantics
8. Filename inference only as a last resort

A lower-ranked source must not override a higher-ranked contradiction.

## Description acceptance criteria

A file description passes only when a new reader can answer:

- Why does this file exist?
- At what point in a user flow is it used?
- What input does it receive?
- What effect or output does it produce?
- Which owner does it ask for other capabilities, and why?
- Is it runtime code, verification, generated output, configuration, documentation, or an asset?

## Disallowed description patterns

Reject and regenerate descriptions that merely say:

- “implements the responsibility corresponding to X”
- “automation for X”
- “handles X-related logic”
- “provides utilities for X”
- “calls module A, module B” without purpose
- a bare list of declarations
- a translated filename with no input, effect, or flow position

## Beginner-readable Chinese

For a Chinese atlas:

- prose explanations are Chinese; English is limited to exact code identifiers, paths, protocol names, and necessary keywords
- never use an untranslated English paragraph as a file or directory description
- prefer “读取会话记录并返回下一页” over “executes session query projection”
- introduce a technical term as `code-name（中文含义）` before using the code name alone
- keep browser-row descriptions to 1–3 short sentences
- put detailed evidence in the fixed drawer sections instead of one oversized paragraph
- translate source comments into concise Chinese `designNotes`; do not display raw English comments

A description with only a Chinese prefix followed by an English paragraph fails.

## Identifier explanations

Good:

- `ReserveCapacity` — atomically holds capacity before external work begins so concurrent requests cannot oversubscribe it.
- `PageCursor` — opaque position returned to the client for requesting the next page without repeating prior rows.

Bad:

- `ReserveCapacity` — capacity logic.
- `PageCursor` — cursor type.

For declarations without a reliable explanation:

- keep them searchable internally if useful
- omit them from the visible “main declarations” section
- show a note that low-confidence private helpers were not interpreted

## Dependency explanations

A dependency explanation must include:

- plain-language dependency name
- capability obtained
- reason this file needs that capability
- important boundary when relevant

Good:

> Uses the identity owner to determine the authenticated account before reading account-scoped records.

Bad:

> Calls auth.

## Core-capability roles

Assign roles at file granularity. Verify common false positives:

- setup/write-path files marked direct in later read/runtime flows
- test files marked as production execution
- deployment files marked as business owners
- a broad module role copied to every narrow file
- shared utilities marked direct simply because many modules import them
- historical or generated files treated as active runtime owners

## Visual and interaction acceptance

Content completeness cannot compensate for a weak shell. The atlas fails when it looks like a plain file tree instead of an onboarding map.

Required:

- the bundled `codebase-understanding-atlas/v3` shell
- compact charcoal repository/search bar
- restrained owner/repository heading with branch and source counts
- top-directory sidebar plus breadcrumb-driven main browser
- pale-blue current-folder explanation
- dense GitHub-style child rows
- right-side drawer for file detail and capability/module/term explanation
- one role card per discovered core capability in every file
- useful content visible at both desktop and mobile widths

Compare the first desktop viewport with the bundled template and `ui-spec.md`. Match their hierarchy, density, contrast, and information priority while using only the target repository's facts. The public demo screenshot illustrates content depth, not the canonical shell.

Reject both a bare title-plus-tree page and an oversized dashboard/hero page, even if either embeds every tracked file.

## Mandatory file drawer

Every file has a structured `purpose` with `summary`, `when`, and `effect`. The drawer always renders, in order:

1. 这个文件主要做什么
2. 在 N 个主要功能中的作用
3. 主要函数、类型和变量
4. 直接涉及的数据表
5. 注册的 HTTP 路由
6. 为什么要使用其他模块
7. 源码设计说明
8. 主要测试场景

File facts appear between the first and second sections. Empty evidence is shown as a short Chinese sentence; headings do not disappear.

Each visible declaration includes its syntactic kind and a Chinese behavioral explanation. Each table includes a Chinese fact name, access mode, and why the file touches it. `designNotes` are translated or summarized source evidence, not invented architecture commentary.

## Completeness checks

- Every tracked file has a non-empty description.
- Every directory has a meaningful summary or a clearly labeled generated/vendor role.
- Every file has a complete structured `purpose` in Chinese.
- Every displayed technical identifier has a plain-language Chinese explanation and declaration kind.
- Every cross-module dependency shown has a purpose explanation.
- Every file has one role card per discovered core capability.
- Search can find both code names and plain-language terms.
- Generated code points to its source of truth.
- Every table entry explains its Chinese fact name, access mode, and file-specific purpose.
- Every displayed route and test keeps its exact identifier but adds a concise Chinese behavior explanation.
- Every file includes a `designNotes` list, even when no design comment exists.
- Binary assets describe their consumer or purpose when evidence exists.
- No repository-specific assumptions are carried over from a previous atlas.
- The mandatory renderer and shell markers pass `audit_atlas.py`.
- The opened page visually matches the reference hierarchy and all required interactions work.
