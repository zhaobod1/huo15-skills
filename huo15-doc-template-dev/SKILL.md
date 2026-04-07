---
name: huo15-doc-template
displayName: 火一五文档模板技能
description: 火一五文档模板技能 — 从客户调查问卷自动生成 OpenClaw 引导文件（SOUL.md、IDENTITY.md、USER.md、AGENTS.md、BOOTSTRAP.md、HEARTBEAT.md、TOOLS.md）。触发词：生成配置、生成引导文件、生成问卷配置、生成工作区。
version: 1.0.0
dependencies:
  scripts: ./scripts/
---

# SKILL.md - huo15-doc-template

> 火一五文档模板技能 — 从客户调查问卷自动生成 OpenClaw 引导文件

---

## 概述

本技能从客户填写的 OpenClaw 调查问卷（JSON 格式）自动生成完整的工作区引导文件，适用于新客户快速配置 AI 助手。

## 生成的文件

| 文件 | 说明 |
|------|------|
| `SOUL.md` | AI 人格定义（语气、风格、定位） |
| `IDENTITY.md` | AI 身份信息（名字、头像、角色） |
| `USER.md` | 用户信息（姓名、公司、职位、作息、偏好） |
| `AGENTS.md` | 工作区规则（启动顺序、红线规则） |
| `BOOTSTRAP.md` | 首次对话引导脚本 |
| `HEARTBEAT.md` | 定期心跳检查任务列表 |
| `TOOLS.md` | 常用工具配置 |
| `MEMORY.md` | 长期记忆文件 |
| `memory/YYYY-MM-DD.md` | 每日记忆目录 |

---

## 触发词

- "生成配置"、"生成引导文件"
- "生成问卷配置"、"生成工作区"
- "帮我配置 OpenClaw"、"初始化工作区"

---

## 使用方法

### 方式一：交互式（推荐）

```
用户：帮我从问卷生成 OpenClaw 配置
助手：请问问卷 JSON 文件路径？
用户：/path/to/questionnaire.json
助手：[调用 generate-config.sh 生成配置]
```

### 方式二：直接调用脚本

```bash
bash scripts/generate-config.sh <问卷JSON路径> <输出目录>
```

示例：

```bash
bash scripts/generate-config.sh ./customer问卷.json ~/.openclaw/workspace
```

---

## 问卷 JSON 格式

```json
{
  "name": "张三",
  "company": "某某公司",
  "role": "技术总监",
  "timezone": "Asia/Shanghai",
  "personality": "jarvis",
  "language": "中文",
  "replyStyle": "简洁直接",
  "workSchedule": {
    "workStart": "09:30",
    "workEnd": "18:00",
    "lunchBreak": "12:00-13:00",
    "restDays": "周末双休",
    "canDisturbAfterHours": false,
    "sleepReminderTime": "23:00"
  },
  "tools": ["Claude", "GitHub", "钉钉"],
  "projects": ["OpenClaw技能开发", "Odoo实施"]
}
```

---

## 预设人格

| ID | 名称 | 说明 |
|----|------|------|
| `jarvis` | 贾维斯 | 专业严谨带英式幽默，技术分析与项目管理 |
| `coding_assistant` | 编程助手 | 全栈开发专家，代码优化与重构 |
| `erp_consultant` | 企业套件顾问 | Odoo全模块实施与定制开发 |
| `marketing_strategist` | 营销策略师 | 抖音/小红书/B站全渠道营销 |
| `project_manager` | 项目经理 | 敏捷管理，进度跟踪与风险预警 |
| `customer_support` | 客服代表 | 温和耐心，多渠道客户支持 |
| `content_engine` | 内容引擎 | 批量内容生产与多平台分发 |
| `data_analyst` | 数据分析师 | 数据清洗、可视化与业务洞察 |
| `executive_assistant` | 行政助手 | 日程管理与战略规划支持 |
| `learning_coach` | 学习教练 | 个性化学习路径与技能提升 |

---

## 自定义人格

如预设人格不满足需求，可在问卷中填写：

```json
{
  "customPersonality": {
    "name": "我的AI助手",
    "description": "性格特征描述...",
    "tone": "正式/轻松/幽默",
    "special": "特殊要求..."
  }
}
```

---

## 示例

**输入：** 客户填写完整的问卷 JSON
**输出：** 完整的 OpenClaw 工作区配置文件

---

## 相关技能

- `huo15-knowledge-base` — 知识库管理
- `huo15-mit-48h-learning-method` — 学习框架
