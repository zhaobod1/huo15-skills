---
type: concept
title: 会话管理
source: openclaw-docs/concepts/session.md
date: 2026-04-06
concepts: [会话路由, DM隔离, 会话生命周期, 会话存储, 会话维护]
---

# 会话管理

OpenClaw 将对话组织成**会话（Session）**。每条消息根据来源路由到对应会话。

## 消息路由规则

| 来源 | 行为 |
|------|------|
| 私信（DM）| 默认共享会话 |
| 群聊 | 每个群独立会话 |
| 房间/频道 | 每个房间独立会话 |
| 定时任务 | 每次运行全新会话 |
| Webhook | 每个 Hook 独立会话 |

## DM 隔离

默认情况下，所有私信共享一个会话，适合单用户场景。

**多用户场景必须启用 DM 隔离**，否则所有用户共享同一对话上下文：

```json5
{
  session: {
    dmScope: "per-channel-peer", // 按渠道 + 发送者隔离
  },
}
```

| 选项 | 说明 |
|------|------|
| `main`（默认）| 所有私信共享一个会话 |
| `per-peer` | 按发送者隔离（跨渠道）|
| `per-channel-peer` | 按渠道 + 发送者隔离（推荐）|
| `per-account-channel-peer` | 按账号 + 渠道 + 发送者隔离 |

> 提示：若同一用户从多个渠道联系，可使用 `session.identityLinks` 链接其身份，使它们共享一个会话。

## 会话生命周期

会话被复用直到过期：

- **每日重置**（默认）— 每天凌晨 4:00（网关宿主机本地时间）开启新会话
- **空闲重置**（可选）— 一段时间不活动后开启新会话，设置 `session.reset.idleMinutes`
- **手动重置** — 在聊天中输入 `/new` 或 `/reset`

## 状态存储位置

所有会话状态由 **Gateway** 拥有：

- **会话存储**: `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- **对话记录**: `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`

## 会话维护

OpenClaw 自动限制会话存储增长。默认在 `warn` 模式下运行（报告将要清理的内容）。设置为 `"enforce"` 启用自动清理：

```json5
{
  session: {
    maintenance: {
      mode: "enforce",
      pruneAfter: "30d",
      maxEntries: 500,
    },
  },
}
```

预览：`openclaw sessions cleanup --dry-run`

## 查看会话

- `openclaw status` — 会话存储路径和最近活动
- `openclaw sessions --json` — 所有会话（用 `--active <minutes>` 过滤）
- `/status` — 上下文用量、模型、开关
- `/context list` — 系统提示词内容

## 相关概念

- [[多智能体路由]]
- [[多渠道集成]]
- [[会话裁剪]] — 精简工具结果
- [[压缩]] — 汇总长对话
