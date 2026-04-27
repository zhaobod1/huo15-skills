---
name: huo15-xiaohongshu
displayName: 火一五小红书创作伙伴（含 Allen 流）
description: 一个有记忆、能学习、会教方法的小红书创作助手。两套打分体系叠加：①工程师流（标题/首段/排版/emoji/话题/合规）②Allen 流（留白度/AI腔/带读者/共鸣度/邀请语 — 来自司志远 Allen 三课五技法）。配以个人风格档案、规则覆盖、写作教练、对话式选题、造词工具、栏目化设计、多读者模拟、周复盘、A/B 测试、写作训练。可一键切换 Allen / engineer / balanced 三种风格预设。绝不自动化发布。触发词：小红书、xhs、写小红书、小红书文案、爆款文案、小红书助手、Allen 流、xiaohongshu。
version: 3.0.0
aliases:
  - 火一五小红书技能
  - 火一五小红书创作伙伴
  - 火一五小红书全流程创作技能
  - 小红书全流程
  - 小红书助手
  - 小红书写作
  - 小红书文案
  - 小红书选题
  - 小红书发布
  - 小红书运营
  - 小红书复盘
  - 小红书教练
  - 写小红书
  - 写xhs
  - xhs
  - xiaohongshu
  - 小红书分析
  - 小红书抓取
dependencies:
  python-packages:
    - requests
    - jieba       # 可选
    - pandas      # 可选
    - anthropic   # 可选 — 教练 LLM 增强
---

# 火一五小红书创作伙伴 v3.0（Allen 流升级）

> **从"工具集"到"创作助手"** — 助手记得你是谁、写过什么、什么风格、
> 哪些规则你不在意。所有打分 / 建议 / 选题都按你自己的画像调。
> 青岛火一五信息科技有限公司

---

## 一、定位与边界（先读）

**这个技能能做什么：**

1. **创作伙伴** — 一个有记忆、能学习的助手，按你自己的画像调每一条建议。
2. **调研** — 抓同行爆款笔记 + 离线分析，找选题方向。
3. **选题** — 基于种子词 / 抓取数据 / 多轮对话，生成选题清单。
4. **创作** — 11 种标题公式 + 7 种正文骨架 + 你自己常用的口头禅，给"骨架草稿"。
5. **优化** — 6 维打分（按你画像加权）+ 教练诊断（为什么 + 怎么改 + 例子）。
6. **合规** — 扫绝对化词、医疗承诺、站外导流、诱导互动、用户自定义敏感词。
7. **发布辅助** — 剪贴板打包 + 发布前 10 项检查表 + 本地日志。
8. **复盘** — 发布后 7 天互动快照 + 周/月复盘报告 + 长线成长建议。
9. **训练** — 命题练习、改写训练、A/B 测试 — 把"写"当成可练习的肌肉。

**这个技能不做什么（重要）：**

- ❌ **不替你按"发布"按钮** — 自动化发布会立刻被风控识别，账号轻则限流重则封禁。
- ❌ 不做点赞 / 关注 / 评论 / 私信自动化（同上）。
- ❌ 不批量翻页采集（搜索只取首页，主页只取 preview）。
- ❌ 不强制调用大模型 — 所有打分 / 诊断 / 选题离线规则可跑；
  教练**可选**用 LLM 增强（设置 `XHS_LLM_PROVIDER=anthropic`）。

**核心原则：** 个人号最贵的资产是"信任画像"，比省 30 秒发布时间值钱多了。

---

## 一·五、v2.5 创作助手（核心新增）

> v2.0 给的是"工具堆"，v2.5 给的是"助手"。
> 区别在于 — 助手**记得你是谁、写过什么、什么风格、哪些规则你不在意**。

### 一站式入口：`assistant.py`

```bash
python3 scripts/assistant.py            # 看状态 + 推荐下一步
python3 scripts/assistant.py next       # 直接执行最优推荐
python3 scripts/assistant.py init ...   # 第一次建风格档案
python3 scripts/assistant.py brainstorm # 5 轮对话收敛选题
python3 scripts/assistant.py write 干皮护肤  # 在风格约束下起草
python3 scripts/assistant.py coach draft.md  # 教练诊断
python3 scripts/assistant.py polish draft.md # 打分模式
python3 scripts/assistant.py publish draft.md# 发布前流程
python3 scripts/assistant.py review     # 周/月复盘
python3 scripts/assistant.py learn disable=emoji add-sensitive=卷王  # 教助手新规则
python3 scripts/assistant.py evolve     # 基于历史 feedback 自动演进规则
```

