---
name: huo15-openclaw-ppt
displayName: 火一五PPT技能
description: 乔布斯极简风格 PPT 生成技能，支持深蓝底色 + 苹方字体 + 白/灰双色调。支持内容规划、单页生成、合并版导出。触发词：做PPT、生成PPT、PPT、第X页、写PPT、制作PPT。
version: 1.0.0
aliases:
  - 火一五PPT技能
  - PPT生成
  - 乔布斯风格PPT
  - 极简PPT
dependencies:
  python-packages:
    - python-pptx
---

# 火一五 PPT 技能 v1.0

> 乔布斯极简风格 PPT 生成 — 青岛火一五信息科技有限公司

---

## 一、设计风格

### 配色系统
| 常量 | RGB | 用途 |
|------|-----|------|
| C_BG | (0x06, 0x0D, 0x1A) | 高级感暗蓝背景（Photoshop风格） |
| C_CARD | (0x0D, 0x18, 0x2A) | 卡片背景 |
| C_TEXT | (0xFF, 0xFF, 0xFF) | 主文字白色 |
| C_SUBTEXT | (0x88, 0x88, 0x88) | 副文字灰色 |
| C_DIVIDER | (0x33, 0x33, 0x44) | 分隔线暗灰 |

### 字体
- 默认字体：`PingFang SC`（苹方，Mac）
- Windows 替代：`Microsoft YaHei`
- 字号层级：标题 64pt / 副标题 26pt / 页面标题 28pt / 卡片标题 14pt / 正文 10pt / 页脚 9pt

### 布局
- 页面尺寸：13.33 × 7.5 寸（16:9）
- 左侧边距：0.6 寸
- 卡片宽度：12.13 寸

---

## 二、卡片组件规范

### add_card()
```python
def add_card(slide, left, top, width, height):
    shape = slide.shapes.add_shape(
        1, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = C_CARD
    shape.line.color.rgb = RGBColor(0x33, 0x33, 0x44)
    shape.line.width = Pt(0.5)
    return shape
```

### add_dot() — 编号小圆点
```python
def add_dot(slide, left, top):
    dot = slide.shapes.add_shape(
        9, Inches(left), Inches(top), Inches(0.28), Inches(0.28)
    )
    dot.fill.solid()
    dot.fill.fore_color.rgb = C_TEXT
    dot.line.fill.background()
    return dot
```

### text_box()
```python
def text_box(slide, text, left, top, width, height,
             font_size=14, bold=False, color=None, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.name = FONT
    run.font.color.rgb = color or C_TEXT
    return tb
```

---

## 三、页面标题规范

每页左上角固定格式：
```
text_box(slide, "页面标题", 0.6, 0.35, 8, 0.55, font_size=28, bold=True, color=C_TEXT)
text_box(slide, "ENGLISH SUBTITLE", 0.6, 0.82, 10, 0.35, font_size=10, color=C_SUBTEXT)
add_divider(slide, 0.6, 1.18, 12.13, RGBColor(0x33, 0x33, 0x44))
```

---

## 四、图片处理规范

**必须保持原始比例，不得拉伸变形。**

```python
from PIL import Image
img = Image.open(path)
# 1080x1542（竖版）→ Inches(2.6), Inches(3.71)
# 1000x1000（方形）→ Inches(3.0), Inches(3.0)
slide.shapes.add_picture(path, Inches(left), Inches(top), Inches(w), Inches(h))
```

---

## 五、合并版输出流程

1. 先做 Slide 1，确认
2. 后续每页叠加到同一 Presentation 对象
3. 输出文件：`/Users/jobzhao/.openclaw/media/outbound/合并版_{主题}.pptx`

**重要：合并版包含前面所有已确认的页面。**

---

## 六、脚本模板

```python
#!/usr/bin/env python3
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

C_BG      = RGBColor(0x06, 0x0D, 0x1A)
C_CARD    = RGBColor(0x0D, 0x18, 0x2A)
C_TEXT    = RGBColor(0xFF, 0xFF, 0xFF)
C_SUBTEXT = RGBColor(0x88, 0x88, 0x88)
FONT = "PingFang SC"

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# 通用函数
def text_box(...): ...
def add_card(...): ...
def add_dot(...): ...

# Slide 1
s1 = prs.slides.add_slide(BLANK)
bg = s1.background; fill = bg.fill; fill.solid(); fill.fore_color.rgb = C_BG
...

# Slide 2 ...
# Slide 3 ...

prs.save("/Users/jobzhao/.openclaw/media/outbound/合并版_{主题}.pptx")
```

---

## 七、触发词

- 做PPT、生成PPT、制作PPT
- 第X页、第X张
- 乔布斯风格、极简PPT、深蓝PPT
- 添加 Slide X

---

## 八、文件路径规范

- 脚本目录：`~/.openclaw/workspace/scripts/`
- 单页输出：`/Users/jobzhao/.openclaw/media/outbound/{序号}_{标题}.pptx`
- 合并版：`/Users/jobzhao/.openclaw/media/outbound/合并版_{主题}.pptx`
- 图片缓存：`/tmp/book_*.jpg`（注意 base64 解码后 PIL 可能无法识别，需用微信接收的本地路径）

---

## 九、图片获取（易踩坑）

1. **Odoo 知识库附件**：`ir.attachment` 的 `datas` 字段是 base64 字符串，必须 `base64.b64decode()` 后才是原始图片数据
2. **COS URL 签名**：微信发的图片 URL 签名有时效，过期返回 403，直接用微信附件路径更可靠
3. **本地附件路径**：`~/.openclaw/media/inbound/` 下以 `---` 分隔符命名的文件是微信接收的原始图片

---

**技术支持：** 青岛火一五信息科技有限公司
