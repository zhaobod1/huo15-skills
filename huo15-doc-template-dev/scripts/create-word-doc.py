#!/usr/bin/env python3
"""
create-word-doc.py - 国家公文标准 Word 文档生成器

国家公文标准 GB/T 9704-2012：
  - 页面边距：上 3.7cm，下 3.5cm，左 2.8cm，右 2.6cm
  - 正文字体：仿宋，小四（12pt），行距 1.5
  - 一级标题：黑体，三号（15pt），加粗
  - 二级标题：楷体，四号（12pt），加粗
  - 页眉：左对齐，LOGO + 公司名称，之间空一格
  - 页脚：居中，"第 X 页 / 共 Y 页"，仿宋

用法：
    python create-word-doc.py <输出路径> [标题] [正文内容]
    python create-word-doc.py report.docx "项目报告" "正文内容..."

或者在 Python 中导入：
    from create_word_doc import create_word_doc
    create_word_doc("output.docx", "标题", "正文...")
"""

import sys
import os
import re
import ssl
import json
import urllib.request
import urllib.error
import xmlrpc.client
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============== 国家公文标准常量 ==============
MARGIN_TOP = 3.7       # cm
MARGIN_BOTTOM = 3.5    # cm
MARGIN_LEFT = 2.8      # cm
MARGIN_RIGHT = 2.6     # cm
HEADER_DISTANCE = Cm(1.5)
FOOTER_DISTANCE = Cm(1.5)

# 默认字体
FONT_BODY = '仿宋'      # 正文
FONT_HEADING1 = '黑体'  # 一级标题
FONT_HEADING2 = '楷体'  # 二级标题
FONT_HEADER = '黑体'    # 页眉
FONT_FOOTER = '仿宋'    # 页脚

SIZE_BODY = 12          # 小四
SIZE_HEADING1 = 15       # 三号
SIZE_HEADING2 = 12       # 四号
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
    info = {
        'company_name': DEFAULT_COMPANY_NAME,
        'logo_path': None,
    }

    # 1. 检查本地缓存
    if os.path.exists(DEFAULT_LOGO_PATH) and os.path.getsize(DEFAULT_LOGO_PATH) > 1000:
        info['logo_path'] = DEFAULT_LOGO_PATH
        return info

    # 2. 尝试从 Odoo 系统获取
    try:
        agent_id = os.environ.get('OC_AGENT_ID', 'main')
        agents_dir = os.path.expanduser('~/.openclaw/agents')
        creds_file = os.path.join(agents_dir, agent_id, 'odoo_creds.json')

        if os.path.exists(creds_file):
            with open(creds_file, 'r') as f:
                creds = json.load(f)

            cfg_file = os.path.expanduser('~/.openclaw/openclaw.json')
            if os.path.exists(cfg_file):
                with open(cfg_file, 'r') as f:
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
                        # 获取公司信息
                        company_data = models.execute_kw(db, uid, password, 'res.company',
                            'search_read', [[('id', '=', 1)]],
                            {'fields': ['name', 'logo'], 'limit': 1})

                        if company_data:
                            info['company_name'] = company_data[0].get('name', DEFAULT_COMPANY_NAME)
                            logo_id = company_data[0].get('logo')
                            if logo_id:
                                logo_url = f'{url}/web/image/res.company/{logo_id}/logo'
                                _download_logo(logo_url, DEFAULT_LOGO_PATH)
                                if os.path.exists(DEFAULT_LOGO_PATH):
                                    info['logo_path'] = DEFAULT_LOGO_PATH
    except Exception as e:
        print(f"获取公司信息失败，使用默认值: {e}")

    # 3. 备用 LOGO
    if not info['logo_path']:
        _download_logo(FALLBACK_LOGO_URL, DEFAULT_LOGO_PATH)
        if os.path.exists(DEFAULT_LOGO_PATH):
            info['logo_path'] = DEFAULT_LOGO_PATH

    return info


def _download_logo(url, dest_path):
    """下载 LOGO 到本地"""
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        return
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"✓ LOGO 已下载: {dest_path}")
    except Exception as e:
        print(f"⚠ LOGO 下载失败: {e}")


