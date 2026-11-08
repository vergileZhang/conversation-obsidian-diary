from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "conversation-obsidian-diary" / "scripts" / "extract_codex_day.py"
FIXTURE = ROOT / "tests" / "fixtures" / "codex-session.jsonl"


class ExtractCodexDayTests(unittest.TestCase):
    def test_extracts_only_messages_in_requested_local_day(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            session_dir = temp / "sessions" / "2026" / "11" / "08"
            session_dir.mkdir(parents=True)
            (session_dir / "session.jsonl").write_text(
                FIXTURE.read_text(encoding="utf-8"), encoding="utf-8"
            )
            output = temp / "transcript.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--date",
                    "2026-11-08",
                    "--timezone",
                    "Asia/Shanghai",
                    "--sessions-root",
                    str(temp / "sessions"),
                    "--output",
                    str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn("# Conversation transcript for 2026-11-08", text)
            self.assertIn("- timezone: Asia/Shanghai", text)
            self.assertIn("- messages: 2", text)
            self.assertIn("00:30:00 User", text)
            self.assertIn("23:59:00 Assistant", text)
            self.assertNotIn("outside requested day", text)
            self.assertNotIn("system-only content", text)


if __name__ == "__main__":
    unittest.main()
