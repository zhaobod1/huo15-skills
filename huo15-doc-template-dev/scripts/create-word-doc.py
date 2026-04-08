#!/usr/bin/env python3
"""
create-word-doc.py - 国家公文标准 Word 文档生成器（WPS/Word 双兼容）

国家公文标准 GB/T 9704-2012：
  - 页面边距：上 3.7cm，下 3.5cm，左 2.8cm，右 2.6cm
  - 正文字体：仿宋，小四（12pt），行距 1.5，首行缩进 2 字符
  - 标题字体：黑体/楷体，加粗
  - 页眉：左对齐，LOGO + 公司名称（紧密挨着）
  - 页脚：居中，"第 X 页 / 共 Y 页"

WPS 兼容性：
  - 使用标准 OOXML 元素，不依赖 Word 专有扩展
  - 中文字体同时设置 rFonts（w:eastAsia）和 font.name
  - 避免复杂的 Word 字段链，使用简单的 fldChar begin/end 结构

用法：
    python create-word-doc.py <输出路径> [标题] [正文]
"""

import sys
import os
import re
import ssl
import json
import urllib.request
import xmlrpc.client
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============== 国家公文标准常量 ==============
MARGIN_TOP = 3.7
MARGIN_BOTTOM = 3.5
MARGIN_LEFT = 2.8
MARGIN_RIGHT = 2.6

# 字体（WPS 和 Word 都支持的标准字体）
FONT_BODY = '仿宋'
FONT_HEADING1 = '黑体'
FONT_HEADING2 = '楷体'
FONT_HEADER = '黑体'
FONT_FOOTER = '仿宋'

SIZE_BODY = 12         # 小四
SIZE_HEADING1 = 16     # 二号
SIZE_HEADING2 = 14     # 小三
SIZE_TITLE = 22        # 文档标题
SIZE_HEADER = 10.5
SIZE_FOOTER = 10.5

# ============== 公司信息 ==============
USER_HOME = os.path.expanduser("~")
LOGO_DIR = os.path.join(USER_HOME, ".huo15", "assets")
DEFAULT_LOGO_PATH = os.path.join(LOGO_DIR, "logo.png")
FALLBACK_LOGO_URL = 'https://tools.huo15.com/uploads/images/system/logo-colours.png'
DEFAULT_COMPANY_NAME = '青岛火一五信息科技有限公司'


def get_company_info():
    """从公司系统获取公司信息和 LOGO"""
    info = {'company_name': DEFAULT_COMPANY_NAME, 'logo_path': None}

    # 1. 本地缓存优先
    if os.path.exists(DEFAULT_LOGO_PATH) and os.path.getsize(DEFAULT_LOGO_PATH) > 1000:
        info['logo_path'] = DEFAULT_LOGO_PATH
        return info

    # 2. 尝试从 Odoo 获取
    try:
        creds_file = os.path.join(
            os.path.expanduser('~/.openclaw/agents'),
            os.environ.get('OC_AGENT_ID', 'main'),
            'odoo_creds.json'
        )
        if os.path.exists(creds_file):
            with open(creds_file) as f:
                creds = json.load(f)

            cfg_file = os.path.expanduser('~/.openclaw/openclaw.json')
            if os.path.exists(cfg_file):
                with open(cfg_file) as f:
                    cfg = json.load(f)
                    odoo_env = cfg.get('skills', {}).get('entries', {}).get('huo15-odoo', {}).get('env', {})
                    url = odoo_env.get('ODOO_URL', 'https://huihuoyun.huo15.com')
                    db = odoo_env.get('ODOO_DB', 'huo15_prod')

                user = creds.get('user', '')
                password = creds.get('password', '')
                if user and password:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
                    uid = common.authenticate(db, user, password, {})
                    if uid:
                        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=ctx)
                        data = models.execute_kw(db, uid, password, 'res.company',
                            'search_read', [[('id', '=', 1)]], {'fields': ['name', 'logo'], 'limit': 1})
                        if data:
                            info['company_name'] = data[0].get('name', DEFAULT_COMPANY_NAME)
                            logo_id = data[0].get('logo')
                            if logo_id:
                                _download(f'{url}/web/image/res.company/{logo_id}/logo', DEFAULT_LOGO_PATH)
                                if os.path.exists(DEFAULT_LOGO_PATH):
                                    info['logo_path'] = DEFAULT_LOGO_PATH
    except Exception as e:
        print(f"获取公司信息失败: {e}")

    # 3. 备用 LOGO
    if not info['logo_path']:
        _download(FALLBACK_LOGO_URL, DEFAULT_LOGO_PATH)
        if os.path.exists(DEFAULT_LOGO_PATH):
            info['logo_path'] = DEFAULT_LOGO_PATH

    return info


