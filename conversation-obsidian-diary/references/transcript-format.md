# Transcript Format

Read this reference when preparing conversation data for the skill.

## Normalized Markdown

The skill expects a UTF-8 Markdown file with metadata followed by chronological message sections:

```markdown
# Conversation transcript for 2026-11-08

- timezone: Asia/Shanghai
- messages: 2

## 09:00:00 User

How should I organize today's notes?

## 09:00:05 Assistant

Use a daily timeline plus durable topic notes.
```

The title may omit a date for exports spanning multiple days. In that case, section headings should include a full local timestamp.

Only user and assistant messages belong in the normalized transcript. Exclude system prompts, developer messages, tool payloads, and hidden reasoning.

## Generic JSON interchange

`scripts/normalize_transcript.py` accepts:

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

Rules:

- `messages` must be an array.
- `role` must be `user` or `assistant` to be included.
- `content` may be a string or an array of strings or objects containing `text`, `input_text`, or `output_text`.
- `timestamp` is optional. ISO 8601 timestamps with `Z` or an explicit offset are converted to the requested timezone.
- Messages keep their source order. Timestamp conversion does not reorder them.

## Codex JSONL adapter

Run:

```bash
python3 scripts/extract_codex_day.py \
  --date 2026-11-08 \
  --timezone Asia/Shanghai \
  --sessions-root /path/to/codex/sessions \
  --output /tmp/conversation-transcript.md
```

The adapter scans date-partitioned JSONL session folders for the requested local day, including adjacent UTC date folders. It reads only `response_item` message events with `user` or `assistant` roles. Malformed JSONL rows are ignored.

## Generic JSON adapter

Run:

```bash
python3 scripts/normalize_transcript.py \
  --input /path/to/conversation.json \
  --timezone Asia/Shanghai \
  --output /tmp/conversation-transcript.md
```

Review exports before processing if the source tool includes secrets, private attachments, or unrelated conversations.
