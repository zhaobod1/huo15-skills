#!/usr/bin/env python3
"""火一五小红书周/月创作复盘 — 自动生成。

数据来源
========
- `~/.xiaohongshu/posts.jsonl`        — publish_helper 写的起草日志
- `~/.xiaohongshu/snapshots.jsonl`    — track_post 写的互动快照
- `~/.xiaohongshu/profile/feedback.jsonl` — coach 的反馈日志

输出
====
一份 markdown 复盘，包含：
1. 时段内起草 / 发布 / 跟踪状况
2. 互动表现：最爆 / 最沉的笔记
3. 风格画像变化（如果 baseline 重新跑过）
4. 反馈总结：你最常 reject 哪类建议
5. 下周建议：哪类选题该多做 / 该少做

用法
----

    python3 weekly_review.py                     # 最近 7 天
    python3 weekly_review.py --days 30           # 最近 30 天（月度）
    python3 weekly_review.py --out review.md     # 保存到文件 + 写入 reviews/
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore  # noqa: E402


def _parse_dt(s: str) -> dt.datetime | None:
    if not s:
        return None
    try:
        return dt.datetime.fromisoformat(s)
    except ValueError:
        return None


def _within(s: str, days: int) -> bool:
    d = _parse_dt(s)
    if not d:
        return False
    return (dt.datetime.now() - d).total_seconds() < days * 86400


def build_review(store: ProfileStore, days: int) -> str:
    posts = store.load_posts()
    snaps = store.load_snapshots()
    feedback = [fb.to_dict() for fb in store.load_feedback()]
    profile = store.load_style()

    in_range = [p for p in posts if _within(p.get("drafted_at", ""), days)]
    drafted = len(in_range)
    published = sum(1 for p in in_range if p.get("note_id"))

    # 最新快照 by note_id
    latest_snap: Dict[str, Dict[str, Any]] = {}
    for s in snaps:
        nid = s.get("note_id", "")
        if not nid:
            continue
        prev = latest_snap.get(nid)
        if not prev or s.get("snapshot_at", "") > prev.get("snapshot_at", ""):
            latest_snap[nid] = s

    # 排互动
    perf: List[Dict[str, Any]] = []
    for p in in_range:
        nid = p.get("note_id", "")
        if nid and nid in latest_snap:
            s = latest_snap[nid]
            engagement = s["liked"] + s["collected"] + s["comment"]
            perf.append({
                "title": p.get("title", "(无)"),
                "score": p.get("score", 0),
                "liked": s["liked"], "collected": s["collected"],
                "comment": s["comment"], "engagement": engagement,
                "drafted_at": p.get("drafted_at", ""),
            })
    perf.sort(key=lambda x: -x["engagement"])

    # 反馈总结
    fb_in_range = [f for f in feedback if _within(f.get("at", ""), days)]
    rejected: collections.Counter = collections.Counter()
    accepted: collections.Counter = collections.Counter()
    for f in fb_in_range:
        key = (f.get("rule_key") or "").split(":", 1)[0]
        if f.get("reaction") == "reject":
            rejected[key] += 1
        elif f.get("reaction") == "accept":
            accepted[key] += 1

    # 渲染
    parts = []
    title_period = "周" if days <= 7 else f"近{days}天"
    parts.append(f"# 火一五小红书 {title_period}创作复盘\n")
    parts.append(f"_生成于 {dt.datetime.now().isoformat(timespec='minutes')}_\n")
    parts.append(f"_档案：{store.root}_\n")

    parts.append("## 一、产出概况\n")
    parts.append(f"- 起草：**{drafted}** 篇")
    parts.append(f"- 发布（已回填 note_id）：**{published}** 篇")
    parts.append(f"- 拉到快照：**{len(perf)}** 篇\n")

    if perf:
        parts.append("## 二、互动表现\n")
        parts.append("| 排名 | 标题 | 文案分 | 点赞 | 收藏 | 评论 | 互动合计 |")
        parts.append("|---|---|---|---|---|---|---|")
        for i, p in enumerate(perf[:10], 1):
            parts.append(f"| {i} | {p['title'][:30]} | {p['score']} | "
                         f"{p['liked']} | {p['collected']} | {p['comment']} | **{p['engagement']}** |")
        parts.append("")

        # 爆款 vs 平均
        avg = sum(x["engagement"] for x in perf) / len(perf)
        top1 = perf[0]
        if top1["engagement"] > avg * 2:
            parts.append(f"📈 **{top1['title']}** 互动 {top1['engagement']}，"
                         f"是平均（{avg:.0f}）的 {top1['engagement']/max(1,avg):.1f} 倍 — 这条值得复盘共性。\n")

    if rejected or accepted:
        parts.append("## 三、教练反馈\n")
        if rejected:
            parts.append(f"- 你最常 reject 的检查项：")
            for k, v in rejected.most_common(5):
                hint = " ← 可考虑跑 `profile_init.py evolve` 永久禁用" if v >= 3 else ""
                parts.append(f"  - {k}（{v} 次）{hint}")
        if accepted:
            parts.append(f"- 你最常 accept 的检查项：")
            for k, v in accepted.most_common(5):
                parts.append(f"  - {k}（{v} 次）")
        parts.append("")

    if profile.sample_count:
        parts.append("## 四、当前风格画像\n")
        parts.append(f"- 人设 / 赛道：{profile.persona or '?'} / {profile.niche or '?'}")
        parts.append(f"- 标题 {profile.avg_title_len} 字 / 正文 {profile.avg_content_len} 字 / "
                     f"{profile.emoji_per_post} emoji 每篇")
        if profile.favorite_formulas:
            top_f = sorted(profile.favorite_formulas.items(), key=lambda x: -x[1])[:3]
            parts.append(f"- 偏好公式：{', '.join(f'{k}({v})' for k, v in top_f)}")
        parts.append("")

    # 下周建议
    parts.append("## 五、下周建议\n")
    if drafted < 3:
        parts.append("- 🐢 起草数 < 3 篇 — 节奏偏慢，建议跑 `brainstorm.py` 找 1~2 个新选题")
    elif drafted > 7:
        parts.append("- 🚀 起草数偏多 — 留意是否有 '模板化' 风险，每一篇都问自己 '读者凭什么收藏'")
    if perf and perf[-1]["engagement"] < perf[0]["engagement"] / 5:
        parts.append("- 📊 最低和最高表现差距过大 — 复盘最低那一篇是哪个环节没做到位")
    if rejected and max(rejected.values()) >= 3:
        top_rej = rejected.most_common(1)[0][0]
        parts.append(f"- 🛠 反复拒绝「{top_rej}」检查 — 跑 `profile_init.py evolve` 让助手学到")
    parts.append("- 把这周最爆的 1 篇加到 baseline：`profile_init.py add path/to/note.json`")

    return "\n".join(parts) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(prog="weekly_review.py", description="周/月创作复盘")
    p.add_argument("--days", type=int, default=7, help="时间窗口（天）")
    p.add_argument("--out", default="", help="输出路径（不填打印到 stdout，并自动写入 reviews/）")
    args = p.parse_args()

    store = ProfileStore()
    text = build_review(store, args.days)

    # 总是存一份到 reviews/
    fname = f"review_{dt.datetime.now().strftime('%Y%m%d_%H%M')}_{args.days}d.md"
    saved = store.reviews_dir / fname
    saved.write_text(text, encoding="utf-8")

    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"✓ 报告已写入 {args.out}", file=sys.stderr)
    else:
        print(text)
    print(f"✓ 已归档到 {saved}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
