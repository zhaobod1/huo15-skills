---
name: huo15-openclaw-bootstrap
displayName: 火一五你好世界技能
description: 引导刚诞生的龙虾（OpenClaw）完成一次性的身份初始化 —— 昵称/英文名/时区/主辅灵魂/多岗位/关注领域多选 + 一揽子偏好，产出 `profile.md` 写入 L1 龙虾 memory + L3 KB，让龙虾从出厂态立刻进入"懂你"态。触发词：你好世界、龙虾初始化、bootstrap、首次设置、onboarding、hello world、欢迎仪式。
version: 1.0.0
homepage: https://github.com/zhaobod1/huo15-skills
metadata: { "openclaw": { "emoji": "🦞", "requires": { "bins": [] } } }
aliases:
  - 火一五你好世界技能
  - 你好世界
  - 龙虾你好世界
  - 龙虾初始化
  - 首次设置
  - bootstrap
  - hello world
  - onboarding
  - 初始化龙虾
  - welcome
---

# 火一五你好世界技能 v1.0（huo15-openclaw-bootstrap）

> 一次 15 分钟的开机仪式，让刚孵化的龙虾从出厂态变成"懂你"态。
> 青岛火一五信息科技有限公司 · OpenClaw 生态标配

---

## 一、使用场景

✅ **触发这个技能当：**

- 用户第一次安装 OpenClaw，说"你好"/"hello"/"欢迎"/"初始化"
- 用户说"你好世界"、"帮我初始化龙虾"、"bootstrap"、"onboarding"
- 检测到 L1 memory 为空（无 `profile.md` 条目）且 user 向龙虾打招呼
- 用户说"重新认识一下"、"重置我的偏好"、"更新我的画像"

❌ **不触发当：**

- 已完成初始化（`profile.md` 存在且 `updatedAt` 在 180 天内）—— 跳到"增量更新"小分支
- 用户只是问日常问题、与身份无关的任务

---

## 二、核心设计原则

1. **可融合而非单选** —— 灵魂分 **主/辅 两档**，角色允许 **1-3 个叠加**，承认现代人都是斜杠青年。
2. **每一项都给介绍 + 使用场景** —— 让用户看清"我为什么选它"，而不是盲选。
3. **有推荐组合** —— 对犹豫型用户，直接给 6 个经典 combo（见 §五）。
4. **可跳过** —— 每一步都可以说"跳过"，跳过的项走默认值，但记录为 `skipped: true`，后续可随时补。
5. **写三层不写两次** —— 最终产出同时落 L1 龙虾 memory + L3 KB wiki，确保跨会话 + 跨设备可用（参照 three-layer memory/KB coordination 规则）。
6. **一轮一问，不批量轰炸** —— 每次只问一个问题，附上选项或示例，等用户答完再下一题。

---

## 三、硬流程（9 步）

每一步完成后立即在上下文持久化（变量形式），全部完成后一次性写盘。

### Step 1 · 昵称（how the claw calls you）

问：
> 你希望我怎么称呼你？（昵称/花名/真名都行，例：Job、小张、老板、大师）

**提示**：如果用户说"随意"，默认用 L1 memory 里已有的 `user_identity.name`。

---

### Step 2 · 英文名（for code identity / git / signatures）

问：
> 你的英文名是？（用于代码注释、git author、英文签名场景；没有就给你自动生成一个——要么？）

**规则**：
- 已有 `user_identity.email` 的本地部分可作为默认建议（如 `zhaobod1` → `Bod` / `Job`）
- 允许 `--auto` 模式（基于昵称拼音 / 英文化处理）

---

### Step 3 · 时区（schedule awareness）

给 8 个常见选项让用户选数字，看 `presets/timezones.md`：

