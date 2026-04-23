"""
templates/helpers.py - 所有模板共用的绘图原语

不同于老的 pptx_toolkit（按 Style），这里按 StylePack 的 design tokens 绘图。
"""

from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from lxml import etree

from design_system import StylePack, hex_to_rgb, resolve_weight


# ============================================================
# 画布基础
# ============================================================

def set_canvas(prs, pack: StylePack):
    """给 deck 设尺寸 —— 第一次调用生效，之后 idempotent。"""
    prs.slide_width = Inches(pack.canvas.width)
    prs.slide_height = Inches(pack.canvas.height)


# ============================================================
# 文本宽度估算 & 自动 fit
# ============================================================

def _approx_text_width_in(text: str, font_size_pt: float) -> float:
    """粗估文本在给定字号下的宽度（inch）。

    Bold display 字体偏宽，宁可高估。用偏保守的比例：
      CJK = 1.1 em（字面 + 间距）
      大写 / 数字 = 0.75 em
      小写 = 0.62 em
      标点 = 0.38 em
      空格 = 0.32 em
    """
    w_em = 0.0
    for c in text:
        cp = ord(c)
        if cp > 0x2E80:           # CJK / fullwidth
            w_em += 1.1
        elif c.isspace():
            w_em += 0.32
        elif c in '.,;:!?\'"-·—':
            w_em += 0.38
        elif c.isdigit() or c.isupper():
            w_em += 0.75
        else:
            w_em += 0.62
    # em → inch (pt/72)
    return w_em * (font_size_pt / 72.0)


def fit_font_size(text: str, width_in: float, base_size_pt: float,
                  *, min_size_pt: float = 24.0,
                  max_lines: int = 1,
                  tolerance: float = 0.88) -> float:
    """返回一个不会在 `width_in × max_lines` 溢出的字号。

    用于 hero / section 这种超大字，避免 CJK 长文本换行后撞到副标题。
    tolerance 留 8% 安全余量，避免 Impress/Keynote 实际渲染比估计略宽。
    """
    budget_in = width_in * max_lines * tolerance
    size = base_size_pt
    w = _approx_text_width_in(text, size)
    if w <= budget_in:
        return size
    # 缩到刚好能容下
    size = size * (budget_in / w)
    return max(min_size_pt, size)


def new_slide(prs, pack: StylePack):
    """新建空白幻灯片（layout 6 = blank）+ 填背景。"""
    set_canvas(prs, pack)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = pack.palette.rgb('bg')
    return slide


# ============================================================
# 字距（tracking）注入 — python-pptx 官方 API 不支持，打 XML
# ============================================================

def _set_run_spacing(run, tracking_em: float, font_size_pt: int):
    """给 run 注入字距 XML。tracking_em 是 em 单位（0.02 = +2%）。"""
    if tracking_em == 0:
        return
    # OOXML 的 <a:rPr spc="N"> N 是 0.01pt 为单位
    spc_pt = tracking_em * font_size_pt  # 换算到 pt
    spc_val = int(spc_pt * 100)           # OOXML 期望 1/100 pt
    rpr = run._r.get_or_add_rPr()
    rpr.set('spc', str(spc_val))


# ============================================================
# 文本框（支持字体/字距/字重/行高）
# ============================================================

def add_text(slide, pack: StylePack, text: str,
             left: float, top: float, width: float, height: float,
             *,
             font=None, font_size=None, weight='regular',
             color_key='text_primary', color=None,
             align='left', valign='top',
             tracking=None, leading=None, uppercase=False):
    """通用文本框。

    - font         指定字体名；缺省用 display_font
    - font_size    pt；缺省用 body
    - weight       'bold' / 'semibold' / 'medium' / 'regular'
    - color_key    调色板 key（text_primary / text_secondary / accent / ...）
    - color        直接传 RGBColor 则覆盖 color_key
    - align        'left' / 'center' / 'right'
    - tracking     em 单位；正值放宽，负值收紧
    """
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0

    # 竖向对齐
    if valign == 'middle':
        tf.vertical_anchor = 3  # MSO_ANCHOR.MIDDLE
    elif valign == 'bottom':
        tf.vertical_anchor = 4

    alignment_map = {'left': PP_ALIGN.LEFT, 'center': PP_ALIGN.CENTER, 'right': PP_ALIGN.RIGHT}
    p = tf.paragraphs[0]
    p.alignment = alignment_map.get(align, PP_ALIGN.LEFT)

    # 行高
    if leading is not None:
        p.line_spacing = leading

    run = p.add_run()
    run.text = text.upper() if uppercase else text

    size_pt = font_size if font_size is not None else pack.typography.body
    run.font.size = Pt(size_pt)
    run.font.bold = resolve_weight(weight)
    run.font.name = font or pack.typography.display_font
    if color is not None:
        run.font.color.rgb = color
    else:
        run.font.color.rgb = pack.palette.rgb(color_key)

    # 字距
    if tracking is not None and tracking != 0:
        _set_run_spacing(run, tracking, size_pt)

    return tb


# ============================================================
# 形状（矩形 / 圆角矩形 / 椭圆 / 直线）
# ============================================================

