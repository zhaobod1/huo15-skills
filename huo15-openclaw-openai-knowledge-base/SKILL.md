---
name: huo15-openclaw-openai-knowledge-base
displayName: 火一五知识库技能
description: 基于 Karpathy LLM Knowledge Bases 方案。raw → LLM编译 → wiki，支持 Obsidian 同步、知识图谱、微信公众号/GitHub 多源入库。触发词：知识库、入库、查询、编译、知识图谱。
version: "2.3.0"
dependencies:
  obsidian-cli:
    description: 可选，用于 Obsidian vault 搜索
    install: brew install yakitrak/yakitrak/obsidian-cli
safety:
  virus_total_note: 无硬编码凭证，凭据从 OpenClaw models.json 运行时加载
---

# SKILL.md — huo15-knowledge-base

> 基于 Karpathy LLM Knowledge Bases 方案：raw → LLM编译 → wiki
> 每个 Agent 隔离，数据在 `~/.openclaw/agents/{agent-id}/agent/kb/`

---

## 核心：4 个脚本

| 脚本 | 做什么 | 成功标准 |
|------|--------|----------|
| `kb-ingest` | 文档入库（URL/文件/文本/微信公众号/GitHub）| raw/ 下文件存在 |
| `kb-compile` | LLM 编译 raw → wiki | wiki/ 下 .md 文件生成 |
| `kb-search` | 搜索知识库 | 搜索结果返回 |
| `kb-graph` | 知识图谱可视化（Mermaid） | kb/wiki/graph.mermaid 生成 |

---

## 快速开始

```bash
kb-ingest --url "https://..."                        # 入库 + 自动抓取
kb-ingest --source wechat --url "https://mp.weixin.qq.com/s/..."  # 微信公众号
kb-ingest --source github --url "https://github.com/user/repo"     # GitHub README
kb-compile                                             # 编译（自动调 LLM）
kb-search "关键词"                                      # 搜索 wiki + Obsidian
kb-graph                                               # 生成知识图谱（Mermaid）
```

---

## 架构

```
raw/   → 原始文档（按日期分目录，status: pending/ready）
wiki/  → LLM 编译后的百科（Markdown，双向链接）
       → graph.mermaid（知识图谱，可视化链接关系）
cache/ → 临时文件

可选: wiki/ → Obsidian vault（知识库/ 文件夹）
```

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

---

## 触发词

- "知识库"、"入库知识库"、"查询知识库"
- "编译知识库"、"激活知识库"
- "Obsidian 同步"
- "知识图谱"、"图谱可视化"、"kb-graph"
