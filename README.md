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

| 技能名称 | 中文别名 | 版本 | 说明 |
|---------|---------|------|------|
| `huo15-cost-tracker-dev` | 火一五成本追踪技能 | v1.0.0 | 追踪 AI API 使用量、Token 消耗和成本计算 |
| `huo15-doc-template-dev` | 火一五文档技能 | v1.0.0 | 从客户调查问卷自动生成 OpenClaw 引导文件 |
| `huo15-memory-evolution-dev` | 火一五记忆进化技能 | v1.0.0 | 四层记忆分类、Dream Agent 日志提炼、Auto Capture |
| `huo15-mit-48h-learning-method-dev` | 火一五麻省理工48小时学习法技能 | v2.1.0 | 三问学习框架：心智模型、专家分歧、暴露性问题 |
| `huo15-multi-agent-dev` | 火一五多智能体技能 | v1.0.0 | 多 Agent 并行工作系统，协调者模式 |
| `huo15-odoo-dev` | 火一五欧度技能 | v1.0.0 | 辉火云企业套件 Odoo 19 XML-RPC 接口访问指南 |
| `huo15-openai-knowledge-base` | 火一五安德烈·卡帕西知识库技能 | v0.7.2 | 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案 |
| `huo15-plan-mode-dev` | 火一五计划模式技能 | v1.1.0 | 危险操作二次确认机制 |

---

## 技能详情

### huo15-cost-tracker-dev — 火一五成本追踪技能

> 追踪 AI API 使用量、Token 消耗和成本计算。支持 MiniMax、OpenAI 等模型。

**触发词：** 成本追踪、火一五成本追踪、花费了多少、token 统计

**依赖：** 可选 `huo15-memory-evolution`

---

### huo15-doc-template-dev — 火一五文档技能

> 从客户调查问卷自动生成 OpenClaw 引导文件（SOUL.md、IDENTITY.md、USER.md 等）。

**触发词：** 生成配置、生成引导文件、生成问卷配置、生成工作区

---

### huo15-memory-evolution-dev — 火一五记忆进化技能

> 完全自主实现，提供四类记忆分类、Dream Agent 日志提炼、Team Memory 共享、Auto Capture 自动捕获、Session State 管理器、任务进度追踪器。

**触发词：** 记忆系统、记忆进化、记忆重构

---

### huo15-mit-48h-learning-method-dev — 火一五麻省理工48小时学习法技能

> 使用 NotebookLM CLI 实现 MIT 研究生 Ihtesham Ali 的三问学习框架。

**三问框架：**
1. **问心智模型**：领域内专家共享的 5 个基本思维框架
2. **问专家分歧**：在哪 3 个问题上根本不同意
3. **问暴露性问题**：生成能区分真懂和假背的 10 个问题

**触发词：** MIT 学习法、48 小时学习、NotebookLM 三问

---

### huo15-multi-agent-dev — 火一五多智能体技能

> 基于 OpenClaw sessions_spawn 的多 Agent 并行工作系统。支持协调者模式、任务分配、结果汇总。

**触发词：** 多智能体协同、多 Agent、并行任务、协调者模式

**依赖：** 可选 `huo15-memory-evolution`、`huo15-cost-tracker`

---

### huo15-odoo-dev — 火一五欧度技能

> 辉火云企业套件（Odoo 19）接口访问指南。提供 XML-RPC API 连接、客户、项目、任务等模型的正确查询和创建方式。

**触发词：** Odoo、欧度、企业套件、XML-RPC

---

### huo15-openai-knowledge-base — 火一五安德烈·卡帕西知识库技能

> 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案。每个 Agent 独立隔离，自动在 Agent 工作目录下创建专属知识库。

**触发词：** 知识库、入库知识库、查询知识库、编译知识库

---

### huo15-plan-mode-dev — 火一五计划模式技能

> 危险操作二次确认机制。检测到危险操作时自动暂停，等待用户确认后再执行。

**触发词：** Plan Mode、危险操作确认、二次确认

**依赖：** 可选 `huo15-memory-evolution`

---

## 使用前提

- OpenClaw AI 助手（建议源码版本）
- Node.js 24+
- 对应技能依赖（见各技能说明）

---

## 安装方式

### 方式一：从 clawhub 安装（推荐）

```bash
clawhub install <技能名称> --dir ~/.openclaw/workspace/skills
```

示例：

```bash
clawhub install huo15-cost-tracker-dev --dir ~/.openclaw/workspace/skills
clawhub install huo15-odoo-dev --dir ~/.openclaw/workspace/skills
```

### 方式二：从源码安装

```bash
# 克隆仓库
git clone git@github.com:zhaobod1/huo15-skills.git

# 复制单个技能到 OpenClaw skills 目录
cp -r <技能目录>/ ~/.openclaw/workspace/skills/

# 重启 OpenClaw 即可生效
```

---

## clawhub 地址

所有技能均已发布到 [ClawHub](https://clawhub.ai)：

- https://clawhub.ai/skills/huo15-cost-tracker-dev
- https://clawhub.ai/skills/huo15-doc-template-dev
- https://clawhub.ai/skills/huo15-memory-evolution-dev
- https://clawhub.ai/skills/huo15-mit-48h-learning-method-dev
- https://clawhub.ai/skills/huo15-multi-agent-dev
- https://clawhub.ai/skills/huo15-odoo-dev
- https://clawhub.ai/skills/huo15-openai-knowledge-base
- https://clawhub.ai/skills/huo15-plan-mode-dev

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>

---