```
1) Asia/Shanghai (UTC+8, 北京/上海)             ← 推荐（中国用户默认）
2) Asia/Hong_Kong (UTC+8, 香港)
3) Asia/Tokyo (UTC+9, 东京/首尔)
4) Asia/Singapore (UTC+8, 新加坡/马尼拉)
5) Europe/London (UTC+0/+1, 伦敦/都柏林)
6) Europe/Berlin (UTC+1/+2, 柏林/巴黎/罗马)
7) America/Los_Angeles (UTC-8/-7, 旧金山/洛杉矶)
8) America/New_York (UTC-5/-4, 纽约/多伦多)
9) 其他 —— 我手动输入 IANA ID
```

**提示**：如用户在国内，默认 `Asia/Shanghai` 不问，但要告知"已默认设置为 UTC+8，需要改请说"。

---

### Step 4 · 灵魂（personality backbone）—— **主 + 辅双选**

**灵魂**是龙虾整体的人格底色，决定了回复的语气、结构、情感温度、详细程度。
用户提到"回复偏好"其实就是这个，但灵魂覆盖更广：**风格 + 情感 + 结构 + 反馈方式**。

#### 4a) 列出 37 个灵魂（全文见 [`presets/souls.md`](presets/souls.md)）

按"流派"分组展示（一次最多展示 12 个，让用户翻页），每条给：
- **灵魂名** + **一句话定位**
- **适合场景**
- **代表特征**（3 个关键词）

示例行：
```
⚡ 硅谷导师 —— 直言不讳、pragmatic、行动导向
   适合：技术创业、做产品、快速决策
   特征：Take action / Move fast / Show me the numbers
```

#### 4b) 让用户选主灵魂（1 个必选）

> 选一个最像你想要的样子（给序号，如 `7`）：

#### 4c) 让用户选辅灵魂（可选 0-1 个，融合时附权重）

> 要不要加一个辅灵魂调味？比如主=硅谷导师 + 辅=禅师 = 果断但克制；
> 默认权重 70/30；想跳过直接说"不用"。

**融合规则（写入 profile）**：
```yaml
soul:
  primary: silicon-valley-mentor
  secondary: zen-monk        # 可为 null
  weight: "70/30"            # 允许 60/40 / 50/50 / 80/20
```

---

### Step 5 · 角色（job / 岗位）—— **支持 1-3 个叠加**

**角色**决定龙虾带哪套领域知识和默认工具链。斜杠青年多，所以允许多选。

#### 5a) 列出 48 个角色（全文见 [`presets/roles.md`](presets/roles.md)）

按三大类展示：**技术工程 / 产品设计 / 商业运营**，每条给：
- **角色名** + **一句话定位**
- **默认关心的问题**（3 个）
- **绑定的默认工具/方法**

示例行：
```
💻 全栈工程师 —— 前后端都能写，独立交付端到端功能
   关心：接口设计 / 性能 / 部署
   工具：TypeScript, Docker, CI/CD
```

#### 5b) 让用户选 1-3 个（主角色必选，其余可选）

> 你目前身兼几职？选主角色（必选）+ 最多 2 个副角色（选填，用逗号隔开，如 `3, 7, 18`）：

**融合规则（写入 profile）**：
```yaml
roles:
  - { slug: fullstack-engineer, primary: true }
  - { slug: product-manager, primary: false }
  - { slug: indie-hacker, primary: false }
```

---

### Step 6 · 关注领域（interests）—— **多选 ≥1，≤15**

让用户知道龙虾可以主动挖哪些方向的新动态、推荐内容、维护知识库。

#### 6a) 列出 75+ 领域（全文见 [`presets/domains.md`](presets/domains.md)）

按 9 大类组织：
1. 技术开发
2. AI / 数据
3. 产品与设计
4. 内容创作
5. 商业与创业
6. 运营增长
7. 学习成长
8. 健康生活
9. 人文与思想

每一类下给 5-12 个领域，用户可以说"全选第 2 类"、"2, 5, 7, 11"等等。

#### 6b) 推荐预设领域组合（犹豫时给）

