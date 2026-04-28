---
name: huo15-xiaohongshu
displayName: 火一五小红书创作伙伴
description: 有记忆、能学习、会教方法的小红书创作助手。两套打分叠加 — ①工程师流（标题/首段/排版/emoji/话题/合规）②Allen 流（留白/AI腔/带读者/共鸣/邀请语/范本范，含 Jarvis 陷阱 5 维），加风格档案、规则覆盖、写作教练（一次只 focus 一维的渐进式 / 全维诊断 / LLM 改写）、对话式选题、对标拆解、造词、栏目化、多读者模拟、封面 brief、草稿版本管理、今日推荐、周复盘、A/B 测试、写作训练。allen / engineer / balanced 三种预设一键切换。绝不自动化发布。触发词：小红书、xhs、写小红书、小红书文案、爆款文案、Allen 流、xiaohongshu。
version: 3.2.0
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

# 火一五小红书创作伙伴 v3.2

> 详细文档见 [README.md](README.md)，版本历史见 [docs/changelog.md](docs/changelog.md)。

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

详见 `data/allen_method.md`（Allen 三课 + 五技法 + 11 案例 + 关键认知转变 + Jarvis 陷阱 5 维差距）。

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