def _download(url, dest_path):
    """下载文件到本地"""
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        return
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"✓ LOGO 已下载: {dest_path}")
    except Exception as e:
        print(f"⚠ LOGO 下载失败: {e}")


def _set_font(run, font_name, size, bold=False):
    """
    设置中文字体，WPS/Word 双兼容
    同时设置西文字体名称和中文字体名称（w:eastAsia）
    """
    run.font.name = font_name
    # 获取或创建 rPr 元素
    rPr = run._element.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        run._element.insert(0, rPr)
    # 获取或创建 rFonts 元素
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    # 同时设置 ascii、hAnsi、eastAsia（WPS 三者都要有）
    rFonts.set(qn('w:eastAsia'), font_name)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    run.font.size = Pt(size)
    run.bold = bold


def _add_border_bottom(paragraph):
    """给段落下方加细线（页眉分隔线）"""
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


def add_header(doc, logo_path, company_name):
    """页眉：LOGO + 公司名称，左对齐，紧密挨着"""
    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False

    # 清除默认段落
    for p in header.paragraphs:
        for r in p.runs:
            r.text = ''
    para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # LOGO（高度 1.0cm）
    if logo_path and os.path.exists(logo_path):
        try:
            run = para.add_run()
            run.add_picture(logo_path, height=Cm(1.0))
        except Exception as e:
            print(f"⚠ LOGO 添加失败: {e}")

    # 公司名称（紧跟 LOGO，中间一个空格）
    run = para.add_run(f' {company_name}')
    _set_font(run, FONT_HEADER, SIZE_HEADER)

    # 页眉底线
    _add_border_bottom(para)


def add_footer(doc):
    """页脚：居中，'第 X 页 / 共 Y 页'"""
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False

    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 清除已有内容
    for r in para.runs:
        r.text = ''

    def add_text(text):
        r = para.add_run(text)
        _set_font(r, FONT_FOOTER, SIZE_FOOTER)
        return r

    def add_field(field_name):
        """添加域（兼容 WPS/Word）"""
        r = para.add_run()
        # begin
        fc1 = OxmlElement('w:fldChar')
        fc1.set(qn('w:fldCharType'), 'begin')
        # instrText
        it = OxmlElement('w:instrText')
        it.set(qn('xml:space'), 'preserve')
        it.text = f' {field_name} '
        # end
        fc2 = OxmlElement('w:fldChar')
        fc2.set(qn('w:fldCharType'), 'end')
        r._element.clear()
        r._element.append(fc1)
        r._element.append(it)
        r._element.append(fc2)
        _set_font(r, FONT_FOOTER, SIZE_FOOTER)

    add_text('第 ')
    add_field('PAGE')
    add_text(' 页 / 共 ')
    add_field('NUMPAGES')
    add_text(' 页')


