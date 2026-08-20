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

- the bundled `codebase-understanding-atlas/v1` shell
- charcoal repository/search bar
- dark overview hero above the browser
- one visible card per discovered core capability
- top-directory sidebar plus breadcrumb-driven main browser
- pale-blue current-folder explanation
- file detail drawer and module/term glossary modal
- useful content visible at both desktop and mobile widths

Compare the first desktop viewport with `../assets/atlas-demo.png`. Match its overall hierarchy, density, contrast, and information priority while using only the target repository's facts. See `ui-spec.md` for exact requirements.

Reject a title-plus-tree page even if it embeds every tracked file.

## Completeness checks

- Every tracked file has a non-empty description.
- Every directory has a meaningful summary or a clearly labeled generated/vendor role.
- Every displayed technical identifier has a plain-language explanation.
- Every cross-module dependency shown has a purpose explanation.
- Every file has one role card per discovered core capability.
- Search can find both code names and plain-language terms.
- Generated code points to its source of truth.
- Binary assets describe their consumer or purpose when evidence exists.
- No repository-specific assumptions are carried over from a previous atlas.
- The mandatory renderer and shell markers pass `audit_atlas.py`.
- The opened page visually matches the reference hierarchy and all required interactions work.