### 三个核心模块

#### 1. 风格档案（StyleProfile）— 让产出"像你写的"

从 1~5 篇 baseline 自动学习：标题长度、正文段落、emoji 密度、口头禅、
偏好的公式 / 骨架、高频话题。后续所有生成都套用这个画像。

```bash
# 用代表作建立档案
python3 scripts/assistant.py init \
    --persona "30+ 干皮女生" --voice casual --niche "护肤" \
    --baseline note1.json note2.md note3.json

# 查看
python3 scripts/profile_init.py show

# 追加（每周把最爆的 1 篇加进来）
python3 scripts/profile_init.py add latest_hit.json
```

存档：`~/.xiaohongshu/profile/`（个人私有，跨 skill 可共用，不入 git）。

#### 2. 规则覆盖（RuleOverride）— 助手会"学"

用户教过的助手记住，下次自动应用。

```bash
# 教："我以后不要 emoji 检查"
python3 scripts/assistant.py learn disable=emoji

# 教："给我加这些自定义敏感词"
python3 scripts/assistant.py learn add-sensitive=卷王 add-sensitive=躺平

# 教："医生我能用'治愈'"
python3 scripts/assistant.py learn allow=治愈

# 演进 — 基于 coach 反馈自动调整
python3 scripts/assistant.py evolve
```

最终规则 = `data/默认 ⊕ profile/rules.json`。

#### 3. 写作教练（Coach）— 不只打分，给"为什么 + 怎么改 + 例子"

```bash
python3 scripts/coach.py --in draft.md
```

每条诊断包含：
- **what** — 哪里有问题（一句话）
- **why** — 为什么有问题（原理 / 数据）
- **how** — 怎么改（具体操作）
- **example** — 改后的样子

附带"风格偏离提醒"（你自己 baseline 长 18 字，这条 28 字了）+
"长线成长建议"（最近 5 篇平均分比早期 10 篇低 5 分，注意是否飘了）。

可选 LLM 增强：设置 `XHS_LLM_PROVIDER=anthropic` + 安装 `anthropic` SDK，
教练会调一次模型把 how/example 写得更具体。

### 闭环数据资产

```
~/.xiaohongshu/
├── posts.jsonl              # 起草历史 (publish_helper 写)
├── snapshots.jsonl          # 互动快照 (track_post 写)
└── profile/
    ├── style.json           # 风格档案
    ├── rules.json           # 规则覆盖
    ├── feedback.jsonl       # 用户对建议的反馈
    ├── practice.jsonl       # 命题/改写练习
    ├── ab_tests.jsonl       # A/B 测试
    ├── baseline/            # 1~5 篇代表作
    └── reviews/             # 周/月复盘报告归档
```

---

## 一·六、v3.0 Allen 流升级（哲学家视角）

> v2.5 的"工程师视角"打分（公式 / 钩子 / 排版 / 合规）+
> v3.0 新增的**「Allen 流」**（留白 / AI腔 / 教带 / 共鸣 / 邀请语）。
> 来源：司志远 Allen 的小红书文案教学（三课 + 五技法 + 11 案例）。

### Allen 5 个新维度

| 维度 | 这是在看 | Allen 课 |
|---|---|---|
| **留白度** breath | 句子是否给读者填情绪的空间 | 第一课：呼吸感 |
| **去 AI 腔** ai_speak | "汇报化 / 模板化 / 装腔"词检测 | 实战教训：避汇报化 |
| **带读者** teach_vs_lead | "你应该" 还是 "你可以试试" | 第一课：教 → 带 |
| **共鸣度** resonance | 共同记忆 vs 冷知识 / 装文化 | 实战教训：共鸣 vs 冷信息 |
| **邀请语** invitation | 互动是任务指令还是 "这里有个局" | 第三课：站文案里 |

### 三个风格预设（一键切换）

```bash
python3 scripts/profile_init.py preset --list

#   allen      — Allen 流（品牌 / 情感共鸣赛道）
#   engineer   — 工程师流（干货 / 教程 / 工具）
#   balanced   — 平衡流（默认）

python3 scripts/assistant.py preset allen
```