def add_rect(slide, pack: StylePack,
             left, top, width, height,
             *, fill_key='bg_elevated', fill=None,
             stroke_key=None, stroke=None, stroke_width=0.0,
             radius=None):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius and radius > 0 else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(
        shape_type, Inches(left), Inches(top), Inches(width), Inches(height),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill if fill is not None else pack.palette.rgb(fill_key)
    if stroke is not None or stroke_key is not None:
        shape.line.color.rgb = stroke if stroke is not None else pack.palette.rgb(stroke_key)
        shape.line.width = Pt(stroke_width)
    else:
        shape.line.fill.background()
    return shape


def add_oval(slide, pack: StylePack, left, top, width, height,
             *, fill_key='accent', fill=None, stroke_width=0.0):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(left), Inches(top), Inches(width), Inches(height),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill if fill is not None else pack.palette.rgb(fill_key)
    shape.line.fill.background()
    return shape


def add_hline(slide, pack: StylePack, left, top, width,
              *, color_key='divider', color=None, thickness=0.008):
    ln = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(thickness),
    )
    ln.fill.solid()
    ln.fill.fore_color.rgb = color if color is not None else pack.palette.rgb(color_key)
    ln.line.fill.background()
    return ln


# ============================================================
# 卡片（带描边 / 假阴影 / 圆角 — 按 pack.elevation）
# ============================================================

def add_card(slide, pack: StylePack, left, top, width, height, *, fill=None):
    """按 pack.elevation 的语言绘制卡片。"""
    elev = pack.elevation
    # 假阴影（先画）
    if elev.use_fake_shadow:
        shadow = add_rect(
            slide, pack,
            left, top + elev.shadow_offset_y, width, height,
            fill=hex_to_rgb(elev.shadow_color.rstrip('00') or '#E5E5EA'),
            radius=elev.card_radius,
        )

    # 主卡片
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if elev.card_radius > 0 else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(
        shape_type, Inches(left), Inches(top), Inches(width), Inches(height),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill if fill is not None else hex_to_rgb(elev.card_fill)
    if elev.card_stroke_width > 0:
        shape.line.color.rgb = hex_to_rgb(elev.card_stroke_color)
        shape.line.width = Pt(elev.card_stroke_width)
    else:
        shape.line.fill.background()
    return shape


# ============================================================
# 图片（带占位符兜底）
# ============================================================

def add_image(slide, pack: StylePack, image_path,
              left, top, width, height, *, rounded=False):
    """插图。image_path 可以是 None → 绘占位方块。"""
    if image_path:
        try:
            return slide.shapes.add_picture(
                image_path, Inches(left), Inches(top),
                Inches(width), Inches(height),
            )
        except Exception:
            pass
    # 占位方块
    radius = pack.elevation.card_radius if rounded else 0
    return add_rect(
        slide, pack, left, top, width, height,
        fill_key='bg_subtle', radius=radius,
    )


# ============================================================
# 标题块（页面标题 + 英文副标题 + accent bar）
# ============================================================

def add_page_header(slide, pack: StylePack, title: str, en_sub: str = ''):
    """标准页头：左上角标题 + 英文副标题 + 可选分隔线。"""
    dec = pack.decoration
    t = pack.typography
    sp = pack.spacing
    W = pack.canvas.width

    y = 0.5

    # 英文副标题（如果是 'above' 位置）
    if en_sub and dec.page_en_sub_position == 'above':
        sub = en_sub.upper() if t.uppercase_en_sub else en_sub
        add_text(slide, pack, sub,
                 left=sp.margin_x, top=y, width=W - 2 * sp.margin_x, height=0.35,
                 font=pack.typography.body_font,
                 font_size=t.page_sub, weight='medium',
                 color_key='accent', align=dec.page_title_align,
                 tracking=0.15 if t.uppercase_en_sub else 0.02)
        y += 0.45

    # accent bar
    if dec.page_accent_bar:
        add_rect(slide, pack,
                 left=sp.margin_x, top=y + 0.05, width=0.08, height=0.55,
                 fill_key='accent')
        title_left = sp.margin_x + 0.25
    else:
        title_left = sp.margin_x

    # 主标题
    add_text(slide, pack, title,
             left=title_left, top=y,
             width=W - title_left - sp.margin_x, height=0.8,
             font_size=t.page_title, weight=t.page_weight,
             color_key='text_primary', align=dec.page_title_align,
             tracking=t.page_tracking)
    y += 0.75

    # 英文副标题（如果是 'under' 位置）
    if en_sub and dec.page_en_sub_position == 'under':
        sub = en_sub.upper() if t.uppercase_en_sub else en_sub
        add_text(slide, pack, sub,
                 left=sp.margin_x, top=y, width=W - 2 * sp.margin_x, height=0.35,
                 font=pack.typography.body_font,
                 font_size=t.page_sub, weight='regular',
                 color_key='text_tertiary', align=dec.page_title_align,
                 tracking=0.12 if t.uppercase_en_sub else 0.01)
        y += 0.4

    # 底部细分隔线（有些风格会画，有些不画）
    if pack.name.startswith('apple') or pack.name == 'jobs-dark':
        pass  # Apple 不画横线
    else:
        add_hline(slide, pack, sp.margin_x, y + 0.1, W - 2 * sp.margin_x)

    return y + 0.25


# ============================================================
# 页脚
# ============================================================

def add_page_footer(slide, pack: StylePack, company: str, page_no: int):
    if not pack.show_footer:
        return
    t = pack.typography
    sp = pack.spacing
    W = pack.canvas.width
    H = pack.canvas.height

    add_text(slide, pack, company,
             left=sp.margin_x, top=H - 0.42, width=6, height=0.3,
             font=t.body_font, font_size=t.page_number,
             color_key='text_tertiary')
    add_text(slide, pack, f'{page_no:02d}',
             left=W - sp.margin_x - 0.8, top=H - 0.42, width=0.8, height=0.3,
             font=t.body_font, font_size=t.page_number,
             color_key='text_tertiary', align='right')
