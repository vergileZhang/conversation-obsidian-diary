#!/usr/bin/env python3
"""Normalize a generic JSON conversation export into Markdown."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any, Optional
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


def local_timestamp(value: Any, timezone: ZoneInfo) -> Optional[dt.datetime]:
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        raise ValueError("timestamp must be an ISO 8601 string")
    try:
        instant = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid timestamp {value!r}") from exc
    if instant.tzinfo is None:
        instant = instant.replace(tzinfo=timezone)
    return instant.astimezone(timezone)


def normalize_messages(data: Any, timezone: ZoneInfo) -> list[tuple[Optional[dt.datetime], str, str]]:
    if not isinstance(data, dict) or not isinstance(data.get("messages"), list):
        raise ValueError("input JSON must contain a messages array")
    rows: list[tuple[Optional[dt.datetime], str, str]] = []
    for index, message in enumerate(data["messages"]):
        if not isinstance(message, dict):
            raise ValueError(f"messages[{index}] must be an object")
        role = message.get("role")
        if role not in {"user", "assistant"}:
            continue
        content = text_from_content(message.get("content"))
        if not content:
            continue
        try:
            instant = local_timestamp(message.get("timestamp"), timezone)
        except ValueError as exc:
            raise ValueError(f"messages[{index}]: {exc}") from exc
        rows.append((instant, role, content))
    return rows


def render_markdown(
    timezone_name: str, rows: list[tuple[Optional[dt.datetime], str, str]]
) -> str:
    lines = ["# Conversation transcript", "", f"- timezone: {timezone_name}", f"- messages: {len(rows)}", ""]
    for instant, role, content in rows:
        label = "User" if role == "user" else "Assistant"
        timestamp = instant.strftime("%Y-%m-%d %H:%M:%S") if instant else "Unknown time"
        lines.extend([f"## {timestamp} {label}", "", content, ""])
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize a generic JSON conversation export into Markdown."
    )
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--output", required=True, help="Destination Markdown file")
    parser.add_argument("--timezone", default="UTC", help="IANA timezone, for example Asia/Shanghai")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        timezone = ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError:
        print(f"error: unknown IANA timezone: {args.timezone}", file=sys.stderr)
        return 2

    input_path = Path(args.input).expanduser()
    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
        rows = normalize_messages(data, timezone)
    except OSError as exc:
        print(f"error: cannot read input: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: input is not valid JSON: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(args.timezone, rows), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
