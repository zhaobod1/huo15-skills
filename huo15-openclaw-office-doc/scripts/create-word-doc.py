#!/usr/bin/env python3
"""
create-word-doc.py - 企业级 Word 文档生成器 v5.3（多规范 + 本地公司信息）

支持多文档规范自动识别：
- 公文格式（GB/T 9704-2012）- 默认
- 合同格式
- 会议纪要格式
- 技术方案格式
- 需求文档格式
- 工作报告格式

公司信息按以下优先级解析：
  1. CLI 显式参数 --company-name / --logo-path
  2. ~/.huo15/company-info.json（本地缓存）
  3. Odoo res.company（可选回落，可用 --no-odoo 关闭）
缺少 company_name 或 logo_path 时以退出码 2 + stderr JSON 提示调用方补录。

用法（推荐）：
    python create-word-doc.py --output 文档.docx --title '标题' --content '...'
兼容旧位置参数：
    python create-word-doc.py <输出路径> [标题] [正文] [编号] [版本] [密级] [格式]
"""

import sys
import os
import re
import json
import argparse
import datetime
import importlib.util
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============== 文档格式预设 ==============
class FormatPreset:
    """文档格式预设"""
    def __init__(self, name, margin_top=3.7, margin_bottom=3.5,
                 margin_left=2.8, margin_right=2.6,
                 font_body='仿宋', font_title='黑体', font_heading='黑体',
                 size_title=22, size_chapter=16, size_section=14, size_body=12,
                 heading_patterns=None, line_spacing=1.5,
                 has_version_history=True, has_approval=True,
                 header_style='company', footer_style='page'):
        self.name = name
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.font_body = font_body
        self.font_title = font_title
        self.font_heading = font_heading
        self.size_title = size_title
        self.size_chapter = size_chapter
        self.size_section = size_section
        self.size_body = size_body
        self.line_spacing = line_spacing
        self.has_version_history = has_version_history
        self.has_approval = has_approval
        self.header_style = header_style
        self.footer_style = footer_style
        # 标题识别模式：[正则, 层级]
        self.heading_patterns = heading_patterns or []

# 预定义格式
PRESET_GONGWEN = FormatPreset(
    name='公文',
    heading_patterns=[
        (r'^第[一二三四五六七八九十百千]+[章节篇款]', 'chapter'),
        (r'^[一二三四五六七八九十百千]+[、．,，]', 'section'),
        (r'^[（\(][一二三四五六七八九十百千]+[）\)]', 'article'),
    ]
)

PRESET_HETONG = FormatPreset(
    name='合同',
    margin_top=2.54, margin_bottom=2.54, margin_left=3.17, margin_right=3.17,
    font_body='宋体', font_title='宋体', font_heading='宋体',
    size_title=22, size_chapter=15, size_section=12, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^第[一二三四五六七八九十百千]+[章节条款]', 'chapter'),
        (r'^[一二三四五六七八九十百千]+[、]', 'section'),
    ],
    has_version_history=False,
    has_approval=True,
    header_style='simple',
    footer_style='page'
)

PRESET_HUIYI = FormatPreset(
    name='会议纪要',
    font_body='仿宋', font_title='方正小标宋简体', font_heading='黑体',
    size_title=22, size_chapter=14, size_section=12, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^【[^】]+】', 'chapter'),
        (r'^[一二三四五六七八九十]+[、]', 'section'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'article'),
    ],
    has_version_history=False,
    has_approval=False,
    header_style='company',
    footer_style='page'
)

