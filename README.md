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

| 技能名称 | slug | 版本 | 说明 | 触发词 |
|---------|------|------|------|--------|
| `huo15-openclaw-openai-knowledge-base` | `huo15-openclaw-openai-knowledge-base` | v0.9.0 | Karpathy 方案知识库 + Obsidian 集成 | 知识库、入库、查询、编译、体检 |
| `huo15-openclaw-mit-48h-learning-method` | `huo15-openclaw-mit-48h-learning-method` | v2.2.0 | MIT 三问学习框架（心智模型/专家分歧/暴露性问题）| MIT学习法、48小时学习 |
| `huo15-openclaw-office-doc` | `huo15-openclaw-office-doc` | v3.1.0 | 企业级 Word 文档生成（规则/模板双模式）| 写word、写文档、生成合同 |
| `huo15-openclaw-multi-agent` | `huo15-openclaw-multi-agent` | v1.0.0 | 多 Agent 并行工作系统（协调者模式）| 多智能体协同、多Agent、并行任务 |
| `huo15-openclaw-memory-curator` | `huo15-openclaw-memory-curator` | v1.1.0 | 记忆整理技能，审查更新 MEMORY.md | 记忆整理、清理记忆 |
| `huo15-openclaw-plan-mode` | `huo15-openclaw-plan-mode` | v1.0.0 | 结构化规划模式，执行前系统性规划 | 规划模式、做计划 |
| `huo15-openclaw-verify-mode` | `huo15-openclaw-verify-mode` | v1.1.0 | 验证模式，检查成果、运行测试 | 验证模式、检查工作 |
| `huo15-openclaw-explore-mode` | `huo15-openclaw-explore-mode` | v1.1.0 | 深度探索模式，只读调研代码库/系统 | 探索模式、调查、深度调研 |
| `huo15-openclaw-frontend-design` | `huo15-openclaw-frontend-design` | v1.0.0 | 高保真 Web UI 原型 + 5 美学流派 + 反 AI Slop 硬红线 | 做网站、落地页、UI 设计、HTML 原型、美化页面 |
| `huo15-openclaw-design-director` | `huo15-openclaw-design-director` | v1.0.0 | 设计方向顾问（5 流派 × 20 哲学 → 3 方向反差对比）| 选设计方向、做几个方向对比、风格提案 |
| `huo15-openclaw-brand-protocol` | `huo15-openclaw-brand-protocol` | v1.0.0 | 品牌规范抓取（Ask/Search/Download/Verify/Codify）| 抓品牌规范、做 brand kit、VI 规范 |
| `huo15-openclaw-design-critique` | `huo15-openclaw-design-critique` | v1.0.0 | 5 维设计评审 + Keep/Fix/Quick Wins 三分类 | 设计评审、UI 审查、给页面打分 |
| `huo15-img-test` | `huo15-img-test` | v2.1.0 | 文生图提示词增强（88 风格预设 + 五锁一致性 + 意图/时间/天气/季节/负向识别 + 角色设定图 + 画质三档 + 系列批量）| 文生图、提示词增强、生成图片、角色一致、系列图、原神风、敦煌风、汉服写真、玻璃拟态、角色设定图 |
| `huo15-openclaw-bootstrap` | `huo15-openclaw-bootstrap` | v1.0.0 | 龙虾首次初始化：昵称/英文名/时区 + 主辅灵魂融合 + 1-3 角色叠加 + 75+ 领域多选 + 6 经典组合，三层记忆同步 | 你好世界、龙虾初始化、bootstrap、hello world、onboarding、首次设置 |
---


## 技能详情

### huo15-openclaw-openai-knowledge-base — 火一五知识库技能

> 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案。raw → LLM编译 → wiki → Obsidian vault 自动同步，形成第二大脑。

**核心特性：**
- 自动复用 OpenClaw 配置的 minimax-cn API（零额外配置）
- 编译后自动同步到 Obsidian vault「知识库/」文件夹
- 支持图谱视图、双向链接、vault 全局搜索
- Obsidian 集成脚本 `obsidian-sync.sh`（支持 `--watch` 监听模式）

**触发词：** 知识库、入库知识库、查询知识库、编译知识库、体检知识库

---

### huo15-openclaw-mit-48h-learning-method — 火一五 MIT 48小时学习法技能

> 使用 NotebookLM CLI 实现 MIT 研究生 Ihtesham Ali 的三问学习框架，快速建立领域专家级认知。

**三问框架：**
1. **问心智模型**：领域内专家共享的 5 个基本思维框架
2. **问专家分歧**：在哪 3 个问题上根本不同意
3. **问暴露性问题**：生成能区分真懂和假背的 10 个问题

**触发词：** MIT学习法、48小时学习、NotebookLM三问

---

### huo15-openclaw-office-doc — 火一五文档技能

> 企业级 Word 文档生成技能，支持两种模式：
> - **规则模式**：根据规则自动生成（合同/方案/报告/会议纪要）
> - **模板模式**：上传 .docx 模板，填充内容