| 预设 | 工程权重 | Allen 权重 | 适合 |
|---|---|---|---|
| `allen` | 50% | 50% | 品牌号、情感号、生活号 |
| `engineer` | 100% | 0% | 干货号、教程、工具测评 |
| `balanced` | 70% | 30% | 综合个人号（默认） |

### 三个新 CLI

#### 1. `critique.py` — Allen 风格诊断

```bash
python3 scripts/critique.py --in draft.md
python3 scripts/critique.py --in draft.md --merged       # 工程 + Allen 综合分
python3 scripts/critique.py --in draft.md --disable breath ai_speak  # 关掉某维度
```

#### 2. `coin_word.py` — 造词工具（Allen 待修炼之一）

```bash
python3 scripts/coin_word.py --brand "尽兴" --value "活得舒服" --n 8
```

输出三种模式：谐音造词 / 概念迁移（生物/建筑/物理/音乐/电影/厨房）/ 形式包装。
设置 `XHS_LLM_PROVIDER=anthropic` 后会调一次模型补优质候选。

#### 3. `series_design.py` — 栏目化 + 互动阶梯

```bash
python3 scripts/series_design.py --theme "尽兴" --persona "30+ 都市女性"
```

输出：
- 5 类栏目名候选（时间型 / 动作型 / 形式型 / 活动型 / 情绪型）
- 5 级互动阶梯（关注 → 评论 → 发图 → 被收录 → 带走大礼）
- 12 个月 IP 节奏建议（启动 / 召集 / 收录 / 实物 / 借势 / 联动 / 沉淀 / 跨界）

#### 4. `reader_simulate.py` — 多读者画像走全文（Allen 第三课落地）

```bash
python3 scripts/reader_simulate.py --in draft.md
```

模拟 6 种典型读者画像（30+ 干皮 / 互联网打工人 / 新手妈妈 / 大学生 / i 人独居 / 二线自由职业）
读完后【开头 / 中段 / 结尾】的情绪曲线 + 是否会做后续动作（stay/like/save/comment/follow）。

### 三份新数据资产

| 文件 | 内容 |
|---|---|
| [data/allen_method.md](data/allen_method.md) | Allen 三课 + 五技法 + 11 案例 + 关键认知转变表 |
| [data/ai_speak_patterns.json](data/ai_speak_patterns.json) | AI 腔黑名单 ~80 条（汇报化/模板化/懂行装腔/夸大煽情/教读者腔/AI 高频开头） |
| [data/seasonal_themes.md](data/seasonal_themes.md) | 24 节气 + 现代节日 + 小红书伪节日的"已存在画面"清单 |

### Allen 哲学心法（速查）

> 1. 「好文案不是写出来的，是留出来的。」— 留白
>
> 2. 「站文案里面读文案，不是站在外面分析。」— 第三课
>
> 3. 「卖的是身份认同，不是商品本身。」— 第二课
>
> 4. 「文案 = 为读者铺设一条通往情绪的路径，然后让路本身消失。」

### coach.py 也升级了

`coach.py` 新增 Allen 美学诊断维度（include_allen=True 默认开），
对每个低于 7 分的 Allen 维度自动产出 (what, why, how, example) 四件套。
不开 `XHS_LLM_PROVIDER` 也完全可用。

### 工程 vs Allen — 不替代是叠加

```
最终分 = 工程分 × (1 - allen_weight) + Allen 分 × allen_weight

allen_weight 由 preset 决定：
  - engineer:  0.0   (纯工程)
  - balanced:  0.3   (默认)
  - allen:     0.5   (一半 Allen)
```

干货账号请用 engineer；品牌 / 情感共鸣账号用 allen。

---

## 二、整体工作流（推荐顺序）