PRESET_FANGAN = FormatPreset(
    name='技术方案',
    font_body='宋体', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[．、]', 'chapter'),
        (r'^[0-9]+[．、]', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    header_style='company',
    footer_style='page'
)

PRESET_XUQIU = FormatPreset(
    name='需求文档',
    font_body='宋体', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[．、]', 'chapter'),
        (r'^[0-9]+[．、]', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    header_style='company',
    footer_style='page'
)

PRESET_GONGZUO = FormatPreset(
    name='工作报告',
    font_body='仿宋', font_title='方正小标宋简体', font_heading='楷体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'section'),
    ],
    has_version_history=False,
    has_approval=True,
    header_style='company',
    footer_style='page'
)

# 格式注册表
FORMAT_PRESETS = {
    '公文': PRESET_GONGWEN,
    '合同': PRESET_HETONG,
    '会议纪要': PRESET_HUIYI,
    '技术方案': PRESET_FANGAN,
    '需求文档': PRESET_XUQIU,
    '工作报告': PRESET_GONGZUO,
}

# 识别关键词
FORMAT_KEYWORDS = {
    '合同': ['合同', '协议', '协议书'],
    '会议纪要': ['会议纪要', '纪要'],
    '技术方案': ['技术方案', '实施方案', '解决方案', '设计文档'],
    '需求文档': ['需求', '需求规格', '需求说明', 'SRS'],
    '工作报告': ['工作报告', '周报', '月报', '季报', '年报', '述职报告'],
}

# ============== 公司信息 ==============
# 从同目录的 company-info.py 导入（文件名含 '-'，需要用 importlib 加载）
_CI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'company-info.py')
_ci_spec = importlib.util.spec_from_file_location('company_info', _CI_PATH)
_ci_module = importlib.util.module_from_spec(_ci_spec)
_ci_spec.loader.exec_module(_ci_module)

# 首行缩进
FIRST_LINE_INDENT = Cm(0.74)


def resolve_company_info(overrides=None, use_odoo=True):
    """按优先级返回公司信息字典。

    优先级：overrides(CLI) > ~/.huo15/company-info.json > Odoo > {}
    返回字典含 company_name / logo_path / slogan 等；字段缺失由调用方处理。
    """
    info = _ci_module.resolve(use_odoo=use_odoo)
    if overrides:
        for key, value in overrides.items():
            if value:
                info[key] = value
    return info


def company_info_missing(info):
    """返回必填但缺失的字段列表。"""
    missing = [k for k in _ci_module.REQUIRED_FIELDS if not info.get(k)]
    if info.get('logo_path') and not _ci_module.logo_is_valid(info.get('logo_path')):
        if 'logo_path' not in missing:
            missing.append('logo_path')
    return missing


def detect_format(title='', content=''):
    """根据标题和内容自动检测文档格式"""
    text = (title + ' ' + (content or '')[:500]).lower()

    for fmt, keywords in FORMAT_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                return fmt

    # 默认公文格式
    return '公文'


def get_preset(format_name):
    """获取格式预设"""
    return FORMAT_PRESETS.get(format_name, PRESET_GONGWEN)


# ============== 字体工具 ==============

def _set_font(run, font_name, size, bold=False, color=None):
    """设置中文字体（WPS/Word 双兼容）"""
    run.font.name = font_name
    rPr = run._element.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        run._element.insert(0, rPr)
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = color


def _add_border_bottom(paragraph):
    """给段落下方加细线"""
    pPr = paragraph._element.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        paragraph._element.insert(0, pPr)
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '000000')
    pBdr.append(bottom)
    pPr.append(pBdr)


