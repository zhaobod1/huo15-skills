# CLAUDE.md

**项目：huo15-knowledge-base** — Karpathy LLM Knowledge Base

## 背景

Karpathy 方案：不用向量数据库，用 LLM 做"研究图书馆员"，把原始文档编译成人类可读的 Wiki百科。

```
raw/ → LLM编译 → wiki/ → Obsidian Vault（可选）
```

## 架构原则

- **数据隔离**：每个 Agent 数据在 `~/.openclaw/agents/{agent-id}/agent/kb/`
- **代码共享**：Skill 代码在技能目录，所有 Agent 共用
- **纯 Markdown**：不用数据库，wiki 是纯 .md 文件
- **无硬编码凭证**：LLM 凭据从 `models.json` 运行时加载

## 脚本清单

**核心（kb-* 前缀）：**
- `kb-ingest` — 入库，支持 URL/文件/文本，自动抓取
- `kb-compile` — 调用 LLM，raw → wiki
- `kb-search` — 搜索 wiki + Obsidian vault
- `kb-lint` — 体检自愈
- `kb-fetch` — 独立网页抓取（Python stdlib）
- `kb-llm.py` — LLM API 调用器（从 models.json 加载）

**Obsidian（可选）：**
- `obsidian-sync.sh` — wiki → vault 同步

**其他（已废弃/合并）：**
- `compile.sh`, `ingest.sh`, `search.sh`, `lint.sh` — 废弃，勿用
- `init.sh`, `activate.sh` — 被 kb-ingest 自动激活取代

## 开发规范

- Python 脚本仅用标准库，无第三方依赖
- LLM 调用走 `kb-llm.py`，不直接调用 API
- 配置走 `config.json`，敏感信息不上传
- 核心脚本不超过 200 行
