"""
style_packs.py - 火一五 PPT v3.0 的 4 个真·审美方案

每个 pack 是完整的 StylePack（Palette + Typography + Spacing + Elevation + Decoration）。

对标：
  apple-keynote       - Apple 发布会（纯黑 + SF Pro + 巨字号）
  apple-light         - Apple.com 产品页（纯白 + 磨砂卡 + 极简）
  xiaohongshu-creator - 真·生活博主（奶油 + 鼠尾草 + 焦糖 / 衬线字）
  xiaohongshu-vintage - 博主复古胶片系（琥珀 + 雾霾蓝 / 衬线字）

附带 5 个 legacy pack 保持向后兼容：jobs-dark / xiaohongshu / xhs-portrait / modern / classic。
"""

from __future__ import annotations

from design_system import (
    StylePack, Palette, Typography, Spacing, Elevation, Decoration, Canvas,
)


# ============================================================
# 一、Apple Keynote（真·发布会暗场）
# ============================================================

APPLE_KEYNOTE = StylePack(
    name='apple-keynote',
    display_name='Apple 发布会（暗场）',
    tagline='纯黑 + SF Pro + 巨字号 + 极致留白',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        # Apple 发布会是纯黑而非蓝黑
        bg='#000000',
        bg_elevated='#1C1C1E',
        bg_subtle='#2C2C2E',
        # 文字白色渐变
        text_primary='#F5F5F7',
        text_secondary='#A1A1A6',
        text_tertiary='#86868B',
        text_muted='#48484A',
        # 品牌蓝
        accent='#0A84FF',
        accent_soft='#0A84FF',
        border='#2C2C2E',
        divider='#1C1C1E',
    ),

    typography=Typography(
        display_font='SF Pro Display',
        body_font='SF Pro Text',
        # Apple 发布会级字号
        hero=160,            # 巨字号
        section=96,
        page_title=48,
        page_sub=16,
        card_title=22,
        body=15,
        caption=11,
        page_number=9,
        hero_weight='bold',
        section_weight='bold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=-0.03,      # 巨字要收字距
        section_tracking=-0.02,
        page_tracking=-0.01,
        hero_leading=0.95,
        body_leading=1.4,
        uppercase_en_sub=True,    # OVERVIEW / INTRO
    ),

    spacing=Spacing(
        gutter=0.08,
        stack_sm=0.17,
        stack_md=0.33,
        stack_lg=0.66,
        stack_xl=1.33,
        margin_x=0.8,
        margin_x_hero=1.2,
        card_pad_x=0.33,
        card_pad_y=0.25,
    ),

    elevation=Elevation(
        card_radius=0.12,
        card_stroke_width=0.0,      # 无描边
        card_stroke_color='#2C2C2E',
        card_fill='#1C1C1E',
        use_fake_shadow=False,
        style='flat',
    ),

    decoration=Decoration(
        cover_hero_align='center',
        cover_hero_case='as-is',
        cover_bottom_line=False,
        cover_top_line=False,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='under',
        tag_style='none',
        stat_hero_size=280,          # Apple 的 "2 Billion" 页
        stat_hero_weight='bold',
        image_treatment='full',
    ),
    show_footer=False,               # Apple 不显示页脚
)


# ============================================================
# 二、Apple Light（Apple.com 产品页）
# ============================================================

APPLE_LIGHT = StylePack(
    name='apple-light',
    display_name='Apple.com（白场）',
    tagline='纯白 + 磨砂卡 + 极简克制',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#FFFFFF',
        bg_elevated='#F5F5F7',      # Apple.com 的经典卡片灰
        bg_subtle='#FBFBFD',
        text_primary='#1D1D1F',
        text_secondary='#424245',
        text_tertiary='#6E6E73',
        text_muted='#D2D2D7',
        accent='#0071E3',           # Apple.com 的链接蓝
        accent_soft='#E6F0FD',
        border='#D2D2D7',
        divider='#F5F5F7',
    ),

    typography=Typography(
        display_font='SF Pro Display',
        body_font='SF Pro Text',
        hero=120,
        section=72,
        page_title=44,
        page_sub=15,
        card_title=21,
        body=15,
        caption=11,
        page_number=10,
        hero_tracking=-0.025,
        section_tracking=-0.02,
        page_tracking=-0.01,
        hero_leading=1.0,
        body_leading=1.45,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        margin_x=0.8,
        margin_x_hero=1.0,
    ),

    elevation=Elevation(
        card_radius=0.18,           # 圆角更圆
        card_stroke_width=0.0,      # 无描边，靠填色区分
        card_stroke_color='#D2D2D7',
        card_fill='#F5F5F7',
        use_fake_shadow=False,
        style='soft',
    ),

    decoration=Decoration(
        cover_hero_align='center',
        stat_hero_size=200,
        image_treatment='rounded',
    ),
    show_footer=True,
)


# ============================================================
# 三、小红书博主风（奶油 + 鼠尾草 + 焦糖）
# ============================================================