def _set_cell_shading(cell, fill_color):
    """设置单元格背景色"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    tcPr.append(shd)


# ============== 页眉页脚 ==============

def add_header(doc, preset, logo_path, company_name, doc_number=None, classification=None, title=''):
    """添加页眉"""
    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False

    for p in header.paragraphs:
        for r in p.runs:
            r.text = ''
    para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    style = preset.header_style
    size = preset.size_body - 2

    if style == 'company':
        # 公文式：LOGO + 公司名 + 文档编号 + 密级
        if logo_path and os.path.exists(logo_path):
            try:
                run = para.add_run()
                run.add_picture(logo_path, height=Cm(1.0))
            except Exception as e:
                print(f"⚠ LOGO 添加失败: {e}")
        run = para.add_run(f' {company_name}')
        _set_font(run, '黑体', size)
        if doc_number:
            run = para.add_run(f'  {doc_number}')
            _set_font(run, '黑体', size)
        if classification:
            run = para.add_run(f'  【{classification}】')
            _set_font(run, '黑体', size, bold=True)
        _add_border_bottom(para)

    elif style == 'simple':
        # 合同式：仅公司名，居中
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(company_name)
        _set_font(run, '宋体', size)
        _add_border_bottom(para)

    elif style == 'title_only':
        # 纪要式：仅标题
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if title:
            run = para.add_run(title)
            _set_font(run, '黑体', size)


def add_footer(doc, preset):
    """添加页脚"""
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False

    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for r in para.runs:
        r.text = ''

    def add_text(text):
        r = para.add_run(text)
        _set_font(r, preset.font_body, preset.size_body - 2)
        return r

    def add_field(name):
        r = para.add_run()
        fc1 = OxmlElement('w:fldChar')
        fc1.set(qn('w:fldCharType'), 'begin')
        it = OxmlElement('w:instrText')
        it.set(qn('xml:space'), 'preserve')
        it.text = f' {name} '
        fc2 = OxmlElement('w:fldChar')
        fc2.set(qn('w:fldCharType'), 'end')
        r._element.clear()
        r._element.append(fc1)
        r._element.append(it)
        r._element.append(fc2)
        _set_font(r, preset.font_body, preset.size_body - 2)

    if preset.footer_style == 'page':
        add_text('第 ')
        add_field('PAGE')
        add_text(' 页 / 共 ')
        add_field('NUMPAGES')
        add_text(' 页')


# ============== 段落样式 ==============

class ParagraphStyle:
    def __init__(self, font, size, bold=False, indent=True,
                 alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                 space_before=0, space_after=6, line_spacing=1.5):
        self.font = font
        self.size = size
        self.bold = bold
        self.indent = indent
        self.alignment = alignment
        self.space_before = space_before
        self.space_after = space_after
        self.line_spacing = line_spacing

    def apply(self, p):
        p.alignment = self.alignment
        p.paragraph_format.line_spacing = self.line_spacing
        p.paragraph_format.space_before = Pt(self.space_before)
        p.paragraph_format.space_after = Pt(self.space_after)
        if self.indent:
            p.paragraph_format.first_line_indent = FIRST_LINE_INDENT
        else:
            p.paragraph_format.first_line_indent = Cm(0)


def get_styles(preset):
    """获取格式对应的段落样式"""
    return {
        'chapter': ParagraphStyle(
            preset.font_heading, preset.size_chapter, bold=True,
            indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
            space_before=18, space_after=6, line_spacing=preset.line_spacing
        ),
        'section': ParagraphStyle(
            preset.font_heading, preset.size_section, bold=True,
            indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
            space_before=12, space_after=4, line_spacing=preset.line_spacing
        ),
        'article': ParagraphStyle(
            preset.font_heading, preset.size_body, bold=True,
            indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
            space_before=6, space_after=3, line_spacing=preset.line_spacing
        ),
        'body': ParagraphStyle(
            preset.font_body, preset.size_body, bold=False,
            indent=True, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
            space_before=0, space_after=6, line_spacing=preset.line_spacing
        ),
        'empty': ParagraphStyle(
            preset.font_body, preset.size_body, bold=False,
            indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
            space_before=0, space_after=0, line_spacing=preset.line_spacing
        ),
        'list': ParagraphStyle(
            preset.font_body, preset.size_body, bold=False,
            indent=False, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
            space_before=0, space_after=4, line_spacing=preset.line_spacing
        ),
    }


def parse_inline_markdown(text, default_font, default_size, default_bold):
    """解析内联 Markdown 语法（**加粗**、*斜体*），返回 runs 列表
    
    每个 run 是 (text, font, size, bold) 元组。
    使用非捕获组匹配标记，仅捕获内容。
    """
    runs = []
    # 匹配 **bold** 或 *italic*，使用非捕获组，捕获内容
    pattern = re.compile(r'(?:\*\*([^*]+?)\*\*|\*([^*]+?)\*)')
    last_end = 0
    for match in pattern.finditer(text):
        # 先处理匹配之前的纯文本
        if match.start() > last_end:
            plain = text[last_end:match.start()]
            if plain:
                runs.append((plain, default_font, default_size, default_bold))
        # 提取加粗或斜体内容
        bold_content = match.group(1)
        italic_content = match.group(2)
        if bold_content is not None:
            runs.append((bold_content, default_font, default_size, True))
        elif italic_content is not None:
            runs.append((italic_content, default_font, default_size, default_bold))
        last_end = match.end()
    # 处理剩余文本
    if last_end < len(text):
        plain = text[last_end:]
        if plain:
            runs.append((plain, default_font, default_size, default_bold))
    return runs if runs else [(text, default_font, default_size, default_bold)]


def add_paragraph(doc, text, style):
    """添加段落并应用样式"""
    p = doc.add_paragraph()
    style.apply(p)
    if text:
        runs = parse_inline_markdown(text, style.font, style.size, style.bold)
        for run_text, run_font, run_size, run_bold in runs:
            run = p.add_run(run_text)
            _set_font(run, run_font, run_size, run_bold)
    return p


def add_empty_line(doc):
    """添加空行"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0


