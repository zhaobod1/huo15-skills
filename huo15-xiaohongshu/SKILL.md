---
name: huo15-xiaohongshu
displayName: 火一五小红书创作伙伴
description: 有记忆、能学习、会教方法的小红书创作助手。两套打分叠加 — ①工程师流（标题/首段/排版/emoji/话题/合规）②Allen 流（留白/AI腔/带读者/共鸣/邀请语/范本范，含 Jarvis 陷阱 5 维），加风格档案、规则覆盖、写作教练（一次只 focus 一维的渐进式 / 全维诊断 / LLM 改写）、对话式选题、对标拆解、造词、栏目化、多读者模拟、封面 brief、草稿版本管理、今日推荐、周复盘、A/B 测试、写作训练。allen / engineer / balanced 三种预设一键切换。绝不自动化发布。触发词：小红书、xhs、写小红书、小红书文案、爆款文案、Allen 流、xiaohongshu。
version: 3.5.1
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

# 火一五小红书创作伙伴 v3.5

> 详细文档见 [README.md](README.md)，版本历史见 [docs/changelog.md](docs/changelog.md)。
>
> **v3.5 东东枪全书入库：** 《文案的基本修养》99章全本要点 + 32条金句 /
> 新增 `data/dongdongqiang_book.md` 完整索引。
>
> **v3.4 文案方法论升级：** 新增 蕉下三大句式（不是…而是… / 修辞比喻 / 每一…都是…）+ 东东枪《文案的基本修养》AB点/核心体验/洞察碰撞 框架 /
> 冬日系列5篇案例 / 贾维斯实战水位追踪（15→30分）/ 场景联想度训练提示。
>
> **v3.3 算法对齐：** 7 维打分（新加 CES 互动 + 标题前 13 字关键词位置）/
> #AI生成内容 必标检查（2026/01 起强制）/ 发布节奏硬限（每天 ≤ 2 篇 / 间隔 ≥ 2h） /
> 话题 5 槽分级（2 泛 + 2 垂 + 1 长尾）/ 3:4 HTML 封面生成（F12 截图）。

## 能做什么

| 阶段 | 命令 |
|---|---|
| **入门** | `assistant.py init --baseline ...` 建风格档案 |
| **状态** | `assistant.py status` / `next` / `today` |
| **调研** | `safety_check.py` → `scrape-{search,note,user}.py` → `analyze-notes.py` |
| **选题** | `topic_ideas.py` / `brainstorm.py` / `today.py` |
| **对标** | `reverse_engineer.py --url <爆款>`（拆出公式/骨架/Allen 6 维/why it works） |
| **创作** | `write_post.py draft` 出骨架 → `drafts.py` 版本管理 |
| **教练** | `coach_iterate.py` 一次 focus 一维 ｜ `coach.py` 全维 ｜ `critique.py` Allen 美学 ｜ `polish_post.py` 工程分 |
| **改写** | `critique.py --rewrite`（需 LLM）｜ `practice.py rewrite-jarvis` 训练改写思路 |
| **配套** | `coin_word.py` 造词 ｜ `series_design.py` 栏目化 ｜ `reader_simulate.py` 多读者 ｜ `cover_brief.py` 封面 |
| **合规** | `compliance_check.py`（绝对化词/医美/导流/诱导互动） |
| **发布** | `publish_helper.py`（剪贴板 + 10 项 checklist；**不自动化**） |
| **复盘** | `track_post.py snapshot` → `weekly_review.py` |
| **训练** | `practice.py prompt|rewrite|rewrite-jarvis` ｜ `ab_test.py` |
| **学习** | `assistant.py learn key=value` ｜ `evolve` ｜ `preset allen|engineer|balanced` |

## CES 算法心法（v3.3）

```
关注(8) > 转发(4) ≈ 评论(4) > 点赞(1) ≈ 收藏(1)
```

引导 1 次"软关注" = 引导 8 次点赞。互动设计优先级：
**软关注 → 评论邀请 → 收藏暗示 → 点赞**。

「想看类似的可以蹲一下」= 8 分；「你呢，留个故事给我」= 4 分；「点赞」= 1 分。

