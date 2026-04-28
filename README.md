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

火一五 Skills 技能库是青岛火一五信息科技有限公司为 OpenClaw / Claude Code AI
助手开发的定制化技能集合。每个技能独立模块化设计，可单独安装使用，也可协同
工作。

仓库镜像：
- **CNB.cool（主）：** [`huo15/ai/huo15-skills`](https://cnb.cool/huo15/ai/huo15-skills)
- **GitHub（同步）：** [`zhaobod1/huo15-skills`](https://github.com/zhaobod1/huo15-skills)
- **ClawHub 发布：** [clawhub.ai/skills?author=huo15](https://clawhub.ai)

---

## 技能列表（按类别）

> 共 **24** 个 skill。✅ = 已发布到 ClawHub，全部均为 MIT-0 / 商用免费。

### 一、OpenClaw 工程模式（PR / Plan / Verify / Explore）

| Slug | 版本 | 一句话说明 |
|------|:----:|-----------|
| [`huo15-openclaw-plan-mode`](huo15-openclaw-plan-mode/) | v1.0.2 | 结构化规划模式 — 借鉴 Claude Code Plan Agent，执行复杂任务前先做系统性规划 |
| [`huo15-openclaw-verify-mode`](huo15-openclaw-verify-mode/) | v2.2.0 | 验证模式 — 检查成果、跑测试、验证假设，借鉴 Claude Code Verification Agent |
| [`huo15-openclaw-explore-mode`](huo15-openclaw-explore-mode/) | v1.1.1 | 深度探索模式 — 系统性调研代码库 / 系统 / 话题，只读不改 |
| [`huo15-openclaw-code-review`](huo15-openclaw-code-review/) | v1.0.0 | GitHub / cnb.cool PR 五维评审（设计 / 实现 / 测试 / 安全 / 可维护），可粘贴到 PR |
| [`huo15-openclaw-security-review`](huo15-openclaw-security-review/) | v1.0.0 | 当前分支 pending 改动安全评审：密钥泄露 / SQLi / XSS / SSRF / 权限绕过 / 危险依赖 |
| [`huo15-openclaw-simplify`](huo15-openclaw-simplify/) | v1.0.0 | "复用 / 质量 / 效率"三维审查刚写完的代码 + 实际修复命中问题 |
| [`huo15-openclaw-multi-agent`](huo15-openclaw-multi-agent/) | v2.2.1 | 基于 OpenClaw sessions_spawn 的多 Agent 并行工作系统（协调者模式 / 任务分配 / 结果汇总） |

### 二、学习与知识库

| Slug | 版本 | 一句话说明 |
|------|:----:|-----------|
| [`huo15-openclaw-openai-knowledge-base`](huo15-openclaw-openai-knowledge-base/) | v2.7.0 | Karpathy LLM Knowledge Bases 方案：raw → LLM 编译 → wiki + Obsidian vault 自动同步 |
| [`huo15-openclaw-mit-48h-learning-method`](huo15-openclaw-mit-48h-learning-method/) | v3.0.0 | MIT 48 小时学习法（Ihtesham Ali 三问框架 + 反馈循环 + 完整 48h 三阶段时间线） |
| [`huo15-karpathy-guidelines`](huo15-karpathy-guidelines/) | v1.0.3 | 把 Andrej Karpathy 的 LLM 编程四大行为规范打包为可触发 skill |

### 三、龙虾身份与记忆（OpenClaw 专属）

| Slug | 版本 | 一句话说明 |
|------|:----:|-----------|
| [`huo15-openclaw-bootstrap`](huo15-openclaw-bootstrap/) | v1.1.0 | 龙虾首次开机仪式：4 步搞定身份初始化（基本信息 / 6 经典组合人设 / 领域套餐 / 沟通偏好） |
| [`huo15-openclaw-memory-curator`](huo15-openclaw-memory-curator/) | v1.1.0 | 审查结构化记忆，提取洞察，更新 MEMORY.md，清理过期条目 |

### 四、文档输出

| Slug | 版本 | 一句话说明 |
|------|:----:|-----------|
| [`huo15-openclaw-office-doc`](huo15-openclaw-office-doc/) | **v7.6.1** ⭐ | 企业级 Word & PDF 文档生成。**39 类规范**（含合同细分 7 类）+ **22 份 markdown 范本**。三条路径：Word 直出 / 原生 PDF / Word→PDF |
| [`huo15-openclaw-ppt`](huo15-openclaw-ppt/) | v3.2.1 | 21 套生产级审美方案（Apple 发布会 / Liquid Glass / Vercel / Linear 等）+ design tokens 驱动 |
| [`huo15-flow-chart`](huo15-flow-chart/) | v1.4.0 | 2026 现代美学的流程图 / 泳道图 / 系统架构 / C4 / 时序 / 状态 / ER / 甘特图（Linear / Vercel / Radix 风格） |
| [`huo15-mind-map`](huo15-mind-map/) | v1.2.0 | 思维导图生成（XMind 2021+ / OPML / FreeMind / Markdown 多格式互转） |

### 五、设计

| Slug | 版本 | 一句话说明 |
|------|:----:|-----------|
| [`huo15-openclaw-frontend-design`](huo15-openclaw-frontend-design/) | v4.7.0 | 高保真 Web UI / H5 / iOS / Android / HarmonyOS / 微信+支付宝+抖音+快手 四端小程序 原生风格原型 |
| [`huo15-openclaw-design-director`](huo15-openclaw-design-director/) | v3.0.0 | 6 大美学流派 × 24 设计哲学库 → 3 方向反差对比（hex 配色 + 字体 + 当代标杆） |
| [`huo15-openclaw-design-critique`](huo15-openclaw-design-critique/) | v2.0.0 | 6 维设计评审（美学 / 可用性 / 品牌 / 内容 / 技术 / 时代感）+ 审美档位识别（AI-Slop / Junior / Senior / Master） |
| [`huo15-openclaw-brand-protocol`](huo15-openclaw-brand-protocol/) | v1.0.0 | 抓品牌规范产出 brand-spec.md（5 步：Ask / Search / Download / Verify+Extract / Codify） |
| [`huo15-img-prompt`](huo15-img-prompt/) | v3.2.0 | 文生图提示词中枢，14 件套 + 88 预设审美锚点 + 故事板 / 品牌套件 / 风格学习 / doctor 健康检查 |

### 六、内容创作

| Slug | 版本 | 一句话说明 |
|------|:----:|-----------|
| [`huo15-xiaohongshu`](huo15-xiaohongshu/) | v3.2.0 | 小红书创作伙伴：工程师流 + Allen 流双打分（标题 / 首段 / 排版 / 留白 / AI 腔 / 带读者 / 共鸣） |
| [`huo15-influencer-video-skill`](huo15-influencer-video-skill/) | v2.0.0 | 火山方舟 Seedance 2.0 第一人称带货短视频 + 剧本驱动配音（edge-tts / 火山 TTS）+ BGM + 字幕 |

### 七、研究与抓取

| Slug | 版本 | 一句话说明 |
|------|:----:|-----------|
| [`huo15-autoresearch-loop`](huo15-autoresearch-loop/) | v1.0.3 | Karpathy 自主研究循环：Modify → Verify → Keep / Discard → Repeat |
| [`huo15-research-pipeline`](huo15-research-pipeline/) | v1.0.3 | 从想法到论文的 6 阶段全自主研究管道（含 HITL，输出 Obsidian） |
| [`huo15-js-scraper`](huo15-js-scraper/) | v1.2.2 | JavaScript 渲染网站抓取（企微文档 / SPA / 企查查 / 反爬绕过） |
| [`huo15-searxng`](huo15-searxng/) | v1.2.2 | SearXNG 自托管元搜索引擎一键部署（Docker Compose + OpenClaw 配置自动化） |

---

## 重点更新

### `huo15-openclaw-office-doc` v7.6.1（2026-04）

企业 Word / PDF 文档生成现已支持 **39 类规范** 与 **22 份开箱即用 markdown 范本**：

- **HR**：个人简历 / 任命书 / 在职证明 / 劳动合同
- **Sales**：报价单 / 销售合同 / 招投标书
- **PM**：项目立项书 / 项目计划书 / 复盘报告 / 项目结项报告 / 会议纪要
- **Ops**：故障报告 (postmortem) / 应急预案 / 操作 SOP / 部署文档 / 风险评估报告
- **Tech**：技术方案 / 需求文档（PRD / SRS）/ 测试报告 / API 文档 / 用户手册 / 培训手册
- **Legal**：公司制度 / 备忘录 (MOU) / 信函 / 服务合同 / 技术开发合同 / 采购合同 / 保密协议 (NDA) / 合作协议
- **Reporting**：公文 / 工作报告 / 商业计划书 / 研究报告 / 验收单
- **Other**：演讲稿 / 新闻稿

每种规范按真实场景决定是否带 【内部】banner / 元数据表 / 版本历史 / 审批 /
TOC，CLI 可覆盖。三条输出路径（Word 直出 / 原生 PDF 直出 / Word→PDF），输入相同得到一致输出。

详见 [huo15-openclaw-office-doc/SKILL.md](huo15-openclaw-office-doc/SKILL.md) 与
[templates/README.md](huo15-openclaw-office-doc/templates/README.md)。

---

## 安装方式

### 方式一：从 ClawHub 安装（推荐）

```bash
# 单个安装
clawhub install <slug> --dir ~/.openclaw/workspace/skills

# 例：装文档技能 + 设计三件套
clawhub install huo15-openclaw-office-doc --dir ~/.openclaw/workspace/skills
clawhub install huo15-openclaw-frontend-design --dir ~/.openclaw/workspace/skills
clawhub install huo15-openclaw-design-director --dir ~/.openclaw/workspace/skills
clawhub install huo15-openclaw-design-critique --dir ~/.openclaw/workspace/skills
```

### 方式二：从源码安装

```bash
git clone git@github.com:zhaobod1/huo15-skills.git
cp -r huo15-skills/<技能目录>/ ~/.openclaw/workspace/skills/
# 重启 OpenClaw / Claude Code 即可生效
```

---

## 发布工作流（开发规范）

```
本地开发（cnb / GitHub 双源）→ git push → clawhub publish → clawhub install
```

**步骤**：

1. 在源仓库开发：`~/workspace/projects/openclaw/huo15-skills/<skill>/`
2. 本地测试通过后提交：
   ```bash
   git add <skill>/...
   git commit -m "feat(<skill>): vX.Y.Z 说明"
   git push origin main      # cnb.cool（主）
   git push github main      # GitHub（镜像）
   ```
3. 发布到 ClawHub：
   ```bash
   clawhub publish "$(pwd)/<skill>" \
     --slug <skill-slug> --version X.Y.Z --changelog "..."
   ```
4. ⚠️ **`_meta.json` 不会自动同步**：publish 成功后手动 Edit `_meta.json` 把
   `version` 字段同步到刚发的版本，单独 chore commit；否则下次升级时 _meta.json
   与线上脱节。

**铁律**：

- 所有技能从本仓库开发，禁止直接在 ClawHub 页面上传
- slug = 目录名，不可二次起名
- 版本号 semver；同一版本号不可重发
- 每小时新 slug 配额上限 5 个；批量首发用现有 slug 升版本不占额度
- ClawHub 嵌入 SKILL.md 上限 8192 tokens（≈ 25KB / ~5K CJK 字）；超限会报
  `Embedding failed`，砍历史 changelog / 重复示例即可

---

## ClawHub 直链

```
https://clawhub.ai/skills/huo15-openclaw-plan-mode
https://clawhub.ai/skills/huo15-openclaw-verify-mode
https://clawhub.ai/skills/huo15-openclaw-explore-mode
https://clawhub.ai/skills/huo15-openclaw-code-review
https://clawhub.ai/skills/huo15-openclaw-security-review
https://clawhub.ai/skills/huo15-openclaw-simplify
https://clawhub.ai/skills/huo15-openclaw-multi-agent
https://clawhub.ai/skills/huo15-openclaw-openai-knowledge-base
https://clawhub.ai/skills/huo15-openclaw-mit-48h-learning-method
https://clawhub.ai/skills/huo15-karpathy-guidelines
https://clawhub.ai/skills/huo15-openclaw-bootstrap
https://clawhub.ai/skills/huo15-openclaw-memory-curator
https://clawhub.ai/skills/huo15-openclaw-office-doc
https://clawhub.ai/skills/huo15-openclaw-ppt
https://clawhub.ai/skills/huo15-flow-chart
https://clawhub.ai/skills/huo15-mind-map
https://clawhub.ai/skills/huo15-openclaw-frontend-design
https://clawhub.ai/skills/huo15-openclaw-design-director
https://clawhub.ai/skills/huo15-openclaw-design-critique
https://clawhub.ai/skills/huo15-openclaw-brand-protocol
https://clawhub.ai/skills/huo15-img-prompt
https://clawhub.ai/skills/huo15-xiaohongshu
https://clawhub.ai/skills/huo15-influencer-video-skill
https://clawhub.ai/skills/huo15-autoresearch-loop
https://clawhub.ai/skills/huo15-research-pipeline
https://clawhub.ai/skills/huo15-js-scraper
https://clawhub.ai/skills/huo15-searxng
```

---

## License

全部 skill 默认 **MIT-0**（无需署名，可自由商用、修改、再发布）。

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>
