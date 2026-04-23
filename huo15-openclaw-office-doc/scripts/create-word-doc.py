#!/usr/bin/env python3
"""
create-word-doc.py - 企业级 Word 文档生成器 v6.0（Block AST 重写版）

相比 v5.3 的改进：
- 全新基于块（Block AST）的 Markdown 解析，修复两列表格、空内容、代码块/引用块缺失等问题
- 页眉始终含公司 LOGO + 公司名（任何规范都有）
- 页脚始终为 "第 X 页 / 共 Y 页"（PAGE / NUMPAGES 字段码，Word/WPS 打开时自动计算）
- 根据规范差异调整字体、行距、页边距、是否生成版本历史/审批表
- 版本历史 / 审批表仅在正式规范下自动追加：公文 / 技术方案 / 需求文档；其他规范仅当显式传入 approval=[...] 时才生成
- 新增代码块 (``` ``` ```) 与引用块 (> ...) 渲染
- Markdown 表格容错：支持 2 列、缺前导 `|`、对齐标记、空单元格；修掉 `pipe_count >= 2` 造成的 2 列误判
- 错误不再静默；缺 company_name / logo_path 时抛 RuntimeError（JSON 消息）+ 退出码 2，便于 Claude 触发补录

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


# ============================================================
# 一、文档规范预设（Format Preset）
# ============================================================

class FormatPreset:
    """每种文档规范的排版参数。"""

    def __init__(self, name,
                 margin_top=3.7, margin_bottom=3.5,
                 margin_left=2.8, margin_right=2.6,
                 font_body='仿宋', font_title='黑体', font_heading='黑体',
                 size_title=22, size_chapter=16, size_section=14, size_body=12,
                 line_spacing=1.5,
                 has_version_history=False, has_approval=False,
                 header_layout='company', heading_patterns=None,
                 first_line_indent_cm=0.74):
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
        self.header_layout = header_layout  # 'company'（默认） / 'centered'（合同）
        self.heading_patterns = heading_patterns or []
        self.first_line_indent_cm = first_line_indent_cm


PRESET_GONGWEN = FormatPreset(
    name='公文',
    heading_patterns=[
        (r'^第[一二三四五六七八九十百千]+[章节篇款]', 'chapter'),
        (r'^[一二三四五六七八九十百千]+[、．]', 'section'),
        (r'^[（\(][一二三四五六七八九十百千]+[）\)]', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
)

PRESET_HETONG = FormatPreset(
    name='合同',
    margin_top=2.54, margin_bottom=2.54, margin_left=3.17, margin_right=3.17,
    font_body='宋体', font_title='宋体', font_heading='宋体',
    size_title=22, size_chapter=15, size_section=13, size_body=12,
    heading_patterns=[
        (r'^第[一二三四五六七八九十百千]+[章节条款]', 'chapter'),
        (r'^[一二三四五六七八九十百千]+[、]', 'section'),
    ],
    has_version_history=False,
    has_approval=False,
    header_layout='centered',
)

PRESET_HUIYI = FormatPreset(
    name='会议纪要',
    font_body='仿宋', font_title='方正小标宋简体', font_heading='黑体',
    size_title=22, size_chapter=14, size_section=12, size_body=12,
    heading_patterns=[
        (r'^【[^】]+】', 'chapter'),
        (r'^[一二三四五六七八九十]+[、]', 'section'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'article'),
    ],
    has_version_history=False,
    has_approval=False,
)

PRESET_FANGAN = FormatPreset(
    name='技术方案',
    font_body='宋体', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[．、]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
)

PRESET_XUQIU = FormatPreset(
    name='需求文档',
    font_body='宋体', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[．、]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
)

PRESET_GONGZUO = FormatPreset(
    name='工作报告',
    font_body='仿宋', font_title='方正小标宋简体', font_heading='楷体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'section'),
    ],
    has_version_history=False,
    has_approval=False,
)


FORMAT_PRESETS = {
    '公文': PRESET_GONGWEN,
    '合同': PRESET_HETONG,
    '会议纪要': PRESET_HUIYI,
    '技术方案': PRESET_FANGAN,
    '需求文档': PRESET_XUQIU,
    '工作报告': PRESET_GONGZUO,
}


FORMAT_KEYWORDS = {
    '合同': ['合同', '协议', '协议书'],
    '会议纪要': ['会议纪要', '纪要'],
    '技术方案': ['技术方案', '实施方案', '解决方案', '设计文档'],
    '需求文档': ['需求规格', '需求说明', 'SRS', 'PRD', '需求文档'],
    '工作报告': ['工作报告', '周报', '月报', '季报', '年报', '述职报告'],
}


def detect_format(title='', content=''):
    """根据标题和正文前 500 字猜测规范类型，默认公文。"""
    text = (title + ' ' + (content or '')[:500]).lower()
    for fmt, keywords in FORMAT_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                return fmt
    return '公文'


def get_preset(format_name):
    return FORMAT_PRESETS.get(format_name, PRESET_GONGWEN)


# ============================================================
# 二、公司信息（来自同目录 company-info.py）
# ============================================================

_CI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'company-info.py')
_ci_spec = importlib.util.spec_from_file_location('company_info', _CI_PATH)
_ci_module = importlib.util.module_from_spec(_ci_spec)
_ci_spec.loader.exec_module(_ci_module)


def resolve_company_info(overrides=None, use_odoo=True):
    info = _ci_module.resolve(use_odoo=use_odoo)
    if overrides:
        for key, value in overrides.items():
            if value:
                info[key] = value
    return info


def company_info_missing(info):
    missing = [k for k in _ci_module.REQUIRED_FIELDS if not info.get(k)]
    if info.get('logo_path') and not _ci_module.logo_is_valid(info.get('logo_path')):
        if 'logo_path' not in missing:
            missing.append('logo_path')
    return missing


# ============================================================
# 三、OOXML 小工具
# ============================================================

def _set_font(run, font_name, size, bold=False, italic=False, color=None):
    """统一设置中英文字体（WPS/Word 双兼容）。"""
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
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def _add_border_bottom(paragraph, color='888888', sz='6'):
    pPr = paragraph._element.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        paragraph._element.insert(0, pPr)
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), sz)
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), color)
    pBdr.append(bottom)
    pPr.append(pBdr)


def _add_border_left(paragraph, color='CCCCCC', sz='18'):
    pPr = paragraph._element.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        paragraph._element.insert(0, pPr)
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), sz)
    left.set(qn('w:space'), '8')
    left.set(qn('w:color'), color)
    pBdr.append(left)
    pPr.append(pBdr)


def _set_cell_shading(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    tcPr.append(shd)


def _set_paragraph_shading(paragraph, fill_color):
    pPr = paragraph._element.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        paragraph._element.insert(0, pPr)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    pPr.append(shd)


def _add_field(paragraph, field_code, font_name, font_size):
    """给段落追加一个字段（如 PAGE / NUMPAGES）。"""
    run = paragraph.add_run()
    fc_begin = OxmlElement('w:fldChar')
    fc_begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = f' {field_code} '
    fc_end = OxmlElement('w:fldChar')
    fc_end.set(qn('w:fldCharType'), 'end')
    run._element.append(fc_begin)
    run._element.append(instr)
    run._element.append(fc_end)
    _set_font(run, font_name, font_size)


# ============================================================
# 四、页眉 & 页脚（任何规范都有）
# ============================================================

def build_header(doc, preset, logo_path, company_name, doc_number=None,
                 classification=None, title=''):
    """页眉始终有公司 LOGO + 名称；公文/技术方案/需求文档额外显示文档编号 + 密级。"""
    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False

    for p in header.paragraphs:
        for r in p.runs:
            r.text = ''

    para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(0)

    if preset.header_layout == 'centered':
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    if logo_path and os.path.exists(logo_path):
        try:
            run = para.add_run()
            run.add_picture(logo_path, height=Cm(0.9))
            para.add_run('  ')
        except Exception as exc:  # pragma: no cover - best-effort
            print(f'⚠️  LOGO 添加失败：{exc}', file=sys.stderr)

    run = para.add_run(company_name)
    _set_font(run, '黑体', preset.size_body - 2)

    if preset.header_layout != 'centered':
        # 公文 / 方案 / 报告 等可带文档编号 + 密级
        if doc_number:
            run = para.add_run(f'    {doc_number}')
            _set_font(run, '黑体', preset.size_body - 2)
        if classification:
            run = para.add_run(f'    【{classification}】')
            _set_font(run, '黑体', preset.size_body - 2, bold=True)

    _add_border_bottom(para, color='888888', sz='6')


def build_footer(doc, preset, company_name):
    """页脚始终为 "第 X 页 / 共 Y 页"；规范字体取 preset.font_body。"""
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False

    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    for r in para.runs:
        r.text = ''
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(0)

    size = preset.size_body - 2

    run = para.add_run('第 ')
    _set_font(run, preset.font_body, size)
    _add_field(para, 'PAGE', preset.font_body, size)
    run = para.add_run(' 页 / 共 ')
    _set_font(run, preset.font_body, size)
    _add_field(para, 'NUMPAGES', preset.font_body, size)
    run = para.add_run(' 页')
    _set_font(run, preset.font_body, size)


# ============================================================
# 五、Block AST 解析
# ============================================================

_HEADING_MD_RE = re.compile(r'^(#{1,6})\s*(.+?)\s*#*\s*$')
_HR_RE = re.compile(r'^\s*([-*_])\1{2,}\s*$')
_UL_ITEM_RE = re.compile(r'^\s*[-*+]\s+(.+)$')
_OL_ITEM_RE = re.compile(r'^\s*(\d+)[\.．)]\s+(.+)$')
_FENCE_RE = re.compile(r'^\s*```([\w+-]*)\s*$')
_BLOCKQUOTE_RE = re.compile(r'^\s*>\s?(.*)$')
_TABLE_SEP_CELL_RE = re.compile(r'^[:\s]*[\-−–—―]{3,}[:\s]*$')
_DOC_META_RE = re.compile(r'(?:文档编号|版本|密级|日期|作者)\s*[:：]')


def _split_table_cells(line):
    r"""智能分割表格行；保留前后 | 之间的内容；允许 `\|` 转义。"""
    s = line.strip()
    leading = s.startswith('|')
    trailing = s.endswith('|') and not s.endswith(r'\|')
    if leading and trailing and len(s) >= 2:
        s = s[1:-1]
    elif leading:
        s = s[1:]
    elif trailing:
        s = s[:-1]

    cells, buf, i = [], '', 0
    while i < len(s):
        ch = s[i]
        if ch == '\\' and i + 1 < len(s) and s[i + 1] == '|':
            buf += '|'
            i += 2
            continue
        if ch == '|':
            cells.append(buf.strip())
            buf = ''
        else:
            buf += ch
        i += 1
    cells.append(buf.strip())
    return cells


def _is_table_separator(line):
    t = line.strip()
    if not t or '|' not in t:
        return False
    cells = _split_table_cells(t)
    if len(cells) < 2:
        return False
    has_sep = False
    for c in cells:
        if not c:
            continue
        if _TABLE_SEP_CELL_RE.match(c):
            has_sep = True
        else:
            return False
    return has_sep


def _looks_like_table_row(line):
    """是不是一行表格数据：含 `|` 且至少能切出 2 个 cell。"""
    t = line.strip()
    if '|' not in t:
        return False
    if _is_table_separator(t):
        return False
    cells = _split_table_cells(t)
    return len(cells) >= 2


def _is_metadata_line(line):
    """文档头部的元数据行（`文档编号：XX | 版本：V1.0 | ...`）。"""
    t = line.strip()
    if '|' not in t:
        return False
    segments = [seg.strip() for seg in _split_table_cells(t) if seg.strip()]
    if len(segments) < 2:
        return False
    meta_hits = sum(1 for seg in segments if _DOC_META_RE.search(seg))
    return meta_hits >= 2


def parse_blocks(content):
    """把 Markdown 文本切成块节点列表。

    每个节点是 dict，含 `type` 与对应负载。类型：
      - heading: {level: 1..6, text}
      - paragraph: {text}
      - list: {ordered: bool, items: [text, ...]}
      - table: {rows: [[cell, ...], ...], has_header: bool}
      - code_block: {lang, code}
      - blockquote: {lines: [text, ...]}
      - metadata: {pairs: [(key, value), ...]}
      - hr: {}
    """
    lines = (content or '').split('\n')
    blocks = []
    i = 0
    n = len(lines)

    def is_blank(idx):
        return idx < n and not lines[idx].strip()

    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue

        fence = _FENCE_RE.match(raw)
        if fence:
            lang = fence.group(1) or ''
            i += 1
            code_lines = []
            while i < n and not _FENCE_RE.match(lines[i]):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1  # 跳过闭合 fence
            blocks.append({'type': 'code_block', 'lang': lang,
                           'code': '\n'.join(code_lines)})
            continue

        if _HR_RE.match(raw):
            blocks.append({'type': 'hr'})
            i += 1
            continue

        bq_match = _BLOCKQUOTE_RE.match(raw)
        if bq_match:
            bq_lines = [bq_match.group(1)]
            i += 1
            while i < n:
                m = _BLOCKQUOTE_RE.match(lines[i])
                if m:
                    bq_lines.append(m.group(1))
                    i += 1
                elif not lines[i].strip():
                    break
                else:
                    # 继行
                    bq_lines.append(lines[i].strip())
                    i += 1
            blocks.append({'type': 'blockquote', 'lines': bq_lines})
            continue

        md_heading = _HEADING_MD_RE.match(raw)
        if md_heading:
            blocks.append({
                'type': 'heading',
                'level': len(md_heading.group(1)),
                'text': md_heading.group(2).strip(),
            })
            i += 1
            continue

        if _is_metadata_line(stripped):
            cells = [c for c in _split_table_cells(stripped) if c.strip()]
            pairs = []
            for cell in cells:
                if '：' in cell:
                    idx = cell.index('：')
                    pairs.append((cell[:idx].strip(), cell[idx + 1:].strip()))
                elif ':' in cell:
                    idx = cell.index(':')
                    pairs.append((cell[:idx].strip(), cell[idx + 1:].strip()))
                else:
                    pairs.append(('', cell.strip()))
            blocks.append({'type': 'metadata', 'pairs': pairs})
            i += 1
            continue

        if _looks_like_table_row(stripped):
            # 表头 + 可选分隔行 + 数据行
            rows = [_split_table_cells(stripped)]
            i += 1
            has_header = False
            if i < n and _is_table_separator(lines[i]):
                has_header = True
                i += 1
            while i < n and _looks_like_table_row(lines[i]):
                rows.append(_split_table_cells(lines[i]))
                i += 1
            blocks.append({'type': 'table', 'rows': rows,
                           'has_header': has_header})
            continue

        ul = _UL_ITEM_RE.match(raw)
        ol = _OL_ITEM_RE.match(raw)
        if ul or ol:
            ordered = bool(ol)
            items = []
            while i < n:
                m_ul = _UL_ITEM_RE.match(lines[i])
                m_ol = _OL_ITEM_RE.match(lines[i])
                if ordered and m_ol:
                    items.append(m_ol.group(2).strip())
                    i += 1
                elif not ordered and m_ul:
                    items.append(m_ul.group(1).strip())
                    i += 1
                elif not lines[i].strip():
                    break
                else:
                    break
            blocks.append({'type': 'list', 'ordered': ordered, 'items': items})
            continue

        # 段落：吃掉连续非空非特殊行
        para_lines = [stripped]
        i += 1
        while i < n:
            nxt = lines[i]
            nxt_strip = nxt.strip()
            if not nxt_strip:
                break
            if (_HEADING_MD_RE.match(nxt) or _HR_RE.match(nxt)
                    or _FENCE_RE.match(nxt) or _BLOCKQUOTE_RE.match(nxt)
                    or _UL_ITEM_RE.match(nxt) or _OL_ITEM_RE.match(nxt)
                    or _is_metadata_line(nxt_strip)
                    or _looks_like_table_row(nxt_strip)):
                break
            para_lines.append(nxt_strip)
            i += 1
        blocks.append({'type': 'paragraph',
                       'text': ' '.join(para_lines).strip()})

    return blocks


# ============================================================
# 六、Inline Markdown（**bold** / *italic* / `code`）
# ============================================================

_INLINE_RE = re.compile(
    r'(\*\*[^*\n]+?\*\*|'        # **bold**
    r'\*[^*\n]+?\*|'             # *italic*
    r'`[^`\n]+?`)'               # `code`
)


def render_inline(paragraph, text, font, size, base_bold=False,
                  color=None, inline_code_font='Consolas'):
    """按内联标记拆分后，往 paragraph 追加多段 run。"""
    if not text:
        return
    parts = _INLINE_RE.split(text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) >= 4:
            run = paragraph.add_run(part[2:-2])
            _set_font(run, font, size, bold=True, color=color)
        elif part.startswith('*') and part.endswith('*') and len(part) >= 2:
            run = paragraph.add_run(part[1:-1])
            _set_font(run, font, size, bold=base_bold, italic=True, color=color)
        elif part.startswith('`') and part.endswith('`') and len(part) >= 2:
            run = paragraph.add_run(part[1:-1])
            _set_font(run, inline_code_font, size, bold=base_bold)
        else:
            run = paragraph.add_run(part)
            _set_font(run, font, size, bold=base_bold, color=color)


# ============================================================
# 七、渲染：把 Block 写到 docx
# ============================================================

def _apply_paragraph_defaults(p, preset, indent=True, align=None,
                              space_before=0, space_after=6):
    p.alignment = align if align is not None else WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = preset.line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.first_line_indent = Cm(preset.first_line_indent_cm)
    else:
        p.paragraph_format.first_line_indent = Cm(0)


def render_heading(doc, preset, level, text):
    if level <= 1:
        font_size, bold = preset.size_chapter, True
        space_before, space_after = 18, 8
    elif level == 2:
        font_size, bold = preset.size_section, True
        space_before, space_after = 14, 6
    else:
        font_size, bold = preset.size_body + 1, True
        space_before, space_after = 8, 4

    p = doc.add_paragraph()
    _apply_paragraph_defaults(p, preset, indent=False,
                              align=WD_ALIGN_PARAGRAPH.LEFT,
                              space_before=space_before,
                              space_after=space_after)
    render_inline(p, text, preset.font_heading, font_size, base_bold=bold)


def render_paragraph(doc, preset, text):
    p = doc.add_paragraph()
    _apply_paragraph_defaults(p, preset, indent=True)
    render_inline(p, text, preset.font_body, preset.size_body)


def render_list(doc, preset, ordered, items):
    for idx, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        _apply_paragraph_defaults(p, preset, indent=False,
                                  align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                                  space_after=3)
        bullet = f'{idx}. ' if ordered else '• '
        run = p.add_run(bullet)
        _set_font(run, preset.font_body, preset.size_body)
        render_inline(p, item, preset.font_body, preset.size_body)


def render_table(doc, preset, rows, has_header=True):
    if not rows:
        return
    max_cols = max(len(r) for r in rows)
    norm = [r + [''] * (max_cols - len(r)) for r in rows]
    table = doc.add_table(rows=len(norm), cols=max_cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for r_idx, row in enumerate(norm):
        is_head = has_header and r_idx == 0
        for c_idx, cell_text in enumerate(row):
            cell = table.rows[r_idx].cells[c_idx]
            cell.text = ''
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            font_name = preset.font_heading if is_head else preset.font_body
            size = preset.size_body - 1
            render_inline(para, cell_text, font_name, size,
                          base_bold=is_head)
            if is_head:
                _set_cell_shading(cell, 'E8ECF0')


def render_code_block(doc, preset, code, lang=''):
    """用带背景色 + 边框的等宽段落模拟代码块。"""
    para = doc.add_paragraph()
    _apply_paragraph_defaults(para, preset, indent=False,
                              align=WD_ALIGN_PARAGRAPH.LEFT,
                              space_before=4, space_after=8)
    para.paragraph_format.line_spacing = 1.2
    para.paragraph_format.left_indent = Cm(0.3)
    _set_paragraph_shading(para, 'F5F5F5')
    _add_border_bottom(para, color='CCCCCC', sz='4')

    if lang:
        tag = para.add_run(f'{lang}\n')
        _set_font(tag, 'Consolas', preset.size_body - 2,
                  color=RGBColor(0x88, 0x88, 0x88))

    run = para.add_run(code)
    _set_font(run, 'Consolas', preset.size_body - 1,
              color=RGBColor(0x22, 0x22, 0x22))


def render_blockquote(doc, preset, lines):
    """引用块：左侧竖线 + 灰色斜体。"""
    for line in lines:
        p = doc.add_paragraph()
        _apply_paragraph_defaults(p, preset, indent=False,
                                  align=WD_ALIGN_PARAGRAPH.LEFT,
                                  space_after=2)
        p.paragraph_format.left_indent = Cm(0.5)
        _add_border_left(p, color='FF7043', sz='18')
        render_inline(p, line, preset.font_body, preset.size_body,
                      color=RGBColor(0x55, 0x55, 0x55))


def render_metadata(doc, preset, pairs):
    """文档头部元数据行 → 两列表格。"""
    if not pairs:
        return
    table = doc.add_table(rows=len(pairs), cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    for r, (key, value) in enumerate(pairs):
        row = table.rows[r]
        row.cells[0].text = ''
        row.cells[1].text = ''
        p0 = row.cells[0].paragraphs[0]
        p1 = row.cells[1].paragraphs[0]
        render_inline(p0, key or '', preset.font_heading,
                      preset.size_body - 1, base_bold=True)
        render_inline(p1, value or '', preset.font_body,
                      preset.size_body - 1)
        _set_cell_shading(row.cells[0], 'F5F5F5')


def render_hr(doc, preset):
    p = doc.add_paragraph()
    _apply_paragraph_defaults(p, preset, indent=False,
                              space_before=4, space_after=6)
    _add_border_bottom(p, color='CCCCCC', sz='6')


_LEVEL_KEY_TO_MD = {'chapter': 1, 'section': 2, 'article': 3}


def _detect_heading_from_preset(text, preset):
    """返回 (md_level, cleaned_text) 或 None。"""
    for pattern, level_key in preset.heading_patterns:
        if re.match(pattern, text):
            md_level = _LEVEL_KEY_TO_MD.get(level_key, 2)
            if level_key == 'chapter':
                return md_level, text  # 章/【主题】 保留前缀
            cleaned = re.sub(pattern, '', text).strip()
            return md_level, cleaned or text
    return None


def render_block(doc, preset, block):
    btype = block['type']
    if btype == 'heading':
        render_heading(doc, preset, block['level'], block['text'])
        return

    if btype == 'paragraph':
        text = block['text']
        detected = _detect_heading_from_preset(text, preset)
        if detected is not None:
            level, cleaned = detected
            render_heading(doc, preset, level, cleaned)
            return
        render_paragraph(doc, preset, text)
        return

    if btype == 'list':
        render_list(doc, preset, block.get('ordered', False),
                    block.get('items', []))
        return

    if btype == 'table':
        render_table(doc, preset, block.get('rows', []),
                     has_header=block.get('has_header', True))
        return

    if btype == 'code_block':
        render_code_block(doc, preset, block.get('code', ''),
                          block.get('lang', ''))
        return

    if btype == 'blockquote':
        render_blockquote(doc, preset, block.get('lines', []))
        return

    if btype == 'metadata':
        render_metadata(doc, preset, block.get('pairs', []))
        return

    if btype == 'hr':
        render_hr(doc, preset)
        return


def render_content(doc, preset, content):
    blocks = parse_blocks(content)
    if not blocks:
        # 空内容时写一行提示，避免生成完全空白页
        p = doc.add_paragraph()
        _apply_paragraph_defaults(p, preset, indent=True, space_after=0)
        run = p.add_run('（无正文内容）')
        _set_font(run, preset.font_body, preset.size_body,
                  color=RGBColor(0x99, 0x99, 0x99))
        return
    for block in blocks:
        render_block(doc, preset, block)


# ============================================================
# 八、文档壳：标题、元数据、版本历史、审批表
# ============================================================

def add_title(doc, preset, title):
    if not title:
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = preset.line_spacing
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(18)
    run = p.add_run(title)
    _set_font(run, preset.font_title, preset.size_title, bold=True)


def add_doc_meta(doc, preset, doc_number, version, classification,
                 author):
    items = []
    if doc_number:
        items.append(('文档编号', doc_number))
    items.append(('版本', version))
    items.append(('密级', classification))
    items.append(('日期', datetime.date.today().strftime('%Y-%m-%d')))
    if author:
        items.append(('作者', author))

    table = doc.add_table(rows=len(items), cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    for r, (key, value) in enumerate(items):
        row = table.rows[r]
        row.cells[0].text = ''
        row.cells[1].text = ''
        p0 = row.cells[0].paragraphs[0]
        p1 = row.cells[1].paragraphs[0]
        run = p0.add_run(key)
        _set_font(run, preset.font_heading, preset.size_body - 1,
                  bold=True)
        run = p1.add_run(str(value))
        _set_font(run, preset.font_body, preset.size_body - 1)
        _set_cell_shading(row.cells[0], 'F5F5F5')

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)


def add_classification_banner(doc, preset, classification):
    if not classification or classification == '公开':
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(f'【{classification}】')
    _set_font(run, preset.font_heading, preset.size_body, bold=True,
              color=RGBColor(0xB0, 0x00, 0x00))


def add_version_history(doc, preset, version, date_str, author):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run('版本历史')
    _set_font(run, preset.font_heading, preset.size_section, bold=True)

    rows = [
        ['版本', '日期', '作者', '修改说明'],
        [version or 'V1.0', date_str, author or '未知', '首次创建'],
    ]
    render_table(doc, preset, rows, has_header=True)


def add_approval_block(doc, preset, approval_list=None):
    items = approval_list if approval_list else [
        {'role': '编制', 'name': ''},
        {'role': '审核', 'name': ''},
        {'role': '批准', 'name': ''},
    ]

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run('审批记录')
    _set_font(run, preset.font_heading, preset.size_section, bold=True)

    today = datetime.date.today().strftime('%Y-%m-%d')
    rows = [['角色', '姓名', '日期', '签字']]
    for item in items:
        role = item.get('role', '')
        name = item.get('name') or '__________'
        date_str = item.get('date') or (today if role == '编制' else '')
        rows.append([role, name, date_str, '__________'])
    render_table(doc, preset, rows, has_header=True)


# ============================================================
# 九、对外入口
# ============================================================

def create_word_doc(output_path, title='', content='', doc_number=None,
                    version='V1.0', classification='内部', author=None,
                    company_name=None, logo_path=None, approval=None,
                    doc_format=None, use_odoo=True,
                    force_version_history=None, force_approval=None):
    """生成企业 Word 文档（v6.0）。

    核心改动：
      - 页眉始终含 LOGO + 公司名；页脚始终为 "第 X 页 / 共 Y 页"
      - Block AST 解析 Markdown，处理 2 列表格、代码块、引用块等
      - 版本历史 / 审批表默认仅在正式规范（公文 / 技术方案 / 需求文档）追加，
        通过 force_version_history / force_approval 可以在任何规范上强制开/关

    缺少 company_name 或 logo_path 时抛 RuntimeError（message 为 JSON），
    CLI 捕获后以退出码 2 退出；Claude 据此发起补录流程。
    """
    info = resolve_company_info(
        overrides={'company_name': company_name, 'logo_path': logo_path},
        use_odoo=use_odoo,
    )
    missing = company_info_missing(info)
    if missing:
        raise RuntimeError(json.dumps({
            'error': 'company_info_missing',
            'missing': missing,
            'hint': ('请先填写 ~/.huo15/company-info.json 或用 '
                     '--company-name / --logo-path 覆盖'),
            'config_path': _ci_module.CONFIG_PATH,
        }, ensure_ascii=False))

    company = info['company_name']
    logo = info['logo_path']

    if not doc_format or doc_format == 'auto':
        doc_format = detect_format(title, content)
    preset = get_preset(doc_format)

    print(f'📄 使用文档规范: {preset.name}')
    print(f'🏢 公司: {company}')
    print(f'🖼  LOGO: {logo}')

    doc = Document()

    for sec in doc.sections:
        sec.top_margin = Cm(preset.margin_top)
        sec.bottom_margin = Cm(preset.margin_bottom)
        sec.left_margin = Cm(preset.margin_left)
        sec.right_margin = Cm(preset.margin_right)
        sec.header_distance = Cm(1.5)
        sec.footer_distance = Cm(1.5)

    build_header(doc, preset, logo, company,
                 doc_number=doc_number,
                 classification=classification,
                 title=title)
    build_footer(doc, preset, company)

    normal_style = doc.styles['Normal']
    normal_style.font.name = preset.font_body
    normal_style.font.size = Pt(preset.size_body)

    add_classification_banner(doc, preset, classification)
    add_title(doc, preset, title)
    add_doc_meta(doc, preset, doc_number, version, classification, author)

    render_content(doc, preset, content)

    want_version = (force_version_history
                    if force_version_history is not None
                    else preset.has_version_history)
    if want_version:
        add_version_history(doc, preset, version,
                            datetime.date.today().strftime('%Y-%m-%d'),
                            author or '未知')

    want_approval = (force_approval if force_approval is not None
                     else preset.has_approval)
    if want_approval or approval:
        add_approval_block(doc, preset, approval)

    doc.save(output_path)
    print(f'✅ 文档已生成: {output_path}')
    return output_path


# ============================================================
# 十、CLI
# ============================================================

def _use_legacy_cli(argv):
    if len(argv) <= 1:
        return False
    return not argv[1].startswith('-')


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        prog='create-word-doc',
        description='火一五企业级 Word 生成器 v6.0（多规范 + 本地公司信息）',
    )
    parser.add_argument('--output', '-o', required=True, help='输出 .docx 路径')
    parser.add_argument('--title', default='', help='文档标题')
    parser.add_argument('--content', default='',
                        help='正文（Markdown）；以 @file 开头时读取文件')
    parser.add_argument('--doc-number', default=None)
    parser.add_argument('--version', default='V1.0')
    parser.add_argument('--classification', default='内部',
                        help='密级：公开/内部/秘密')
    parser.add_argument('--author', default=None)
    parser.add_argument('--doc-format', default='auto',
                        choices=['auto', '公文', '合同', '会议纪要',
                                 '技术方案', '需求文档', '工作报告'])
    parser.add_argument('--company-name', default=None,
                        help='覆盖本地缓存的公司名')
    parser.add_argument('--logo-path', default=None,
                        help='覆盖本地缓存的 LOGO 路径')
    parser.add_argument('--no-odoo', action='store_true', help='不从 Odoo 回落')
    parser.add_argument('--with-version-history', action='store_true',
                        help='强制追加版本历史（即便当前规范默认关闭）')
    parser.add_argument('--no-version-history', action='store_true',
                        help='强制不追加版本历史')
    parser.add_argument('--with-approval', action='store_true',
                        help='强制追加审批表')
    parser.add_argument('--no-approval', action='store_true',
                        help='强制不追加审批表')
    return parser.parse_args(argv[1:])


def _load_content(content_arg):
    if content_arg and content_arg.startswith('@'):
        path = content_arg[1:]
        with open(path, 'r', encoding='utf-8') as fh:
            return fh.read()
    return content_arg


def _flag_tristate(on, off):
    if on and off:
        return None
    if on:
        return True
    if off:
        return False
    return None


def main(argv=None):
    argv = argv if argv is not None else sys.argv
    try:
        if _use_legacy_cli(argv):
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
            args = _parse_args(argv)
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
                force_version_history=_flag_tristate(
                    args.with_version_history, args.no_version_history),
                force_approval=_flag_tristate(
                    args.with_approval, args.no_approval),
            )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
