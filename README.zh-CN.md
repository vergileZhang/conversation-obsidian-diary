# Conversation Obsidian Diary

[English](README.md) · [MIT License](LICENSE)

这是一个不绑定具体 AI 工具的 [Agent Skill](https://agentskills.io/)，用于把 AI 对话整理成 Obsidian 每日回顾和按主题长期积累的第二大脑。

## 它能做什么

- 按时间线整理当天有价值的 AI 对话。
- 把可复用知识、决策、排障经验和项目进展归档到长期主题笔记。
- 将内容划分为知识学习、项目相关、操作实践、个人成长、学术研究和生活事务。
- 只维护带有明确标记的区域，保留用户自己写的其他内容。
- 一次性操作只进入当日日记，避免污染长期知识库。
- 支持标准 Markdown 对话、通用 JSON 导出和可选的 Codex JSONL 会话提取。

该 Skill 不会上传对话，也不依赖 Obsidian 在线服务；它只通过宿主 Agent 已有的文件能力操作本地笔记。

## 仓库结构

```text
conversation-obsidian-diary/     # 安装这个内层目录
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

## 安装

克隆仓库，然后把内层 `conversation-obsidian-diary` 目录复制或软链接到你的 AI 工具所支持的 Skill 目录：

```bash
git clone https://github.com/vergileZhang/conversation-obsidian-diary.git
cp -R conversation-obsidian-diary/conversation-obsidian-diary /path/to/your/agent/skills/
```

正确安装后应存在：

```text
conversation-obsidian-diary/SKILL.md
```

不同工具和版本的 Skill 安装路径可能不同，请以对应工具的官方文档为准。这个仓库本身不依赖任何厂商。

## 配置

可以在请求中告诉 Agent 以下信息，也可以复制 `assets/config.example.yaml` 后在本地填写：

- Obsidian Vault 路径
- 目标日期与 IANA 时区
- 每日日记文件名规则
- 第二大脑根目录
- 附件目录

完整说明见 [configuration.md](conversation-obsidian-diary/references/configuration.md)。不要提交包含本地路径的实际配置文件。

## 使用示例

```text
使用 conversation-obsidian-diary，把我今天的 AI 对话整理成 Obsidian 每日回顾，并更新值得长期保留的主题笔记。Vault 位于 <vault-path>，时区是 Asia/Shanghai。保留托管标记以外的全部原文。
```

如果你的工具不会自动发现 Skill，可以明确要求它读取 `conversation-obsidian-diary/SKILL.md` 并执行其中流程。

## 准备对话数据

核心 Skill 使用 [transcript-format.md](conversation-obsidian-diary/references/transcript-format.md) 中定义的标准 Markdown 对话格式。

### 通用 JSON 导出

```bash
python3 conversation-obsidian-diary/scripts/normalize_transcript.py \
  --input /path/to/conversation.json \
  --timezone Asia/Shanghai \
  --output /tmp/conversation-transcript.md
```

### Codex JSONL 会话

```bash
python3 conversation-obsidian-diary/scripts/extract_codex_day.py \
  --date 2026-11-08 \
  --timezone Asia/Shanghai \
  --sessions-root /path/to/codex/sessions \
  --output /tmp/conversation-transcript.md
```

两个适配器都只使用 Python 3 标准库，不会发起网络请求。

## 隐私与安全

- 如果导出内容可能包含密钥，请先人工检查。
- 不要把 Vault、真实对话、附件或填写后的本地配置提交到 Git。
- Skill 不会自动授权上传或公开任何私人笔记。
- 用户自己写的内容位于托管标记之外，必须保留。
- 如果托管标记损坏或含义不明确，应先备份并停止，而不是覆盖文件。

## 开发与验证

```bash
python3 -m unittest discover -s tests -v
```

如果已安装 Agent Skills 参考验证器：

```bash
skills-ref validate ./conversation-obsidian-diary
```

测试还会检查公开文本是否意外包含作者主目录或常见凭证格式。

## 来源

这个项目源自一个个人使用的 Codex → Obsidian 日记工作流。公开版本把 Codex 降为可选的数据适配器，核心流程可以接收来自任何 AI 工具的标准化对话。

## 许可证

[MIT](LICENSE)
