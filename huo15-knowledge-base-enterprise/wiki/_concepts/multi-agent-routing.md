---
type: concept
title: 多智能体路由
source: openclaw-docs/concepts/multi-agent.md
date: 2026-04-06
concepts: [多智能体, 工作区隔离, 路由规则, 渠道账号, 绑定]
---

# 多智能体路由

目标：在一个 Gateway 进程中运行多个**隔离的智能体**（独立的工作区 + `agentDir` + 会话），外加多个渠道账号（如两个 WhatsApp）。

## 核心概念

### 什么是"一个智能体"？

每个**智能体（agent）** 是完整作用域的大脑，拥有自己的：

- **工作区（Workspace）** — 文件、AGENTS.md/SOUL.md/USER.md、本地笔记、角色规则
- **状态目录（agentDir）** — 认证配置、模型注册表、每个智能体的配置
- **会话存储** — 聊天历史和路由状态，位于 `~/.openclaw/agents/<agentId>/sessions`

认证配置是**每个智能体独立**的，不能跨智能体共享。

### 关键路径

| 路径 | 说明 |
|------|------|
| `~/.openclaw/openclaw.json` | 全局配置 |
| `~/.openclaw/agents/<agentId>/agent/` | 智能体状态目录 |
| `~/.openclaw/agents/<agentId>/sessions/` | 会话存储 |
| `~/.openclaw/workspace` 或 `workspace-<agentId>/` | 工作区 |

### 单智能体模式（默认）

- `agentId` 默认为 **`main`**
- 会话 key 为 `agent:main:<mainKey>`
- 工作区默认为 `~/.openclaw/workspace`

## 路由规则

消息通过 **绑定（binding）** 选择智能体，规则为**确定性 + 最具体优先**：

1. `peer` 匹配（精确 DM/群组/频道 ID）
2. `parentPeer` 匹配（线程继承）
3. `guildId + roles`（Discord 角色路由）
4. `guildId`（Discord）
5. `teamId`（Slack）
6. `accountId` 匹配
7. 渠道级别匹配（`accountId: "*"`）
8. 回退到默认智能体

## 快速开始

```bash
# 1. 创建智能体
openclaw agents add work

# 2. 添加入站路由绑定
openclaw agents list --bindings

# 3. 重启并验证
openclaw gateway restart
openclaw channels status --probe
```

## 典型配置场景

### Discord Bot 多智能体

每个 Discord bot 账号映射到唯一的 `accountId`：

```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" },
    ],
  },
  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } },
  ],
}
```

### Telegram Bot 多智能体

```json5
{
  bindings: [
    { agentId: "main", match: { channel: "telegram", accountId: "default" } },
    { agentId: "alerts", match: { channel: "telegram", accountId: "alerts" } },
  ],
}
```

### WhatsApp 多号码

```bash
openclaw channels login --channel whatsapp --account personal
openclaw channels login --channel whatsapp --account biz
```

绑定路由：
```json5
{
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

## 跨智能体内存搜索

如果一个智能体需要搜索另一个智能体的 QMD 会话记录，在 `agents.list[].memorySearch.qmd.extraCollections` 中添加额外集合。

## 沙箱与工具权限

每个智能体可以有自己的沙箱和工具限制：

```json5
{
  agents: {
    list: [{
      id: "family",
      sandbox: { mode: "all", scope: "agent" },
      tools: {
        allow: ["read", "sessions_list"],
        deny: ["exec", "write", "edit"],
      },
    }],
  },
}
```

## 相关概念

- [[OpenClaw 概述]]
- [[网关架构]]
- [[多渠道集成]]
- [[会话管理]]
