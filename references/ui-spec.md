# Mandatory Atlas UI Specification

This specification prevents different agents from turning the same evidence into unrelated or low-quality pages. Content varies by repository; the shell, hierarchy, and interactions do not.

## Canonical reference

`../templates/atlas-shell.html` and this specification are the canonical visual references. `../assets/atlas-demo.png` demonstrates the kind of repository-specific content an atlas can contain, but must not be copied as a shell or as a source of facts.

Never copy a demonstration repository's name, counts, aliases, capabilities, or descriptions into another atlas.

## Mandatory shell

Use `../templates/atlas-shell.html` through `../scripts/render_atlas.py`.

The generated document must contain:

- `data-atlas-template="codebase-understanding-atlas/v2"`
- `#atlas-topbar`
- `#repository-head`
- `#top-directory`
- `#content-panel`
- `#detail-drawer`
- `#search`
- `#search-results`

Removing, renaming, or replacing these structures causes the audit to fail.

## Desktop hierarchy

At a viewport near 1036 × 797, the first screen must follow the bundled shell:

1. **Repository bar** — compact charcoal strip, repository identity on the left, one module/term explanation control beside it, and wide search on the right.
2. **Repository heading** — small GitHub-like owner/repository title, revision and file/directory counts, with a branch pill on the right.
3. **Repository browser** — a narrow sticky top-directory sidebar and wider main content area.
4. **Folder context** — breadcrumbs followed by a pale-blue summary that explains the current folder in plain language.
5. **Repository rows** — dense bordered rows with blue clickable code name plus alias, concrete responsibility, and compact count metadata.

The browser is the primary surface. Do not place a large hero, dashboard, chart, marketing banner, or decorative void above it.

## Visual tokens

The template owns these tokens. Do not casually redesign them:

- page background: GitHub-like `#f6f8fa`
- sticky top bar: charcoal `#24292f`
- links and code names: `#0969da`
- folder summary: pale blue `#ddf4ff`
- panels and rows: white with subtle `#d0d7de` borders
- body text: near-black; secondary explanations: slate gray
- corners: restrained 7–8 px radii
- spacing: compact and information-dense, not dashboard-like
- maximum content width: approximately 1450 px

## Core capabilities

Core capabilities are evidence, not decoration. Present them in two places:

1. at the top of the “核心能力、模块与名词” right-side drawer opened from the header
2. as the first major card section in every file detail drawer

Do not use capability cards as a large full-width hero above the repository browser.

## Required interactions

- Directory rows navigate without reloading the file.
- Breadcrumbs and “返回上级” navigate to ancestors.
- Search opens a bounded result popover and covers paths, aliases, descriptions, declarations, and capability roles.
- File rows open a right-side detail drawer.
- The header explanation button opens the same right-side drawer with capabilities, modules, and recurring terms.
- Clicking the backdrop or close control dismisses the drawer.
- The page remains usable under `file://` with networking disabled.
- At narrow widths the sidebar disappears and rows stack without horizontal scrolling.

## File drawer hierarchy

Show user meaning before implementation trivia:

1. display name
2. prominent plain-language purpose
3. compact file facts
4. one card per core capability
5. declarations
6. dependency purposes
7. storage, routes, tests, and source notes

Do not put a redundant full-path block above the capability cards.

## Rejected layouts

Reject and regenerate any page that:

- adds a large dark hero or dashboard above the file browser
- omits the repository heading, sidebar, blue folder summary, or dense rows
- hides capabilities entirely or fails to show them per file
- uses a full-width flat table with no directory context
- displays raw JSON or unexplained identifier lists
- uses CDN CSS/JS or fails offline
- copies capability names or aliases from the reference screenshot
- passes content checks but visibly diverges from the mandatory shell

## Visual acceptance

Before completion:

1. run `audit_atlas.py`
2. open the generated HTML around 1036 × 797
3. compare the first viewport with the mandatory hierarchy and visual tokens above
4. verify density, colors, widths, row structure, and information priority
5. open the capability/module drawer, one directory, one source file, one test, and one search result
6. repeat at a mobile-width viewport

Do not report success if the screenshot comparison reveals a missing, oversized, or rearranged major region, even when the automated audit passes.
