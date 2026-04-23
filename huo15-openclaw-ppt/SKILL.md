---
name: huo15-openclaw-ppt
displayName: 火一五演示稿技能
description: 基于 design tokens 的 PPT 生成技能。内置 4 套审美方案（Apple 发布会暗场 / Apple.com 白场 / 小红书博主奶油生活系 / 小红书复古胶片）+ 10 个语义化页面模板（hero/section/stat/kpi/quote/list/compare/product/timeline/cta），自动 fit 防止 CJK 溢出。触发词：做PPT、生成PPT、PPT、Apple发布会、小红书博主PPT、复古胶片PPT、封面、分章、大字页、KPI、对比页、时间线、封底。
version: 3.0.0
aliases:
  - 火一五PPT技能
  - 火一五演示稿技能
  - PPT生成
  - AppleKeynote风格
  - Apple发布会PPT
  - 苹果风格PPT
  - 小红书博主PPT
  - 奶油博主PPT
  - 复古胶片PPT
  - 乔布斯风格PPT
  - 小红书风格PPT
dependencies:
  python-packages:
    - python-pptx
    - Pillow
---

# 火一五 PPT 技能 v3.0

> Design tokens + 10 页面模板 + 4 套审美方案 — 青岛火一五信息科技有限公司

---

## 一、v3.0 核心理念

以前 v2.x 是「色卡游戏」——只改 primary/accent 两个颜色就叫一个新风格。v3.0 重写成真正的**设计系统**：

```
StylePack = Palette + Typography + Spacing + Elevation + Decoration + Canvas
```

每一层都是独立的 tokens，单一风格对应一整组 tokens。例如「Apple 发布会」不只是「黑底」，而是：

- **Palette**：纯黑 `#000000` 底 + 4 级灰阶文字 + Apple 蓝 `#0A84FF`
- **Typography**：SF Pro Display + hero 160pt + 负字距 -3% + 行高 0.95
- **Spacing**：8pt grid + hero 页左右留白 1.2"
- **Elevation**：完全 flat，无阴影
- **Decoration**：居中对齐、英文全大写、不显示页脚

---

## 二、4 套审美方案（v3.0）

| pack key | 风格 | 适用场景 |
|---------|------|---------|
| `apple-keynote`（别名 `apple`, `苹果`, `发布会`） | Apple 发布会暗场 | 新品发布、融资路演、重磅主题 |
| `apple-light`（别名 `苹果白`, `苹果官网`） | Apple.com 白场 | 产品介绍页、功能说明、官网风 |
| `xiaohongshu-creator`（别名 `博主`, `博主风`, `生活博主`, `奶油博主`） | 小红书博主（奶油生活系） | 博主笔记、种草分享、温度叙事 |
| `xiaohongshu-vintage`（别名 `复古`, `胶片`, `复古胶片`） | 小红书博主（复古胶片） | 旅行手记、文艺向、生活美学 |

### 2.1 apple-keynote —— 真·发布会

- **配色**：纯黑 `#000000`（不是深蓝！）+ 白灰文字 + Apple 品牌蓝
- **字体**：SF Pro Display + SF Pro Text
- **hero 字号**：**160pt**（是 v2 的 2.5 倍，带自动 fit 避免 CJK 溢出）
- **装饰**：完全居中、英文小字全大写（INTRODUCING / SCALE）、不显示页脚
- **big_stat 字号**：280pt — "2B" 一张页的视觉锚点

### 2.2 apple-light —— 产品页白场

- **配色**：纯白 + Apple.com 的卡片灰 `#F5F5F7` + 链接蓝 `#0071E3`
- **字体**：SF Pro Display
- **hero 字号**：120pt
- **卡片**：无描边，圆角 0.18"，靠填色区分
- **装饰**：居中对齐、英文不全大写

### 2.3 xiaohongshu-creator —— 奶油生活博主

- **配色**：奶油 `#FBF7F0` 底 + 焦糖咖 `#3E2E1F` 主文字 + 鼠尾草绿 `#9FAE8B` 点缀
- **字体**：**Noto Serif SC**（衬线！）+ PingFang SC 正文
- **hero 字号**：72pt + 正字距 +2%（衬线字撑开）
- **装饰**：左对齐、标题左侧竖条 accent bar、圆角 0.22" 卡片 + 微阴影
- **特色**：文字不用纯黑而用焦糖咖色，配 sage green accent 做博主的温度

### 2.4 xiaohongshu-vintage —— 复古胶片

- **配色**：复古米 `#F2EAD9` + 深栗咖 `#4A3526` 文字 + 雾霾蓝 `#A8B8C6` accent
- **字体**：Noto Serif SC（标题和正文都衬线，强化胶片感）
- **hero 字号**：64pt + 更松字距 +3% + 高行高 1.2
- **装饰**：封面顶/底装饰横线、卡片直角 0.08" 有描边（胶片边框感）

---

## 三、10 个页面模板

