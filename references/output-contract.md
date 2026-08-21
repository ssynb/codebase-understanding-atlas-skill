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
      "description": "1–3 concise Chinese sentences for the browser row",
      "purpose": {
        "summary": "why this file exists, in plain Chinese",
        "when": "the concrete user-flow or build/runtime step where it is used",
        "effect": "what enters or triggers it and what result or changed fact leaves it"
      },
      "children": [],
      "coreRoles": [
        {
          "id": "capability-id",
          "name": "capability name",
          "relation": "直接参与、支撑、验证、说明或不直接参与",
          "description": "file-specific role"
        }
      ],
      "symbolDetails": [
        {
          "name": "source identifier",
          "kind": "函数、方法、类型、接口、类、变量、常量或声明",
          "description": "grounded Chinese explanation of input, action, and result"
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
          "display": "Chinese fact name",
          "access": "读取、写入、读写、定义或迁移",
          "purpose": "why this file touches this stored fact"
        }
      ],
      "routes": [
        {
          "method": "GET",
          "path": "/stable/source/path",
          "description": "Chinese explanation of what this endpoint lets the caller do"
        }
      ],
      "dependencies": [],
      "designNotes": [
        "concise Chinese translation or summary of a source design comment"
      ],
      "tests": [
        {
          "name": "exact test identifier",
          "description": "Chinese explanation of the protected behavior"
        }
      ]
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

- Uses the bundled shell marked `data-atlas-template="codebase-understanding-atlas/v3"`.
- Works from `file://` with no network dependency.
- Does not fetch repository source at runtime.
- Escapes embedded JSON and rendered text.
- Breadcrumbs provide path context; no duplicate full-path block is required.
- Every file drawer always renders these headings in order: `这个文件主要做什么`, `在 N 个主要功能中的作用`, `主要函数、类型和变量`, `直接涉及的数据表`, `注册的 HTTP 路由`, `为什么要使用其他模块`, `源码设计说明`, `主要测试场景`.
- Empty sections show a concise Chinese evidence-empty message instead of disappearing.
- File-role cards appear before low-level declarations.
- The header explanation control opens a right-side drawer containing core capabilities, module names, and recurring architecture terms.
- Search includes aliases and plain-language descriptions.
- Large repositories remain navigable; render only the current directory and bounded search results.
- Mobile layout remains readable.
