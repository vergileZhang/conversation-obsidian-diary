# Conversation Obsidian Diary

[中文说明](README.zh-CN.md) · [MIT License](LICENSE)

A vendor-neutral [Agent Skill](https://agentskills.io/) that turns AI conversations into an Obsidian daily review and a durable, topic-based second brain.

## What it does

- Builds a chronological daily note from substantive conversations.
- Promotes reusable knowledge, decisions, troubleshooting, and project progress into topic notes.
- Classifies entries as learning, projects, operations, personal growth, academic research, or life matters.
- Preserves user-written content outside explicit managed markers.
- Keeps one-off actions in the daily timeline without polluting the long-term archive.
- Works from normalized Markdown, generic JSON exports, or optional Codex JSONL session extraction.

The skill does not upload conversations or connect to Obsidian services. It works on local files through the host agent's existing file tools.

## Repository layout

```text
conversation-obsidian-diary/     # Install this directory as the skill
├── SKILL.md
├── scripts/
│   ├── extract_codex_day.py
│   └── normalize_transcript.py
├── references/
│   ├── configuration.md
│   └── transcript-format.md
└── assets/
    └── config.example.yaml
```

## Install

### Any Agent Skills-compatible tool

Clone the repository, then copy or symlink the inner `conversation-obsidian-diary` directory into the skill directory supported by your agent:

```bash
git clone https://github.com/vergileZhang/conversation-obsidian-diary.git
cp -R conversation-obsidian-diary/conversation-obsidian-diary /path/to/your/agent/skills/
```

The installed path must end with:

```text
conversation-obsidian-diary/SKILL.md
```

Skill locations differ between tools and versions. Use the tool's documented skill directory; the package itself does not depend on a particular vendor.

### Project-local installation

If your agent discovers project-local skills, copy the inner directory into the project's supported skills folder. Commit it only if the whole team should share the workflow.

## Configure

Tell the agent these values in your request, through its local instructions, or with a private config copied from `assets/config.example.yaml`:

- Obsidian vault path
- target date and IANA timezone
- daily-note filename pattern
- second-brain root folder
- attachments folder

See [configuration.md](conversation-obsidian-diary/references/configuration.md). Never commit a filled config containing local paths.

## Use

Example prompt:

```text
Use conversation-obsidian-diary to turn today's AI conversations into my Obsidian daily review and update durable topic notes. My vault is at <vault-path>, and my timezone is Asia/Shanghai. Preserve everything outside managed blocks.
```

If your agent does not auto-discover skills, explicitly ask it to read `conversation-obsidian-diary/SKILL.md` and follow the workflow.

## Prepare a transcript

The core skill consumes the normalized Markdown format documented in [transcript-format.md](conversation-obsidian-diary/references/transcript-format.md).

### Generic JSON export

Input:

```json
{
  "messages": [
    {
      "timestamp": "2026-11-08T01:00:00Z",
      "role": "user",
      "content": "A message"
    }
  ]
}
```

Normalize it:

```bash
python3 conversation-obsidian-diary/scripts/normalize_transcript.py \
  --input /path/to/conversation.json \
  --timezone Asia/Shanghai \
  --output /tmp/conversation-transcript.md
```

### Codex JSONL sessions

```bash
python3 conversation-obsidian-diary/scripts/extract_codex_day.py \
  --date 2026-11-08 \
  --timezone Asia/Shanghai \
  --sessions-root /path/to/codex/sessions \
  --output /tmp/conversation-transcript.md
```

Both adapters use only the Python 3 standard library and make no network requests.

## Privacy and safety

- Review transcripts before processing them if they may contain secrets.
- Keep vaults, exported conversations, attachments, and filled local configs out of Git.
- The skill never authorizes uploading or publishing private note content.
- User-authored note content is outside the managed markers and must be preserved.
- If markers are malformed or ambiguous, back up the note and stop instead of overwriting it.

## Development

Run the test suite:

```bash
python3 -m unittest discover -s tests -v
```

Validate the skill with the Agent Skills reference validator when available:

```bash
skills-ref validate ./conversation-obsidian-diary
```

The tests also scan public text files for the current author's home path and common credential patterns.

## Origin

This project generalizes a personal Codex-to-Obsidian diary workflow into a portable Agent Skill. Codex is now only one optional transcript adapter; the core workflow accepts normalized conversation data from any source.

## License

[MIT](LICENSE)
