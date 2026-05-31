# CLAUDE.md — huo15-skills 仓库级开发规范

> 适用范围：`~/workspace/projects/openclaw/huo15-skills/` 目录下的所有开发与文档工作。

---

## 项目定位

火一五 Skills 技能库是青岛火一五信息科技有限公司为 OpenClaw / Claude Code 开发的定制化技能集合，托管于 [CNB.cool](https://cnb.cool/huo15/ai/huo15-skills)（主）与 GitHub（镜像）。  
Monorepo 架构：每个 skill 独立可发布，根目录 SKILL.md 是仓库级 marketplace 描述。

---

## 版权与品牌原则（铁律，对外文档必须遵守）

### 一、移动端技术栈

- **对外统一表述**：原生 Swift（iOS / macOS）/ 原生 Kotlin（Android）开发
- **禁止出现**：`uniapp`、`uni-app`、`uniapp-x`、`跨平台框架`、`HBuilderX`、`DCloud`
- **范围**：README / SKILL.md / docs/ 所有对外文档及对话输出；内部调试注释不限

### 二、ERP / 企业管理套件

| 禁止使用 | 统一替换为 |
|---|---|
| Odoo、odoo、ODOO、欧度 | 辉火云企业套件 |
| OWL（Odoo Web Library）前端框架 | 辉火云前端组件库 |
| Odoo Module / odoo 模块 | 辉火云企业套件模块 |
| odoo.com 版权声明 | 删除或替换为青岛火一五信息科技有限公司版权 |

> **例外**：已发布的目录名 / slug（如 `huo15-odoo19-module-dev`）不可改名，此规则对 slug 本身不适用，但**描述文字**必须符合上表。

---

## 目录结构规范

```
huo15-skills/
├── CLAUDE.md              ← 本文件（仓库级规范）
├── README.md              ← 公开文档（遵循 ~/workspace/study/README模板.md）
├── SKILL.md               ← ClawHub marketplace 描述（仓库级）
├── _meta.json             ← 仓库级元数据（version / ownerId）
├── .gitignore
├── LICENSE
├── docs/                  ← 仓库级记忆 / 经验 / 聊天记录（本目录）
│   ├── README.md          ← docs 说明与索引
│   ├── experience.md      ← 踩坑与经验沉淀
│   └── changelog.md       ← 仓库级重要变更（非 skill 级）
├── scripts/               ← 仓库级工具脚本
├── research/              ← 技术调研
├── skills/                ← 技能草稿 / 实验区
└── <slug>/                ← 各 skill 子目录（每个独立可发布）
    ├── SKILL.md            ← ClawHub 嵌入源（≤ 25KB / 8192 tokens 硬限）
    ├── _meta.json          ← 元数据（ownerId / slug / version）
    ├── README.md           ← 详细文档
    ├── CLAUDE.md           ← 该 skill 开发规范（仅本仓库内可见）
    ├── data/               ← 知识资产（人类 + LLM 共读）
    ├── scripts/            ← Python 脚本（零依赖优先）
    └── docs/changelog.md   ← 该 skill 版本历史
```

---

## 项目开发铁律

1. **所有修改只在本仓库进行**，禁止直接编辑 ClawHub 安装目录（`~/.openclaw/workspace/skills/`）的副本
2. **slug = 目录名**，一旦发布不可变，不可二次起名
3. **版本号 semver**，同一版本号不可重发；遇"幽灵占用"立刻 +1 patch 跳过
4. **SKILL.md 嵌入上限 8192 tokens（≈ 25KB）**，超限报 `Embedding failed`，砍历史 changelog / 重复示例
5. **`_meta.json` 不会自动同步**，`clawhub publish` 成功后手动 bump version，单独 `chore` commit
6. **每小时新 slug 配额 5 个**；存量 slug 升版本不占额度
7. **版权自查**：修改对外文档后必须执行 `grep -riE "odoo|uniapp|uni-app|欧度" README.md SKILL.md docs/`，命中 = 必须替换

---

## 版本号规则

| 变更类型 | 版本号 |
|---|---|
| 架构 / 哲学 / 触发器重构 | 次版本 +1（1.0 → 1.1） |
| 常规功能新增、新触发词 | 次版本 +1 |
| Bug 修复、文案调整、文档更新 | 补丁号 +1（1.0.0 → 1.0.1） |

---

## 标准发布流程

```bash
# 1. 在本仓库开发
cd ~/workspace/projects/openclaw/huo15-skills

# 2. 提交
git add <slug>/
git commit -m "feat(<slug>): vX.Y.Z 说明"

# 3. 同步双 remote
git push origin main    # CNB（主）
git push github main    # GitHub（镜像）

# 4. 发布 ClawHub
clawhub publish "$(pwd)/<slug>" \
  --slug <slug> --version X.Y.Z --changelog "..."

# 5. 手动 bump _meta.json + chore commit
# Edit <slug>/_meta.json → "version": "X.Y.Z"
git add <slug>/_meta.json
git commit -m "chore(<slug>): bump _meta to vX.Y.Z"
git push origin main && git push github main
```

**凭据**：见 `~/CLAUDE.md §2` 或 `~/.claude/projects/-Users-jobzhao/memory/publish_credentials.md`  
**铁律**：凭据禁止出现在 commit / log / PR / 此文件 / 任何 LLM 上下文。

---

## OpenClaw 全局原则

### 最高铁律

> **enhance the runtime, never modify or duplicate it.**

- 加新功能前先 `grep <runtime-source>` 找原生等价物
- 原生有就走原生 API（`registerMemoryCapability` / `registerCompactionProvider` / `on(hook, handler)` 等）
- 只补主框架真没有的能力；复制原生功能 = 双账本 + 状态漂移

### Plugin vs Skill 决策

**默认 Skill-first**；以下任一才做 Plugin：

- 需要 hook（PreToolUse / SessionStart 等系统事件）
- 需要注册新 tool / MCP server / subagent
- 需要跨项目 marketplace 分发
- 需要改用户 settings

两者都需要 → **Plugin 注册基建 + Skill 承载领域知识**（对齐 anthropic-skills 官方做法）。

### 插件开发铁律（6 条）

1. `compat.pluginApi` 必须是 semver range（`>=X.Y.Z`），**不能是裸版本**
2. 禁 `child_process`（含 `execSync` / `spawn` / `spawnSync`）；需要外部命令走 return-cliCmd 模式
3. `registerMemoryCorpusSupplement` / `registerMemoryPromptSupplement` 是**单参**
4. 「诊断不修复」：建议改配置一律 return-cliCmd，**永不 `fs.writeFileSync` 用户配置文件**
5. LLM 生成的 target / URL / 路径一律视为不可信，必须经插件层 sanitizer
6. 发版前自查：`grep -rE "child_process|execSync|spawnSync" --include="*.ts" src/`

### 记忆三层架构（OpenClaw）

| 层 | 位置 | 内容 | 写入时机 |
|---|---|---|---|
| L1 龙虾原生 | `~/.openclaw/memory/<agent>.sqlite` | 向量 + FTS | 原生自动 |
| L2 enhance | `~/.openclaw/memory/enhance-memory.sqlite` | 短条目，"怎么做" | `enhance_memory_store` |
| L3 共享 KB | `~/.openclaw/kb/shared/wiki/` | 长文档，"是什么" | `kb-ingest --scope shared` |

- `memory_search` 一次拿三层，**不要绕过去 grep 文件**
- Agent 个人笔记 → L3 `kb-ingest`（默认 agent scope）

### ClawHub 发布六坑（CLI v0.8.0）

| # | 坑 | 应对 |
|---|---|---|
| 1 | 必须绝对路径 | `clawhub publish "$(pwd)/<slug>"` |
| 2 | `--version` 必填 | CLI 不读 frontmatter / package.json |
| 3 | Plugin 需双发布 | `npm publish` + `clawhub publish` |
| 4 | 新 slug 每小时 5 个配额 | 存量 slug 升版本不占额度；撞限流不 sleep 重试 |
| 5 | `_meta.json` 不自动刷新 | 手动 bump + chore commit |
| 6 | 幽灵占用（inspect=2.5 但报 exists on 2.6） | 立刻跳 +1 patch，**不重试同一版本号** |

### 权威参考源

1. [anthropics/skills](https://github.com/anthropics/skills) — SKILL.md 规范
2. marketplace.json schema：`https://anthropic.com/claude-code/marketplace.schema.json`
3. VILA-Lab/Dive-into-Claude-Code — 1.6% AI / 98.4% harness 结论

---

## 发版自查 checklist

```bash
# 品牌词检查（所有对外文档必跑）
grep -riE "odoo|uniapp|uni-app|欧度" README.md SKILL.md docs/

# SKILL.md 大小（应 < 25KB）
wc -c SKILL.md

# compat.pluginApi 是 ranged（插件专用）
grep -E '"pluginApi"' package.json *.plugin.json

# 无 child_process（插件专用）
grep -rE "child_process|execSync|spawnSync" --include="*.ts" src/

# typecheck（如有 TS）
npx tsc --noEmit
```
