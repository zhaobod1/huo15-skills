# 辉火 Token 优化器 (huo15-token-optimizer) — 设计规格

> 版本: v1.1 | 日期: 2026-06-26 | 作者: 贾维斯
> v1.1 变更: 安全模式 — clean 默认 dry-run、备份先行、AGENTS 永不自动替换、阈值放宽

## 一、目标

在不降低 OpenClaw 性能与能力的前提下，系统化节省 token 消耗。封装为可复用的 ClawHub skill，AI 读 SKILL.md 即可触发，支持手动/定时两种模式。

## 二、架构

```
huo15-token-optimizer/
├── SKILL.md                  # AI 指令入口
├── scripts/
│   ├── token-opt             # CLI 统一入口
│   ├── scan.py               # 扫描所有工作区 → 冗余报告
│   ├── clean.py              # 清理动作（dry-run 默认，--force 才执行）
│   ├── report.py             # Token 消耗统计看板
│   └── watch.py              # 监控模式（阈值告警）
├── config.json               # 阈值默认值
└── references/
    ├── token-best-practices.md   # 2026 手法参考
    └── openclaw-config-guide.md  # compaction/route 调优
```

## 三、模块设计

### 3.1 scan.py — 工作区扫描

**输入:** 无（自动扫描 `~/.openclaw/workspace*`）

**输出:** JSON 报告
```json
{
  "total_tokens_est": 196000,
  "workspaces": [
    {
      "name": "huangshuo",
      "files": {
        "AGENTS.md": {"size": 8302, "token_est": 2500, "status": "oversized"},
        "DREAMS.md": {"size": 54768, "token_est": 16400, "status": "oversized"}
      },
      "issues": ["AGENTS.md > 5KB （自定义格式，需人工确认）", "DREAMS.md > 30 dream entries"]
    }
  ],
  "actions": [
    {"type": "truncate_dreams", "workspace": "huangshuo", "entries_now": 55, "keep": 15, "savings_est": 12000},
    {"type": "agents_warning", "workspace": "huangshuo", "msg": "自定义 AGENTS.md 8.3KB，不会自动替换"}
  ]
}
```

**判断逻辑:**
- AGENTS.md > 5KB → 仅警告，**永不自动替换**（自定义内容有风险）
- DREAMS.md 梦境条目 > 30 → 标记 oversized
- MEMORY.md > 5KB → 标记，建议手动归档
- 无 `~/.openclaw/sessions-archive/` → 提示安装 archiver

### 3.2 clean.py — 清理执行（安全模式）

**核心安全机制:**
- 默认 `--dry-run`，仅预览
- `--force` 才真正执行
- 执行前自动备份到 `~/.openclaw/.token-opt-backups/YYYY-MM-DD/`
- AGENTS.md 永不自动替换

**子命令:**
- `clean --workspace <name> --dry-run` — 预览（默认）
- `clean --all --force` — 全量执行
- `clean --restore <backup-date>` — 从备份恢复

**清理动作:**

1. **DREAMS 截断** — 保留最近 15 条（config.dreams_keep_entries），先备份原始文件
2. **AGENTS.md** — 仅 report 标红，**不做任何自动修改**
3. **MEMORY 瘦身** — 仅报告 oversized，提示手动操作路径，不自动归档
4. **Session 归档** — 输出 `enhance_trajectory_archiver_setup` 命令提示，不自动执行

### 3.3 report.py — 统计看板

**输出格式:** Markdown 表格

**统计维度:**
- 各工作区 token 消耗排名
- 各文件类型占比
- 近 7 天趋势（需 cron 采集）
- 节省预估（scan 前 vs clean 后）

### 3.4 watch.py — 监控模式

**触发条件:** DREAMS.md > 60KB 或 AGENTS.md > 10KB

**告警方式:** stdout + `~/.openclaw/workspace/memory/token-alert.md`

### 3.5 config.json — 安全阈值配置

```json
{
  "thresholds": {
    "agents_max_kb": 5,
    "dreams_max_entries": 30,
    "dreams_keep_entries": 15,
    "memory_max_kb": 5,
    "watch_dreams_max_kb": 60,
    "watch_agents_max_kb": 10
  },
  "sessions": {
    "archive_days": 30,
    "auto_archive": false
  },
  "safety": {
    "backup_dir": "~/.openclaw/.token-opt-backups",
    "backup_keep_days": 90,
    "auto_replace_agents": false,
    "max_one_shot_savings_kb": 500,
    "clean_default_dry_run": true
  }
}
```

| 参数 | 值 | 理由 |
|------|-----|------|
| `dreams_max_entries` | 30 | 触发告警阈值宽松，不频繁打扰 |
| `dreams_keep_entries` | 15 | 保留约 30 天梦境记忆 |
| `auto_replace_agents` | false | AGENTS.md 可能含自定义规则，永不自动替换 |
| `backup_keep_days` | 90 | 三个月可恢复，给足后悔药 |
| `clean_default_dry_run` | true | 安全第一，无 --force 不执行 |

## 四、SKILL.md 设计

### 触发词

- 「token 优化」「节约 token」「扫描 token」「token 报告」
- AI 检测到 session 上下文过大时自动建议

### AI 决策树

```
收到触发词
  → 无参数 → scan（只读报告）
  → "清理" → scan → clean --dry-run（预览）→ 确认 → clean --all --force
  → "报告" → report
  → "监控" → watch
  → "恢复" → clean --restore <date>
```

### AI 执行流程

1. `python3 scripts/scan.py` → 报告给用户
2. 用户说「清理」→ `python3 scripts/clean.py --all --dry-run` → 预览变更
3. 用户确认 → `python3 scripts/clean.py --all --force` → 展示结果

## 五、发布流程

1. 本地开发: `~/workspace/projects/openclaw/huo15-skills/huo15-token-optimizer/`
2. Push: CNB + GitHub
3. 发布: `clawhub publish huo15-token-optimizer --version 1.0.0`
4. 安装: `clawhub install huo15-token-optimizer`

## 六、成功标准

- scan 准确反映 token 消耗现状
- clean 默认 dry-run，不加 --force 不执行
- clean --force 后 DREAMS 截断至 15 条，原文件有备份
- AGENTS.md 在报告中标红但永不自动修改
- clean 后不损坏任何有效配置
- report 看板清晰可读