```
                    ╔══════════════════════════════════════╗
                    ║   assistant.py — 一站式入口          ║
                    ║   status / next / init / write /     ║
                    ║   coach / publish / review / learn   ║
                    ╚════════════════╤═════════════════════╝
                                     ↓
   ┌─────────────────────────────────────────────────────────────────┐
   │  0. 建档案  ─→ profile_init.py（1~5 篇 baseline，自动学习风格）  │
   │                              ↓                                   │
   │  1. 调研   ─→  scrape-{search,note,user}.py（Cookie + 强节流）    │
   │                              ↓                                   │
   │  2. 分析   ─→  analyze-notes.py                                   │
   │                              ↓                                   │
   │  3. 选题   ─→  brainstorm.py（对话式）/ topic_ideas.py（一次性）  │
   │                              ↓                                   │
   │  4. 创作   ─→  write_post.py（标题 + 骨架占位，套你的 profile）   │
   │                              ↓ Claude / 你填具体内容              │
   │  5a. 教练  ─→  coach.py（为什么 + 怎么改 + 例子 + 风格偏离）      │
   │  5b. 打分  ─→  polish_post.py（6 维打分，按 profile 调权重）      │
   │                              ↓                                   │
   │  6. 合规   ─→  compliance_check.py                                │
   │                              ↓                                   │
   │  7. 发布   ─→  publish_helper.py（剪贴板 + 10 项检查表）          │
   │              ↓ 你打开 App，粘贴并按发布                          │
   │  8. 跟踪   ─→  track_post.py（24h/3d/7d 互动快照）                │
   │                              ↓                                   │
   │  9. 复盘   ─→  weekly_review.py（周/月报告 + 下周建议）           │
   │                              ↓                                   │
   │  10. 训练  ─→  practice.py（命题 / 改写）/ ab_test.py（A/B 对比） │
   │                              ↓                                   │
   │  ↻  助手学习 ─→ assistant.py learn / evolve（规则演进）           │
   └─────────────────────────────────────────────────────────────────┘
```

每一步都是独立 CLI，**也可以一律走 `assistant.py`** 让它根据上下文路由。

---

## 三、防封号原则（依然适用）

> 小红书风控很严。违反任何一条都可能导致账号被限流、封禁或要求验证。

1. **用自己的 Cookie**。脚本不做登录自动化 — 输密码 / 刷验证码会被立刻识别。
   浏览器登录后从 DevTools → Application → Cookies 复制完整字符串。
2. **不共享 Cookie**。多账号别在同一台设备混用。
3. **节奏第一**。每次请求随机 3~7 秒延时，单会话 30 次封顶。
4. **会话间隔 10~30 分钟**。
5. **日请求不超过 100 次**。
6. **不自动写**。脚本无任何 post / like / follow / comment 接口。
7. **风控即退出**。460 / 461 / 403 / "captcha" / 重定向登录 → 立刻停 30 分钟。
8. **不翻页批量抓**。

---

## 四、准备工作

### 4.1 安装

```bash
pip install requests
pip install jieba pandas    # 可选，分析更准
```

### 4.2 获取 Cookie（3 分钟）

1. 浏览器打开 https://www.xiaohongshu.com 正常登录；
2. F12 → Application → Cookies → 选 `https://www.xiaohongshu.com`；
3. 全选复制，拼成 `name1=value1; name2=value2; ...`；
4. 关键字段：`web_session` / `a1` / `webId` / `xsecappid`；
5. 导出环境变量：

```bash
export XHS_COOKIE='web_session=...; a1=...; webId=...; xsecappid=xhs-pc-web; ...'
```

### 4.3 自检

```bash
python3 scripts/safety_check.py
```

应当看到 `✓ __INITIAL_STATE__ 解析成功`，否则先别跑抓取。

---

## 五、命令速查 — 调研与分析（v1.0 已有）

### 5.1 抓单篇笔记
```bash
python3 scripts/scrape-note.py --url "https://www.xiaohongshu.com/explore/64abc...?xsec_token=xxx" \
  --out /tmp/note.json
```

### 5.2 抓用户主页
```bash
python3 scripts/scrape-user.py --url "https://www.xiaohongshu.com/user/profile/5f123..." \
  --out /tmp/user.json
```

### 5.3 关键词搜索（首页）
```bash
python3 scripts/scrape-search.py --keyword 秋冬护肤 --out /tmp/search.json
```

### 5.4 离线分析
```bash
# 多篇合并
for id in 64abc 64abd 64abe; do
  python3 scripts/scrape-note.py --note-id $id >> notes.jsonl
done

python3 scripts/analyze-notes.py --input notes.jsonl --out report.md
```

样例数据：`examples/sample_notes.jsonl`（5 条，可直接 analyze 跑通）。

---

## 六、命令速查 — 创作与发布（v2.0 新增）

### 6.1 选题灵感

```bash
# 完全靠公式
python3 scripts/topic_ideas.py --seed "干皮护肤" --persona "30+ 干皮女生" --n 10

# 结合抓取数据（同行高频关键词、话题、爆款标题）
python3 scripts/topic_ideas.py --seed "干皮护肤" --notes notes.jsonl --n 10 --format md --out ideas.md
```

