#!/usr/bin/env python3
"""创作哲学速查 — 动笔前的决策清单。

每次写小红书笔记前跑一下，30 秒过 8 个问题。
也可以单独深入某一层。

用法:
    python3 scripts/philosophy.py              # 速查：8 个问题
    python3 scripts/philosophy.py --layer 1    # 深入第一层：创作原点
    python3 scripts/philosophy.py --layer 2    # 深入第二层：创作支点
    python3 scripts/philosophy.py --layer 3    # 深入第三层：创作手艺
    python3 scripts/philosophy.py --layer 4    # 深入第四层：创作陷阱
    python3 scripts/philosophy.py --layer 5    # 深入第五层：创作系统
    python3 scripts/philosophy.py --mantra     # 只输出四句心法
    python3 scripts/philosophy.py --checklist  # 输出纯文本 8 问，可粘贴到草稿顶部
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _read_philosophy() -> str:
    path = _DATA_DIR / "creative_philosophy.md"
    if path.exists():
        return path.read_text()
    return ""


def _extract_section(text: str, header: str) -> str:
    """Extract a section between ## headers."""
    lines = text.split("\n")
    in_section = False
    result = []
    for line in lines:
        if line.startswith("## " + header):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            result.append(line)
    return "\n".join(result).strip()


def show_all():
    """速查：8 个问题 + 四句心法"""
    print(
        """
╔══════════════════════════════════════════════════════════╗
║      🖊️  火一五小红书创作哲学 — 动笔前速查              ║
╚══════════════════════════════════════════════════════════╝

  四句心法（写前 30 秒默念）：
  ─────────────────────────────────────────────
  1. 「好文案不是写出来的，是留出来的。」
  2. 「卖的是身份认同，不是商品本身。」
  3. 「站文案里面读文案，不是站在外面分析。」
  4. 「一流的糖衣，本身就是炮弹。」

  ─────────────────────────────────────────────
  动笔前 4 问：
  ─────────────────────────────────────────────
  □ 心象：我为谁写？（不是人口标签，是认知状态）
  □ AB 点：她现在怎么想？看完想让她怎么想？
  □ 核心体验：我卖的不是内容，是哪种感觉？
  □ 功课：涉及品牌/产品，我查了官方定位吗？

  动笔中 2 问：
  ─────────────────────────────────────────────
  □ 留白：这句话是把答案给她了，还是把空间留给她了？
  □ 五法：有没有出现配料/成分/参数/功能描述？有就改掉。

  写完后 2 问：
  ─────────────────────────────────────────────
  □ Jarvis 陷阱：我是在教「怎么做」还是在展示「什么样的人」？
  □ AI 腔：删掉所有「提升/优化/赋能/众所周知/首先其次最后」。

  ══════════════════════════════════════════════════════════
  深入某层：philosophy.py --layer 1~5
  只出心法：philosophy.py --mantra
  只出清单：philosophy.py --checklist
  ══════════════════════════════════════════════════════════
"""
    )


def show_layer(text: str, layer: int):
    """Show a specific layer of the philosophy."""
    layer_map = {
        1: "第一层：创作原点",
        2: "第二层：创作支点",
        3: "第三层：创作手艺",
        4: "第四层：创作陷阱",
        5: "第五层：创作系统",
    }
    header = layer_map.get(layer, "")
    if not header:
        print(f"没有第 {layer} 层，只有 1~5 层。")
        return

    section = _extract_section(text, header)
    if section:
        print(f"\n{'─' * 60}")
        print(f"  {header}")
        print(f"{'─' * 60}\n")
        print(section)
    else:
        print(f"未找到「{header}」章节。")


def show_mantra():
    """只输出四句心法"""
    print(
        """
  1. 「好文案不是写出来的，是留出来的。」— 留白让读者填情绪
  2. 「卖的是身份认同，不是商品本身。」— 把"卖"包装成"懂你"
  3. 「站文案里面读文案，不是站在外面分析。」— 文案是情境
  4. 「一流的糖衣，本身就是炮弹。」— 东东枪 041
"""
    )


def show_checklist():
    """输出纯文本 8 问，可粘贴到草稿顶部"""
    print(
        """## 动笔前
- [ ] 心象：我为谁写？（认知状态，不是人口标签）
- [ ] AB 点：她现在怎么想？→ 看完想让她怎么想？
- [ ] 核心体验：我卖的不是内容，是哪种感觉？
- [ ] 功课：涉及品牌/产品，查了官方定位吗？

## 动笔中
- [ ] 留白：这句话是把答案给她了，还是把空间留给她了？
- [ ] 五法：有没有出现配料/成分/参数/功能描述？

## 写完后
- [ ] Jarvis 陷阱：我是在教「怎么做」还是在展示「什么样的人」？
- [ ] AI 腔：「提升/优化/赋能/众所周知/首先其次最后」删了吗？
"""
    )


def main():
    parser = argparse.ArgumentParser(
        description="火一五创作哲学速查 — 动笔前的决策清单"
    )
    parser.add_argument(
        "--layer", type=int, choices=[1, 2, 3, 4, 5],
        help="深入某一层（1=原点 2=支点 3=手艺 4=陷阱 5=系统）"
    )
    parser.add_argument(
        "--mantra", action="store_true",
        help="只输出四句心法"
    )
    parser.add_argument(
        "--checklist", action="store_true",
        help="只输出纯文本 8 问清单，可粘贴到草稿顶部"
    )
    args = parser.parse_args()

    text = _read_philosophy()

    if args.mantra:
        show_mantra()
    elif args.checklist:
        show_checklist()
    elif args.layer:
        show_layer(text, args.layer)
    else:
        show_all()


if __name__ == "__main__":
    main()