# ============== 内容解析 ==============

def detect_paragraph_type(text, preset):
    """检测段落类型"""
    if not text or not text.strip():
        return 'blank', ''

    t = text.strip()

    # 支持标准 Markdown 标题 (# 后面有或没有空格)
    md_heading_match = re.match(r'^(#{1,6})\s*(.+)$', t)
    if md_heading_match:
        level = len(md_heading_match.group(1))
        title_text = md_heading_match.group(2).strip()
        if level == 1:
            return 'chapter', title_text
        elif level == 2:
            return 'section', title_text
        else:
            return 'article', title_text

    for pattern, ptype in preset.heading_patterns:
        if re.match(pattern, t):
            # chapter 类型保留完整文本（【标题】格式需要保留括号）
            # section/article 类型去掉前缀
            if ptype == 'chapter':
                return ptype, t
            cleaned = re.sub(pattern, '', t).strip()
            return ptype, cleaned

    # 支持 Markdown 无序列表（- item 或 * item）
    list_match = re.match(r'^[-*]\s+(.+)$', t)
    if list_match:
        return 'list', list_match.group(1)

    return 'body', t


def is_metadata_row(line):
    """判断是否是元数据行（文档编号、版本、密级等）
    
    识别格式：
    - 文档编号：XXX  |  版本：V1.0  |  密级：内部  |  日期：2026-04-22
    - 文档编号：XXX | 版本：V1.0 | 密级：内部
    """
    t = line.strip()
    if not t:
        return False
    
    # 必须包含"文档编号"
    if '文档编号' not in t:
        return False
    
    # 计算 | 的数量（至少2个表示多列）
    if t.startswith('|'):
        t = t.strip('|')
    pipe_count = t.count('|')
    
    # 至少有2个 | 分隔符
    return pipe_count >= 2


def parse_metadata_row(line):
    """解析元数据行，返回键值对列表"""
    t = line.strip()
    
    # 去掉首尾的 |
    if t.startswith('|') and t.endswith('|'):
        t = t[1:-1]
    elif t.startswith('|'):
        t = t[1:]
    elif t.endswith('|'):
        t = t[:-1]
    
    # 按 | 分割
    cells = []
    current = ''
    i = 0
    while i < len(t):
        if t[i] == '|':
            cells.append(current.strip())
            current = ''
            i += 1
        else:
            current += t[i]
            i += 1
    if current:
        cells.append(current.strip())
    
    # 解析每个单元格为 key:value
    result = []
    for cell in cells:
        cell = cell.strip()
        if '：' in cell:
            idx = cell.index('：')
            key = cell[:idx].strip()
            value = cell[idx+1:].strip()
            result.append((key, value))
        elif ':' in cell:
            idx = cell.index(':')
            key = cell[:idx].strip()
            value = cell[idx+1:].strip()
            result.append((key, value))
        else:
            result.append(('', cell))
    
    return result


