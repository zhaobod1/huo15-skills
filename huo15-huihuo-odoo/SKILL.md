---
name: huo15-huihuo-odoo
displayName: 火一五 Odoo 技能
description: >-
  Use when the user wants to operate the 火一五/辉火云 company Odoo system
  (www.huo15.com, db=huo15) through its API. Covers four apps: 待办/To-do
  (create, list, complete personal tasks), 项目/Project (edit projects, manage
  tasks, stages, assignees, hours), 工时单/Timesheets (per-employee / project /
  month hour reports), and CRM/客户 (manage leads & opportunities, pipeline by
  stage / salesperson / team, mark won or lost with reason, convert leads,
  schedule follow-up activities). Also use when the user mentions odoo,
  辉火云企业套件, 公司系统的待办/项目/工时单/CRM/商机/销售管道/线索,
  www.huo15.com/odoo/to-do, /odoo/project, /odoo/timesheets, /odoo/crm, or asks
  to log in to and save credentials for the company Odoo system. First run via
  login.py init prompts for system address / database / account / password,
  saved to the user's personal ~/.huo15/tools.md (chmod 600). Pure XML-RPC /
  JSON-RPC, zero third-party dependencies.
version: 1.1.0
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
  - huo15-odoo
dependencies:
  python-packages: []   # 纯标准库，无第三方依赖
---

# 火一五 Odoo 技能 v1.0

通过 XML-RPC / JSON-RPC 操作公司 Odoo 系统（**辉火云企业套件**，www.huo15.com，db=`huo15`）。
四大能力：**待办**（/odoo/to-do）、**项目**（/odoo/project）、**工时单**（/odoo/timesheets）、**CRM**（/odoo/crm）。

> API 知识沉淀（出问题先查这里）：
> [todo](references/odoo-todo-api.md) ·
> [project](references/odoo-project-api.md) ·
> [timesheet](references/odoo-timesheet-api.md) ·
> [crm](references/odoo-crm-api.md)

## 触发场景

- "帮我登录公司系统" / "连一下 odoo" / "保存我的 odoo 账号"
- "新建一个待办：xxx，截止周五" / "把待办 123 标记完成" / "看我的待办"
- "看一下 X 项目" / "给 X 项目加个任务" / "把任务移到进行中" / "改任务负责人"
- "统计这个月每个员工的工时" / "看 X 项目的工时" / "研发部本月工时报表"
- "看我的商机/销售管道" / "新建商机" / "把商机标记赢单/输单" / "线索转商机" / "按阶段统计 pipeline"

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

## 1. 待办管理（/odoo/to-do）

待办 = `project.task` 且 `project_id` 为空 + 指派给本人。脚本 `scripts/todo.py`。

```bash
# 新建：标题必填，截止/优先级/阶段/标签可选
python3 scripts/todo.py add --title "跟进三和红木分账" --deadline 2026-06-10 --priority 2
python3 scripts/todo.py add --title "写周报" --desc "本周三大进展" --stage Today --tags "管理,周报"

# 列出（默认未完成）
python3 scripts/todo.py list                 # 我的未完成待办
python3 scripts/todo.py list --all           # 含已完成
python3 scripts/todo.py list --stage Today    # 按个人阶段筛
python3 scripts/todo.py stages               # 看我有哪些个人阶段（Inbox/Today/...）

# 改状态
python3 scripts/todo.py done 1234            # 标记完成（可多个 id）
python3 scripts/todo.py reopen 1234          # 重新打开
python3 scripts/todo.py cancel 1234          # 取消

# 修改内容
python3 scripts/todo.py update 1234 --deadline "2026-06-12 18:00" --priority 3
```

关键：截止日期填 `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM`（按你本地时间，脚本自动转 UTC）；优先级 0普通/1中/2高/3紧急；完成=state `1_done`。

---

## 2. 项目管理（/odoo/project）

`project.project` + `project.task`。脚本 `scripts/project.py`。项目/用户/客户都可用**名字**代替 id。

