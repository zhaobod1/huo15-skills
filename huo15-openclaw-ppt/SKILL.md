---
name: huo15-openclaw-ppt
displayName: 火一五演示稿技能
description: 多风格 PPT 生成技能。内置乔布斯极简暗蓝 + 小红书暖奶油风格（含竖版 9:16 发帖模式）；支持 JSON deck 规约一键生成 + 自动注入本地公司名。触发词：做PPT、生成PPT、PPT、第X页、写PPT、制作PPT、小红书风格PPT、小红书帖。
version: 2.0.0
aliases:
  - 火一五PPT技能
  - 火一五演示稿技能
  - PPT生成
  - 乔布斯风格PPT
  - 小红书风格PPT
  - 小红书帖
  - 极简PPT
dependencies:
  python-packages:
    - python-pptx
    - Pillow
---

# 火一五 PPT 技能 v2.0

> 多风格 PPT 生成 — 青岛火一五信息科技有限公司

---

## 一、核心能力

1. **多风格切换** — 一行 `--style` 切换：`jobs-dark`（乔布斯极简）/ `xiaohongshu`（小红书 16:9）/ `xiaohongshu-portrait`（小红书竖版 9:16 发帖）。
2. **JSON deck 规约** — 用 JSON 描述一整份 deck，自动按风格渲染。适合 Claude 和脚本化生成。
3. **本地公司信息** — 页脚自动注入 `~/.huo15/company-info.json` 的公司名（若无则回落默认串），与 `huo15-openclaw-office-doc` 共享。
4. **复用绘图原语** — `pptx_toolkit.py` 暴露封面/分章/列表/引言/结尾页构建函数，便于在单独脚本里拼装特殊页面。

---

## 二、内置风格

| 风格 key | 名称 | 尺寸 | 配色主调 | 适用场景 |
|---------|------|------|---------|---------|
| `jobs-dark` (别名 `jobs`) | 乔布斯极简暗蓝 | 13.33 × 7.5" (16:9) | #060D1A 暗蓝 / 白灰 | 对外正式汇报、产品发布 |
| `xiaohongshu` (别名 `xhs`, `小红书`) | 小红书风 | 13.33 × 7.5" (16:9) | #FFF8F3 暖奶油 / #FF2442 小红书红 | 营销演示、品牌故事 |
| `xiaohongshu-portrait` (别名 `xhs-portrait`, `小红书竖版`) | 小红书发帖版 | 7.5 × 13.33" (9:16) | 同上 | 小红书 Feed 帖子、朋友圈长图 |

### 2.1 乔布斯风格（默认）

- **背景**：深蓝暗底 `#060D1A`
- **卡片**：深灰蓝 `#0D182A`，1px 暗灰描边，圆角
- **主文字**：白 `#FFFFFF`；副文字 `#888888`；点缀 `#CCCCCC`
- **字号**：封面标题 64pt / 页面标题 28pt / 卡片标题 14pt / 正文 11pt
- **装饰**：无渐变、无阴影、留白充足

### 2.2 小红书风格（新增）

- **背景**：暖奶油 `#FFF8F3`
- **卡片**：纯白 `#FFFFFF`，淡粉描边 `#F5E6E6`，圆角
- **主色**：小红书红 `#FF2442` 用于分章标题、副标题、tag 胶囊
- **主文字**：深黑 `#1A1A1A`；副文字中灰 `#8A8A8A`；深灰 `#4A4A4A` 强调
- **装饰**：
  - 封面顶部整条红色细条
  - 标题左侧红色竖条（accent bar）
  - 左下角 `#火一五` tag 胶囊
- **英文副标题**：不强制大写，保留原始大小写
- **字号**：封面标题 60pt / 页面标题 30pt / 卡片标题 16pt / 正文 12pt

### 2.3 小红书竖版（9:16）

同 2.2，但画布切换为 7.5 × 13.33"，字号统一放大约 15%（标题 72pt / 页面标题 36pt 等）。输出的 pptx 可用 **"文件 → 导出为图片"** 直接得到 1242×2208 长图，适合发小红书 Feed。

---

## 三、JSON deck 规约

