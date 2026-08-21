---
name: codebase-understanding-atlas
description: Builds an evidence-based interactive HTML atlas for understanding an unfamiliar software repository. Use for architecture onboarding, repository tours, file-by-file responsibility maps, dependency explanations, core user-flow tracing, or when technical names need plain-language explanations.
compatibility: Requires filesystem access, repository search, and Python 3. Git is optional but preferred for exact tracked-file inventory.
---

# Codebase Understanding Atlas

Create a standalone interactive HTML repository browser that explains the system from user-visible capabilities down to modules, files, declarations, dependencies, data, routes, and tests.

This is an investigation workflow, not a filename paraphraser. Every claim must come from repository evidence.

## Non-negotiable rules

1. Read repository instructions and trust/configuration files before analysis.
2. Do not modify production source merely to build the atlas. Put generated artifacts outside the repository unless the user chooses another location.
3. Establish the current source baseline. If the repository requires synchronization, follow its own safe-worktree policy before reading facts.
4. Inventory every tracked file with `git ls-files -z` when Git is available. Otherwise use a filesystem walk with explicit exclusions.
5. Derive the project's 3–5 most important user-visible capabilities from product docs, routes, screens, acceptance tests, and entry points. Never reuse capability names from another repository.
6. Explain technical identifiers as `code-name（plain-language meaning）`. Never show a list of unexplained module, function, type, table, or service names.
7. Explain dependencies as purpose: “uses X to obtain Y or enforce Z,” not merely “calls X.”
8. Prefer source comments, signatures, call sites, routes, SQL, schemas, contracts, and tests over inference.
9. Do not invent descriptions for opaque private helpers. Omit low-confidence helpers from the “main declarations” list and state that they were omitted rather than guessing.
10. Describe files in the user's language. For Chinese users, all explanations must be Chinese; preserve English only for searchable source identifiers, paths, protocol names, and unavoidable technical keywords.
11. Never expose a raw English README paragraph or source comment as the explanation. Translate its meaning into concise Chinese and keep the original identifier only where it helps locate source.
12. The bundled data schema and drawer sections are mandatory. Do not rename, omit, merge, or reorder them merely because an agent generated less evidence.

## Workflow

### 1. Establish the evidence baseline

- Read the nearest repository instruction files.
- Inspect worktree status and current revision.
- Read product overview, architecture/ownership docs, terminology docs, manifests, build files, service entry points, route registration, schemas/migrations, and representative behavior tests.
- Use `rg` to locate call sites and same-pattern implementations.
- Record the revision in the generated page.

### 2. Discover 3–5 core capabilities

A core capability must be a user-observable end-to-end outcome, not an infrastructure noun.

For each candidate, prove it with at least two of:

- UI route or screen
- public API route
- business service/state machine
- persistence facts
- end-to-end or contract test
- product requirement

Create a capability map with:

- plain-language name
- user trigger
- successful outcome
- main stages
- owning modules
- important failure/recovery boundaries

If the evidence does not support 3 capabilities, use fewer and explain why. Never pad the list.

### 3. Build a module glossary

For every important module or service, record:

- stable code name
- plain-language name
- what facts or behavior it owns
- why other modules use it
- what it explicitly does not own
- direct upstream and downstream dependencies

Display directory names as `code-name（plain-language name）` where a reliable alias exists.

### 4. Build per-file evidence

For every tracked file, gather applicable evidence:

- path, type, size, and text line count
- owning module
- routes registered
- tables or storage objects explicitly referenced
- imports and cross-module dependencies
- top-level functions, types, classes, exported values, and adjacent comments
- tests and behavior names
- build/deploy/config consumers
- generated-source marker and source-of-truth file

Read binary assets by metadata and usage references; do not pretend to parse them as source.

### 5. Write Chinese explanations a beginner can understand

Read [references/beginner-writing-guide.md](references/beginner-writing-guide.md) completely before writing visible prose.

For every file, create both a compact row `description` and a structured `purpose` object. Do not make the row description carry the entire drawer.

The compact description should use 1–3 short Chinese sentences and answer what the file does and where it is used. The structured purpose must contain:

- `summary` — why this file exists, in plain Chinese
- `when` — at which concrete step it is used; for docs/assets/config, who consumes it and when
- `effect` — what enters or triggers it, and what observable result or changed fact leaves it

Then gather these drawer facts separately:

1. role in each main user capability
2. main functions, types, and variables, each with a syntactic kind and Chinese explanation
3. directly touched tables, with Chinese fact name, read/write mode, and purpose
4. registered routes
5. dependency purpose
6. Chinese translation or summary of source design comments
7. behavior tests