XHS_CREATOR = StylePack(
    name='xiaohongshu-creator',
    display_name='小红书博主（奶油生活系）',
    tagline='奶油 + 鼠尾草 + 焦糖咖 + 衬线字',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        # 博主风是奶油底 + 低饱和
        bg='#FBF7F0',               # 奶油主背
        bg_elevated='#FFFFFF',      # 纯白卡片
        bg_subtle='#F5F1EA',        # 次奶油
        # 文字不用纯黑，用焦糖咖色
        text_primary='#3E2E1F',     # 焦糖咖替代黑
        text_secondary='#8B6F47',   # 奶茶咖
        text_tertiary='#B3A28A',    # 浅咖
        text_muted='#D4C8B8',
        # 鼠尾草绿作为点缀主色
        accent='#9FAE8B',           # 鼠尾草
        accent_soft='#E6EAD9',
        border='#E8DFD0',
        divider='#F0E8D9',
    ),

    typography=Typography(
        # 博主风关键：衬线字体！
        display_font='Noto Serif SC',
        display_fallbacks=[
            'Source Han Serif SC', 'Songti SC',
            'STSong', 'SimSun', 'serif',
        ],
        body_font='PingFang SC',
        body_fallbacks=[
            'Noto Sans CJK SC', 'Microsoft YaHei', 'sans-serif',
        ],
        hero=72,                    # 博主风不需要 Apple 那种巨字
        section=52,
        page_title=32,
        page_sub=14,
        card_title=18,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='semibold',     # 衬线字体 semibold 足够
        section_weight='semibold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=0.02,         # 衬线字要放一点字距
        section_tracking=0.01,
        page_tracking=0.01,
        hero_leading=1.15,
        body_leading=1.6,           # 衬线字需要更大行高
        uppercase_en_sub=False,     # 博主风英文不全大写
    ),

    spacing=Spacing(
        margin_x=0.7,
        margin_x_hero=1.0,
        stack_md=0.4,               # 段落间距更大，呼吸感
        stack_lg=0.8,
    ),

    elevation=Elevation(
        card_radius=0.22,           # 圆润
        card_stroke_width=0.75,
        card_stroke_color='#E8DFD0',
        card_fill='#FFFFFF',
        use_fake_shadow=True,       # 微微阴影
        shadow_color='#E8DFD0',
        shadow_offset_y=0.06,
        style='soft',
    ),

    decoration=Decoration(
        cover_hero_align='left',    # 博主封面常左对齐
        cover_bottom_line=False,
        page_title_align='left',
        page_accent_bar=True,       # 标题左侧小竖条
        page_en_sub_position='above',
        tag_style='pill',
        stat_hero_size=140,
        image_treatment='rounded',
    ),
    show_footer=True,
)


# ============================================================
# 四、小红书复古胶片（琥珀 + 雾霾蓝）
# ============================================================

XHS_VINTAGE = StylePack(
    name='xiaohongshu-vintage',
    display_name='小红书博主（复古胶片）',
    tagline='琥珀 + 雾霾蓝 + 衬线字 + 胶片质感',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#F2EAD9',               # 复古米
        bg_elevated='#FFFAF1',      # 象牙白
        bg_subtle='#E8D0CD',        # 琥珀粉
        text_primary='#4A3526',     # 深栗咖
        text_secondary='#7A5C42',
        text_tertiary='#A88B6D',
        text_muted='#C9B195',
        # 雾霾蓝点缀
        accent='#A8B8C6',           # 雾霾蓝
        accent_soft='#D6DFE8',
        border='#D9C8A8',
        divider='#E8D7B5',
    ),

    typography=Typography(
        display_font='Noto Serif SC',
        display_fallbacks=[
            'Source Han Serif SC', 'Songti SC',
            'STSong', 'serif',
        ],
        body_font='Noto Serif SC',   # 胶片风全衬线
        body_fallbacks=[
            'Source Han Serif SC', 'Songti SC', 'serif',
        ],
        hero=64,
        section=46,
        page_title=30,
        page_sub=13,
        card_title=17,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='semibold',
        section_weight='semibold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=0.03,           # 复古字距更松
        section_tracking=0.02,
        page_tracking=0.01,
        hero_leading=1.2,
        body_leading=1.65,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        margin_x=0.75,
        margin_x_hero=1.0,
        stack_md=0.4,
        stack_lg=0.8,
    ),

    elevation=Elevation(
        card_radius=0.08,            # 复古卡片角不要太圆
        card_stroke_width=1.0,
        card_stroke_color='#D9C8A8',
        card_fill='#FFFAF1',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_top_line=True,
        cover_bottom_line=True,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='underline',
        stat_hero_size=110,
        image_treatment='film',
    ),
    show_footer=True,
)


# ============================================================
# 五、Legacy packs（向后兼容老的 v2.x）
# ============================================================