def set_font(run, font_name, size, bold=False):
    """设置中文字体（兼容 WPS 和 Word）"""
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size)
    run.bold = bold


def add_header(doc, logo_path, company_name):
    """
    添加页眉：LOGO + 公司名称，左对齐，紧密挨着
    """
    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False

    # 清除默认段落
    for para in header.paragraphs:
        para.clear()

    # 创建同一行：LOGO + 公司名称
    para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # LOGO（高度 1.0cm）
    if logo_path and os.path.exists(logo_path):
        try:
            run = para.add_run()
            run.add_picture(logo_path, height=Cm(1.0))
        except Exception as e:
            print(f"⚠ 添加 LOGO 失败: {e}")

    # 公司名称（紧跟 LOGO，中间一个空格）
    run = para.add_run(f' {company_name}')
    set_font(run, FONT_HEADER, SIZE_HEADER)

    # 页眉底线（细线分隔）
    pPr = OxmlElement('w:pPr')
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '000000')
    pBdr.append(bottom)
    pPr.append(pBdr)
    para._element.insert(0, pPr)


def add_footer(doc):
    """
    添加页脚：居中，"第 X 页 / 共 Y 页"
    """
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False

    if not footer.paragraphs:
        para = footer.add_paragraph()
    else:
        para = footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for run in para.runs:
        run.text = ''

    # "第 "
    r1 = para.add_run('第 ')
    set_font(r1, FONT_FOOTER, SIZE_FOOTER)

    # PAGE 域
    fc1 = OxmlElement('w:fldChar')
    fc1.set(qn('w:fldCharType'), 'begin')
    it1 = OxmlElement('w:instrText')
    it1.set(qn('xml:space'), 'preserve')
    it1.text = ' PAGE '
    fc2 = OxmlElement('w:fldChar')
    fc2.set(qn('w:fldCharType'), 'end')
    r_page = para.add_run()
    r_page._element.clear()
    r_page._element.append(fc1)
    r_page._element.append(it1)
    r_page._element.append(fc2)
    set_font(r_page, FONT_FOOTER, SIZE_FOOTER)

    # " 页 / 共 "
    r2 = para.add_run(' 页 / 共 ')
    set_font(r2, FONT_FOOTER, SIZE_FOOTER)

    # NUMPAGES 域
    fc3 = OxmlElement('w:fldChar')
    fc3.set(qn('w:fldCharType'), 'begin')
    it2 = OxmlElement('w:instrText')
    it2.set(qn('xml:space'), 'preserve')
    it2.text = ' NUMPAGES '
    fc4 = OxmlElement('w:fldChar')
    fc4.set(qn('w:fldCharType'), 'end')
    r_total = para.add_run()
    r_total._element.clear()
    r_total._element.append(fc3)
    r_total._element.append(it2)
    r_total._element.append(fc4)
    set_font(r_total, FONT_FOOTER, SIZE_FOOTER)

    # " 页"
    r3 = para.add_run(' 页')
    set_font(r3, FONT_FOOTER, SIZE_FOOTER)


