# CLAUDE.md

**项目：huo15-huihuo-odoo** — 火一五 Odoo 技能 v1.0.0

## 项目定位

用自然语言 + API 操作公司**辉火云企业套件**（www.huo15.com，db=`huo15`，Odoo 19）的待办 / 项目 / 工时单三大应用。纯 Python 标准库（`xmlrpc.client` + `urllib`），零第三方依赖。

## 品牌口径（对外文档必守）

- **对外**（PRD/汇报/客户文档/营销）：辉火云企业套件 / 辉火云。
- **对内调试 / 本技能 SKILL.md / references / 代码注释**：可用 odoo 等真实技术标识符（API 协议文档性质，§11.8 豁免）。
- README.md 主体用业务名，技术实现小节如实写 Odoo 19 API。
- 版权：青岛火一五信息科技有限公司。

## 目录结构

```
huo15-huihuo-odoo/
├── SKILL.md            # 技能主文档（触发词 / 工作流 / 命令速查 / 字段坑）
├── README.md           # 对外文档（模板：logo + 标语 + 机构表 + 正文 + 页脚）
├── CLAUDE.md           # 本文件
├── _meta.json          # ClawHub 元数据（slug / version）
├── scripts/
│   ├── odoo_client.py  # 核心：凭据(tools.md 读写) + XML-RPC/JSON-RPC + 通用 ORM 封装
│   ├── odoo_utils.py   # 时区(本地↔UTC) / m2o 格式化 / 中文宽度对齐表格 / state-priority 标签
│   ├── login.py        # 配置并验证凭据（getpass / stdin / 参数三种入口）
│   ├── todo.py         # 待办（add/list/done/reopen/cancel/update/stages）
│   ├── project.py      # 项目+任务（list/show/add/edit/archive + task-*）
│   └── timesheet.py    # 工时单（by-employee/by-project/by-month/detail/log）
└── references/         # Odoo 19 API 知识沉淀（读企业版源码而来）
    ├── odoo-todo-api.md       # 待办=project.task 私有态 + state 取值 + 个人阶段坑
    ├── odoo-project-api.md    # project.project/task/task.type + allocated_hours/user_ids
    └── odoo-timesheet-api.md  # account.analytic.line + unit_amount + read_group lazy 坑
```

## 开发规范

1. **所有修改在本地仓库**：`/Users/jobzhao/workspace/projects/openclaw/huo15-skills/huo15-huihuo-odoo/`，禁止改 ClawHub 安装副本。
2. **不新增第三方依赖**：保持纯标准库（`_meta.json` 的 dependencies 为空）。
3. **改/写 ORM 调用前必查 `references/`**：Odoo 19 字段坑很多（见下表），别凭记忆。
4. 入口分层：业务脚本（todo/project/timesheet）→ `odoo_client.Odoo` → execute_kw。新功能优先复用 `Odoo` 的便捷方法，别重复写 execute_kw 拼装。
5. 共用逻辑（时区/格式化/表格）放 `odoo_utils.py`，别在各脚本里复制。

## 字段坑速查（改代码前对照，详见 references/）

| 坑 | 正确做法 |
|---|---|
| 待办归属 | `project.task` 且不传 project_id（False）+ user_ids 含本人 |
| 截止日期 | `date_deadline` 是 Datetime/UTC（`odoo_utils.to_utc` 已转） |
| 完成状态 | `state='1_done'` / 取消 `'1_canceled'` / 进行中 `'01_in_progress'` / 等待 `'04_waiting_normal'` |
| 任务负责人 | `user_ids` 是 m2m，`[(6,0,[ids])]` |
| 分配工时 | `allocated_hours`（非 planned_hours） |
| 工时小时数 | `unit_amount`（非 amount） |
| 工时单判定 | `('project_id','!=',False)`（无 is_timesheet 字段） |
| 分组聚合 | read_group 多 groupby 必 `lazy=False`；优先 formatted_read_group |
| 个人阶段筛 | personal_stage_type_id 无 search，走 project.task.stage.personal 关联表 |

## 凭据 / 安全

- 运行期凭据写 `~/.huo15/tools.md`（标记块 + 权限 600），代码里**绝不内嵌任何 secret**。
- secret 入参优先 `--secret-stdin`。
- 测试连接：`python3 scripts/login.py test`。

## 发布流程

> 本技能是独立 skill，无 plugin 引用它，直接发即可（无"先 skill 后 plugin"顺序问题）。

```bash
cd /Users/jobzhao/workspace/projects/openclaw/huo15-skills
git add huo15-huihuo-odoo/
git commit -m "feat(huihuo-odoo): v1.0.0 - 待办/项目/工时单三大应用 XML-RPC 管理"
git push origin main      # cnb.cool 主
git push github main      # GitHub 镜像

# ClawHub（绝对路径 + 显式 --version，见 ~/CLAUDE.md §7 六坑）
CLAWHUB_TOKEN=clh_... clawhub publish "$(pwd)/huo15-huihuo-odoo" --version 1.0.0

# publish 后手动同步 _meta.json 的 version（CLI 不会自动刷）并单独 chore commit
```

**发布凭据**：见 `~/CLAUDE.md` §2（cnb git / npm / ClawHub token），不写进本仓库。
**发布六坑**：见 `~/CLAUDE.md` §7（绝对路径 / --version 必填 / rate limit / _meta.json 手动同步 / 幽灵占用 +1 patch / SKILL.md 8192 token 上限）。

## 版本号规则

- 新增应用/大改 API 层 → 次版本（1.0→1.1）。
- 新增命令/参数 → 次版本。
- 修 bug/字段坑 → 补丁号（1.0.0→1.0.1）。
- 每次发版同步 bump `package.json`(无)/`_meta.json`/SKILL.md frontmatter `version` 三处一致。