Do not paste long package descriptions into every child file. Explain the narrow action owned by that file. Prefer short sentences and common words; when a technical term is necessary, write `code-name（中文含义）` the first time.

When showing a declaration, include a grounded explanation:

- `Execute` — performs an already-authorized operation and returns the stable result shape.
- `Request` — fields accepted at this boundary.
- `Store` — database reads/writes and transaction boundary for this area.

These examples illustrate form only. Replace them with repository-specific evidence.

Use adjacent source comments first. Otherwise infer from signature plus callers. If confidence remains low, do not list the declaration as “main.”

### 6. Explain each file against the core capabilities

In the file detail drawer, show one card per discovered capability. Classify the file as one of:

- **Direct** — executes a stage of the user flow.
- **Support** — supplies shared identity, storage, transport, policy, billing, observability, or runtime capability.
- **Verification** — tests or validates the flow but is not production execution.
- **Documentation** — specifies the flow but does not execute it.
- **Not involved** — belongs to another product area.

Every card must explain the exact role. Do not mechanically copy the module-level role when the file is narrower. A file used only during setup must not be marked direct in later runtime flows merely because its parent module participates in both.

### 7. Generate evidence data, then use the mandatory renderer

Default output: a self-contained `repository-browser.html` in a repository-external report directory.

**Do not improvise a new page design.** The bundled shell is part of this Skill's output contract. First write the evidence model to `atlas-data.json`, then render it with:

```bash
python3 /path/to/this-skill/scripts/render_atlas.py \
  --data /path/to/atlas-data.json \
  --output /external/report/repository-browser.html
```

Use `templates/atlas-shell.html` unchanged unless the user explicitly asks for a different visual design. Read [references/ui-spec.md](references/ui-spec.md) completely before generating data. `assets/atlas-demo.png` is a public-repository content example, not the canonical shell specification.

The required visual hierarchy is:

1. compact dark GitHub-style repository bar with repository identity, glossary button, and wide search
2. restrained repository heading with branch, revision, file count, and directory count
3. two-column browser with a compact top-directory sidebar and main content
4. breadcrumbs, pale-blue folder summary, and dense repository-style child rows
5. one right-side drawer reused for file detail and the capability/module/terminology overview

The repository browser is the primary surface. Do not add a large marketing hero, dashboard tiles, oversized title, or decorative empty space above it. Core capabilities remain prominent inside the glossary/overview drawer and as the first major section of every file detail.

The file detail drawer must always use this exact order and these Chinese headings:

1. `这个文件主要做什么`
2. file facts (type, size, lines)
3. `在 N 个主要功能中的作用`
4. `主要函数、类型和变量`
5. `直接涉及的数据表`
6. `注册的 HTTP 路由`
7. `为什么要使用其他模块`
8. `源码设计说明`
9. `主要测试场景`

Show an explicit short Chinese empty-state sentence when a section has no direct evidence; do not silently remove the section. Never show raw English source comments. Translate or summarize them into `designNotes` first.

Do not add a separate “full path” section. The path is already visible through breadcrumbs and browser context; capability role is more useful.

The renderer safely embeds the JSON and produces a responsive `file://` page. Do not replace it with CDN assets, framework bundles, runtime source fetching, or a hand-written alternate shell.

### 8. Validate before reporting completion

Read [references/quality-standard.md](references/quality-standard.md) and [references/output-contract.md](references/output-contract.md).

Run:

```bash
python3 scripts/audit_atlas.py --repo /path/to/repo --html /path/to/repository-browser.html
```

Also extract the application JavaScript and run `node --check` when Node.js is available. Open the page at approximately 1024 px desktop width and verify the hierarchy required by `references/ui-spec.md`: compact top bar, repository heading, sidebar, folder summary, and dense child rows must all be visible before accepting the result. Then open the overview drawer and inspect representative files from UI, backend/domain, persistence, runtime, deployment, generated code, tests, and binary assets.

Report:

- output path
- source revision
- tracked file and directory counts
- core capabilities selected and evidence used
- validation performed
- any areas intentionally omitted because evidence was insufficient

## Updating an existing atlas

On refresh:

1. re-establish the source revision
2. diff tracked files against embedded entries
3. re-run capability discovery rather than assuming the old set is still correct
4. regenerate descriptions affected by changed routes, tables, declarations, imports, or tests
5. remove stale aliases and roles
6. rerun the full audit

Do not patch only the visible sentence that exposed a systemic description problem. Fix the extraction or description rule and verify all same-pattern entries.