def is_markdown_table_separator(line):
    """判断是否是 Markdown 表格分隔行
    
    支持格式：
    - |---|---|---|  (标准)
    - | --- | --- | --- |  (带空格)
    - |:---|:---:|---:|  (对齐标记)
    - | :--- | :---: | ---: |  (对齐+空格)
    - ||  (只有分隔符)
    - 混合使用 - − – — 等各种破折号
    - 也支持没有前导 | 的分隔行：---|---|--- (用户粘贴时经常省略)
    """
    # 去掉首尾空格后检查
    t = line.strip()
    if not t:
        return False
    
    # 必须以 | 开头，或完全是破折号（没有前导 | 的分隔行）
    if not t.startswith('|') and not re.match(r'^[\-–—―\s]+$', t):
        return False
    
    # 去掉首尾的 |
    if t.startswith('|'):
        t = t.strip('|')
    
    # 按 | 分割成单元格
    parts = t.split('|')
    
    # 每个部分必须是有效的分隔符（允许对齐标记）
    # 有效模式: "---", ":---", "--::", "---:", ":--:" 等
    # 其中 - 可以是 - − – — ―
    separator_pattern = r'^[:\s]*[\-−–—―]+[:\s]*$'
    
    # 至少要有一个分隔符
    has_separator = False
    
    for part in parts:
        part = part.strip()
        # 跳过空部分（连续 || 产生空cell）
        if not part:
            continue
        if re.match(separator_pattern, part):
            has_separator = True
        else:
            return False
    
    return has_separator


def split_table_row(line):
    r"""智能分割表格行，正确处理转义管道符
    
    支持:
    - 标准单元格: |A|B|C|
    - 带空格的: | A | B | C |
    - 没有前导|的单元格: A|B|C (用户粘贴时常省略)
    - 转义管道符: |A\|B|C| → ["A|B", "C"]
    - 开头结尾有|: ||A|B| → ["A", "B"]
    - 空单元格: |A||C| → ["A", "", "C"]
    """
    # 去掉首尾的 |
    line = line.strip()
    has_leading_pipe = line.startswith('|')
    has_trailing_pipe = line.endswith('|')
    
    if has_leading_pipe and has_trailing_pipe:
        line = line[1:-1]
    elif has_leading_pipe:
        line = line[1:]
    elif has_trailing_pipe:
        line = line[:-1]
    
    # 使用负向后顾来分割，避开转义的 \|
    # 方法：按 | 分隔，但 | 前面有反斜号的跳过
    cells = []
    current = ''
    i = 0
    while i < len(line):
        if line[i] == '\\' and i + 1 < len(line) and line[i + 1] == '|':
            # 转义管道符，保留原始的 | 
            current += '|'
            i += 2
        elif line[i] == '|':
            # 分隔符
            cells.append(current.strip())
            current = ''
            i += 1
        else:
            current += line[i]
            i += 1
    
    # 最后一个单元格
    if current:
        cells.append(current.strip())
    
    return cells


def is_table_row(line):
    """判断一行是否是表格数据行（而非分隔行或普通文本）
    
    判断标准：包含两个或以上的 | 分隔符（表格特征）
    """
    t = line.strip()
    if not t:
        return False
    
    # 如果是分隔行，不是数据行
    if is_markdown_table_separator(t):
        return False
    
    # 计算 | 的数量
    # 有前导 | 时：去掉前后 | 后计算
    # 没有前导 | 时：直接计算
    if t.startswith('|'):
        t = t.strip('|')
    
    pipe_count = t.count('|')
    
    # 至少有2个 | 分隔符（3列或以上）才是表格
    return pipe_count >= 2