JOBS_DARK = StylePack(
    name='jobs-dark',
    display_name='乔布斯极简暗蓝（v1.x 默认）',
    tagline='深蓝暗底 + 白灰克制',

    palette=Palette(
        bg='#060D1A',
        bg_elevated='#0D182A',
        bg_subtle='#14243D',
        text_primary='#FFFFFF',
        text_secondary='#CCCCCC',
        text_tertiary='#888888',
        text_muted='#444455',
        accent='#FFFFFF',
        border='#333344',
        divider='#333344',
    ),
    typography=Typography(
        hero=64, section=48, page_title=28, page_sub=10,
        card_title=14, body=11, caption=10, page_number=9,
        uppercase_en_sub=True,
    ),
    elevation=Elevation(
        card_stroke_width=0.5,
        card_stroke_color='#333344',
        card_fill='#0D182A',
    ),
    decoration=Decoration(),
    show_footer=True,
)


XIAOHONGSHU_BRAND = StylePack(
    name='xiaohongshu',
    display_name='小红书品牌风（v2.x 默认）',
    tagline='小红书红 + 暖奶油',

    palette=Palette(
        bg='#FFF8F3',
        bg_elevated='#FFFFFF',
        bg_subtle='#F5E6E6',
        text_primary='#1A1A1A',
        text_secondary='#4A4A4A',
        text_tertiary='#8A8A8A',
        text_muted='#C8C8C8',
        accent='#FF2442',
        accent_soft='#FFE5EC',
        border='#F5E6E6',
        divider='#F2E6E6',
    ),
    typography=Typography(
        hero=60, section=48, page_title=30, page_sub=12,
        card_title=16, body=12, caption=10, page_number=9,
        uppercase_en_sub=False,
    ),
    elevation=Elevation(
        card_stroke_width=0.75,
        card_stroke_color='#F5E6E6',
        card_fill='#FFFFFF',
    ),
    decoration=Decoration(
        cover_top_line=True,
        page_accent_bar=True,
        tag_style='pill',
    ),
    show_footer=True,
)


XIAOHONGSHU_PORTRAIT = StylePack(
    name='xiaohongshu-portrait',
    display_name='小红书品牌风 · 竖版 9:16',
    tagline='直接发帖用的竖版',

    canvas=Canvas(width=7.5, height=13.33),
    palette=XIAOHONGSHU_BRAND.palette,
    typography=Typography(
        hero=72, section=56, page_title=36, page_sub=13,
        card_title=18, body=14, caption=11, page_number=10,
        uppercase_en_sub=False,
    ),
    elevation=XIAOHONGSHU_BRAND.elevation,
    decoration=XIAOHONGSHU_BRAND.decoration,
    show_footer=True,
)


# ============================================================
# 六、注册表
# ============================================================

REGISTRY = {
    # v3.0 审美 pack
    'apple-keynote': APPLE_KEYNOTE,
    'apple-dark': APPLE_KEYNOTE,
    'apple': APPLE_KEYNOTE,
    '苹果': APPLE_KEYNOTE,
    '苹果发布会': APPLE_KEYNOTE,
    '发布会': APPLE_KEYNOTE,

    'apple-light': APPLE_LIGHT,
    'apple-white': APPLE_LIGHT,
    '苹果白': APPLE_LIGHT,
    '苹果官网': APPLE_LIGHT,

    'xiaohongshu-creator': XHS_CREATOR,
    'xhs-creator': XHS_CREATOR,
    '博主风': XHS_CREATOR,
    '生活博主': XHS_CREATOR,
    '博主': XHS_CREATOR,
    '奶油博主': XHS_CREATOR,

    'xiaohongshu-vintage': XHS_VINTAGE,
    'xhs-vintage': XHS_VINTAGE,
    '复古': XHS_VINTAGE,
    '胶片': XHS_VINTAGE,
    '复古胶片': XHS_VINTAGE,

    # Legacy packs
    'jobs-dark': JOBS_DARK,
    'jobs': JOBS_DARK,
    '乔布斯': JOBS_DARK,

    'xiaohongshu': XIAOHONGSHU_BRAND,
    'xhs': XIAOHONGSHU_BRAND,
    '小红书': XIAOHONGSHU_BRAND,

    'xiaohongshu-portrait': XIAOHONGSHU_PORTRAIT,
    'xhs-portrait': XIAOHONGSHU_PORTRAIT,
    '小红书竖版': XIAOHONGSHU_PORTRAIT,
}


def get_pack(name: str) -> StylePack:
    if not name:
        return APPLE_KEYNOTE
    key = name.strip().lower()
    if key in REGISTRY:
        return REGISTRY[key]
    if name in REGISTRY:
        return REGISTRY[name]
    return APPLE_KEYNOTE


def list_packs():
    """主要 pack 名，供 --help 展示。"""
    return (
        'apple-keynote',
        'apple-light',
        'xiaohongshu-creator',
        'xiaohongshu-vintage',
        'jobs-dark',
        'xiaohongshu',
        'xiaohongshu-portrait',
    )
