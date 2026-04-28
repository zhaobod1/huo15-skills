# 火一五小红书创作伙伴 — 版本历史

## v3.2.0（2026-04-28）— 工作流闭环 + SKILL.md 瘦身

> 触发：发现 SKILL.md 超 ClawHub embedding 8192 token 上限（135% 已用），
> 后半部分内容（v3.0/v3.1 章节）被截断，搜索可发现性受损。

**结构调整：**
- SKILL.md 瘦身到 ≤ 5K 字符，留触发词 + 命令速查 + 核心定位
- 详细教程 / 典型场景 / Python API / 数据资产 / 错误对照 → `README.md`
- 完整版本历史 → `docs/changelog.md`（本文件）

**新增三个能力（解决真实工作流痛点）：**

### 1. `coach_iterate.py` — 渐进式教练

来源：Allen 给贾维斯的最终评价 *"看出问题 ≠ 写得出来"*。

`critique.py` 一次给所有 6 维反馈 = 信息过载，用户不知道先改哪。
`coach-iterate` 一次只 focus **当前最差的那一维**，给 (what, why, how, example)
四件套；用户改完跑同一命令 → 自动对比该维分数变化 → 升了给下一维 / 没升继续追问。

记录在 `~/.xiaohongshu/profile/iter_sessions/<draft-id>/` 形成"改稿轨迹"。

### 2. `drafts.py` — 草稿版本管理

之前草稿散在 /tmp/、~/Desktop/，改稿无追踪。

```bash
drafts new --topic "下班后副业"            # 创建 ~/.xiaohongshu/drafts/<id>/
drafts add <id> /path/to/content.md       # 加版本（v01, v02, v03...）
drafts list                                # 列所有草稿
drafts show <id>                           # 看最新版
drafts diff <id>                           # 对比 v_n vs v_{n-1} 的 6 维分变化
drafts promote <id>                        # 标记终稿，转给 publish_helper
```

### 3. `today.py` — 今日选题推荐

解决"打开技能不知道写什么"的空白页焦虑。
综合：
- **当前节气**（自动从 `data/seasonal_themes.md` 命中）
- **栏目化**（如果有 series 沉淀，提醒"周三存档"该更新了）
- **公式轮换**（最近一直用 T2，建议试试 T3 / T11）
- **风格档案**（按你的 niche / persona 定制）

输出 1~3 条选题 + 推荐理由 + 可执行的 `assistant.py write ...` 命令。

---

## v3.1.0（2026-04-27）— Jarvis 陷阱 + 对标拆解 + Prompt Caching

来源：Allen 2026-04-27 夜「重启尽兴」对照课 + Anthropic API 进阶能力调研
+ 主流小红书工具市场调研。

**新增第 6 个 Allen 美学维度「范本范」(jarvis_trap)：**
检测大多数 AI / 工程师写文案的 5 维系统性偏差 —
开头挖痛点 / 引导建议动作 / 我在说话 / 运营口吻 / 教做型结尾。
最核心：'教读者怎么做' vs '展示什么样的人已经在做'。

**新增 [reverse_engineer.py](../scripts/reverse_engineer.py)** — 对标爆款 URL 反向拆解：
公式 / 骨架 / 钩子 / Allen 6 维 / 关键词 / "why it works" / "你赛道怎么用"。
可一键 `--add-baseline` 进风格档案。

**新增 [llm_helper.py](../scripts/llm_helper.py)** — Anthropic SDK 统一封装：
- prompt caching（Allen 数据 5min TTL，命中后 0.1x 成本）
- streaming（critique --watch 实时反馈）
- JSON 模式（critique --rewrite 一键攻略型→范本型）
- tool use 接口预留

**新增 [cover_brief.py](../scripts/cover_brief.py)** — 封面文案 + 版式建议
（3 套方案，按赛道配色）。

**critique.py** 新增 `--rewrite`（LLM 改写）+ `--watch`（流式分析）。