def parse_table_lines(lines, start_idx):
    """解析连续表格行
    
    支持两种格式：
    1. 标准 markdown：| 列1 | 列2 | 列3 |
    2. 简化格式：列1 | 列2 | 列3 (用户粘贴时常省略前后 |)
    """
    table_lines = []
    i = start_idx
    while i < len(lines):
        t = lines[i].strip()
        if not t:
            i += 1
            continue
            
        # 是分隔行则跳过
        if is_markdown_table_separator(t):
            i += 1
            continue
        
        # 是表格数据行（有足够多 | 分隔符）则收集
        if is_table_row(t):
            table_lines.append(t)
            i += 1
            continue
        
        # 否则不是表格行，退出
        break
    
    return table_lines, i


def build_table(doc, table_lines):
    """将表格行数据写入 Word 表格"""
    rows_data = []
    for line in table_lines:
        # 使用智能分割
        cells = split_table_row(line)
        if cells:  # 确保不是空行
            rows_data.append(cells)

    if len(rows_data) < 2:
        return

    # 计算最大列数，处理列数不一致的情况
    max_cols = max(len(row) for row in rows_data)
    
    # 补齐列数不一致的行（用空字符串填充）
    normalized_rows = []
    for row in rows_data:
        if len(row) < max_cols:
            row = row + [''] * (max_cols - len(row))
        normalized_rows.append(row)

    table = doc.add_table(rows=len(normalized_rows), cols=max_cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for r, row in enumerate(normalized_rows):
        is_header = (r == 0)
        for c, text in enumerate(row):
            cell = table.rows[r].cells[c]
            cell.text = text
            for para in cell.paragraphs:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                font_name = '宋体' if is_header else '仿宋'
                for run in para.runs:
                    _set_font(run, font_name, 10.5, bold=is_header)
            if is_header:
                _set_cell_shading(cell, 'D9D9D9')

    return table


def parse_content(doc, content, preset):
    """将纯文本内容解析并写入 Word"""
    if not content:
        return

    styles = get_styles(preset)
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        t = line.strip()

        if not t:
            add_empty_line(doc)
            i += 1
            continue

        # 先检测元数据行（文档编号、版本、密级等），优先于表格检测
        if is_metadata_row(t):
            metadata = parse_metadata_row(t)
            if metadata:
                # 转换为两列表格
                table = doc.add_table(rows=len(metadata), cols=2)
                table.style = 'Table Grid'
                for r, (key, value) in enumerate(metadata):
                    row = table.rows[r]
                    row.cells[0].text = key
                    row.cells[1].text = value
                    for cell in row.cells:
                        for para in cell.paragraphs:
                            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                            for run in para.runs:
                                _set_font(run, preset.font_body, preset.size_body - 1)
                add_empty_line(doc)
            i += 1
            continue

        # 检测 Markdown 水平分隔线 (---)
        if re.match(r'^\s*[-−–—―]{3,}\s*$', t):
            add_empty_line(doc)
            i += 1
            continue

        # 使用 is_table_row 检测表格（支持有/无前导 | 的格式）
        if is_table_row(t):
            table_lines, i = parse_table_lines(lines, i)
            build_table(doc, table_lines)
            continue

        ptype, clean_text = detect_paragraph_type(t, preset)

        if ptype == 'blank':
            add_empty_line(doc)
        elif ptype in styles:
            # 统一使用 clean_text（detect_paragraph_type 已处理好）
            add_paragraph(doc, clean_text, styles[ptype])
        else:
            add_paragraph(doc, clean_text, styles['body'])

        i += 1


# ============== 版本历史 & 审批区 ==============

def add_version_history(doc, preset, version='V1.0', date=None, author=None):
    """添加版本历史表"""
    if not preset.has_version_history:
        return

    if not date:
        date = datetime.date.today().strftime('%Y-%m-%d')

    add_empty_line(doc)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run('【版本历史】')
    _set_font(run, preset.font_heading, preset.size_section, bold=True)
    p.paragraph_format.space_after = Pt(6)

    table_data = [
        '| 版本 | 日期 | 作者 | 修改内容 |',
        f'| {version} | {date} | {author or "未知"} | 首次创建 |',
    ]
    build_table(doc, table_data)


def add_approval_block(doc, preset, approval_list=None):
    """添加审批签字区"""
    if not preset.has_approval:
        return

    if approval_list is None:
        approval_list = [
            {'role': '编制', 'name': ''},
            {'role': '审核', 'name': ''},
            {'role': '批准', 'name': ''},
        ]

    add_empty_line(doc)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run('【审批记录】')
    _set_font(run, preset.font_heading, preset.size_section, bold=True)
    p.paragraph_format.space_after = Pt(6)

    today = datetime.date.today().strftime('%Y-%m-%d')

    header = '| 角色 | 姓名 | 日期 | 签字 |'
    rows = [header]
    for item in approval_list:
        role = item.get('role', '')
        name = item.get('name', '__________')
        date_str = item.get('date', today if role == '编制' else '')
        rows.append(f'| {role} | {name or "__________"} | {date_str} | __________ |')

    build_table(doc, rows)


def add_classification_mark(doc, classification):
    """添加密级标识"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(f'【{classification}】')
    _set_font(run, '仿宋', 12, bold=True)
    p.paragraph_format.space_after = Pt(0)


# ============== 主函数 ==============

def create_word_doc(output_path, title='', content='', doc_number=None, version='V1.0',
                   classification='内部', author=None, company_name=None,
                   logo_path=None, approval=None, footer_page=True, header_doc_number=True,
                   doc_format=None, use_odoo=True):
    """
    生成企业标准 Word 文档 v5.3（多规范 + 本地公司信息）

    参数:
        output_path: 输出文件路径（必需）
        title: 文档标题（可选）
        content: 正文内容（可选）
        doc_number: 文档编号（可选）
        version: 版本号（默认 V1.0）
        classification: 密级（默认内部）
        author: 作者（可选）
        company_name: 公司名称，显式覆盖本地缓存（可选）
        logo_path: LOGO 绝对路径，显式覆盖本地缓存（可选）
        approval: 审批人列表（可选）
        footer_page: 页脚显示页码（默认 True）
        header_doc_number: 页眉显示文档编号（默认 True）
        doc_format: 文档格式（自动检测：公文/合同/会议纪要/技术方案/需求文档/工作报告）
        use_odoo: 是否允许 Odoo 作为第三优先级回落（默认 True）

    缺少公司名或 LOGO 时抛出 RuntimeError，调用方（SKILL 工作流）需提示用户补录。
    """
    # 公司信息：先解析，缺字段直接抛错让上层处理
    overrides = {'company_name': company_name, 'logo_path': logo_path}
    info = resolve_company_info(overrides=overrides, use_odoo=use_odoo)
    missing = company_info_missing(info)
    if missing:
        raise RuntimeError(json.dumps({
            'error': 'company_info_missing',
            'missing': missing,
            'hint': '请先填写 ~/.huo15/company-info.json，或使用 --company-name / --logo-path 覆盖',
            'config_path': _ci_module.CONFIG_PATH,
        }, ensure_ascii=False))

    company = info['company_name']
    logo = info['logo_path']

    doc = Document()

    # 检测格式
    if not doc_format or doc_format == 'auto':
        doc_format = detect_format(title, content)

    preset = get_preset(doc_format)
    print(f"📄 使用文档格式: {preset.name} ({doc_format})")
    print(f"🏢 公司: {company}")
    print(f"🖼  LOGO: {logo}")

    # 页面设置
    for sec in doc.sections:
        sec.top_margin = Cm(preset.margin_top)
        sec.bottom_margin = Cm(preset.margin_bottom)
        sec.left_margin = Cm(preset.margin_left)
        sec.right_margin = Cm(preset.margin_right)
        sec.header_distance = Cm(1.5)
        sec.footer_distance = Cm(1.5)

    # 页眉
    header_doc_num = doc_number if header_doc_number else None
    add_header(doc, preset, logo, company, header_doc_num, classification, title)

    # 页脚
    if footer_page:
        add_footer(doc, preset)

    # 默认样式
    style = doc.styles['Normal']
    style.font.name = preset.font_body
    style.font.size = Pt(preset.size_body)

    # 密级标识
    if classification and classification != '公开':
        add_classification_mark(doc, classification)

    # 文档标题
    if title:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        _set_font(run, preset.font_title, preset.size_title, bold=True)
        p.paragraph_format.line_spacing = preset.line_spacing
        p.paragraph_format.space_after = Pt(18)

    # 元数据
    meta_items = []
    if doc_number:
        meta_items.append(f'文档编号：{doc_number}')
    meta_items.append(f'版本：{version}')
    meta_items.append(f'密级：{classification}')
    today = datetime.date.today().strftime('%Y-%m-%d')
    meta_items.append(f'日期：{today}')
    if author:
        meta_items.append(f'作者：{author}')

    if meta_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(6)
        meta_text = '  |  '.join(meta_items)
        run = p.add_run(meta_text)
        _set_font(run, preset.font_body, preset.size_body - 1)

    # 版本历史
    add_version_history(doc, preset, version, today, author or '未知')

    # 正文
    parse_content(doc, content, preset)

    # 审批签字区
    if approval is not None:
        add_approval_block(doc, preset, approval)

    doc.save(output_path)
    print(f'✅ 文档已生成: {output_path}')
    return output_path


def _use_legacy_cli(argv):
    """旧位置参数模式：首个参数不以 '--' 开头 且 不是 '-h'。"""
    if len(argv) <= 1:
        return False
    first = argv[1]
    return not first.startswith('-')


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        prog='create-word-doc',
        description='火一五企业级 Word 生成器（多规范 + 本地公司信息）',
    )
    parser.add_argument('--output', '-o', required=True, help='输出 .docx 路径')
    parser.add_argument('--title', default='', help='文档标题')
    parser.add_argument('--content', default='', help='正文内容；以 @file 开头时读取文件')
    parser.add_argument('--doc-number', default=None)
    parser.add_argument('--version', default='V1.0')
    parser.add_argument('--classification', default='内部', help='密级：公开/内部/秘密')
    parser.add_argument('--author', default=None)
    parser.add_argument('--doc-format', default='auto',
                        choices=['auto', '公文', '合同', '会议纪要', '技术方案', '需求文档', '工作报告'])
    parser.add_argument('--company-name', default=None, help='覆盖本地缓存的公司名')
    parser.add_argument('--logo-path', default=None, help='覆盖本地缓存的 LOGO 路径')
    parser.add_argument('--no-odoo', action='store_true', help='不从 Odoo 回落')
    return parser.parse_args(argv[1:])


def _load_content(content_arg):
    if content_arg and content_arg.startswith('@'):
        path = content_arg[1:]
        with open(path, 'r', encoding='utf-8') as fh:
            return fh.read()
    return content_arg


if __name__ == '__main__':
    try:
        if _use_legacy_cli(sys.argv):
            argv = sys.argv
            create_word_doc(
                output_path=argv[1] if len(argv) > 1 else 'output.docx',
                title=argv[2] if len(argv) > 2 else '',
                content=argv[3] if len(argv) > 3 else '',
                doc_number=argv[4] if len(argv) > 4 else None,
                version=argv[5] if len(argv) > 5 else 'V1.0',
                classification=argv[6] if len(argv) > 6 else '内部',
                doc_format=argv[7] if len(argv) > 7 else 'auto',
            )
        else:
            args = _parse_args(sys.argv)
            create_word_doc(
                output_path=args.output,
                title=args.title,
                content=_load_content(args.content),
                doc_number=args.doc_number,
                version=args.version,
                classification=args.classification,
                author=args.author,
                company_name=args.company_name,
                logo_path=args.logo_path,
                doc_format=args.doc_format,
                use_odoo=not args.no_odoo,
            )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
