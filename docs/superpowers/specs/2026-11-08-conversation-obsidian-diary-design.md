# Conversation Obsidian Diary: Public Skill Design

## Goal

Publish the existing personal diary workflow as a vendor-neutral Agent Skill that turns AI conversation transcripts into an Obsidian daily note and durable, topic-based second-brain notes.

## Product boundary

The public package is not tied to Codex, Claude, Cursor, or another agent. Its canonical input is a simple Markdown transcript. Platform-specific session extraction is optional; the first bundled adapter reads Codex JSONL sessions because that implementation already exists.

The repository must not include private conversations, generated diary entries, local usernames, API credentials, or absolute paths from the author's machine.

## Repository structure

```text
conversation-obsidian-diary/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
├── conversation-obsidian-diary/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── extract_codex_day.py
│   │   └── normalize_transcript.py
│   ├── references/
│   │   ├── configuration.md
│   │   └── transcript-format.md
│   └── assets/
│       └── config.example.yaml
├── tests/
│   ├── fixtures/
│   ├── test_extract_codex_day.py
│   └── test_normalize_transcript.py
└── docs/superpowers/
    ├── specs/
    └── plans/
```

## Skill architecture

`SKILL.md` contains only the shared workflow, classification model, privacy invariants, output markers, and links to conditional references. Configuration and input schemas live in `references/` so agents load them only when needed. The skill conforms to the Agent Skills open format: the directory name and frontmatter name match, and bundled resources use relative paths.

The workflow accepts either an existing normalized transcript or a platform adapter's output. It preserves user-authored Obsidian content outside managed markers and never uploads note data.

## Configuration

Configuration is resolved in this order:

1. Explicit command arguments or user instructions.
2. Environment variables documented by the repository.
3. A local configuration file based on `assets/config.example.yaml`.
4. Portable defaults based on the user's home directory and current timezone.

No public file contains an author-specific home-directory path.

## Scripts

`extract_codex_day.py` remains a stdlib-only optional adapter. It reads JSONL session files for one local calendar day and emits normalized Markdown.

`normalize_transcript.py` accepts a small JSON conversation interchange format and emits the same normalized Markdown. This provides a vendor-neutral bridge for tools that can export conversations but do not expose Codex-style session files.

Both scripts provide `--help`, deterministic output, useful validation errors, and no network access.

## Documentation and installation

The English README is canonical and the Chinese README provides equivalent installation and usage guidance. Installation is a directory copy or Git clone into any agent's supported skill directory. Tool-specific paths are examples, not core requirements.

The documentation includes privacy warnings, the transcript contract, configuration, Codex adapter usage, generic JSON usage, and example invocation prompts.

## Testing and validation

Python `unittest` covers local-day timezone selection, malformed JSONL handling, role filtering, normalized Markdown output, JSON input validation, and privacy scans. The skill is also checked with an available Agent Skills validator or an equivalent local conformance check.

Before publication, the repository is scanned for the author's home path, credentials, real diary content, and session payloads. All tests and validation must pass immediately before the public push.

## Publication

Create `github.com/vergileZhang/conversation-obsidian-diary` as a public repository under the MIT License. Push the verified `main` branch and set a concise description and Agent Skills/Obsidian topics.
