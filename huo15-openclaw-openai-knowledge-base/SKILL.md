---
name: huo15-openclaw-openai-knowledge-base
displayName: 火一五知识库技能
description: 基于 Karpathy LLM Knowledge Bases 方案。raw → LLM编译 → wiki，支持 Obsidian 同步、知识图谱、微信公众号/GitHub 多源入库，以及 agent/shared 双作用域。触发词：知识库、入库、查询、编译、知识图谱。
version: "2.5.0"
aliases:
  - 火一五知识库
  - 火一五知识库技能
  - 卡帕西知识库
  - 火一五卡帕西知识库技能
dependencies:
  obsidian-cli:
    description: 可选，用于 Obsidian vault 搜索
    install: brew install yakitrak/yakitrak/obsidian-cli
safety:
  virus_total_note: 无硬编码凭证，凭据从 OpenClaw models.json 运行时加载
---

# SKILL.md — huo15-knowledge-base

> 基于 Karpathy LLM Knowledge Bases 方案：raw → LLM编译 → wiki
> 双作用域：
> - **agent**（默认）：`~/.openclaw/agents/{agent-id}/agent/kb/` — 每个 Agent 独立，互不可见
> - **shared**：`~/.openclaw/kb/shared/` — 跨 Agent 共享；通过 @huo15/openclaw-enhance 并入龙虾原生 `memory_search`（corpus=\"kb\"）

---

## 核心：4 个脚本

| 脚本 | 做什么 | 成功标准 |
|------|--------|----------|
| `kb-ingest` | 文档入库（URL/文件/文本/微信公众号/GitHub）| raw/ 下文件存在 |
| `kb-compile` | LLM 编译 raw → wiki | wiki/ 下 .md 文件生成 |
| `kb-search` | 搜索知识库（默认聚合 agent+shared+obsidian） | 搜索结果返回 |
| `kb-graph` | 知识图谱可视化（Mermaid） | kb/wiki/graph.mermaid 生成 |

所有写入类脚本（ingest/compile/graph/lint/sync/obsidian-sync）均支持 `--scope agent|shared`（或 `--shared` 快捷），默认 `agent`。`obsidian-sync` 额外支持 `--all-scopes` 一次同步两层。

---

## 快速开始

```bash
# Agent 私有（默认）
kb-ingest --url "https://..."                        # 入库到当前 Agent
kb-compile                                             # 编译（自动调 LLM）
kb-search "关键词"                                      # 搜全部：agent + shared + Obsidian

# 跨 Agent 共享（长期、稳定的知识资料）
kb-ingest --scope shared --url "https://..."          # 入库到共享库
kb-compile --scope shared                              # 编译共享库
kb-search "关键词" --shared-only                       # 只搜共享库

# 特殊源
kb-ingest --source wechat --url "https://mp.weixin.qq.com/s/..."  # 微信公众号
kb-ingest --source github --url "https://github.com/user/repo"     # GitHub README
kb-graph                                               # 生成知识图谱（Mermaid）
```

---

## 架构

```
agent scope（隔离）：~/.openclaw/agents/{id}/agent/kb/
shared scope（共享）：~/.openclaw/kb/shared/
  ├─ raw/     原始文档（按日期分目录，status: pending/ready）
  ├─ wiki/    LLM 编译后的百科（Markdown，双向链接）
  │          graph.mermaid（知识图谱）
  └─ cache/   临时文件

可选: wiki/ → Obsidian vault（知识库/ 文件夹）
```

---

## 与 @huo15/openclaw-enhance 的协作

| 层 | 存什么 | 入口 |
|----|--------|------|
| L1 龙虾原生 memory | 向量+FTS 底座 | `memory_search` / `memory_get` |
| L2 enhance 结构化记忆 | 短条目「规则/为什么/怎么做」（per-agent） | `enhance_memory_*` 工具 |
| L3 本技能 shared KB | 长文档「事实/资料」（跨 agent） | `kb-*` 脚本；通过 corpus=\"kb\" 被 memory_search 搜到 |

**边界原则**：短规则 → L2；长资料 → L3 shared；agent 私有实验性知识 → L3 agent。

---

## Obsidian 集成

`config.json` 配置：
```json
{
  "obsidian": {
    "enabled": true,
    "vault_path": "/Users/xxx/Documents/我的笔记"
  }
}
```

`kb-search` 自动搜索 wiki/ + Obsidian vault（如果启用）。

同步命令：
```bash
obsidian-sync.sh                     # 默认同步 agent scope → vault/知识库/agent/
obsidian-sync.sh --shared            # 同步 shared scope → vault/知识库/shared/
obsidian-sync.sh --all-scopes        # 两层一起同步（分别入独立子目录）
obsidian-sync.sh --dry-run --all-scopes  # 预览
obsidian-sync.sh --watch --all-scopes    # 监听两层的变化
```

Vault 布局：
```
vault/知识库/
├── agent/    ← 本 Agent 私有 wiki
└── shared/   ← 跨 Agent 共享 wiki
```

---

## 触发词

- "知识库"、"入库知识库"、"查询知识库"
- "编译知识库"、"激活知识库"
- "Obsidian 同步"
- "知识图谱"、"图谱可视化"、"kb-graph"
- "共享知识库"、"跨 Agent 知识库"、"shared kb"