def parse_content(doc, content):
    """将纯文本内容按公文标准写入 Word"""
    if not content:
        return

    lines = content.split('\n')
    table_rows = []
    in_table = False

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            return
        rows_data = []
        for line in table_rows:
            line = line.strip()
            if not line or re.match(r'^[\|\-\s]+$', line):
                continue
            rows_data.append([c.strip() for c in line.strip('|').split('|')])
        if len(rows_data) >= 2:
            table = doc.add_table(rows=len(rows_data), cols=len(rows_data[0]))
            table.style = 'Table Grid'
            for r, row in enumerate(rows_data):
                for c, text in enumerate(row):
                    cell = table.rows[r].cells[c]
                    cell.text = text
                    for p in cell.paragraphs:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if r == 0 else WD_ALIGN_PARAGRAPH.LEFT
                        for run in p.runs:
                            _set_font(run, FONT_BODY if r > 0 else FONT_HEADING1, SIZE_BODY, r == 0)
        table_rows = []
        in_table = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            flush_table()
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.5
            continue

        # 表格行
        if stripped.startswith('|'):
            table_rows.append(stripped)
            in_table = True
            continue
        else:
            if in_table:
                flush_table()

        # 判断段落类型
        is_heading = re.match(r'^[一二三四五六七八九十]+[、\.．]', stripped)
        is_chapter = re.match(r'^第[一二三四五六七八九十]+[章节篇]', stripped)
        is_paren = re.match(r'^[（\(][一二三四五六七八九十]+[）\)]', stripped)
        is_number = re.match(r'^\d+[．.、]', stripped)

        if is_heading or is_chapter or is_paren or is_number:
            # 标题段落
            p = doc.add_paragraph()
            run = p.add_run(stripped)
            _set_font(run, FONT_HEADING2, SIZE_HEADING2, bold=True)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
        else:
            # 普通正文（清除 markdown 符号）
            text = _clean(stripped)
            if text:
                p = doc.add_paragraph()
                run = p.add_run(text)
                _set_font(run, FONT_BODY, SIZE_BODY)
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.first_line_indent = Cm(0.74)  # 约 2 中文字符

    flush_table()


def _clean(text):
    """清除 markdown 符号"""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'^#+\s*', '', text)
    text = re.sub(r'^[-*+]\s+', '', text)
    text = re.sub(r'^\d+\.\s+', '', text)
    return text.strip()


def create_word_doc(output_path, title='', content='', company_name=None, logo_path=None):
    """
    生成国家公文标准 Word 文档（WPS/Word 双兼容）

    参数:
        output_path: 输出路径（必需）
        title: 文档标题（可选）
        content: 正文内容（可选），支持纯文本
        company_name: 公司名（可选，默认自动获取）
        logo_path: LOGO 路径（可选，默认自动获取）
    """
    doc = Document()

    # 页面边距（GB/T 9704-2012）
    for sec in doc.sections:
        sec.top_margin = Cm(MARGIN_TOP)
        sec.bottom_margin = Cm(MARGIN_BOTTOM)
        sec.left_margin = Cm(MARGIN_LEFT)
        sec.right_margin = Cm(MARGIN_RIGHT)
        sec.header_distance = Cm(1.5)
        sec.footer_distance = Cm(1.5)

    # 公司信息
    info = get_company_info()
    logo = logo_path or info.get('logo_path')
    company = company_name or info.get('company_name', DEFAULT_COMPANY_NAME)

    # 页眉页脚
    add_header(doc, logo, company)
    add_footer(doc)

    # 默认样式
    style = doc.styles['Normal']
    style.font.name = FONT_BODY
    style.font.size = Pt(SIZE_BODY)
    style._element.find(qn('w:rPr')).find(qn('w:rFonts')).set(qn('w:eastAsia'), FONT_BODY)

    # 文档标题（居中，黑体二号加粗）
    if title:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        _set_font(run, FONT_HEADING1, SIZE_TITLE, bold=True)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(12)

    # 正文
    parse_content(doc, content)

    doc.save(output_path)
    print(f'✅ 文档已生成: {output_path}')
    return output_path


if __name__ == '__main__':
    args = sys.argv
    output = args[1] if len(args) > 1 else 'output.docx'
    title = args[2] if len(args) > 2 else ''
    content = args[3] if len(args) > 3 else ''
    create_word_doc(output, title, content)
