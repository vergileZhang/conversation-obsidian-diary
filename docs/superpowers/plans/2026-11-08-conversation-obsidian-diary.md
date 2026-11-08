# Conversation Obsidian Diary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a tested, privacy-safe, vendor-neutral Agent Skill for turning AI conversations into Obsidian daily and second-brain notes.

**Architecture:** A standard `conversation-obsidian-diary/SKILL.md` defines the portable workflow. Stdlib-only adapters normalize Codex JSONL or generic JSON into one Markdown transcript contract; references and an example config keep platform details out of the core instructions.

**Tech Stack:** Agent Skills open format, Markdown, Python 3 standard library, `unittest`, Git, GitHub CLI.

---

### Task 1: Establish failing public-package tests

**Files:**
- Create: `tests/test_public_package.py`
- Create: `tests/test_extract_codex_day.py`
- Create: `tests/test_normalize_transcript.py`
- Create: `tests/fixtures/codex-session.jsonl`
- Create: `tests/fixtures/conversation.json`

- [ ] Write structural tests requiring valid skill frontmatter, matching directory name, referenced resources, absence of author-specific paths, and required public documentation.
- [ ] Write behavior tests for timezone-aware Codex extraction and generic JSON normalization.
- [ ] Run `python3 -m unittest discover -s tests -v` and confirm failure because the public package and scripts do not exist.
- [ ] Commit the RED tests and fixtures.

### Task 2: Build the portable skill package

**Files:**
- Create: `conversation-obsidian-diary/SKILL.md`
- Create: `conversation-obsidian-diary/references/configuration.md`
- Create: `conversation-obsidian-diary/references/transcript-format.md`
- Create: `conversation-obsidian-diary/assets/config.example.yaml`

- [ ] Adapt the existing diary classification and managed-marker rules into vendor-neutral instructions.
- [ ] Move conditional configuration and transcript details into linked references.
- [ ] Run the structural tests and confirm the skill-package checks pass.
- [ ] Commit the portable skill resources.

### Task 3: Implement transcript adapters

**Files:**
- Create: `conversation-obsidian-diary/scripts/extract_codex_day.py`
- Create: `conversation-obsidian-diary/scripts/normalize_transcript.py`

- [ ] Generalize the existing Codex extractor without personal paths and preserve its stdlib-only behavior.
- [ ] Implement JSON-to-Markdown normalization for timestamped `user` and `assistant` messages.
- [ ] Run `python3 -m unittest discover -s tests -v` and confirm all adapter tests pass.
- [ ] Commit the scripts.

### Task 4: Add public documentation and licensing

**Files:**
- Create: `README.md`
- Create: `README.zh-CN.md`
- Create: `LICENSE`
- Create: `.gitignore`

- [ ] Document clone/copy installation, portable invocation, both adapters, configuration, privacy boundaries, and contribution workflow.
- [ ] Add the MIT license and ignore caches, virtual environments, generated transcripts, local configuration, and vault data.
- [ ] Run the full test suite and link checks.
- [ ] Commit the public documentation.

### Task 5: Validate and publish

**Files:**
- Verify all tracked repository files.

- [ ] Run `python3 -m unittest discover -s tests -v`.
- [ ] Run Python bytecode compilation and both scripts' `--help` commands.
- [ ] Run skill conformance validation.
- [ ] Scan tracked files for author-specific home paths, credential patterns, and private conversation data.
- [ ] Review `git diff --check`, the commit history, and the final tracked-file list.
- [ ] Create the public GitHub repository `vergileZhang/conversation-obsidian-diary`, push `main`, set description/topics, and verify the remote repository URL and visibility.
