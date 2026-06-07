---
name: huo15-huihuo-odoo
displayName: 火一五 Odoo 技能
description: >-
  Use this skill whenever the user wants to manage their work — to-dos / tasks
  ("记个待办" "加个任务" "我的待办" "做个待办事项" "标记完成"), projects and
  project tasks, timesheets / hours ("记工时" "统计每个人工时"), CRM leads and
  sales opportunities ("新建商机" "跟进客户" "看销售管道" "赢单/输单"), follow-up
  activities and reminders ("提醒我" "3天后回访这个客户"), or calendar events and
  meetings ("安排个会议" "我这周有什么日程" "提前30分钟提醒"). It is backed by the
  火一五/辉火云 company Odoo system (www.huo15.com, db=huo15) over XML-RPC /
  JSON-RPC. Also triggers on: odoo, 辉火云企业套件, 公司系统, www.huo15.com/odoo
  /to-do, /odoo/project, /odoo/timesheets, /odoo/crm, /odoo/calendar, or
  "登录/连接公司系统、保存 odoo 账号". Treat bare work-context mentions of
  待办/任务/项目/工时/客户/商机/会议/日程/提醒 as this skill. First run:
  login.py init (system address / database / account / password →
  ~/.huo15/tools.md, chmod 600). Pure standard library, zero dependencies.
version: 1.2.1
aliases:
  - 火一五odoo技能
  - 火一五Odoo技能
  - 辉火云odoo
  - odoo待办
  - odoo项目
  - odoo工时单
  - 公司系统待办
  - 公司系统项目
  - 公司系统工时单
  - 公司系统CRM
  - odoo商机
  - odoo-crm
  - 销售管道
  - 客户管理
  - 商机管理
  - 活动管理
  - odoo日历
  - 日程安排
  - 会议提醒
  - 公司系统日历
  - 待办事项
  - 记待办
  - 加任务
  - 跟进客户
  - 提醒我
  - 安排会议
  - 记工时
  - huo15-odoo
dependencies:
  python-packages: []   # 纯标准库，无第三方依赖
---

# 火一五 Odoo 技能 v1.0

通过 XML-RPC / JSON-RPC 操作公司 Odoo 系统（**辉火云企业套件**，www.huo15.com，db=`huo15`）。
六大能力：**待办**（/odoo/to-do）、**项目**（/odoo/project）、**工时单**（/odoo/timesheets）、**CRM**（/odoo/crm）、**活动**（My Activities）、**日历**（/odoo/calendar）。

> **完整命令** → [references/commands.md](references/commands.md)
> **API/字段细节** → [todo](references/odoo-todo-api.md) · [project](references/odoo-project-api.md) · [timesheet](references/odoo-timesheet-api.md) · [crm](references/odoo-crm-api.md) · [activity+calendar](references/odoo-activity-calendar-api.md)

## 触发场景

- "帮我登录公司系统" / "连一下 odoo" / "保存我的 odoo 账号"
- "新建一个待办：xxx，截止周五" / "把待办 123 标记完成" / "看我的待办"
- "看一下 X 项目" / "给 X 项目加个任务" / "把任务移到进行中" / "改任务负责人"
- "统计这个月每个员工的工时" / "看 X 项目的工时" / "研发部本月工时报表"
- "看我的商机/销售管道" / "新建商机" / "把商机标记赢单/输单" / "线索转商机" / "按阶段统计 pipeline"
- "看我的活动/待跟进" / "给这个商机加个3天后回访" / "我这周有什么日程/会议" / "建个会议提醒我" / "提前30分钟提醒"

---

## ⚠️ 第一步：凭据初始化（首次必做）

所有脚本都依赖已保存的凭据。**没配过就先初始化这 4 项，别直接跑 todo/project/timesheet。**

| # | 输入项 | 示例 | 说明 |
|---|---|---|---|
| ① | 公司系统地址 | `www.huo15.com` | 只输域名即可，脚本自动补 `https://` |
| ② | 数据库 | `huo15` | 数据库名 |
| ③ | 账号 | 邮箱 / 用户名 | 登录账号 |
| ④ | 密码 | 密码或 API Key | 推荐 API Key（偏好设置→账户安全→新建，可随时吊销） |

保存到 `~/.huo15/tools.md`（权限 600）。

### 方式 A：Claude 代配（默认，在对话里完成）

1. 在对话里**依次问用户这 4 项**（地址 / 数据库 / 账号 / 密码），不要自己编。
2. 用 stdin 传密码（避免明文进 shell 历史 / ps）：

```bash
printf '%s' "<用户输入的密码>" | python3 scripts/login.py set \
    --url www.huo15.com --db huo15 --login "<账号>" --auth-type password
# 密码填的是 API Key 就把 --auth-type 换成 apikey
```

### 方式 B：用户自助初始化（密码不回显）

```bash
python3 scripts/login.py init     # 交互式依次提示输入 ①地址 ②数据库 ③账号 ④密码（无参等效）
```

login.py 会**先验证连接成功才落盘**，写入 `~/.huo15/tools.md`（权限 600）；失败报中文原因（账号错 / db 错 / 网络）。验证：`python3 scripts/login.py test`。

> 凭据文件默认 `~/.huo15/tools.md`，可用环境变量 `HUO15_TOOLS_MD` 改路径。
> 临时/CI 可用环境变量免落盘：`HUO15_ODOO_LOGIN` / `HUO15_ODOO_SECRET` / `HUO15_ODOO_DB` / `HUO15_ODOO_URL`。
> **此文件含明文凭据，务必不要提交 git。**

---

## 四大应用速览