### 6.2 生成标题候选

```bash
# 列出所有公式 / 骨架代号
python3 scripts/write_post.py list

# 用指定公式生成标题（每种公式 2 条）
python3 scripts/write_post.py titles --topic "干皮护肤" --persona "30+" \
  --payoff "稳油不闷痘" --formulas T1,T2,T5 --n 2
```

### 6.3 渲染正文骨架

```bash
python3 scripts/write_post.py skeleton --code S1
```

### 6.4 一键产出 markdown 草稿

```bash
python3 scripts/write_post.py draft --topic "干皮护肤" --persona "30+" \
  --payoff "稳油不闷痘" --formula T2 --skeleton S1 \
  --tags "护肤,干皮护肤,30岁护肤,敏感肌护肤" \
  --cover-hint "护肤品平铺 + 手写标题字" \
  --out draft.md
```

输出的 `draft.md` 是骨架占位，让 Claude / 你接着把 `{hook}` `{step1_label}` 等填进去。

### 6.5 文案打分 + 修改建议

```bash
python3 scripts/polish_post.py --in draft.md
# 或直接传字符串
python3 scripts/polish_post.py --title "..." --content "..." --tags "护肤,干皮护肤"
```

输出 6 个子项分（标题 / 首段 / 排版 / emoji / 话题 / 合规），每项 0~10，加权出 0~100 总分。
**总分 ≥ 80 可发；60~80 建议优化；<60 建议重写。**

### 6.6 合规扫描（发布前必跑）

```bash
python3 scripts/compliance_check.py --in draft.md
```

退出码：
- `0` — 完全干净
- `1` — 中风险（建议改）
- `2` — 高风险（必须改）

可串到 CI / pre-publish hook。

### 6.7 发布辅助

```bash
# 一站式：跑打分 + 复制到剪贴板 + 打印检查表 + 写本地日志
python3 scripts/publish_helper.py --in draft.md \
  --log ~/.xiaohongshu/posts.jsonl

# 跳过打分（确认过了想直接发）
python3 scripts/publish_helper.py --in draft.md --skip-score
```

复制完成后：**打开小红书 App → 粘贴 → 选图 → 你点发布按钮。** 脚本到这就停。

### 6.8 发布后跟踪

```bash
# 1) 发布完拿到 note_id 后，回填到日志
python3 scripts/track_post.py register --uid abc123 --note-id 64abcd... --xsec-token xxx

# 2) 拉一次互动快照
python3 scripts/track_post.py snapshot --note-id 64abcd... --xsec-token xxx

# 3) 给所有跟踪期内的笔记一次性快照（节流）
python3 scripts/track_post.py snapshot-all

# 4) 看跟踪报告
python3 scripts/track_post.py report --out tracking.md
```

---

## 七、Python API（创作向）

```python
import sys; sys.path.insert(0, 'scripts')

from xhs_writer import (
    Draft, generate_titles, render_skeleton, score_post, make_draft,
    load_draft, save_draft, load_sensitive_words,
)

# 1. 生成标题候选
titles = generate_titles("干皮护肤", persona="30+ 干皮女生",
                        payoff="稳油不闷痘", formulas=["T1", "T2", "T5"], n_each=2)
for t in titles:
    print(t["formula"], t["title"])

# 2. 一键骨架草稿
draft = make_draft("干皮护肤", persona="30+", payoff="稳油不闷痘",
                   formula="T2", skeleton="S1",
                   tags=["护肤", "干皮护肤", "30岁护肤"])
print(draft.to_markdown())

# 3. 自己填好后打分
draft.content = "..."  # 填好的正文
score = score_post(draft.title, draft.content, draft.tags)
print(score.total, score.suggestions)

# 4. 保存为 markdown
save_draft(draft, "draft.md")
```

主要接口：

| 模块 | 函数/类 | 说明 |
|------|--------|------|
| `xhs_writer` | `generate_titles(topic, persona, payoff, formulas, n_each)` | 标题候选（11 种公式） |
| `xhs_writer` | `render_skeleton(code, fields)` | 渲染正文骨架 |
| `xhs_writer` | `make_draft(topic, ...)` | 一键骨架草稿 |
| `xhs_writer` | `score_post(title, content, tags)` | 6 维打分 |
| `xhs_writer` | `Draft` | 草稿数据结构（to_markdown / to_clipboard_text） |
| `xhs_writer` | `load_draft(path)` / `save_draft(draft, path)` | IO |
| `xhs_writer` | `load_sensitive_words()` | 敏感词列表 |

