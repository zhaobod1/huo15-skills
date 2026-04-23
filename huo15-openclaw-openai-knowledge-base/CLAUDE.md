# CLAUDE.md

**项目：huo15-knowledge-base** — Karpathy LLM Knowledge Base

## 背景

Karpathy 方案：不用向量数据库，用 LLM 做"研究图书馆员"，把原始文档编译成人类可读的 Wiki百科。

```
raw/ → LLM编译 → wiki/ → Obsidian Vault（可选）
```

## 架构原则

- **双作用域**：
  - `agent` 作用域：每个 Agent 数据在 `~/.openclaw/agents/{agent-id}/agent/kb/`（默认，私有）
  - `shared` 作用域：跨 Agent 共享数据在 `~/.openclaw/kb/shared/`（通过 `--scope shared` 写入）
- **代码共享**：Skill 代码在技能目录，所有 Agent 共用
- **纯 Markdown**：不用数据库，wiki 是纯 .md 文件
- **无硬编码凭证**：LLM 凭据从 `models.json` 运行时加载
- **共享 KB 的对接**：@huo15/openclaw-enhance 会把 `~/.openclaw/kb/shared/wiki/` 注册为龙虾 memory 的 corpus（corpus="kb"），使 `memory_search` 能同时搜到共享知识库内容，而无需单独调用 `kb-search`

## 三层记忆/知识库协调

```
L1 龙虾原生 memory（~/.openclaw/memory/*.sqlite, per-agent）
    ├── L2 enhance 结构化记忆（短规则，enhance-memory.sqlite，corpus="enhance"）
    └── L3 共享知识库（长文档，~/.openclaw/kb/shared/wiki/, corpus="kb")
```

**内容归属判断**：
- **一句话能说清 + 关于「怎么做」** → L2 enhance_memory_store
- **整篇文档 + 关于「是什么」** → L3 kb-ingest --scope shared
- **Agent 个人实验性笔记** → L3 kb-ingest（默认 agent scope，不会被其它 agent 看到）

## 脚本清单

**核心（kb-* 前缀）：**
- `kb-ingest` — 入库，支持 URL/文件/文本，自动抓取
- `kb-compile` — 调用 LLM，raw → wiki
- `kb-search` — 搜索 wiki + Obsidian vault
- `kb-lint` — 体检自愈
- `kb-fetch` — 独立网页抓取（Python stdlib）
- `kb-llm.py` — LLM API 调用器（从 models.json 加载）

**Obsidian（可选）：**
- `obsidian-sync.sh` — wiki → vault 同步；支持 `--scope agent|shared` / `--shared` / `--all-scopes`
  - agent scope  → `vault/知识库/agent/`
  - shared scope → `vault/知识库/shared/`

**其他（已废弃/合并）：**
- `compile.sh`, `ingest.sh`, `search.sh`, `lint.sh` — 废弃，勿用
- `init.sh`, `activate.sh` — 被 kb-ingest 自动激活取代

## 开发规范

- Python 脚本仅用标准库，无第三方依赖
- LLM 调用走 `kb-llm.py`，不直接调用 API
- 配置走 `config.json`，敏感信息不上传
- 核心脚本不超过 200 行