```bash
# 项目层
python3 scripts/project.py list                      # 所有项目
python3 scripts/project.py list --mine                # 只看我负责的
python3 scripts/project.py show 5                      # 项目详情 + 按阶段统计任务
python3 scripts/project.py add --name "官网改版" --manager 我 --customer "某客户" --deadline 2026-08-31
python3 scripts/project.py edit 5 --manager 张三 --deadline 2026-09-30
python3 scripts/project.py archive 5                   # 归档 / unarchive 恢复

# 任务层
python3 scripts/project.py tasks 5                     # 列项目 5 的未完成任务（--all 全部）
python3 scripts/project.py task-add --project 5 --title "首页设计" --assignee 我 --deadline 2026-06-20 --hours 8
python3 scripts/project.py task-move 88 --stage 进行中  # 移到某看板阶段
python3 scripts/project.py task-assign 88 --users "张三,李四"
python3 scripts/project.py task-done 88                # 标记完成
python3 scripts/project.py task-update 88 --priority 3 --deadline 2026-06-22
```

关键：任务负责人是**多对多**（可多人，逗号分隔）；"我"会自动解析成当前登录用户；分配工时字段是 `allocated_hours`（脚本已处理）。

---

## 3. 工时单统计（/odoo/timesheets）

工时单 = `account.analytic.line` 且 `project_id` 非空。脚本 `scripts/timesheet.py`。**默认本月**。

```bash
# 汇总报表
python3 scripts/timesheet.py by-employee                    # 本月每个员工总工时
python3 scripts/timesheet.py by-employee --month 2026-06     # 指定月
python3 scripts/timesheet.py by-employee --department 研发部 --from 2026-06-01 --to 2026-06-30
python3 scripts/timesheet.py by-project --month 2026-06      # 按项目
python3 scripts/timesheet.py by-month --employee 张三 --year 2026   # 某员工逐月趋势

# 明细
python3 scripts/timesheet.py detail --employee 张三 --month 2026-06

# 录入一条工时（可选）
python3 scripts/timesheet.py log --project 5 --hours 3 --task 88 --desc "对接联调"
```

时间范围参数通用：`--month YYYY-MM` / `--from --to` / `--year`，缺省本月。
筛选：`--employee 名字` / `--project 名字或id` / `--department 部门名`。
输出对齐表格 + 合计；加 `--json` 给程序解析。

---

## 4. CRM 管理（/odoo/crm）

线索/商机同为 `crm.lead`（`type` 区分）。脚本 `scripts/crm.py`。客户/负责人/团队可用**名字**。

```bash
# 商机列表与详情
python3 scripts/crm.py list                  # 我的进行中商机（带预期收入合计）
python3 scripts/crm.py list --all            # 全部进行中；--won 已赢 / --lost 已输
python3 scripts/crm.py list --user 张三 --stage 报价
python3 scripts/crm.py show 88

# 新建 / 修改
python3 scripts/crm.py add --name "某客户-ERP项目" --customer "某客户" --revenue 50000 --user 我 --team 销售一组 --priority 2
python3 scripts/crm.py update 88 --revenue 60000 --probability 70

# 推进 / 赢单 / 输单 / 复活
python3 scripts/crm.py move 88 --stage 谈判          # 推进阶段
python3 scripts/crm.py won 88                        # 标记赢单（自动置赢单阶段 + 100%）
python3 scripts/crm.py lost 88 --reason "价格太高"    # 标记输单（原因不存在自动建）
python3 scripts/crm.py restore 88                    # 复活已输单

# 线索转商机 / 安排跟进活动
python3 scripts/crm.py convert 90 --customer "某客户"
python3 scripts/crm.py activity 88 --type call --date 2026-06-10 --summary "回访报价"

# 销售管道统计（预期收入 + 加权预测）
python3 scripts/crm.py pipeline --by stage           # 按阶段；--by user 负责人 / --by team 团队
```

关键：建商机自动用 `type=opportunity`；负责人 `user_id` 单数；赢单/输单/复活走 Odoo 专用方法（脚本已封装），别手动改 stage/active/probability。

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
