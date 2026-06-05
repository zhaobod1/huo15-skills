#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agenda.py — 火一五 Odoo「日历 / Calendar」事件与提醒管理（calendar.event + calendar.alarm）

> 脚本名特意叫 agenda（不叫 calendar），避免遮蔽 Python 标准库 calendar
> （odoo_utils / timesheet 都 import 了它）。

字段坑（详见 references/odoo-activity-calendar-api.md）：
  - start/stop 是 **Datetime / UTC**（脚本自动把你输入的本地时间转 UTC）。
  - 写 partner_ids 会自动建参与人记录（attendee），不用手动建。
  - 提醒 alarm 只有 notification / email 两类（无 sms）。

命令
  list      我的日程（默认本周）   --today/--month/--from --to
  show      事件详情（参与人/提醒）
  add       新建事件               --name --start --end|--duration --location --with --remind --allday
  cancel    删除事件               cancel <id> ...
  remind    给事件加提醒           remind <id> --before 30m [--type notification|email]

提醒/时长写法：30m=30分钟 / 2h=2小时 / 1d=1天（默认分钟）。

示例
  python3 agenda.py add --name "方案评审" --start "2026-06-10 10:00" --duration 1 --location 会议室A --with "张三,李四" --remind 30m
  python3 agenda.py list --today
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, render_table, to_utc, today

EVENT = "calendar.event"
ALARM = "calendar.alarm"


def _parse_remind(s) -> tuple[int, str]:
    s = str(s).strip().lower()
    unit = {"m": "minutes", "h": "hours", "d": "days"}
    if s and s[-1] in unit:
        return int(s[:-1]), unit[s[-1]]
    return int(s), "minutes"


def _resolve_partners(odoo: Odoo, s: str) -> list[int]:
    out = []
    for n in s.split(","):
        n = n.strip()
        if not n:
            continue
        if n in ("我", "me", "self"):
            uid = odoo.ensure_uid()
            pr = odoo.read("res.users", [uid], ["partner_id"])
            if pr and pr[0].get("partner_id"):
                out.append(pr[0]["partner_id"][0])
            continue
        if n.isdigit():
            out.append(int(n))
            continue
        r = odoo.name_search("res.partner", n, limit=1)
        if not r:
            raise OdooError(f"找不到联系人「{n}」。")
        out.append(r[0][0])
    return out


