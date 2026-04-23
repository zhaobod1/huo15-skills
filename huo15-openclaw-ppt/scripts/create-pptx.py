#!/usr/bin/env python3
"""
create-pptx.py - 通用 PPT 生成器（v2.0）

按风格（--style）+ JSON deck 规约生成 pptx。
支持两种输入形式：
  1. --spec deck.json          （完整 deck 规约）
  2. --cover "标题|副标题"      （快速生成单页试样）

可用风格：jobs-dark（默认） | xiaohongshu | xiaohongshu-portrait

公司名优先级：--company > ~/.huo15/company-info.json > 默认字符串
"""

import os
import sys
import json
import argparse
import importlib.util

from pptx import Presentation
from pptx.util import Inches

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from styles import get_style, list_styles
import pptx_toolkit as pk


def _load_company_name(explicit=None):
    if explicit:
        return explicit
    ci_path = os.path.expanduser('~/.huo15/company-info.json')
    if os.path.exists(ci_path):
        try:
            with open(ci_path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            return data.get('company_name') or '青岛火一五信息科技有限公司'
        except (OSError, json.JSONDecodeError):
            pass
    return '青岛火一五信息科技有限公司'


SLIDE_BUILDERS = {
    'cover': lambda prs, style, s, ctx: pk.cover_slide(
        prs, style,
        title=s.get('title', ''),
        subtitle=s.get('subtitle', ''),
        footnote=s.get('footnote', f"{ctx['company']}  ·  {ctx['year']}"),
    ),
    'section': lambda prs, style, s, ctx: pk.section_slide(
        prs, style,
        big_title=s.get('title', ''),
        sub=s.get('subtitle', ''),
    ),
    'list': lambda prs, style, s, ctx: pk.list_slide(
        prs, style,
        title=s.get('title', ''),
        en_subtitle=s.get('en_subtitle', ''),
        items=s.get('items', []),
        company=ctx['company'],
        page_no=ctx['page_no'],
    ),
    'quote': lambda prs, style, s, ctx: pk.quote_slide(
        prs, style,
        title=s.get('title', ''),
        en_subtitle=s.get('en_subtitle', ''),
        quote=s.get('quote', ''),
        author=s.get('author', ''),
        role=s.get('role', ''),
        image=s.get('image'),
        company=ctx['company'],
        page_no=ctx['page_no'],
    ),
    'end': lambda prs, style, s, ctx: pk.end_slide(
        prs, style,
        title=s.get('title', ''),
        sub=s.get('subtitle', ''),
        qrcodes=s.get('qrcodes'),
    ),
}


def build_presentation(spec, style_name, company):
    style = get_style(style_name)
    prs = Presentation()
    prs.slide_width = Inches(style.slide_width)
    prs.slide_height = Inches(style.slide_height)

    slides = spec.get('slides', [])
    ctx_common = {
        'company': company,
        'year': spec.get('year', ''),
    }

    for idx, slide_spec in enumerate(slides, start=1):
        stype = slide_spec.get('type', 'cover')
        builder = SLIDE_BUILDERS.get(stype)
        if builder is None:
            print(f'⚠️  未知 slide 类型: {stype}，跳过', file=sys.stderr)
            continue
        ctx = dict(ctx_common)
        ctx['page_no'] = idx
        builder(prs, style, slide_spec, ctx)
    return prs


def _quick_deck(args, company):
    title, _, subtitle = args.cover.partition('|')
    return {
        'slides': [
            {'type': 'cover', 'title': title.strip(),
             'subtitle': subtitle.strip(),
             'footnote': f'{company}  ·  {args.year or ""}'.strip(' ·')},
        ],
        'year': args.year or '',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='create-pptx',
        description='火一五 PPT 生成器（多风格）',
    )
    parser.add_argument('--output', '-o', required=True, help='输出 .pptx 路径')
    parser.add_argument('--style', default='jobs-dark',
                        help=f'风格名，可选：{" / ".join(list_styles())}')
    parser.add_argument('--spec', help='deck JSON 规约路径')
    parser.add_argument('--cover', help='快速生成单页封面，格式："标题|副标题"')
    parser.add_argument('--company', help='覆盖公司名（默认读 ~/.huo15/company-info.json）')
    parser.add_argument('--year', default='', help='封面底部标注年份')
    args = parser.parse_args(argv)

    if not args.spec and not args.cover:
        parser.error('必须提供 --spec <deck.json> 或 --cover "标题|副标题"')

    company = _load_company_name(args.company)

    if args.spec:
        with open(args.spec, 'r', encoding='utf-8') as fh:
            spec = json.load(fh)
    else:
        spec = _quick_deck(args, company)

    prs = build_presentation(spec, args.style, company)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or '.', exist_ok=True)
    prs.save(args.output)
    print(f'✅ 已生成: {args.output}（风格: {args.style}，幻灯片数: {len(spec.get("slides", []))}）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