每个应用一个脚本，风格统一（`add`/`list`/… 子命令，名字可代 id，`--json` 输出，`-h` 看完整参数）。
**完整命令示例 → [references/commands.md](references/commands.md)；字段/API 细节 → 各 `references/odoo-<app>-api.md`。**

| 应用 | 脚本 | 核心模型 | 主要子命令 |
|---|---|---|---|
| 📝 待办 `/odoo/to-do` | `todo.py` | project.task（私有态） | `add` `list` `done` `reopen` `cancel` `update` `stages` |
| 📁 项目 `/odoo/project` | `project.py` | project.project + task | `list` `show` `add` `edit` `archive` `tasks` `task-add` `task-move` `task-assign` `task-done` |
| ⏱️ 工时单 `/odoo/timesheets` | `timesheet.py` | account.analytic.line | `by-employee` `by-project` `by-month` `detail` `log` |
| 💼 CRM `/odoo/crm` | `crm.py` | crm.lead（线索/商机） | `list` `show` `add` `move` `won` `lost` `restore` `convert` `pipeline` `activity` |
| 🔔 活动 My Activities | `activity.py` | mail.activity | `list` `add` `done` `cancel` `reschedule` |
| 📅 日历 `/odoo/calendar` | `agenda.py` | calendar.event + alarm | `list` `show` `add` `cancel` `remind` |

下方「命令速查」给最常用命令的具体写法，够日常用；要完整参数/示例读 [references/commands.md](references/commands.md)。

---

## 命令速查

| 想做 | 命令 |
|---|---|
| 初始化(交互) | `python3 scripts/login.py init` —— 提示输入 地址/数据库/账号/密码 |
| 配登录(代配) | `printf '%s' "$PWD" \| python3 scripts/login.py set --url www.huo15.com --db huo15 --login X` |
| 测连接 | `python3 scripts/login.py test` |
| 新建待办 | `todo.py add --title ... [--deadline --priority --stage --tags]` |
| 我的待办 | `todo.py list` |
| 完成待办 | `todo.py done <id>` |
| 项目列表/详情 | `project.py list` / `project.py show <id>` |
| 建项目/任务 | `project.py add --name ...` / `project.py task-add --project <id> --title ...` |
| 移阶段/改负责人 | `project.py task-move <id> --stage X` / `task-assign <id> --users a,b` |
| 工时汇总 | `timesheet.py by-employee\|by-project\|by-month [--month/--from/--to]` |
| 工时明细 | `timesheet.py detail --employee X --month YYYY-MM` |
| CRM 商机 | `crm.py list` / `crm.py add --name ... --customer ... --revenue N --user 我` |
| 赢/输/管道 | `crm.py won\|lost <id>` / `crm.py pipeline --by stage\|user\|team` |
| 活动/提醒 | `activity.py list` / `activity.py add --model crm.lead --id N --type call --date ...` |
| 日历/会议 | `agenda.py list` / `agenda.py add --name ... --start "... HH:MM" --with X --remind 30m` |

所有脚本支持 `--json` 输出、`--tools-md <path>` 指定凭据文件。

---

## 字段坑速查（最容易错，改脚本前必看）

| 坑 | 正确做法 |
|---|---|
| 待办放哪 | `project.task` 且 **不传 project_id**（保持 False）+ `user_ids` 含本人 |
| 截止日期 | `date_deadline` 是 **Datetime / UTC**，不是 date（脚本已自动本地→UTC） |
| 完成状态 | `state='1_done'`；取消 `'1_canceled'`；进行中 `'01_in_progress'`；等待 `'04_waiting_normal'` |
| 任务负责人 | `user_ids` 是 **Many2many**，写 `[(6,0,[ids])]`；不是 user_id |
| 分配工时 | 任务用 `allocated_hours`，**不是 planned_hours**（19 已删） |
| 工时小时数 | 工时单求和用 `unit_amount`（不是 amount，amount 是钱） |
| 是不是工时单 | 没有 is_timesheet 字段，判定 `('project_id','!=',False)` |
| 分组统计 | `read_group` 多 groupby 必须 `lazy=False`；优先 `formatted_read_group`（脚本已封装） |
| 个人阶段筛选 | `personal_stage_type_id` 无 search，按阶段筛走 `project.task.stage.personal` 关联表（脚本已处理） |
| CRM 赢/输单 | 建商机必传 `type='opportunity'`；负责人 `user_id` 单数；赢/输/复活调 `action_set_won/lost/restore`，别手动 write |
| CRM 字段 | 手机号写 `phone`（无 mobile）；`crm.stage.team_ids` 复数 m2m（空=全团队）；`description` 是 Html |
| 活动 | `date_deadline` 是 **Date**；完成=archive(`action_feedback`)不是删；`state` computed 无 search，查逾期用 `date_deadline` 比较 |
| 日历 | `start/stop` 是 **Datetime/UTC**（脚本自动转）；写 `partner_ids` 自动建参与人；alarm 只有 notification/email |

> 这些都已在脚本里处理对。手工写新调用 / 改脚本时对照本表和 references/。

---

## 品牌口径

- **对外**（PRD/汇报/客户文档）：辉火云企业套件 / 辉火云。
- **对内调试 / 本技能文档 / 代码注释**：可用 odoo 等真实技术标识符。
- 版权：青岛火一五信息科技有限公司。

## 安全红线

1. 凭据只写 `~/.huo15/tools.md`（权限 600），**永不进 git / commit / 日志**。
2. secret 传参优先 `--secret-stdin`，避免明文进 shell 历史。
3. 推荐 API Key 而非主密码（可吊销）。
4. 删除/归档/批量改状态前向用户确认。
