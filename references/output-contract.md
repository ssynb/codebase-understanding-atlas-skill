# Output Data Contract

The HTML implementation may vary, but the embedded JSON should expose equivalent information.

```json
{
  "revision": "source revision",
  "capabilities": [
    {
      "id": "stable-id",
      "name": "plain-language name",
      "trigger": "user action",
      "outcome": "observable successful result"
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

## HTML behavior contract

- Works from `file://` with no network dependency.
- Does not fetch repository source at runtime.
- Escapes embedded JSON and rendered text.
- Breadcrumbs provide path context; no duplicate full-path block is required.
- File-role cards appear before low-level declarations.
- Glossary explains both module names and recurring architecture terms.
- Search includes aliases and plain-language descriptions.
- Large repositories remain navigable; render only the current directory and bounded search results.
- Mobile layout remains readable.
