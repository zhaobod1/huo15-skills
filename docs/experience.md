# 开发经验与踩坑记录

> 格式：`## YYYY-MM-DD 标题`，按时间倒序追加。

---

## 2026-05 ClawHub 发布常见坑（v0.8.0）

### 必须绝对路径

`clawhub publish .` 报 `SKILL.md required`，必须用 `clawhub publish "$(pwd)/<slug>"`。

### 幽灵占用版本号

`inspect` 显示 Latest=X.Y.Z，但 publish 同版本号报 `Version already exists`。
**应对**：直接 +1 patch 跳过，同步更新 `_meta.json` 和 `SKILL.md`，不要重试同一版本号。

### `_meta.json` 不自动同步

`clawhub publish` 成功后 `_meta.json` 中的 version 字段**不会自动更新**，必须手动 bump + 单独 `chore` commit。

### SKILL.md token 超限

嵌入上限 8192 tokens（约 25KB）。超限报 `Embedding failed`。
优先砍：历史 changelog 章节 / 重复 CLI 示例 / frontmatter 超长触发词。
详细内容挪到 `README.md` 或 `templates/README.md`（不参与嵌入）。

### 每小时新 slug 配额 5 个

只对首次 publish 计数，存量 slug 升版本不占额度。撞限流时切换到升版本策略，**不要 sleep 轮询重试**。

---

## 2026-05 openclaw-bootstrap v2.0 架构迁移经验

- v1.x 产 `profile.md`，v2.0 改产原生五件套（`SOUL/IDENTITY/USER/TOOLS/AGENTS.md`）
- 完成信号从"写完文件"改为"删 `BOOTSTRAP.md`"，openclaw workspace state 才转 complete
- 删 L1 龙虾 memory 写盘：原生 file→memory 链路自己工作，不要复制

---

## 2026-05 品牌词替换规则

对外文档（README / SKILL.md / docs/）中：

- `uniapp` / `uni-app` / `uniapp-x` / `跨平台框架` → 原生 Swift（iOS）/ 原生 Kotlin（Android）开发
- `Odoo` / `odoo` / `ODOO` / `欧度` → 辉火云企业套件
- `OWL (Odoo Web Library)` → 辉火云前端组件库

发版前自查命令：

```bash
grep -riE "odoo|uniapp|uni-app|欧度" README.md SKILL.md docs/
```

---

## 2026-05 openclaw Plugin 开发教训

- `compat.pluginApi` 一定要用 range（`>=X.Y.Z`），裸版本 runtime 升小版本就 install 失败
- `child_process` / `execSync` 部分企业 npm 扫描器整包拦截，改用 return-cliCmd 模式
- `registerMemoryCorpusSupplement` 是单参，不要传 pluginId
