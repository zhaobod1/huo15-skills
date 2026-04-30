---
name: huo15-xiaohongshu
displayName: 火一五小红书创作伙伴
description: 有记忆、能学习、会教方法的小红书创作助手。以「五层创作哲学」为核心（Allen 心法 + 东东枪修养 + 算法实践），两套打分叠加 — ①工程师流（标题/首段/排版/emoji/话题/合规/CES）②Allen 流（留白/AI腔/带读者/共鸣/邀请语/范本范，含 Jarvis 陷阱 5 维），加风格档案、规则覆盖、写作教练（一次一维渐进式/全维/LLM改写）、动笔前哲学速查、对话式选题、对标拆解、造词、栏目化、多读者模拟、封面 brief、草稿版本管理、9案例苏格拉底式学习、今日推荐、周复盘、A/B 测试、写作训练。allen / engineer / balanced 三种预设一键切换。绝不自动化发布。触发词：小红书、xhs、写小红书、小红书文案、爆款文案、Allen 流、xiaohongshu。
version: 3.7.0
aliases:
  - 火一五小红书技能
  - 火一五小红书创作伙伴
  - 小红书全流程
  - 小红书助手
  - 小红书写作
  - 小红书文案
  - 小红书选题
  - 小红书发布
  - 小红书运营
  - 小红书复盘
  - 小红书教练
  - Allen 流
  - 写小红书
  - xhs
  - xiaohongshu
dependencies:
  python-packages:
    - requests
    - jieba       # 可选
    - pandas      # 可选
    - anthropic   # 可选 — LLM 增强
---

# 火一五小红书创作伙伴 v3.7

> 详细文档见 [README.md](README.md)，版本历史见 [docs/changelog.md](docs/changelog.md)。
>
> **v3.7 创作哲学入库：** 五层创作决策框架（原点→支点→手艺→陷阱→系统），
> 综合 Allen 三课五技法 + 东东枪 99 篇 + 算法实践，封装为 `data/creative_philosophy.md`。
> 案例库从 4 个扩到 9 个。AI 腔黑名单新增 Jarvis 攻略句式类别。新增 `philosophy.py` CLI。
>
> **v3.6 旺旺教学：** 先做功课红线 + 60分文案五法 + 态度vs成分框架。
>
> **v3.5 东东枪全书：** 99章全本要点 + 32条金句入库。

## 创作哲学（写前 30 秒速查）

> 详见 [data/creative_philosophy.md](data/creative_philosophy.md)。这是本技能的**灵魂**。

**四句心法：**
1. 「好文案不是写出来的，是留出来的。」— 留白
2. 「卖的是身份认同，不是商品本身。」— Allen 第二课
3. 「站文案里面读文案，不是站在外面分析。」— Allen 第三课
4. 「一流的糖衣，本身就是炮弹。」— 东东枪

**8 问决策清单：**

动笔前：□ 心象（为谁写） □ AB点（改什么） □ 核心体验（卖什么感觉） □ 功课（查了没）
动笔中：□ 留白（给空间还是给答案） □ 五法（有没有配料/参数/功能）
写完后：□ Jarvis 陷阱（教怎么做 vs 展示什么样的人） □ AI 腔（删干净没）

```bash
python3 scripts/philosophy.py              # 速查 8 问 + 心法
python3 scripts/philosophy.py --checklist  # 纯文本清单，可粘贴到草稿顶部
python3 scripts/philosophy.py --mantra     # 只看四句心法
python3 scripts/philosophy.py --layer 1    # 深入某一层（1~5）
```

## 能做什么

| 阶段 | 命令 |
|---|---|
| **哲学** | `philosophy.py` 速查 / `--checklist` 粘贴 / `--layer 1~5` 深入 |
| **入门** | `assistant.py init --baseline ...` 建风格档案 |
| **状态** | `assistant.py status` / `next` / `today` |
| **调研** | `safety_check.py` → `scrape-{search,note,user}.py` → `analyze-notes.py` |
| **选题** | `topic_ideas.py` / `brainstorm.py` / `today.py` |
| **对标** | `reverse_engineer.py --url <爆款>`（拆出公式/骨架/Allen 6 维/why it works） |
| **案例** | `case_study.py list|study|show|related`（9 案例苏格拉底式学习） |
| **创作** | `write_post.py draft` 出骨架 → `drafts.py` 版本管理 |
| **教练** | `coach_iterate.py` 一次一维 ｜ `coach.py` 全维 ｜ `critique.py` Allen 美学 ｜ `polish_post.py` 工程分 |
| **改写** | `critique.py --rewrite`（需 LLM）｜ `practice.py rewrite-jarvis` 训练改写思路 |
| **配套** | `coin_word.py` 造词 ｜ `series_design.py` 栏目化 ｜ `reader_simulate.py` 多读者 ｜ `cover_brief.py` 封面 |
| **框架** | `frameworks.py jiaoxia|ab|key|spark` 蕉下句式/AB点/核心体验/创意碰撞 |
| **合规** | `compliance_check.py`（绝对化词/医美/导流/诱导互动/AI标签） |
| **发布** | `publish_helper.py`（剪贴板 + 10 项 checklist；**不自动化**） |
| **复盘** | `track_post.py snapshot` → `weekly_review.py` |
| **训练** | `practice.py prompt|rewrite|rewrite-jarvis` ｜ `ab_test.py` |
| **学习** | `assistant.py learn key=value` ｜ `evolve` ｜ `preset allen|engineer|balanced` |

## CES 算法心法

```
关注(8) > 转发(4) ≈ 评论(4) > 点赞(1) ≈ 收藏(1)
```