def _period(args):
    """返回 (utc_lo, utc_hi, 标签)。"""
    t = today()
    base = datetime.strptime(t, "%Y-%m-%d")
    if args.date_from or args.date_to:
        lo_d = args.date_from or t
        hi_d = args.date_to or t
        hi_next = (datetime.strptime(hi_d, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        return to_utc(lo_d + " 00:00:00"), to_utc(hi_next + " 00:00:00"), f"{lo_d}~{hi_d}"
    if args.today:
        lo, hi, label = base, base + timedelta(days=1), "今天"
    elif args.month:
        lo = base.replace(day=1)
        hi = (lo.replace(day=28) + timedelta(days=4)).replace(day=1)
        label = lo.strftime("%Y-%m")
    else:  # 默认本周
        lo = base - timedelta(days=base.weekday())
        hi = lo + timedelta(days=7)
        label = "本周"
    return (to_utc(lo.strftime("%Y-%m-%d %H:%M:%S")),
            to_utc(hi.strftime("%Y-%m-%d %H:%M:%S")), label)


def cmd_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    lo, hi, label = _period(args)
    pr = odoo.read("res.users", [uid], ["partner_id"])
    my_partner = pr[0]["partner_id"][0] if pr and pr[0].get("partner_id") else 0
    domain = ["&",
              "|", ("user_id", "=", uid), ("partner_ids", "in", [my_partner]),
              "&", ("start", ">=", lo), ("start", "<", hi)]
    evs = odoo.search_read(
        EVENT, domain,
        ["id", "name", "start", "stop", "allday", "location", "partner_ids", "alarm_ids"],
        order="start asc", limit=args.limit)
    if args.json:
        print(json.dumps(evs, ensure_ascii=False, default=str))
        return
    rows = []
    for e in evs:
        if e.get("allday"):
            when = (e.get("start") or "")[:10] + " 全天"
        else:
            when = from_utc(e.get("start"), "%m-%d %H:%M") + "-" + from_utc(e.get("stop"), "%H:%M")
        rows.append([
            e["id"], when, (e.get("name") or "")[:24],
            (e.get("location") or "-")[:14],
            f"{len(e.get('partner_ids') or [])}人",
            "🔔" if e.get("alarm_ids") else "",
        ])
    print(render_table(rows, ["ID", "时间", "主题", "地点", "参与", "提醒"]))
    print(f"\n共 {len(evs)} 个事件（{label}）")


def cmd_show(odoo: Odoo, args):
    e = odoo.read(EVENT, [args.id], [
        "name", "start", "stop", "allday", "location", "description",
        "user_id", "partner_ids", "alarm_ids"])
    if not e:
        raise OdooError(f"事件 #{args.id} 不存在。")
    e = e[0]
    print(f"📅 事件 #{args.id}：{e['name']}")
    if e.get("allday"):
        print(f"   时间：{(e.get('start') or '')[:10]} 全天")
    else:
        print(f"   时间：{from_utc(e.get('start'))} ~ {from_utc(e.get('stop'), '%H:%M')}（本地）")
    print(f"   地点：{e.get('location') or '-'}   组织者：{m2o_name(e.get('user_id')) or '-'}")
    pids = e.get("partner_ids") or []
    if pids:
        names = [p["name"] for p in odoo.read("res.partner", pids, ["name"])]
        print(f"   参与人：{', '.join(names)}")
    aids = e.get("alarm_ids") or []
    if aids:
        al = odoo.read(ALARM, aids, ["name"])
        print(f"   提醒：{', '.join(a['name'] for a in al)}")


def cmd_add(odoo: Odoo, args):
    vals = {"name": args.name, "user_id": odoo.ensure_uid()}
    if args.allday:
        d = args.start.strip()[:10]
        end = args.end.strip()[:10] if args.end else d
        vals.update(allday=True, start=f"{d} 08:00:00", stop=f"{end} 18:00:00")
    else:
        vals["start"] = to_utc(args.start)
        if args.end:
            vals["stop"] = to_utc(args.end)
        else:
            vals["duration"] = args.duration if args.duration else 1.0
    if args.location:
        vals["location"] = args.location
    if getattr(args, "with_", None):
        vals["partner_ids"] = [(6, 0, _resolve_partners(odoo, args.with_))]
    if args.desc:
        vals["description"] = f"<p>{args.desc}</p>"
    if args.remind:
        dur, iv = _parse_remind(args.remind)
        vals["alarm_ids"] = [(0, 0, {
            "name": f"提前{args.remind}", "alarm_type": "notification",
            "duration": dur, "interval": iv})]
    eid = odoo.create(EVENT, vals)
    print(f"✅ 已新建日历事件 #{eid}：{args.name}")
    if args.remind:
        print(f"   提醒：提前 {args.remind} 通知")


def cmd_cancel(odoo: Odoo, args):
    odoo.unlink(EVENT, args.ids)
    print(f"✅ 已删除事件：{', '.join('#' + str(i) for i in args.ids)}")


def cmd_remind(odoo: Odoo, args):
    dur, iv = _parse_remind(args.before)
    odoo.write(EVENT, [args.id], {"alarm_ids": [(0, 0, {
        "name": f"提前{args.before}", "alarm_type": args.type,
        "duration": dur, "interval": iv})]})
    print(f"✅ 已给事件 #{args.id} 加提醒：提前 {args.before}（{args.type}）")


def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo 日历事件与提醒")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    li = sub.add_parser("list", help="我的日程")
    li.add_argument("--today", action="store_true")
    li.add_argument("--month", action="store_true")
    li.add_argument("--from", dest="date_from", help="YYYY-MM-DD")
    li.add_argument("--to", dest="date_to", help="YYYY-MM-DD")
    li.add_argument("--limit", type=int, default=100)

    sh = sub.add_parser("show", help="事件详情")
    sh.add_argument("id", type=int)

    ad = sub.add_parser("add", help="新建事件")
    ad.add_argument("--name", required=True)
    ad.add_argument("--start", required=True, help="开始 YYYY-MM-DD HH:MM（本地）")
    ad.add_argument("--end", help="结束 YYYY-MM-DD HH:MM")
    ad.add_argument("--duration", type=float, help="时长（小时），无 --end 时用")
    ad.add_argument("--location")
    ad.add_argument("--with", dest="with_", help="参与人，逗号分隔（名字/id/我）")
    ad.add_argument("--remind", help="提醒，如 30m/1h/1d")
    ad.add_argument("--allday", action="store_true")
    ad.add_argument("--desc")

    ca = sub.add_parser("cancel", help="删除事件")
    ca.add_argument("ids", nargs="+", type=int)

    rm = sub.add_parser("remind", help="给事件加提醒")
    rm.add_argument("id", type=int)
    rm.add_argument("--before", required=True, help="提前量，如 30m/1h/1d")
    rm.add_argument("--type", choices=["notification", "email"], default="notification")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {"list": cmd_list, "show": cmd_show, "add": cmd_add,
                    "cancel": cmd_cancel, "remind": cmd_remind}
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