**practice.py** 新增 `rewrite-jarvis` — 用 Allen 5 维差距训练改写思路。

---

## v3.0.0（2026-04-27）— Allen 流升级（哲学家视角）

来源：司志远（Allen）2026-04-23~27 三课 + 五技法 + 11 案例教学。

v2.5 给的是工程师视角（钩子/排版/合规），v3.0 加上 Allen 美学叠加。

**新增 5 个 Allen 美学维度（[xhs_aesthetic.py](../scripts/xhs_aesthetic.py)）：**
- breath 留白度
- ai_speak 去 AI 腔
- teach_vs_lead 带读者
- resonance 共鸣度
- invitation 邀请语

**新增 4 个 CLI：**
- `critique.py` — Allen 风格诊断
- `coin_word.py` — 造词工具（谐音/概念迁移/形式包装）
- `series_design.py` — 栏目化 + 5 级互动阶梯 + 12 月节奏
- `reader_simulate.py` — 6 种读者画像走全文

**新增 3 份数据资产：**
- `data/allen_method.md` — 三课五技法 + 11 案例 + 认知转变表
- `data/ai_speak_patterns.json` — AI 腔黑名单 80+ 条
- `data/seasonal_themes.md` — 24 节气 + 节日"已存在画面"清单

**新增风格预设（profile_init.py preset）：**
- `allen` — 工程 50% + Allen 50%（品牌/情感共鸣赛道）
- `engineer` — 纯工程（干货/教程/工具）
- `balanced` — 工程 70% + Allen 30%（默认）

`coach.py` 整合 Allen 维度，对低于 7 分的维度自动产出 (what, why, how, example)。

---

## v2.5.x（2026-04-27）— 从"工具堆"升级为"创作助手"

**三个跃迁：**

### 1. 从无记忆 → 有档案

新增 `~/.xiaohongshu/profile/`（用户私有，跨 skill 可共用）：
- `style.json` — 自动从 baseline 学习语调/长度/emoji/口头禅
- `rules.json` — 用户教过的助手记住
- `feedback.jsonl` — 用户对每条建议的反馈
- `baseline/` — 1~5 篇代表作样本

### 2. 从单点工具 → 对话入口

新增 `assistant.py` — 一个入口把所有能力串起来：
status / next / init / write / coach / publish / review / learn / evolve。

### 3. 从静态规则 → 学习演进

`learn` 教规则、`evolve` 自动演进、`feedback.jsonl` 跟踪。

**新增 9 个文件：**
xhs_profile / xhs_coach / profile_init / coach / brainstorm / weekly_review /
assistant / practice / ab_test。

---

## v2.0.x（2026-04-27）— 全流程创作能力大改版

新增 7 个 CLI：选题 / 创作 / 打分 / 合规 / 发布辅助 / 跟踪。
新增 6 份数据资产：标题公式 / 正文骨架 / emoji / 话题 / 社区规则 / 敏感词。

---

## v1.0.x（2026-04-23）— 抓取 + 分析能力首版

Cookie 抓取 + 离线分析（互动 / 关键词 / 时段 / 爆款特征）。
强节流 + 风控检测（460 / 461 / 403 / captcha / redirect-to-login）。

---

## 设计哲学

1. **个人号 / 小团队**为目标用户，不是 MCN 批量号工厂
2. **规则可解释** — 标题公式、骨架、打分项明文写在 data/，Claude 和你都能读
3. **不依赖大模型** — 所有脚本零 API 成本可跑；让 Claude 调用产物
4. **半自动 ≠ 全自动** — 发布按钮永远在人手里，账号才安全
5. **闭环优于单点** — 调研 / 写 / 发 / 复盘任何一环少了，都做不长
6. **协同创作不是 AI 替写** — 助手让你看见 AI 腔 / 教读者腔 / 攻略型陷阱，
   然后你自己重写。从 48 → 80 分的差距是真实的写作能力提升空间。
