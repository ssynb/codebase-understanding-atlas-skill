# Output Data and Rendering Contract

The evidence varies by repository. The HTML shell does not: render this data with `scripts/render_atlas.py` and the bundled `templates/atlas-shell.html`. Alternate shells fail the default Skill contract unless the user explicitly requests a redesign.

```json
{
  "repository": {
    "name": "short repository name",
    "fullName": "owner/repository when known",
    "title": "reader-facing project title",
    "branch": "source branch",
    "architecture": "optional short architecture phrase"
  },
  "revision": "full source revision",
  "counts": {
    "files": 123,
    "dirs": 45
  },
  "capabilities": [
    {
      "id": "stable-id",
      "name": "plain-language name",
      "trigger": "user action",
      "outcome": "observable successful result",
      "summary": "one or two concise sentences shown in the hero card"
    }
  ],
  "modules": {
    "stable-code-name": {
      "name": "plain-language name",
      "owns": "facts or behavior owned here",
      "usedFor": "why other areas depend on it",
      "doesNotOwn": "important boundary"
    }
  },
  "glossary": [
    {
      "code": "recurring technical term",
      "meaning": "meaning in this repository"
    }
  ],
  "entries": {
    "relative/path": {
      "kind": "file or dir",
      "name": "source name",
      "display": "source name plus optional alias",
      "description": "plain-language responsibility",
      "children": [],
      "coreRoles": [
        {
          "id": "capability-id",
          "name": "capability name",
          "relation": "Direct, Support, Verification, Documentation, or Not involved",
          "description": "file-specific role"
        }
      ],
      "symbolDetails": [
        {
          "name": "source identifier",
          "description": "grounded plain-language meaning"
        }
      ],
      "dependencies": [
        {
          "name": "stable code name",
          "display": "plain-language name",
          "purpose": "why this file uses it"
        }
      ],
      "tables": [
        {
          "name": "storage identifier",
          "display": "plain-language fact name"
        }
      ],
      "routes": [],
      "tests": []
    }
  }
}
```

## Rendering command

```bash
python3 scripts/render_atlas.py \
  --data /path/to/atlas-data.json \
  --output /path/to/repository-browser.html
```

Do not bypass this command by emitting an improvised HTML page. Read `ui-spec.md` for the mandatory first-screen hierarchy and visual acceptance process.

## HTML behavior contract

- Uses the bundled shell marked `data-atlas-template="codebase-understanding-atlas/v1"`.
- Works from `file://` with no network dependency.
- Does not fetch repository source at runtime.
- Escapes embedded JSON and rendered text.
- Breadcrumbs provide path context; no duplicate full-path block is required.
- File-role cards appear before low-level declarations.
- Glossary explains both module names and recurring architecture terms.
- Search includes aliases and plain-language descriptions.
- Large repositories remain navigable; render only the current directory and bounded search results.
- Mobile layout remains readable.
