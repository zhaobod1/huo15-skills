#!/usr/bin/env python3
"""火一五小红书"草稿管理" — 版本化、可对比、可追踪改进。

为什么需要
==========
之前草稿散在 /tmp/draft.md, ~/Desktop/v2.md... 改稿没记录、进步无法看。
drafts.py 把每个主题做成"草稿包"，自动版本号、自动 6 维分对比。

存档结构
========
~/.xiaohongshu/drafts/
  2026-04-28-fuye-xiaban-hou/         # YYYY-MM-DD-<slug>
    ├── meta.json                      # topic / created_at / scores
    ├── v01.md                         # 初稿
    ├── v02.md                         # 第二版
    └── v03.md                         # 终稿（promote 后）

用法
----

    drafts new --topic "下班后副业"               # 新建草稿
    drafts new --topic X --from /tmp/v1.md       # 用现有文件做初稿
    drafts add <id> /tmp/improved.md             # 加新版（自动 v02, v03...）
    drafts list                                  # 列所有草稿（最近优先）
    drafts show <id>                             # 看最新版内容
    drafts show <id> v01                         # 看指定版本
    drafts diff <id>                             # 对比 v_n vs v_{n-1} 的 6 维分
    drafts diff <id> v01..v03                    # 对比指定范围
    drafts edit <id>                             # 用 $EDITOR 打开最新版
    drafts promote <id>                          # 标记终稿，输出路径给 publish
    drafts archive <id>                          # 归档到 archived/
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))

from xhs_aesthetic import aesthetic_score  # noqa: E402
from xhs_writer import load_draft, score_post  # noqa: E402


def drafts_root() -> Path:
    base = os.environ.get("XHS_DRAFTS_DIR")
    if base:
        return Path(os.path.expanduser(base))
    return Path(os.path.expanduser("~/.xiaohongshu/drafts"))


def _slugify(text: str) -> str:
    """把中文/英文主题词转成文件夹友好的 slug。"""
    s = text.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^\w一-鿿\-]", "", s)
    return s[:30] or "draft"


def _draft_id(topic: str, when: Optional[dt.date] = None) -> str:
    when = when or dt.date.today()
    return f"{when.isoformat()}-{_slugify(topic)}"


# =====================================================================
# Meta + IO
# =====================================================================


@dataclass
class DraftMeta:
    draft_id: str
    topic: str
    created_at: str
    updated_at: str = ""
    versions: List[Dict[str, Any]] = field(default_factory=list)
    promoted: bool = False
    note_id: str = ""           # 发布后填回

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_meta(draft_dir: Path) -> Optional[DraftMeta]:
    p = draft_dir / "meta.json"
    if not p.exists():
        return None
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return DraftMeta(**{k: v for k, v in d.items() if k in DraftMeta.__dataclass_fields__})
    except (json.JSONDecodeError, TypeError):
        return None


def save_meta(draft_dir: Path, meta: DraftMeta) -> None:
    meta.updated_at = dt.datetime.now().isoformat(timespec="seconds")
    (draft_dir / "meta.json").write_text(
        json.dumps(meta.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def latest_version(draft_dir: Path) -> Optional[Path]:
    versions = sorted(draft_dir.glob("v*.md"))
    return versions[-1] if versions else None


def all_versions(draft_dir: Path) -> List[Path]:
    return sorted(draft_dir.glob("v*.md"))


def next_version_path(draft_dir: Path) -> Path:
    n = len(list(draft_dir.glob("v*.md"))) + 1
    return draft_dir / f"v{n:02d}.md"


def find_draft_dir(draft_id: str) -> Optional[Path]:
    """允许部分匹配 — drafts show fuye 也能找到 2026-04-28-fuye-xxx。"""
    root = drafts_root()
    if not root.exists():
        return None
    direct = root / draft_id
    if direct.is_dir():
        return direct
    # 模糊匹配
    candidates = [d for d in root.iterdir()
                  if d.is_dir() and draft_id in d.name]
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        print(f"⚠️ 找到多个匹配：{[c.name for c in candidates]}", file=sys.stderr)
        return None
    return None


# =====================================================================
# 子命令
# =====================================================================


def cmd_new(args: argparse.Namespace) -> int:
    if not args.topic:
        print("❌ --topic 必填", file=sys.stderr)
        return 1
    did = _draft_id(args.topic)
    root = drafts_root()
    root.mkdir(parents=True, exist_ok=True)
    draft_dir = root / did
    if draft_dir.exists() and not args.force:
        print(f"⚠️ 已存在：{draft_dir}（加 --force 覆盖）", file=sys.stderr)
        return 1
    draft_dir.mkdir(parents=True, exist_ok=True)

    meta = DraftMeta(
        draft_id=did, topic=args.topic,
        created_at=dt.datetime.now().isoformat(timespec="seconds"),
    )

    # 初稿来源
    if args.from_file:
        src = Path(args.from_file)
        if not src.exists():
            print(f"❌ 找不到文件 {src}", file=sys.stderr)
            return 1
        v01 = draft_dir / "v01.md"
        shutil.copy(src, v01)
        scores = _score_file(v01)
        meta.versions.append({"version": "v01", "from": str(src), **scores})
        print(f"✓ 创建草稿 {did}")
        print(f"  v01 内容来自：{src}")
        print(f"  v01 分数：工程 {scores['engineering']} / Allen {scores['aesthetic']}")
    else:
        # 空模板
        v01 = draft_dir / "v01.md"
        v01.write_text(f"# {args.topic}\n\n（在这里写正文）\n\n#话题1 #话题2\n", encoding="utf-8")
        meta.versions.append({"version": "v01", "from": "template"})
        print(f"✓ 创建草稿 {did}（空模板）")

    save_meta(draft_dir, meta)
    print(f"\n下一步：")
    print(f"  $EDITOR {v01}")
    print(f"  python3 scripts/drafts.py add {did} <修改后路径>")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    draft_dir = find_draft_dir(args.draft_id)
    if not draft_dir:
        print(f"❌ 找不到草稿 {args.draft_id}", file=sys.stderr)
        return 1
    src = Path(args.path)
    if not src.exists():
        print(f"❌ 找不到 {src}", file=sys.stderr)
        return 1
    next_path = next_version_path(draft_dir)
    shutil.copy(src, next_path)
    scores = _score_file(next_path)
    meta = load_meta(draft_dir) or DraftMeta(
        draft_id=draft_dir.name, topic=draft_dir.name,
        created_at=dt.datetime.now().isoformat(timespec="seconds"),
    )
    meta.versions.append({"version": next_path.stem, "from": str(src), **scores})
    save_meta(draft_dir, meta)
    print(f"✓ 已加 {next_path.stem}：工程 {scores['engineering']} / Allen {scores['aesthetic']}")
    if len(meta.versions) >= 2:
        prev = meta.versions[-2]
        cur = meta.versions[-1]
        print(f"  对比 {prev['version']} → {cur['version']}：")
        print(f"    工程 {prev.get('engineering','?')} → {cur['engineering']} "
              f"({_delta(prev.get('engineering'), cur['engineering'])})")
        print(f"    Allen {prev.get('aesthetic','?')} → {cur['aesthetic']} "
              f"({_delta(prev.get('aesthetic'), cur['aesthetic'])})")
    return 0


def _delta(a: Any, b: Any) -> str:
    if a is None or b is None:
        return "?"
    diff = b - a
    return f"{'+' if diff >= 0 else ''}{diff}"


def cmd_list(args: argparse.Namespace) -> int:
    root = drafts_root()
    if not root.exists():
        print("（还没有草稿。用 drafts new --topic 创建）")
        return 0
    drafts = sorted([d for d in root.iterdir() if d.is_dir() and not d.name.startswith(".")],
                    key=lambda d: d.stat().st_mtime, reverse=True)
    if not drafts:
        print("（还没有草稿）")
        return 0
    print(f"📂 共 {len(drafts)} 个草稿（最近优先）：\n")
    for d in drafts[:args.limit]:
        meta = load_meta(d)
        if not meta:
            print(f"  {d.name}  (没有 meta)")
            continue
        n_versions = len(meta.versions)
        latest = meta.versions[-1] if meta.versions else {}
        promote = "🚀" if meta.promoted else " "
        print(f"  {promote} {d.name}")
        print(f"      主题: {meta.topic}    {n_versions} 版    "
              f"工程 {latest.get('engineering', '?')} / Allen {latest.get('aesthetic', '?')}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    draft_dir = find_draft_dir(args.draft_id)
    if not draft_dir:
        print(f"❌ 找不到草稿 {args.draft_id}", file=sys.stderr)
        return 1
    if args.version:
        path = draft_dir / f"{args.version}.md"
        if not path.exists():
            print(f"❌ 找不到版本 {args.version}", file=sys.stderr)
            return 1
    else:
        path = latest_version(draft_dir)
    if not path:
        print("❌ 草稿目录里没有版本文件", file=sys.stderr)
        return 1
    print(f"=== {path.name} ===\n")
    print(path.read_text(encoding="utf-8"))
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    draft_dir = find_draft_dir(args.draft_id)
    if not draft_dir:
        print(f"❌ 找不到草稿 {args.draft_id}", file=sys.stderr)
        return 1
    versions = all_versions(draft_dir)
    if len(versions) < 2:
        print("（只有 1 个版本，没法 diff。用 drafts add 加新版）")
        return 0

    # 解析 v01..v03 范围
    if args.range and ".." in args.range:
        a, b = args.range.split("..", 1)
        v_a = draft_dir / f"{a}.md"
        v_b = draft_dir / f"{b}.md"
        if not v_a.exists() or not v_b.exists():
            print(f"❌ 范围版本不存在：{args.range}", file=sys.stderr)
            return 1
    else:
        v_a, v_b = versions[-2], versions[-1]

    sa = _score_file(v_a)
    sb = _score_file(v_b)

    print("=" * 60)
    print(f"📊 {v_a.stem} → {v_b.stem}  6 维分对比")
    print("=" * 60)
    print()
    print(f"  工程总分：{sa['engineering']} → {sb['engineering']}  "
          f"({_delta(sa['engineering'], sb['engineering'])})")
    print(f"  Allen 总分：{sa['aesthetic']} → {sb['aesthetic']}  "
          f"({_delta(sa['aesthetic'], sb['aesthetic'])})")
    print()
    print("  Allen 各维度（0~10）：")
    labels = {"breath": "留白度", "ai_speak": "去AI腔", "teach_vs_lead": "带读者",
              "resonance": "共鸣度", "invitation": "邀请语", "jarvis_trap": "范本范"}
    for k, label in labels.items():
        ka = sa["aesthetic_breakdown"].get(k, "?")
        kb = sb["aesthetic_breakdown"].get(k, "?")
        delta = _delta(ka, kb) if isinstance(ka, int) and isinstance(kb, int) else "?"
        emoji = "📈" if isinstance(ka, int) and isinstance(kb, int) and kb > ka else \
                "➖" if ka == kb else "📉"
        print(f"    {emoji} {label:<8} {ka} → {kb}  ({delta})")
    print()

    # 最大改进 / 最大退步
    if isinstance(sa["aesthetic_breakdown"], dict) and isinstance(sb["aesthetic_breakdown"], dict):
        deltas = {k: sb["aesthetic_breakdown"].get(k, 0) - sa["aesthetic_breakdown"].get(k, 0)
                  for k in labels if k in sa["aesthetic_breakdown"] and k in sb["aesthetic_breakdown"]}
        if deltas:
            best = max(deltas, key=deltas.get)
            worst = min(deltas, key=deltas.get)
            if deltas[best] > 0:
                print(f"  🎯 最大改进：{labels[best]} +{deltas[best]} 分")
            if deltas[worst] < 0:
                print(f"  ⚠️  最大退步：{labels[worst]} {deltas[worst]} 分")
    return 0


def cmd_edit(args: argparse.Namespace) -> int:
    draft_dir = find_draft_dir(args.draft_id)
    if not draft_dir:
        print(f"❌ 找不到草稿 {args.draft_id}", file=sys.stderr)
        return 1
    path = latest_version(draft_dir)
    if not path:
        print("❌ 没有版本文件", file=sys.stderr)
        return 1
    editor = os.environ.get("EDITOR", "vim")
    subprocess.call([editor, str(path)])
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    draft_dir = find_draft_dir(args.draft_id)
    if not draft_dir:
        print(f"❌ 找不到草稿 {args.draft_id}", file=sys.stderr)
        return 1
    meta = load_meta(draft_dir)
    if not meta:
        print("❌ meta.json 缺失", file=sys.stderr)
        return 1
    meta.promoted = True
    save_meta(draft_dir, meta)
    path = latest_version(draft_dir)
    print(f"🚀 已标记为终稿：{path}")
    print(f"\n下一步：")
    print(f"  python3 scripts/publish_helper.py --in {path}")
    return 0


def cmd_archive(args: argparse.Namespace) -> int:
    draft_dir = find_draft_dir(args.draft_id)
    if not draft_dir:
        print(f"❌ 找不到草稿 {args.draft_id}", file=sys.stderr)
        return 1
    archive_root = drafts_root().parent / "drafts_archived"
    archive_root.mkdir(parents=True, exist_ok=True)
    target = archive_root / draft_dir.name
    shutil.move(str(draft_dir), str(target))
    print(f"📦 已归档到 {target}")
    return 0


# =====================================================================
# 工具
# =====================================================================


def _score_file(path: Path) -> Dict[str, Any]:
    draft = load_draft(str(path))
    eng = score_post(draft.title, draft.content, draft.tags)
    aes = aesthetic_score(draft.title, draft.content)
    return {
        "engineering": eng.total,
        "aesthetic": aes.total,
        "aesthetic_breakdown": {k: v["score"] for k, v in aes.by_dim.items()},
    }


# =====================================================================
# 入口
# =====================================================================


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="drafts.py", description="草稿版本管理")
    sub = p.add_subparsers(dest="cmd", required=True)

    pn = sub.add_parser("new", help="新建草稿")
    pn.add_argument("--topic", required=True)
    pn.add_argument("--from", dest="from_file", default="", help="用现有文件做初稿")
    pn.add_argument("--force", action="store_true")
    pn.set_defaults(func=cmd_new)

    pa = sub.add_parser("add", help="加新版（v02, v03...）")
    pa.add_argument("draft_id")
    pa.add_argument("path")
    pa.set_defaults(func=cmd_add)

    pl = sub.add_parser("list", help="列所有草稿")
    pl.add_argument("--limit", type=int, default=20)
    pl.set_defaults(func=cmd_list)

    ps = sub.add_parser("show", help="查看草稿内容")
    ps.add_argument("draft_id")
    ps.add_argument("version", nargs="?", default="")
    ps.set_defaults(func=cmd_show)

    pd = sub.add_parser("diff", help="对比版本的 6 维分变化")
    pd.add_argument("draft_id")
    pd.add_argument("range", nargs="?", default="", help="如 v01..v03；空 = 最新两版")
    pd.set_defaults(func=cmd_diff)

    pe = sub.add_parser("edit", help="$EDITOR 打开最新版")
    pe.add_argument("draft_id")
    pe.set_defaults(func=cmd_edit)

    pp = sub.add_parser("promote", help="标记终稿")
    pp.add_argument("draft_id")
    pp.set_defaults(func=cmd_promote)

    pr = sub.add_parser("archive", help="归档")
    pr.add_argument("draft_id")
    pr.set_defaults(func=cmd_archive)

    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
