"""
styles.py - 可复用的 PPT 风格预设

提供两套开箱即用的风格：
- JOBS_DARK  乔布斯极简暗蓝（原 v1.x 默认）
- XIAOHONGSHU 小红书风格（v2.0 新增，暖奶油 + 小红书红）

每套风格集中定义配色、字体、字号、卡片圆角/描边、封面副标题样式等。
`create-pptx.py` 和 `pptx_toolkit.py` 按风格参数化渲染。
"""

from dataclasses import dataclass, field
from typing import Tuple

from pptx.dml.color import RGBColor


def rgb(hex_str: str) -> RGBColor:
    """#RRGGBB → RGBColor"""
    s = hex_str.lstrip('#')
    return RGBColor(int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


@dataclass
class Style:
    """PPT 风格规格。所有尺寸单位为英寸（Inches），字号单位为 Pt。"""

    name: str

    # 画布
    slide_width: float = 13.33
    slide_height: float = 7.5  # 16:9 横版；小红书帖可改 9:16

    # 配色
    bg: RGBColor = field(default_factory=lambda: rgb('#060D1A'))
    card: RGBColor = field(default_factory=lambda: rgb('#0D182A'))
    accent: RGBColor = field(default_factory=lambda: rgb('#FFFFFF'))
    text: RGBColor = field(default_factory=lambda: rgb('#FFFFFF'))
    subtext: RGBColor = field(default_factory=lambda: rgb('#888888'))
    light: RGBColor = field(default_factory=lambda: rgb('#CCCCCC'))
    divider: RGBColor = field(default_factory=lambda: rgb('#333344'))

    # 字体
    font: str = 'PingFang SC'
    font_fallback: str = 'Microsoft YaHei'

    # 字号
    size_cover_title: int = 64
    size_cover_subtitle: int = 26
    size_cover_footnote: int = 14
    size_page_title: int = 28
    size_page_subtitle_en: int = 10
    size_card_title: int = 14
    size_body: int = 11
    size_small: int = 10
    size_footer: int = 9

    # 卡片
    card_line_width: float = 0.5
    card_stroke: RGBColor = field(default_factory=lambda: rgb('#333344'))

    # 封面是否加装饰（小红书风格会开）
    cover_decoration: bool = False

    # 页脚
    show_footer: bool = True
    footer_company_font_size: int = 9

    # 英文副标题是否大写
    upper_en_subtitle: bool = True


JOBS_DARK = Style(
    name='jobs-dark',
    bg=rgb('#060D1A'),
    card=rgb('#0D182A'),
    accent=rgb('#FFFFFF'),
    text=rgb('#FFFFFF'),
    subtext=rgb('#888888'),
    light=rgb('#CCCCCC'),
    divider=rgb('#333344'),
    card_stroke=rgb('#333344'),
)


XIAOHONGSHU = Style(
    name='xiaohongshu',
    # 暖奶油背景，小红书帖经典色调
    bg=rgb('#FFF8F3'),
    card=rgb('#FFFFFF'),
    accent=rgb('#FF2442'),        # 小红书红
    text=rgb('#1A1A1A'),          # 深黑
    subtext=rgb('#8A8A8A'),       # 中灰
    light=rgb('#4A4A4A'),         # 深灰
    divider=rgb('#F2E6E6'),       # 淡粉分隔
    card_stroke=rgb('#F5E6E6'),
    card_line_width=0.75,
    # 稍小字号，避免在暖底上显得笨重
    size_cover_title=60,
    size_cover_subtitle=24,
    size_page_title=30,
    size_card_title=16,
    size_body=12,
    cover_decoration=True,
    upper_en_subtitle=False,
)


XIAOHONGSHU_PORTRAIT = Style(
    name='xiaohongshu-portrait',
    # 9:16 适合直接导出图片发 Feed
    slide_width=7.5,
    slide_height=13.33,
    bg=rgb('#FFF8F3'),
    card=rgb('#FFFFFF'),
    accent=rgb('#FF2442'),
    text=rgb('#1A1A1A'),
    subtext=rgb('#8A8A8A'),
    light=rgb('#4A4A4A'),
    divider=rgb('#F2E6E6'),
    card_stroke=rgb('#F5E6E6'),
    card_line_width=0.75,
    size_cover_title=72,
    size_cover_subtitle=28,
    size_page_title=36,
    size_card_title=18,
    size_body=14,
    cover_decoration=True,
    upper_en_subtitle=False,
)


REGISTRY = {
    'jobs': JOBS_DARK,
    'jobs-dark': JOBS_DARK,
    'xiaohongshu': XIAOHONGSHU,
    'xhs': XIAOHONGSHU,
    '小红书': XIAOHONGSHU,
    'xiaohongshu-portrait': XIAOHONGSHU_PORTRAIT,
    'xhs-portrait': XIAOHONGSHU_PORTRAIT,
    '小红书竖版': XIAOHONGSHU_PORTRAIT,
}


def get_style(name: str) -> Style:
    """按名字查风格；未知名称回落到 jobs-dark。"""
    if name in REGISTRY:
        return REGISTRY[name]
    # 大小写/空白容忍
    key = name.strip().lower()
    if key in REGISTRY:
        return REGISTRY[key]
    return JOBS_DARK


def list_styles() -> Tuple[str, ...]:
    """返回主要风格名（用于 CLI --help）。"""
    return ('jobs-dark', 'xiaohongshu', 'xiaohongshu-portrait')