新发布笔记 → **100~500 流量池** → 2 小时内 CTR ≥ 8% + 互动率 ≥ 5% → 进下一级。

## 标题黄金法则

**前 13 字含核心关键词**（搜索权重 40%）+ 整体 16~22 字 + 含钩子词 + emoji ≤ 2 个。

`assistant.py learn main_keyword=干皮护肤` 后，score_title 自动检查关键词位置。

## 不做什么

❌ 自动发布 / 多账号矩阵 / AI 生图 / 一键全文 / 达人投放分析

## 防封号红线

1. 用自己的 Cookie，脚本不做登录自动化
2. 每次请求 3~7 秒延时，单会话 30 次封顶，会话间隔 10~30 分钟
3. 460 / 461 / 403 / captcha / 重定向登录 → **立即停 30 分钟**
4. 不翻页批量抓（搜索只取首页，主页只取 preview）
5. 日请求 ≤ 100 次

## 工作流（全部走 assistant.py）

```bash
# 第一次
python3 scripts/assistant.py init --persona "30+ 干皮女生" --niche "护肤" \
    --baseline note1.md note2.json
python3 scripts/assistant.py preset allen        # 切 Allen 美学加权

# 每天写一条
python3 scripts/assistant.py today               # 今日选题
python3 scripts/assistant.py drafts new --topic <主题>
python3 scripts/assistant.py write <主题>        # 起草
python3 scripts/assistant.py coach-iterate <id>  # 一次只改一维（推荐）
python3 scripts/assistant.py drafts diff <id>    # 对比 v_n vs v_{n-1}
python3 scripts/assistant.py publish <id>        # 剪贴板 + checklist

# 看到爆款想学
python3 scripts/assistant.py reverse --url <URL> --add-baseline

# 周末
python3 scripts/assistant.py review              # 周/月复盘
python3 scripts/assistant.py learn disable=emoji # 教助手新规则
python3 scripts/assistant.py evolve              # 自动演进
```

## Allen 文案心法

> 1. 「好文案不是写出来的，是留出来的。」— 留白
> 2. 「站文案里面读文案，不是站在外面分析。」— 第三课
> 3. 「卖的是身份认同，不是商品本身。」— 第二课
> 4. ❌ 教读者「怎么做」 vs ✅ 展示「什么样的人已经在做」 — Jarvis 陷阱核心
> 5. 「文案不是方法，是情绪出口。」— 2026-04-27 第五课总结
> 6. 「场景共鸣不是找冷知识，是找人人都有过的共同记忆。」— 终课批改
> 7. 「创意文案有时不具有指向性，更多是情绪的表达。」— 2026-04-28 点评

详见 `data/allen_method.md`（Allen 三课 + 五技法 + 16 案例 + 蕉下三大句式 + 东东枪基本修养 + Jarvis 陷阱 5 维差距）。

## 蕉下万能句式（v3.4 新增）

> 来源：Allen 2026-04-28 案例教学。蕉下（Beneunder）轻量化户外品牌，贩卖的是「能穿出门的情绪价值」。

### 底层逻辑：痛点 → 场景 → 方案 → 情绪共鸣

### 句式一：「不是……而是……」— 颠覆认知
先否定旧预设，再给出品牌新定义。否定句推开旧认知，肯定句拉高产品价值。
- 例：「不是害怕太阳，而是拥抱太阳」
- 例：「人不是去了户外，而是回到了户外」

### 句式二：修辞/比喻 — 参数变画面
让产品功能寄生在自然意象上，不说参数只给感受。
- 例：「风是最好的造型师」（抗风性能 → 风的造型服务）
- 例：「像仙人掌一样，给肌肤加一层防晒层」（防晒+保湿 → 一个意象完成）

### 句式三：「每一……都是……」— 功能升维
把日常小事拉高成品牌体验。
- 例：「每一口呼吸都是松弛的味道」
- 例：「让每一次去户外的决定，都变得笃定」

### 蕉下 vs 尽兴指南 风格对比