调研抓取 / 离线分析的 API 见 v1.0 部分（`xhs_client` / `xhs_parser` / `xhs_analyzer`）。

---

## 八、数据资产（data/）

| 文件 | 内容 |
|------|------|
| `data/title_templates.md` | 11 种爆款标题公式（T1~T11）+ 适用 + 踩坑 + 示例 |
| `data/content_structures.md` | 7 种正文骨架（S1~S7）+ 适用 + 字段说明 |
| `data/emoji_palette.md` | emoji 调色板 + 类目向 + 用量建议 |
| `data/hashtag_topics.md` | 话题标签库（大词/中词/小词）+ 选题工作流 |
| `data/community_rules.md` | 平台社区规则要点 + 红线清单 + 发布前 checklist |
| `data/sensitive_words.txt` | 敏感词列表（广告法 + 平台风控） |

这些文件不止给脚本读，也是 Claude 在调用本技能时的"参考手册" — 当用户问
「30 岁干皮怎么写选题？」，Claude 应该读 `title_templates.md` + `hashtag_topics.md` 给出答案。

---

## 九、典型场景示例

### 场景 A0：第一次用助手（建档案）

```bash
# 1) 准备 1~5 篇你的代表作（json/md 都行）
# 2) 一键建档
python3 scripts/assistant.py init \
    --persona "30+ 干皮女生" --voice casual --niche "护肤" \
    --baseline note1.json note2.md note3.json

# 3) 看状态 — 助手会告诉你接下来该干什么
python3 scripts/assistant.py status
```

### 场景 A1：让助手主导整周创作

```bash
# 周一早上
python3 scripts/assistant.py status   # 看推荐
python3 scripts/assistant.py next     # 直接执行（如：跑 brainstorm）

# 周内每篇笔记
python3 scripts/assistant.py write 干皮护肤   # 起草
python3 scripts/assistant.py coach draft.md   # 教练诊断
python3 scripts/assistant.py publish draft.md # 发布前流程

# 周末
python3 scripts/assistant.py review            # 周复盘
python3 scripts/assistant.py learn disable=emoji   # 教助手新规则
python3 scripts/assistant.py evolve            # 让助手吸收过去一周的反馈
```

### 场景 A：从零开始写一篇（手动版）

```bash
# 1) 调研竞品 (3~5 篇就够)
python3 scripts/scrape-note.py --url "https://..." >> notes.jsonl

# 2) 找选题
python3 scripts/topic_ideas.py --seed "干皮护肤" --notes notes.jsonl --n 10 \
  --format md --out ideas.md

# 3) 选一条选题，生成草稿骨架
python3 scripts/write_post.py draft --topic "干皮护肤" --persona "30+" \
  --formula T2 --skeleton S1 --tags "护肤,干皮护肤,30岁护肤" --out draft.md

# 4) 把 {hook} {step1_label} 等占位替换成真实内容（手动 or 让 Claude 写）

# 5) 打分 + 改
python3 scripts/polish_post.py --in draft.md

# 6) 合规扫
python3 scripts/compliance_check.py --in draft.md

# 7) 发布
python3 scripts/publish_helper.py --in draft.md --log ~/.xiaohongshu/posts.jsonl

# 8) 发布后回填 note_id + 拍快照
python3 scripts/track_post.py register --uid xxxxx --note-id 64abc... --xsec-token xxx
python3 scripts/track_post.py snapshot --note-id 64abc... --xsec-token xxx
```

### 场景 B：已经有草稿，想做一次完整发布前检查

```bash
python3 scripts/polish_post.py --in my_draft.md       # 打分
python3 scripts/compliance_check.py --in my_draft.md  # 合规
python3 scripts/publish_helper.py --in my_draft.md    # 准备发布
```

### 场景 C：批量看上周发的 5 条笔记表现

```bash
python3 scripts/track_post.py snapshot-all  # 一次性给跟踪期内所有笔记拍快照
python3 scripts/track_post.py report        # 查看报告
```

---

## 十、常见错误对照

