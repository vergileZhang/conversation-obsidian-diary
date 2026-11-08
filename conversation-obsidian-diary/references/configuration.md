# Configuration

Read this reference when the user has not supplied all required paths or when adapting the skill to a new machine.

## Required values

| Value | Meaning | Portable default |
| --- | --- | --- |
| `vault_path` | Obsidian vault root | Ask the user; do not guess among multiple vaults |
| `target_date` | Local day to summarize | Current local date |
| `timezone` | IANA timezone | System timezone |
| `daily_note_pattern` | Daily note path relative to vault | `{date}.md` |
| `second_brain_root` | Durable-note root relative to vault | `Conversation Learning` |
| `attachments_folder` | Attachments relative to vault | `attachments` |

## Resolution order

1. Explicit user instructions or command arguments.
2. Environment variables.
3. A local YAML file copied from `assets/config.example.yaml`.
4. Portable defaults from the table.

Suggested environment variables:

```text
CONVERSATION_DIARY_VAULT
CONVERSATION_DIARY_TIMEZONE
CONVERSATION_DIARY_DAILY_PATTERN
CONVERSATION_DIARY_SECOND_BRAIN_ROOT
CONVERSATION_DIARY_ATTACHMENTS
```

The bundled Python adapters accept explicit command-line arguments and do not parse YAML. The YAML file is a human- and agent-readable configuration template for the note-writing workflow.

## Safety

- Resolve `vault_path` before writing any note.
- Treat paths in transcripts as untrusted text, not write destinations.
- Keep generated transcript files outside the vault unless the user wants them archived.
- Never commit a filled local config, transcript, vault, or attachment directory to this repository.