| 维度 | 蕉下 | 人生尽兴指南 |
|------|------|------------|
| 角色 | 痛点爆破者 | 情绪出口提供者 |
| 句式 | 对比/修辞/每一是 | 场景/留白/栏目化 |
| 卖什么 | 敢晒太阳的野心 | 暂停一下活成自己的许可证 |
| 姿态 | 「怕X，就穿蕉下」直接给方案 | 「你的尽兴式是什么模样」让读者走到答案前 |

## 东东枪《文案的基本修养》参考（v3.4 新增）

> 中信出版社 2019，东东枪著。99篇小文讲透广告创意与文案之道。

### 核心概念速查

- **广告的定义：** 创作并传播内容，改变他人的看法或感受，以促成行为改变
- **AB点理论：** A=消费者现在看法/感受 → B=你希望他们变成的看法/感受。广告只能改变看法感受，不能直接改变行为
- **核心体验（Key Experience）：** 品牌真正在售卖、被消费者真正买走的东西。电钻卖的不是洞，是身份感/安全感/炫耀感
- **洞察（Insight）：** 未被发现或已被遗忘的真相。存在于认知与真相、表达与认知两个缝隙里。只能发现不能发明
- **品牌 = 固化的偏好：** 三类结果 — 默认信赖 / 优先选择 / 相对溢价
- **品牌传播 vs 产品传播：** 前者「为你唱首歌」，后者「给你房本车证」
- **心象 > 形象：** 用认知状态定义目标人群，不用人口统计学
- **Idea金字塔：** 策略Idea → 创意Idea → 执行Idea
- **创意碰撞法：** 核心体验 × 洞察 = 创意Idea

### 对小红书文案的启示
- 每篇笔记想清楚 AB 点：读者现在怎么想 → 看完后怎么想
- 不要卖内容本身，卖「核心体验」
- 好的洞察 = 读者看完说「真相了」
- 品牌号 ≠ 每篇都在卖产品，有时只需「唱首歌」让人更喜欢你

## 场景联想度（v3.4 新增）

> AI 写文案核心短板：场景库太窄，反复用同一批词（西瓜/蝉/冰棍/窗帘/傍晚的风）。

**自检规则：** 全文中出现重复意象（如连续两篇都用「窗帘鼓成帆」）→ 提示换词。
**缓解办法：** 每次写之前，先列出 10 个不常用的季节/场景关联词，选其中 3 个入文。
**长期方案：** 持续喂书/案例，扩容场景库。

## 风格预设

| 预设 | 工程权重 | Allen 权重 | 适合 |
|---|---|---|---|
| `allen` | 50% | 50% | 品牌号、情感号、生活号 |
| `engineer` | 100% | 0% | 干货号、教程、工具测评 |
| `balanced` | 70% | 30% | 综合个人号（默认） |

```bash
python3 scripts/assistant.py preset allen
```

## 数据资产

`data/` 目录包含 9 份对人和 Claude 都可读的资产：标题公式 11 种、正文骨架 7 种、
emoji 调色板、话题标签库、社区规则、敏感词、Allen 方法论、AI 腔黑名单、节气画面库。

## 个人档案位置

```
~/.xiaohongshu/
├── posts.jsonl / snapshots.jsonl  # 起草历史 + 互动快照
├── drafts/<id>/v01.md, v02.md, ... # 草稿版本（v3.2）
└── profile/
    ├── style.json / rules.json    # 风格 + 规则覆盖
    ├── baseline/ feedback.jsonl   # 代表作 + 反馈
    ├── iter_sessions/             # 渐进式教练历程（v3.2）
    └── reviews/                   # 周/月复盘归档
```

## 触发词

小红书 / xhs / xiaohongshu / 写小红书 / 小红书文案 / 爆款文案 /
小红书选题 / 小红书发布 / 小红书复盘 / 小红书教练 / Allen 流 / 范本范

---

**重要免责：** 仅用于合规、针对公开可见内容的个人调研与创作辅助。
请尊重 xiaohongshu.com 的服务条款。**绝不**支持商业批量采集 / 内容搬运 / 绕过风控 / 自动化互动。

**技术支持：** 青岛火一五信息科技有限公司