| template key（type） | 用途 | 别名 |
|----|----|----|
| `hero_cover` | 封面大字页（eyebrow + title + subtitle + footnote） | `cover` |
| `section_divider` | 分章大字页（编号 + 章节标题 + 副标） | `section` |
| `big_stat` | 单数字大字页（Apple "2B" 招牌页） | `stat`, `big_number` |
| `kpi_triple` | 3 宫格 KPI 卡 | `kpi`, `kpi_card` |
| `quote_card` | 引用金句卡（大引号 + 引文 + 作者） | `quote` |
| `content_list` | 编号/要点列表 | `list` |
| `compare_columns` | 左右对比（before/after, 方案 A/B） | `compare`, `vs`, `before_after` |
| `product_shot` | 产品摄影页（大图 + 侧栏叙事） | `product`, `image`, `gallery` |
| `timeline` | 时间线（横向多节点） | `story` |
| `call_to_action` | 封底行动号召（大字 + CTA + 联系方式） | `cta`, `end`, `thanks`, `contact` |

所有模板自动：
- 按 `StylePack` 的 tokens 绘图 — 换 pack 整套风格变
- **自动 fit 大字号** — hero/section/big_stat/cta 的大字按宽度约束自动缩放，避免 CJK 长文本溢出换行
- 按 `decoration` 切换布局 — 居中/左对齐/accent bar/装饰线 都由 pack 控制
- 支持 6 个 v3 pack + 3 个 v2.x legacy pack 全兼容

---

## 四、JSON deck 规约

```json
{
  "year": "2026",
  "slides": [
    { "type": "hero_cover",
      "eyebrow": "INTRODUCING",
      "title": "M4 Ultra.",
      "subtitle": "地球上最强的芯片。",
      "footnote": "Apple · Cupertino · 2026" },

    { "type": "section_divider",
      "number": "01",
      "title": "Performance",
      "subtitle": "性能" },

    { "type": "big_stat",
      "caption": "CPU PERFORMANCE",
      "value": "2x",
      "unit": "比 M3 Ultra 快",
      "footnote": "基于实际应用工作负载",
      "accent": true },

    { "type": "kpi_triple",
      "title": "重要数字",
      "en_sub": "Key Metrics",
      "items": [
        { "value": "192", "label": "GB 统一内存", "caption": "整张内存池共享" },
        { "value": "80B",  "label": "晶体管",      "caption": "3nm 工艺" },
        { "value": "4TB/s","label": "内存带宽",    "caption": "AI 推理飞起" }
      ] },

    { "type": "quote_card",
      "quote": "One more thing…",
      "author": "Tim Cook",
      "role": "Apple CEO" },

    { "type": "content_list",
      "title": "我们做了什么",
      "en_sub": "What We Did",
      "numbered": true,
      "items": [
        { "label": "重构设计系统", "desc": "把审美分解成 tokens" },
        { "label": "10 个语义模板", "desc": "hero / section / stat / ..." }
      ] },

    { "type": "compare_columns",
      "title": "升级对比",
      "en_sub": "Before vs After",
      "emphasize": "right",
      "left":  { "label": "BEFORE", "title": "色卡游戏", "items": ["..."] },
      "right": { "label": "AFTER",  "title": "审美方案", "items": ["..."] } },

    { "type": "product_shot",
      "title": "产品页",
      "kicker": "NEW",
      "subtitle": "Apple.com 风的大图 + 侧栏叙事",
      "bullets": ["图占大块面积", "文字简洁克制"],
      "image": "/tmp/shot.png",
      "layout": "right" },

    { "type": "timeline",
      "title": "产品演进",
      "en_sub": "Timeline",
      "events": [
        { "time": "2024", "label": "v1.0", "desc": "乔布斯暗蓝" },
        { "time": "2026", "label": "v3.0", "desc": "tokens + 4 pack" }
      ] },

    { "type": "call_to_action",
      "title": "Thank You.",
      "subtitle": "一起做有设计感的幻灯片",
      "cta": "hello@huo15.com",
      "footnote": "火一五 · openclaw-ppt v3.0" }
  ]
}
```

---

## 五、命令行

```bash
# 列出所有 pack
python3 scripts/create-pptx.py --list-packs

# 列出所有 template
python3 scripts/create-pptx.py --list-templates

# 1. 按 JSON 生成完整 deck（推荐）
python3 scripts/create-pptx.py \
  --pack apple-keynote \
  --spec ./deck.json \
  --output /tmp/deck.pptx

# 2. 快速试样封面
python3 scripts/create-pptx.py \
  --pack 博主风 \
  --cover "关于做幻灯片这件小事|写给刚入行的小伙伴" \
  --year 2026 \
  --output /tmp/cover.pptx

# 3. 老的 --style 兼容（等价于 --pack）
python3 scripts/create-pptx.py --style jobs-dark --spec deck.json -o out.pptx
```

公司名解析顺序：`--company` > `~/.huo15/company-info.json` > `青岛火一五信息科技有限公司`（默认）。

---

## 六、示例 decks

`examples/decks/` 提供 4 份对应 4 套 pack 的完整样例：