def parse_content_to_doc(doc, content):
    """
    将纯文本内容按国家公文标准格式写入 Word
    - 每段之间空一行
    - 不保留任何 markdown 语法符号
    """
    if not content:
        return

    lines = content.split('\n')
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        rows_data = []
        for line in table_rows:
            line = line.strip()
            if not line or re.match(r'^[\|\-\s]+$', line):
                continue
            cells = [c.strip() for c in line.strip('|').split('|')]
            rows_data.append(cells)
        if len(rows_data) >= 2:
            table = doc.add_table(rows=len(rows_data), cols=len(rows_data[0]))
            table.style = 'Table Grid'
            for r, row in enumerate(rows_data):
                for c, cell_text in enumerate(row):
                    cell = table.rows[r].cells[c]
                    cell.text = cell_text
                    for para in cell.paragraphs:
                        para.alignment = WD_ALIGN_PARAGRAPH.CENTER if r == 0 else WD_ALIGN_PARAGRAPH.LEFT
                        for run in para.runs:
                            set_font(run, FONT_BODY if r > 0 else FONT_HEADING1, SIZE_BODY, r == 0)
        table_rows = []

    for line in lines:
        stripped = line.strip()

        # 空行
        if not stripped:
            flush_table()
            doc.add_paragraph()
            continue

        # 表格行
        if stripped.startswith('|'):
            if re.match(r'^[\|\-\s]+$', stripped):
                continue
            table_rows.append(stripped)
            in_table = True
            continue
        else:
            if in_table:
                flush_table()
                in_table = False

        # 标题行（以 "第X章"、"一、"、"（一）" 等开头）
        if re.match(r'^[一二三四五六七八九十]+[、\.]', stripped) or \
           re.match(r'^第[一二三四五六七八九十]+[章节]', stripped) or \
           re.match(r'^[（\(][一二三四五六七八九十]+[）\)]', stripped):
            p = doc.add_paragraph()
            run = p.add_run(stripped)
            set_font(run, FONT_HEADING2, SIZE_HEADING2, bold=True)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
        # 普通段落（去除 ** ## 之类的 markdown 符号）
        else:
            clean_text = _clean_text(stripped)
            if clean_text:
                p = doc.add_paragraph()
                run = p.add_run(clean_text)
                set_font(run, FONT_BODY, SIZE_BODY)
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.first_line_indent = Cm(0.85)  # 首行缩进2字符

    # 处理最后残留的表格
    flush_table()


def _clean_text(text):
    """清除 markdown 符号但保留纯文本"""
    # 去除 **bold**、__underline__、*italic* 等符号
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    # 去除 [text](url) 链接
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # 去除 ![alt](url) 图片
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    # 去除 # 标题符号（但保留标题文字）
    text = re.sub(r'^#+\s*', '', text)
    # 去除列表符号
    text = re.sub(r'^[-*+]\s+', '', text)
    text = re.sub(r'^\d+\.\s+', '', text)
    return text.strip()


def create_word_doc(output_path, title='', content='', company_name=None, logo_path=None):
    """
    生成符合国家公文标准的 Word 文档

    参数:
        output_path: 输出文件路径（必需）
        title: 文档标题（可选）
        content: 正文内容（可选），支持纯文本
        company_name: 公司名称（可选，默认自动获取）
        logo_path: LOGO 路径（可选，默认自动获取）

    示例:
        create_word_doc("合同.docx", "销售合同", "一、甲方...\n二、乙方...")
    """
    # 1. 创建文档
    doc = Document()

    # 2. 设置页面边距（GB/T 9704-2012）
    for section in doc.sections:
        section.top_margin = Cm(MARGIN_TOP)
        section.bottom_margin = Cm(MARGIN_BOTTOM)
        section.left_margin = Cm(MARGIN_LEFT)
        section.right_margin = Cm(MARGIN_RIGHT)
        section.header_distance = HEADER_DISTANCE
        section.footer_distance = FOOTER_DISTANCE

    # 3. 获取公司信息
    info = get_company_info()
    logo = logo_path or info.get('logo_path')
    company = company_name or info.get('company_name', DEFAULT_COMPANY_NAME)

    # 4. 添加页眉
    add_header(doc, logo, company)

    # 5. 添加页脚
    add_footer(doc)

    # 6. 设置默认样式
    style = doc.styles['Normal']
    style.font.name = FONT_BODY
    style.font.size = Pt(SIZE_BODY)
    style._element.rPr.rFonts.set(qn('w:eastAsia'), FONT_BODY)

    # 7. 添加标题（居中，黑体二号加粗）
    if title:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        set_font(run, FONT_HEADING1, SIZE_HEADING1 * 1.5, bold=True)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(12)

    # 8. 写入正文
    parse_content_to_doc(doc, content)

    # 9. 保存
    doc.save(output_path)
    print(f'✅ 文档已生成: {output_path}')
    return output_path


if __name__ == '__main__':
    output = sys.argv[1] if len(sys.argv) > 1 else 'output.docx'
    title = sys.argv[2] if len(sys.argv) > 2 else ''
    content = sys.argv[3] if len(sys.argv) > 3 else ''

    create_word_doc(output, title, content)