互动设计优先级：**软关注 → 评论邀请 → 收藏暗示 → 点赞**。
「想看类似的可以蹲一下」= 8 分；「你呢」= 4 分；「点赞」= 1 分。
新笔记 → 100~500 流量池 → 2h 内 CTR≥8% + 互动率≥5% → 进下一级。

## 标题黄金法则

**前 13 字含核心关键词**（搜索权重 40%）+ 整体 16~22 字 + 含钩子词 + emoji ≤ 2 个。

## Allen 文案心法

> 1. 「好文案不是写出来的，是留出来的。」
> 2. 「站文案里面读文案，不是站在外面分析。」
> 3. 「卖的是身份认同，不是商品本身。」
> 4. ❌ 教读者「怎么做」 vs ✅ 展示「什么样的人已经在做」— Jarvis 陷阱
> 5. 「文案不是方法，是情绪出口。」
> 6. 「场景共鸣不是找冷知识，是找人人都有过的共同记忆。」
> 7. 「创意文案有时不具有指向性，更多是情绪的表达。」
> 8. 「先去做功课——深度了解品牌官方定位之后再开始创意。」

详见 `data/allen_method.md`（三课 + 五技法 + 17 案例 + 蕉下句式 + 东东枪对齐 + Jarvis 陷阱 5 维）。

## 先做功课（Allen 红线）

写任何产品/品牌前：① 搜官方宣传语 ② 理解品牌怎么定义自己 ③ 提取 3-5 个核心意象 ④ 判断态度还是成分 ⑤ 再创意。❌ 跳过 = 从零发明产品 = 0 分。

## Allen 60分文案五法

| # | 手法 | ❌ | ✅ |
|---|------|-----|-----|
| 1 | 用感受代配料 | 写配料表/成分 | 写吃下去的感觉 |
| 2 | 用场景代功能 | 说产品能干嘛 | 展示什么场景下吃/用 |
| 3 | 用情绪代产品 | 以产品为主角 | 以读者情绪为主角 |
| 4 | 用过程代成分 | 列成分/参数 | 写从源头到成品的旅程 |
| 5 | 用比喻代描述 | 直接描述产品 | 用自然意象包裹产品 |

## 蕉下万能句式

- **「不是……而是……」** — 先否定旧预设，再给品牌新定义
- **修辞/比喻** — 参数变画面（「风是最好的造型师」）
- **「每一……都是……」** — 功能升维（「每一口呼吸都是松弛的味道」）

## 风格预设

| 预设 | 工程权重 | Allen 权重 | 适合 |
|---|---|---|---|
| `allen` | 50% | 50% | 品牌号、情感号、生活号 |
| `engineer` | 100% | 0% | 干货号、教程、工具测评 |
| `balanced` | 70% | 30% | 综合个人号（默认） |

```bash
python3 scripts/assistant.py preset allen
```

## 工作流（全部走 assistant.py）

```bash
# 第一次
python3 scripts/assistant.py init --persona "30+ 干皮女生" --niche "护肤" \
    --baseline note1.md note2.json
python3 scripts/assistant.py preset allen

# 动笔前 30 秒：过创作哲学
python3 scripts/philosophy.py

# 每天写一条
python3 scripts/assistant.py today
python3 scripts/assistant.py drafts new --topic <主题>
python3 scripts/assistant.py write <主题>
python3 scripts/assistant.py coach-iterate <id>
python3 scripts/assistant.py publish <id>

# 看到爆款想学
python3 scripts/assistant.py reverse --url <URL> --add-baseline

# 周末
python3 scripts/assistant.py review
python3 scripts/assistant.py learn disable=emoji
python3 scripts/assistant.py evolve
```

## 数据资产

`data/` 目录包含 11 份对人和 Claude 都可读的资产：

| 文件 | 内容 |
|------|------|
| `creative_philosophy.md` | **五层创作哲学**（v3.7 新增） |
| `allen_method.md` | Allen 三课五技法 + 17 案例 |
| `dongdongqiang_book.md` | 东东枪 99 篇要点 + 32 金句 |
| `algorithm_guide.md` | 小红书算法指南 2025-2026 |
| `copywriting_frameworks.md` | 蕉下句式 + 东东枪框架 |
| `scene_library.md` | ~200 场景画面库 |
| `case_library/` | 9 真实案例（v3.7 扩至 9） |
| `ai_speak_patterns.json` | AI 腔黑名单（含 Jarvis 攻略句式） |
| `seasonal_themes.md` | 24 节气借势画面库 |
| `title_templates.md` | 标题公式 11 种 |
| `content_structures.md` | 正文骨架 7 种 |

## 个人档案位置

```
~/.xiaohongshu/
├── posts.jsonl / snapshots.jsonl
├── drafts/<id>/v01.md, v02.md, ...
└── profile/
    ├── style.json / rules.json
    ├── baseline/ feedback.jsonl
    ├── iter_sessions/
    └── reviews/
```

## 不做什么

❌ 自动发布 / 多账号矩阵 / AI 生图 / 一键全文 / 达人投放分析

## 防封号红线

1. 用自己的 Cookie，脚本不做登录自动化
2. 每次请求 3~7 秒延时，单会话 30 次封顶
3. 460/461/403/captcha/重定向登录 → **立即停 30 分钟**
4. 不翻页批量抓
5. 日请求 ≤ 100 次

---

**重要免责：** 仅用于合规、针对公开可见内容的个人调研与创作辅助。
请尊重 xiaohongshu.com 的服务条款。**绝不**支持商业批量采集 / 内容搬运 / 绕过风控 / 自动化互动。

**技术支持：** 青岛火一五信息科技有限公司
