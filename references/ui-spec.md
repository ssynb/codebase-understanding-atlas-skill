# Mandatory Atlas UI Specification

This specification prevents different agents from turning the same evidence into unrelated or low-quality pages. Content varies by repository; the shell, hierarchy, and interactions do not.

## Reference

Before rendering, inspect `../assets/atlas-demo.png`.

The screenshot is a structural reference, not a source of repository facts. Never copy its repository name, capability names, counts, directory aliases, or descriptions into another atlas.

## Mandatory shell

Use `../templates/atlas-shell.html` through `../scripts/render_atlas.py`.

The generated document must contain:

- `data-atlas-template="codebase-understanding-atlas/v1"`
- `#atlas-topbar`
- `#capability-hero`
- `#top-directory`
- `#content-panel`
- `#detail-drawer`
- `#glossary-dialog`
- `#search`

Removing, renaming, or replacing these structures causes the audit to fail.

## Desktop hierarchy

At a viewport near 1024 × 860, the first screen must show:

1. **Repository bar** — about 56 px high, charcoal background, repository identity on the left, glossary control near it, search on the right.
2. **Capability hero** — dark navy rounded panel directly below the bar. It contains one title, revision/file/directory facts, and 3–5 capability cards in a balanced grid.
3. **Repository browser** — starts immediately below the hero. A narrow left sidebar lists top-level directories; the wider right side contains breadcrumbs, a pale-blue current-folder summary, and direct children.
4. **Repository rows** — blue clickable code name plus plain-language alias, concrete responsibility, and compact item/line count.

The first screen must not contain a large empty area between title and browser.

## Visual tokens

The template owns these tokens. Do not casually redesign them:

- page background: very light gray
- sticky top bar: charcoal
- overview hero: dark navy/blue gradient
- links and code names: accessible GitHub-like blue
- folder summary: pale blue with blue border
- panels: white, subtle gray border, 8–12 px corner radius
- body text: dark gray; secondary explanations: slate gray
- spacing: dense enough to expose useful information without looking like a spreadsheet dump

Capability cards must use equal visual weight. Do not replace them with tiny tags, a long prose paragraph, or a hidden accordion.

## Required interactions

- Directory rows navigate without reloading the file.
- Breadcrumbs navigate back to every ancestor.
- Search covers path, aliases, descriptions, declarations, and capability roles; results are bounded.
- File rows open a right-side detail drawer.
- The glossary button opens a centered modal.
- Clicking the backdrop or close control dismisses drawer/modal.
- The page remains usable under `file://` with networking disabled.
- At narrow widths capability cards stack, the sidebar disappears, and rows remain readable.

## File drawer hierarchy

Show user meaning before implementation trivia:

1. display name
2. short file facts
3. prominent plain-language purpose
4. one card per core capability
5. declarations
6. dependency purposes
7. storage, routes, tests, and source notes

Do not put a redundant full-path block above the capability cards.

## Rejected layouts

Reject and regenerate any page that:

- shows only a repository heading and file tree
- omits the dark capability hero
- hides core capabilities in a modal or below thousands of files
- uses a full-width flat table with no directory context
- displays raw JSON or unexplained identifier lists
- uses CDN CSS/JS or fails offline
- copies capability names or aliases from the reference screenshot
- passes content checks but visibly diverges from the mandatory shell

## Visual acceptance

Before completion:

1. run `audit_atlas.py`
2. open the generated HTML
3. compare the first viewport with `assets/atlas-demo.png`
4. verify the hero has repository-specific capability cards
5. open one directory, one source file, one test, and the glossary
6. repeat at a mobile-width viewport

Do not report success if the screenshot comparison reveals a missing or collapsed major region, even when the automated audit passes.