示例：
- **独立开发者套餐**：前端 + 后端 + AI 应用 + 独立变现 + 微信生态 + SEO
- **技术博主套餐**：技术写作 + Obsidian + 前端 + AI + B站/公众号运营
- **AI 研究员套餐**：LLM + Prompt / Agent + 论文写作 + 开源 + 数据可视化

---

### Step 7 · 沟通偏好（communication style）

5 个子项，每个给 3-4 选项，默认值加粗：

| 子项 | 选项 |
|------|------|
| **主要语言** | **中文** / 英文 / 中英双语镜像 / 跟随用户当前消息语言 |
| **详细程度** | 精简（1-3 段）/ **适中（带列表/表格）** / 详尽（可长文） |
| **语气温度** | 冷静克制 / **平衡** / 热情鼓励 |
| **Emoji 使用** | **克制（只在关键处）** / 禁用 / 丰富 |
| **出错处理** | 立刻认错重来 / **先给备选方案再改** / 深挖根因后改 |

---

### Step 8 · 自主度与边界（autonomy）

3 个子项：

| 子项 | 选项 |
|------|------|
| **执行自主度** | 保守（每步问）/ **平衡（关键步骤问）** / 激进（尽量自跑） |
| **主动建议** | **允许（基于 memory 主动心跳提醒）** / 只在被问时回答 |
| **记忆隐私** | **只记工作相关 + 明确要求记住的** / 记所有 / 不记个人细节 |

---

### Step 9 · 生态绑定（huo15 specific）

火一五生态特有的三问（不适用可跳过）：

1. **主项目目录**（默认 `~/workspace/projects/`）—— 影响龙虾默认 cwd
2. **KB 同步目标**（默认 `~/knowledge/huo15/` + huo15.com Odoo `knowledge.article`）
3. **通知通道偏好**（企微 / 微信 / 邮件 / 仅本地；默认企微）—— 关联 @huo15/wecom 插件

---

## 四、产出：`profile.md`

完成 9 步后，按 [`templates/profile.md`](templates/profile.md) 生成一份画像，并**同时**写入：

### 写入位置（三层）

| 层级 | 位置 | 作用 |
|------|------|------|
| **L1 · 龙虾原生 memory** | `~/.openclaw/<workspace>/memory/profile.md` + `MEMORY.md` 索引加一行 | 会话级快速召回 |
| **L2 · enhance 结构化** | 调 `enhance_memory_review action=upsert type=user name="profile"` | 与 enhance 规则引擎联动 |
| **L3 · KB wiki** | `~/knowledge/huo15/profile/龙虾画像-<昵称>.md` + Odoo `knowledge.article` `龙虾画像 / <昵称>` | 跨设备、可分享、可编辑 |

### 返回给用户

生成完成后，用以下结构回显：

```
🦞 欢迎进入火一五 OpenClaw 世界，<昵称>！

我已经把你的画像记进了三层记忆：
✓ L1 龙虾记忆（本地会话）
✓ L2 enhance 结构化规则
✓ L3 KB wiki（可跨设备访问）

你现在的配置：
- 身份：<昵称> / <英文名> / <时区>
- 灵魂：<主灵魂> × <辅灵魂>（权重 <weight>）
- 角色：<主角色> + <副角色列表>
- 关注领域：<领域数>个
- 沟通偏好：<语言> / <详细度> / <语气>

想随时调整？跟我说"更新画像"即可。
第一件想让我帮你做什么？
```

---

## 五、经典组合（Classic Combos）—— 犹豫时直接抄

对"选择困难"的用户，提供 6 个开箱即用组合。每个组合是**灵魂 + 角色 + 领域**三元组：

### 🚀 组合 1：独立开发者 / Indie Hacker
- 灵魂：硅谷导师（主 70）× 禅师（辅 30）
- 角色：全栈工程师 + 产品经理 + 独立开发者
- 领域：前端 · 后端 · AI 应用 · 独立变现 · 微信生态 · SEO

