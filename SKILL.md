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
10. Describe files in the user's language. Preserve code identifiers only where they help the reader find source.

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

### 5. Write plain-language file descriptions

Each description should answer, in this order:

1. Which product/module area contains this file?
2. What concrete step does it perform?
3. What enters and what leaves?
4. Which persistent facts, routes, or external systems does it touch?
5. Why does it use each cross-module dependency?
6. What behavior do its tests protect?

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

Use `templates/atlas-shell.html` unchanged unless the user explicitly asks for a different visual design. Read [references/ui-spec.md](references/ui-spec.md) completely and inspect [assets/atlas-demo.png](assets/atlas-demo.png) before generating data.

The required visual hierarchy is:

1. dark sticky repository bar with repository name, glossary button, and wide search
2. dark blue overview hero with title, revision/counts, and 3–5 equal capability cards
3. two-column browser with a compact top-directory sidebar and main content
4. breadcrumbs, blue folder summary, and repository-style child rows
5. right-side file detail drawer
6. centered module/terminology glossary dialog

A plain repository title followed immediately by a file tree is a failure, even if all files are present. The capability hero is the primary onboarding surface and must appear above the browser.

The file detail drawer must contain, when evidence exists:

1. functional purpose
2. file facts (type, size, lines)
3. role in each core capability
4. explained main declarations
5. translated data/storage names
6. routes
7. dependency purpose explanations
8. useful source design comments
9. behavior tests

Do not add a separate “full path” section. The path is already visible through breadcrumbs and browser context; capability role is more useful.

The renderer safely embeds the JSON and produces a responsive `file://` page. Do not replace it with CDN assets, framework bundles, runtime source fetching, or a hand-written alternate shell.

### 8. Validate before reporting completion

Read [references/quality-standard.md](references/quality-standard.md) and [references/output-contract.md](references/output-contract.md).

Run:

```bash
python3 scripts/audit_atlas.py --repo /path/to/repo --html /path/to/repository-browser.html
```

Also extract the application JavaScript and run `node --check` when Node.js is available. Open the page at approximately 1024 px desktop width and compare the overall hierarchy with `assets/atlas-demo.png`: top bar, capability hero, sidebar, folder summary, and child rows must all be visible before accepting the result. Then inspect representative files from UI, backend/domain, persistence, runtime, deployment, generated code, tests, and binary assets.

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
