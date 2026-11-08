from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "conversation-obsidian-diary"


class PublicPackageTests(unittest.TestCase):
    def test_required_public_files_exist(self) -> None:
        required = [
            ROOT / "README.md",
            ROOT / "README.zh-CN.md",
            ROOT / "LICENSE",
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "scripts" / "extract_codex_day.py",
            SKILL_ROOT / "scripts" / "normalize_transcript.py",
            SKILL_ROOT / "references" / "configuration.md",
            SKILL_ROOT / "references" / "transcript-format.md",
            SKILL_ROOT / "assets" / "config.example.yaml",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [])

    def test_skill_frontmatter_matches_directory(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match, "SKILL.md must start with YAML frontmatter")
        frontmatter = match.group(1)
        self.assertRegex(frontmatter, r"(?m)^name: conversation-obsidian-diary$")
        description = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
        self.assertIsNotNone(description)
        self.assertGreater(len(description.group(1).strip()), 20)
        self.assertLessEqual(len(description.group(1).strip()), 1024)

    def test_skill_links_every_bundled_reference(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for relative in [
            "references/configuration.md",
            "references/transcript-format.md",
            "scripts/extract_codex_day.py",
            "scripts/normalize_transcript.py",
        ]:
            self.assertIn(relative, skill)

    def test_public_text_does_not_contain_author_home_or_credentials(self) -> None:
        author_home = str(Path.home())
        forbidden_patterns = [
            re.compile(re.escape(author_home)),
            re.compile(r"gh[opurs]_[A-Za-z0-9_]{20,}"),
            re.compile(r"sk-[A-Za-z0-9]{20,}"),
        ]
        violations: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if any(pattern.search(text) for pattern in forbidden_patterns):
                violations.append(str(path.relative_to(ROOT)))
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