| 错误 | 含义 | 处理 |
|------|------|------|
| `LoginRequired: HTTP 401` | Cookie 过期 | 重新浏览器登录 + 重新 export |
| `RateLimited: HTTP 460/461` | 频率风控 | **立即停止**，至少等 30 分钟 |
| `BlockedByCaptcha: HTTP 403` / 出现 verify | 需要滑块 | 浏览器过验证 + 等 30 分钟 |
| `NotFound: HTTP 404` | 笔记被删 / id 错 | 换一个 |
| `没找到 __INITIAL_STATE__` | HTML 结构变了 / 重定向 | `--save-html` 看原始页 |
| `polish_post 退出码 2` | 文案分 < 60 | 看 suggestions 修改 |
| `compliance_check 退出码 2` | 高风险违规 | 必须改（联系方式 / 绝对化词） |

---

## 十一、触发词

- 小红书 / xhs / xiaohongshu / red
- 写小红书 / 小红书文案 / 爆款文案 / 小红书选题
- 小红书调研 / 小红书分析 / 同行分析
- 小红书发布 / 发小红书 / 小红书运营
- 小红书复盘 / 小红书数据

---

## 十二、版本历史

- **v3.0.0（当前，2026-04-27）** — Allen 流升级（哲学家视角）
  - 新增 5 个 Allen 美学维度：留白度 / 去 AI 腔 / 带读者 / 共鸣度 / 邀请语
  - 新增 3 个 CLI：`critique.py` / `coin_word.py` / `series_design.py` / `reader_simulate.py`
  - 新增 3 份数据资产：`allen_method.md` / `ai_speak_patterns.json` / `seasonal_themes.md`
  - 新增风格预设：`allen` / `engineer` / `balanced` 三种一键切换
  - 工程打分 + Allen 美学**叠加**而不替代，权重按预设
  - coach.py 整合 Allen 维度，对低于 7 分的维度自动产出 4 件套
  - 来源：司志远（Allen）2026-04-23~27 三课 + 五技法 + 11 案例教学

- **v2.5.x** — 从"工具堆"升级为"创作助手"
  - **新增个性化**：StyleProfile 风格档案（从 baseline 自动学习语调/长度/emoji/口头禅）
  - **新增可学习**：RuleOverride 规则覆盖（用户教过的助手记住） + evolve 自动演进
  - **新增写作教练** `coach.py`：每条问题给 (what, why, how, example) 四件套，
    支持可选 LLM 增强（XHS_LLM_PROVIDER=anthropic）
  - **新增对话式选题** `brainstorm.py`：5 轮对话从模糊到具体
  - **新增周复盘** `weekly_review.py`：自动汇总 7/30 天产出 + 互动 + 反馈 + 下周建议
  - **新增写作训练** `practice.py`：命题练习 + 改写训练 + 历史成绩
  - **新增 A/B 测试** `ab_test.py`：同选题 2 版各发，互动数据告诉你哪版赢
  - **新增主入口** `assistant.py`：根据上下文推荐下一步，把全流程串起来
  - **打分系统升级**：score_post 接收 RuleOverride，按个人画像加权
  - **个人档案**位于 `~/.xiaohongshu/profile/`（用户私有，跨 skill 共用）

- **v2.0.0** — 全流程创作能力大改版
  - 新增 7 个 CLI：选题 / 创作 / 打分 / 合规 / 发布辅助 / 跟踪
  - 新增 6 份数据资产：标题公式 / 正文骨架 / emoji 调色板 /
    话题标签库 / 社区规则 / 敏感词

- **v1.0.x** — 抓取 + 分析能力首版（详见上版 README）

---

## 十三、设计哲学

1. **个人号 / 小团队**为目标用户，不是 MCN 批量号工厂。
2. **规则可解释** — 标题公式、骨架、打分项都明文写在 data/ 里，Claude 和你都能读。
3. **不依赖大模型** — 所有脚本零 API 成本可跑；让 Claude 来调它们的产物。
4. **半自动 ≠ 全自动** — 发布按钮永远在人手里，账号才安全。
5. **闭环优于单点** — 调研 / 写 / 发 / 复盘任何一环少了，都做不长。

---

**重要免责：** 本技能仅用于合规、针对公开可见内容的个人调研与创作辅助。
请尊重 xiaohongshu.com 的服务条款和当地法律法规。
商业批量采集、内容搬运、绕过风控、自动化发布 / 互动等行为均**不在本技能支持范围内**。

**技术支持：** 青岛火一五信息科技有限公司