**触发词：** 写word、写文档、生成word、生成文档、创建文档、.docx、Word文档、写合同、写方案、写报告、写会议纪要、按模板生成

---

### huo15-openclaw-multi-agent — 火一五多智能体技能

> 基于 OpenClaw `sessions_spawn` 的多 Agent 并行工作系统。支持协调者模式、任务分配、结果汇总。

**触发词：** 多智能体协同、多Agent、并行任务、协调者模式

---

### huo15-openclaw-memory-curator — 火一五记忆整理技能

> 审查结构化记忆，提取洞察，更新 MEMORY.md，清理过期条目。周期性心跳检查时自动触发。

**触发词：** 记忆整理、清理记忆、整理记忆

---

### huo15-openclaw-plan-mode — 火一五规划模式技能

> 结构化规划模式 — 在执行复杂任务前先做系统性规划，借鉴 Claude Code Plan Agent。

**触发词：** 规划模式、做计划、帮我规划

---

### huo15-openclaw-verify-mode — 火一五验证模式技能

> 验证模式 — 检查工作成果、运行测试、验证假设，借鉴 Claude Code Verification Agent。

**触发词：** 验证模式、检查工作、验证成果

---

### huo15-openclaw-explore-mode — 火一五探索模式技能

> 深度探索模式 — 系统性调研代码库、系统或话题，只读不改，借鉴 Claude Code Explore Agent。

**触发词：** 探索模式、调查、深度调研、了解项目架构

---

### huo15-openclaw-bootstrap — 火一五你好世界技能

> 刚孵化的龙虾一次性 15 分钟开机仪式：昵称/英文名/时区 → 主辅灵魂融合 → 1-3 角色叠加 → 75+ 领域多选 → 沟通/自主度/生态偏好。支持 6 个经典组合（独立开发者 / 品牌设计师 / PM / 技术博主 / AI 研究员 / 创业者）一键套用，结果三层同步（L1 龙虾 memory / L2 enhance 规则 / L3 KB wiki）。

**核心设计：**
- **灵魂融合**：主 + 辅双选（权重 70/30 / 60/40 等），如"硅谷导师 × 禅师 = 果断但克制"
- **角色叠加**：1 主 + 0-2 辅，支持斜杠青年
- **领域多选**：82 项跨 10 大类，黄金区 5-15 项
- **可跳过**：每步都可跳过，记 `skipped: true`，后续可补
- **增量更新**：再次触发时自动进入 diff 模式

**触发词：** 你好世界、龙虾初始化、bootstrap、hello world、onboarding、首次设置、欢迎、初始化龙虾、重新认识一下

---

## 安装方式

### 方式一：从 clawhub 安装（推荐）

```bash
# 安装单个技能
clawhub install <slug> --dir ~/.openclaw/workspace/skills

# 示例
clawhub install huo15-openclaw-openai-knowledge-base --dir ~/.openclaw/workspace/skills
clawhub install huo15-openclaw-mit-48h-learning-method --dir ~/.openclaw/workspace/skills
clawhub install huo15-openclaw-office-doc --dir ~/.openclaw/workspace/skills
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

## 发布工作流（开发规范）

```
GitHub 仓库（主） → clawhub publish → 本地 clawhub update
```

**步骤：**
1. 在 GitHub 仓库开发：`~/workspace/projects/openclaw/huo15-skills/`
2. 提交推送：`git add -A && git commit -m "说明" && git push`
3. 发布到 clawhub：`clawhub publish /path/to/skill --slug <slug> --version x.y.z`
4. 本地更新：`clawhub update 技能名 --force`

**⚠️ 强制规则：**
- 所有技能从 `huo15-skills` 仓库开发，禁止直接在 clawhub 页面上传
- slug 必须与目录名一致，若 slug 被占用（报 "Slug is already taken"），先清理残留记录再发布，不要另起新名
- 版本号必须语义化（semver），发布后不可重复同一版本号

---

## clawhub 地址

所有技能均已发布到 [ClawHub](https://clawhub.ai)：

- https://clawhub.ai/skills/huo15-openclaw-openai-knowledge-base
- https://clawhub.ai/skills/huo15-openclaw-mit-48h-learning-method
- https://clawhub.ai/skills/huo15-openclaw-office-doc
- https://clawhub.ai/skills/huo15-openclaw-multi-agent
- https://clawhub.ai/skills/huo15-openclaw-memory-curator
- https://clawhub.ai/skills/huo15-openclaw-plan-mode
- https://clawhub.ai/skills/huo15-openclaw-verify-mode
- https://clawhub.ai/skills/huo15-openclaw-explore-mode
- https://clawhub.ai/skills/huo15-openclaw-frontend-design
- https://clawhub.ai/skills/huo15-openclaw-design-director
- https://clawhub.ai/skills/huo15-openclaw-brand-protocol
- https://clawhub.ai/skills/huo15-openclaw-design-critique
- https://clawhub.ai/skills/huo15-openclaw-bootstrap
- https://clawhub.ai/skills/huo15-img-test

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>