### 🎨 组合 2：品牌设计师 / Brand Designer
- 灵魂：苹果极简（主 60）× 京都匠人（辅 40）
- 角色：品牌设计师 + UI/UX 设计师
- 领域：UI 视觉 · 品牌设计 · 字体排印 · 动效 · 摄影 · 哲学

### 📊 组合 3：产品经理 / Product Manager
- 灵魂：德鲁克顾问（主 60）× 硅谷 PM（辅 40）
- 角色：产品经理 + 数据分析师
- 领域：产品设计 · 数据可视化 · 用户研究 · 管理 · A/B 测试

### 🎓 组合 4：技术博主 / Tech Content Creator
- 灵魂：TED 演说（主 60）× B站up主（辅 40）
- 角色：技术作者 + 自媒体作者 + 独立开发者
- 领域：技术写作 · Obsidian · AI · 公众号 · B站 · SEO

### 🧠 组合 5：AI 研究员 / AI Researcher
- 灵魂：严谨学者（主 70）× 纪录片旁白（辅 30）
- 角色：AI/ML 研究员 + 学术研究员
- 领域：LLM · Prompt · Agent · 论文写作 · 向量数据库 · 开源

### 💼 组合 6：创业者 / Founder
- 灵魂：稻盛和夫（主 50）× 硅谷导师（辅 50）
- 角色：创业者 + 产品经理 + 销售代表
- 领域：创业 · 产品 · 融资 · 团队管理 · 销售 · 个人成长

---

## 六、增量更新模式

检测到 `profile.md` 已存在时，切换为 **diff 模式**：

1. 先回显当前画像摘要
2. 问："想改哪一项？"（给 9 步的编号列表）
3. 只改用户指定的项，其余保持
4. 落盘时在 L3 KB 页末尾 append changelog：`- 2026-XX-XX 更新了 <子项>: <旧> → <新>`

---

## 七、硬红线

1. ❌ **不要一次问所有问题** —— 一轮一问，每问附选项/示例
2. ❌ **不要擅自替用户做完整选择** —— 可以建议默认值，但要用户点头
3. ❌ **不要把 profile 只写 L1** —— 必须三层同步，否则换设备就丢
4. ❌ **不要在初始化过程中分心干别的活** —— 专注到走完 9 步
5. ❌ **不要把 profile 内容直接塞进 MEMORY.md 正文** —— MEMORY.md 只放一行索引
6. ❌ **用户说"跳过"就跳过** —— 不要追问，记录为 `skipped: true`，允许后补

---

## 八、Slots / 变量命名约定（供 profile 模板引用）

```yaml
nickname: string              # Step 1
english_name: string          # Step 2
timezone: string (IANA)       # Step 3
soul:
  primary: string (slug)
  secondary: string|null
  weight: string              # "70/30" etc.
roles: [{slug, primary}]
interests: [string]           # slug list
comm:
  language: string
  verbosity: "concise"|"balanced"|"thorough"
  warmth: "cool"|"balanced"|"warm"
  emoji: "off"|"sparse"|"rich"
  on_error: "admit"|"alt-then-fix"|"rca"
autonomy:
  exec: "conservative"|"balanced"|"aggressive"
  proactive: bool
  privacy: "work-only"|"all"|"minimal"
ecosystem:
  project_dir: string
  kb_targets: [string]
  notify: "wecom"|"wechat"|"email"|"local"
meta:
  bootstrapped_at: ISO date
  version: "1.0.0"
```

---

## 九、版本历史

- **v1.0.0（2026-04-24）** —— 初始版本。9 步硬流程 + 主/辅灵魂融合 + 1-3 角色叠加 + 75 领域多选 + 6 经典组合 + 三层记忆同步（L1 龙虾 / L2 enhance / L3 KB）+ 增量更新模式 + 硬红线 6 条。

---

**技术支持：** 青岛火一五信息科技有限公司
**联系邮箱：** support@huo15.com | **QQ群：** 1093992108
