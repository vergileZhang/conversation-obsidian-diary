#!/usr/bin/env python3
"""Extract one local day of Codex conversation messages as normalized Markdown."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def text_from_content(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict):
            text = item.get("text") or item.get("input_text") or item.get("output_text")
            if text:
                parts.append(str(text))
    return "\n".join(parts).strip()


def session_files(root: Path, day: dt.date) -> list[Path]:
    candidates: set[Path] = set()
    for offset in (-1, 0, 1):
        candidate_day = day + dt.timedelta(days=offset)
        folder = root / f"{candidate_day.year:04d}" / f"{candidate_day.month:02d}" / f"{candidate_day.day:02d}"
        if folder.exists():
            candidates.update(folder.glob("*.jsonl"))
    return sorted(candidates)


def parse_timestamp(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def collect_messages(
    sessions_root: Path, local_day: dt.date, timezone: ZoneInfo
) -> list[tuple[dt.datetime, str, str]]:
    start = dt.datetime.combine(local_day, dt.time.min, tzinfo=timezone)
    end = start + dt.timedelta(days=1)
    rows: list[tuple[dt.datetime, str, str]] = []

    for path in session_files(sessions_root, local_day):
        try:
            handle = path.open("r", encoding="utf-8")
        except OSError as exc:
            print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
            continue
        with handle:
            for line in handle:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                timestamp = event.get("timestamp")
                if not isinstance(timestamp, str):
                    continue
                try:
                    instant = parse_timestamp(timestamp).astimezone(timezone)
                except (ValueError, TypeError):
                    continue
                if not start <= instant < end or event.get("type") != "response_item":
                    continue
                payload = event.get("payload") or {}
                if payload.get("type") != "message":
                    continue
                role = payload.get("role")
                if role not in {"user", "assistant"}:
                    continue
                content = text_from_content(payload.get("content"))
                if content:
                    rows.append((instant, role, content))

    rows.sort(key=lambda item: item[0])
    return rows


def render_markdown(
    local_day: dt.date, timezone_name: str, rows: list[tuple[dt.datetime, str, str]]
) -> str:
    lines = [
        f"# Conversation transcript for {local_day.isoformat()}",
        "",
        f"- timezone: {timezone_name}",
        f"- messages: {len(rows)}",
        "",
    ]
    for instant, role, content in rows:
        label = "User" if role == "user" else "Assistant"
        lines.extend([f"## {instant.strftime('%H:%M:%S')} {label}", "", content, ""])
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract one local day of Codex JSONL messages into normalized Markdown."
    )
    parser.add_argument("--date", required=True, help="Local date in YYYY-MM-DD format")
    parser.add_argument("--timezone", default="UTC", help="IANA timezone, for example Asia/Shanghai")
    parser.add_argument("--sessions-root", required=True, help="Root of date-partitioned Codex sessions")
    parser.add_argument("--output", required=True, help="Destination Markdown file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        local_day = dt.date.fromisoformat(args.date)
    except ValueError as exc:
        print(f"error: invalid --date: {exc}", file=sys.stderr)
        return 2
    try:
        timezone = ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError:
        print(f"error: unknown IANA timezone: {args.timezone}", file=sys.stderr)
        return 2

    sessions_root = Path(args.sessions_root).expanduser()
    if not sessions_root.is_dir():
        print(f"error: sessions root is not a directory: {sessions_root}", file=sys.stderr)
        return 2

    rows = collect_messages(sessions_root, local_day, timezone)
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(local_day, args.timezone, rows), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
