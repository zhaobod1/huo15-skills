# 火一五 Odoo 技能 — 完整命令参考

> SKILL.md 的「命令速查」表覆盖最常用命令；本文件是每个应用的完整 CLI 示例与说明。
> 所有脚本通用：`--json`（程序解析）、`--tools-md <path>`（指定凭据文件）、`-h`（看完整参数）。
> 字段/API 细节见各 `references/odoo-<app>-api.md`。

## 待办（/odoo/to-do）—— todo.py

待办 = `project.task` 且 `project_id` 为空 + 指派给本人。

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

## 项目（/odoo/project）—— project.py

`project.project` + `project.task`。项目/用户/客户都可用**名字**代替 id。

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

## 工时单（/odoo/timesheets）—— timesheet.py

工时单 = `account.analytic.line` 且 `project_id` 非空。**默认本月**。

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

## CRM（/odoo/crm）—— crm.py

线索/商机同为 `crm.lead`（`type` 区分）。客户/负责人/团队可用**名字**。

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