```json
{
  "year": "2026",
  "slides": [
    { "type": "cover",
      "title": "火一五 × 具身智能",
      "subtitle": "2026 Q2 产品路线图",
      "footnote": "可选；未填会用公司名+年份" },

    { "type": "list",
      "title": "五大支柱",
      "en_subtitle": "Five Pillars",
      "items": [
        { "title": "龙虾 OpenClaw", "desc": "AI 原生企业操作系统",
          "rep": "核心平台", "year": "2026" }
      ] },

    { "type": "quote",
      "title": "远见与品味",
      "en_subtitle": "Vision and Taste",
      "quote": "找不到方向的根本原因，不是不够聪明，是没有品味。",
      "author": "Steve Jobs", "role": "苹果公司创始人",
      "image": "/tmp/steve_jobs.png" },

    { "type": "section",
      "title": "为什么押宝龙虾",
      "subtitle": "WHY WE BET ON OPENCLAW" },

    { "type": "end",
      "title": "Thanks",
      "subtitle": "期待与你同行",
      "qrcodes": [
        { "path": "/tmp/qr_gzh.png", "label": "逸寻智库公众号" },
        { "path": "/tmp/qr_bili.png", "label": "B 站频道" }
      ] }
  ]
}
```

| slide.type | 必填字段 | 可选字段 |
|-----------|---------|---------|
| `cover` | `title` | `subtitle` / `footnote` |
| `list` | `title` / `items[]` | `en_subtitle`；`items[i]`: `title` 必填，`desc` / `rep` / `year` 可选 |
| `quote` | `title` / `quote` | `en_subtitle` / `author` / `role` / `image` |
| `section` | `title` | `subtitle` |
| `end` | `title` | `subtitle` / `qrcodes`[] |

> 仍想手工拼页？直接 `import pptx_toolkit` 调用 `cover_slide / list_slide / quote_slide / section_slide / end_slide`，或用底层 `text_box / add_card / add_divider / add_tag / add_accent_bar`。

---

## 四、命令行

```bash
# 1. 按 JSON 生成完整 deck
python3 scripts/create-pptx.py \
  --output /tmp/deck.pptx \
  --style xiaohongshu \
  --spec ./mydeck.json

# 2. 快速试样（单页封面）
python3 scripts/create-pptx.py \
  --output /tmp/cover.pptx \
  --style xiaohongshu-portrait \
  --cover "买房避坑指南|新手必看 8 条" \
  --year 2026

# 3. 显式覆盖公司名
python3 scripts/create-pptx.py --output out.pptx --spec deck.json \
  --company "某某科技有限公司"
```

公司名解析顺序：`--company` > `~/.huo15/company-info.json` > `青岛火一五信息科技有限公司`（默认）。
如需补录本地公司信息，见 `huo15-openclaw-office-doc` 的 `company-info.py`。

---

## 五、触发词

- 做 PPT / 生成 PPT / 制作 PPT / 写 PPT
- 小红书风格 PPT / 小红书帖 / 发小红书 / 小红书封面
- 乔布斯风格 / 极简 PPT / 深蓝 PPT
- 添加 Slide X / 第 X 页 / 继续

---

## 六、历史（v1.x）参考

v1.x 的深蓝乔布斯风格绘图思路与示例页保留在 `scripts/create_pptx_combined.py` 与 `scripts/slide5_why_openclaw.py` 中，仅作为排版参考。v2.0 之后请优先走 `create-pptx.py` + JSON 规约。

### v1.x 页面类型速查

- 封面页：纯色、大标题居中、无装饰
- 内容页：左上标题 + 英文副标题 + 分隔线
- 卡片列表页：编号圆点 + 标题 + 描述 + 代表 + 年份
- 双栏对比页：左右各 5.9"，间距 0.23"
- 时间轴页：轴线 0.025" + 节点圆 0.42"
- 引言页：图片 + 引言卡片
- 封底页：大字 + 二维码（左右对称）

### v1.x 图片处理要点

- 保持原始比例，不得拉伸
- 横版 800×400 → 宽 12.13"；竖版 1080×1542 → 宽 2.6"；方版 1000×1000 → 宽 3.0"
- PNG 带透明通道：先用 `Image.save()` 转一次
- 微信图片务必走本地路径（`~/.openclaw/media/inbound/`），COS URL 会签名过期

---

## 七、版本历史

- **v2.0.0（当前）**：
  - 新增：`scripts/styles.py` — 风格化注册表（Jobs / 小红书 / 小红书竖版）
  - 新增：`scripts/pptx_toolkit.py` — 风格感知的绘图原语（cover/list/quote/section/end）
  - 新增：`scripts/create-pptx.py` — 通用 CLI 生成器，支持 `--spec` / `--cover` / `--style`
  - 新增：小红书配色 / tag 胶囊 / accent bar / 9:16 竖版
  - 集成：页脚公司名自动读 `~/.huo15/company-info.json`
- v1.1.0：封面页去装饰；图片比例规则补齐
- v1.0.0：初始乔布斯风格单页脚本集合

---

**技术支持：** 青岛火一五信息科技有限公司
