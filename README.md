# 火一五 Skills 技能库

---

<div align="center">

<img src="https://tools.huo15.com/uploads/images/system/logo-colours.png" alt="火一五Logo" style="width: 120px; height: auto; display: inline; margin: 0;" />

</div>

<div align="center">

<h3>打破信息孤岛，用一套系统驱动企业增长</h3>
<h3>加速企业用户向全场景人工智能机器人转变</h3>

</div>

<div align="center">

| 🏫 教学机构 | 👨‍🏫 讲师 | 📧 联系方式         | 💬 QQ群      | 📺 配套视频                         |
|:-----------:|:--------:|:------------------:|:-----------:|:-----------------------------------:|
| 逸寻智库 | Job | support@huo15.com | 1093992108  | [📺 B站视频](https://space.bilibili.com/400418085) |

</div>

---

## 项目简介

火一五 Skills 技能库是青岛火一五信息科技有限公司为 OpenClaw AI 助手开发的定制化技能集合。每个技能独立模块化设计，可单独安装使用，也可协同工作。

---

## 技能列表

| 技能名称 | 版本 | 说明 |
|---------|------|------|
| [huo15-knowledge-base](#huo15-knowledge-base) | v0.7.2 | 火一五知识库技能 — 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案 |
| [huo15-mit-48h-learning-method](#huo15-mit-48h-learning-method) | — | 麻省理工 48 小时学习法 — 三问学习框架 |

---

## huo15-knowledge-base

> 火一五知识库技能 — 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案

### 核心概念

```
共享 Skill 代码（~/.openclaw/workspace/skills/huo15-knowledge-base/）
                ↓
每个 Agent 独立的数据目录（~/.openclaw/agents/{agent-id}/agent/kb/）
    ├── raw/     → 原始文档（按日期分目录）
    ├── wiki/    → LLM 编译后的结构化百科
    └── cache/   → 临时缓存
```

### 核心脚本

| 脚本 | 功能 |
|------|------|
| `kb-ingest` | 入库文档（自动抓取网页内容）|
| `kb-compile` | LLM 自动编译 raw → wiki |
| `kb-search` | 搜索知识库 |
| `kb-lint` | 体检知识库（自愈）|
| `kb-fetch` | 独立网页抓取工具 |
| `kb-sync` | 桥接 memory-evolution（可选）|

### 触发词

- "知识库"、"入库知识库"、"查询知识库"
- "编译知识库"、"体检知识库"、"同步知识库"
- "激活知识库"

### 安装方式

该技能已集成到 OpenClaw 插件 `@huo15/openclaw-enhance` 中，加载即启用。

---

## huo15-mit-48h-learning-method

> 麻省理工 48 小时学习法 — 三问学习框架

### 核心概念

借鉴 MIT 研究生 Ihtesham Ali 的三问学习框架：

1. **问心智模型**：领域内专家共享的 5 个基本思维框架
2. **问专家分歧**：在哪 3 个问题上根本不同意
3. **问暴露性问题**：生成能区分真懂和假背的 10 个问题

### 触发场景

- 用户要求快速学习某个领域
- 用户提到 MIT 学习法、48 小时学习、NotebookLM 三问
- 用户需要生成播客/视频概览
- 用户想用 AI 辅助构建知识体系

### 实现方式

使用 NotebookLM CLI 实现，自动生成三个维度的学习内容。

---

## 使用前提

- OpenClaw AI 助手（建议源码版本）
- Node.js 24+
- 对应技能依赖（见各技能说明）

---

## 快速开始

```bash
# 克隆仓库
git clone git@github.com:zhaobod1/huo15-skills.git

# 安装技能（复制到 OpenClaw skills 目录）
cp -r huo15-*/ ~/.openclaw/workspace/skills/

# 重启 OpenClaw 即可生效
```

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>

---