| 文件 | pack | 讲什么 |
|----|----|----|
| `apple-keynote-launch.json` | `apple-keynote` | Apple "M4 Ultra" 发布会风 6 页 |
| `apple-light-product.json`  | `apple-light`   | OpenClaw Enhance 产品介绍 5 页 |
| `xhs-creator-vlog.json`     | `xiaohongshu-creator` | 博主笔记「关于做幻灯片这件小事」5 页 |
| `xhs-vintage-travel.json`   | `xiaohongshu-vintage` | 青岛老城旅行手记 6 页 |

对应的渲染预览放在 `examples/previews/*.png`。

---

## 七、触发词

- 做 PPT / 生成 PPT / 制作 PPT / 写 PPT
- Apple 发布会 / 发布会风 / 苹果风格 / 官网风
- 小红书博主 / 博主风 PPT / 生活博主 / 奶油风
- 复古胶片 / 胶片风 / 复古 PPT / 文艺风
- 封面 / 分章页 / 大字页 / KPI / 对比页 / 时间线 / 封底
- 第 X 页 / 继续 / 加一页

---

## 八、选 pack 指南

| 想要的效果 | 选 |
|----|----|
| 发布会大字 / 新品宣发 / 投融资路演 | `apple-keynote` |
| 产品介绍页 / 官网风 / 功能说明 | `apple-light` |
| 博主笔记 / 种草分享 / 温度叙事 | `xiaohongshu-creator` |
| 旅行手记 / 文艺向 / 生活美学 | `xiaohongshu-vintage` |
| 稳妥正式汇报（兼容 v1.x） | `jobs-dark` |
| 小红书品牌红 Feed 帖（兼容 v2.x） | `xiaohongshu` / `xiaohongshu-portrait` |

---

## 九、技术细节

### 9.1 Design tokens 层次

```
StylePack
├── Canvas       画布尺寸（默认 13.33×7.5" 16:9）
├── Palette      3 级背景 + 4 级文字 + accent + border/divider
├── Typography   display/body 两字体 stack + 6 级字号阶梯 + 字重 + 字距 + 行高
├── Spacing      8pt grid — gutter/stack_sm/md/lg/xl + margin_x/margin_x_hero
├── Elevation    card_radius + stroke + 假阴影（python-pptx 无真阴影）
└── Decoration   cover 对齐、cover top/bottom line、accent bar、
                 tag_style、stat_hero_size、image_treatment
```

### 9.2 字距（tracking/letter-spacing）

python-pptx 官方 API 不支持字距。v3.0 在 `templates/helpers.py::_set_run_spacing` 里用 OOXML XML 注入 `<a:rPr spc="N">`，单位是 1/100 pt。hero 大字用 -3% em（收紧），衬线字用 +2% em（展开）。

### 9.3 Auto-fit 大字号

hero/section/big_stat/cta 的文本在 `fit_font_size(text, width, base_size)` 里自动缩放，防止 CJK 长文本换行撞副标题。宽度估算按 CJK 1.1em / 大写 0.75em / 小写 0.62em / 标点 0.38em，留 12% 安全余量。

### 9.4 假阴影

`xhs-creator` 开启 `use_fake_shadow=True`，在卡片下方偏移 0.06" 画一个比卡片色深的色块模拟阴影。python-pptx 没有真阴影 API。

### 9.5 与 v2.x 兼容

- `--style` 参数保留，等价于 `--pack`
- legacy pack（`jobs-dark`, `xiaohongshu`, `xiaohongshu-portrait`）仍可用
- JSON 字段 `en_subtitle` 自动映射到 `en_sub`，`sub` 自动映射到 `subtitle`
- slide type `cover/section/list/quote/end` 仍能跑，走 templates 注册表的别名

---

## 十、版本历史

- **v3.0.0（当前）**：重写为 design tokens 架构。
  - **新增 design_system.py**：Palette + Typography + Spacing + Elevation + Decoration + Canvas 六层独立 tokens
  - **新增 style_packs.py**：4 个 v3 审美方案（apple-keynote / apple-light / xiaohongshu-creator / xiaohongshu-vintage）+ 3 个 legacy pack
  - **新增 templates/**：10 个语义化页面模板 + helpers 共享原语
  - **新增字距**：OOXML XML 注入 `<a:rPr spc="N">` 实现 letter-spacing（python-pptx 不支持）
  - **新增 auto-fit**：大字号自动缩放避免 CJK 溢出换行
  - **新增 4 套示例 deck**：examples/decks/*.json + examples/previews/*.png
  - **向后兼容**：`--style` 参数、v2 字段名、legacy pack 全保留
- v2.1.0：扩展 7 种风格（ocean/forest/sunset/minimal/pastel/github/tech-blue）
- v2.0.0：styles 注册表 + pptx_toolkit 绘图原语 + create-pptx.py CLI + 小红书配色
- v1.x：深蓝乔布斯单页脚本集合

---

**技术支持：** 青岛火一五信息科技有限公司
