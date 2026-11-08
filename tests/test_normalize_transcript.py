from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "conversation-obsidian-diary" / "scripts" / "normalize_transcript.py"
FIXTURE = ROOT / "tests" / "fixtures" / "conversation.json"


class NormalizeTranscriptTests(unittest.TestCase):
    def test_normalizes_generic_json_messages(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "transcript.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(FIXTURE),
                    "--output",
                    str(output),
                    "--timezone",
                    "Asia/Shanghai",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn("# Conversation transcript", text)
            self.assertIn("- messages: 3", text)
            self.assertIn("## 2026-11-08 09:00:00 User", text)
            self.assertIn("How should I organize today's notes?", text)
            self.assertIn("## 2026-11-08 09:00:05 Assistant", text)
            self.assertNotIn("ignored system message", text)

    def test_rejects_json_without_messages_array(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            invalid = temp / "invalid.json"
            invalid.write_text('{"items": []}', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(invalid), "--output", str(temp / "out.md")],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("messages", result.stderr)


if __name__ == "__main__":
    unittest.main()
