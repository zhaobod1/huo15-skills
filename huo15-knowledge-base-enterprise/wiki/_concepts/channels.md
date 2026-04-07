---
type: concept
title: 多渠道集成
source: openclaw-docs/channels/index.md
date: 2026-04-06
concepts: [WhatsApp, Telegram, Discord, iMessage, 渠道配置, 消息路由]
---

# 多渠道集成

## 支持的渠道

OpenClaw 支持同时连接多个聊天平台：

| 渠道 | 说明 | 多账号 |
|------|------|--------|
| **WhatsApp** | 通过 Baileys 库连接 | ✅ |
| **Telegram** | 通过 Bot API | ✅ |
| **Discord** | Bot 账号 | ✅ |
| **iMessage** | 通过 BlueBubbles | ✅ |
| **Signal** | 支持 | ✅ |
| **Slack** | 支持 | ✅ |
| **Microsoft Teams** | 支持 | ✅ |
| **IRC** | 支持 | ✅ |
| **Matrix** | 支持 | ✅ |
| **LINE** | 支持 | ✅ |
| **Feishu（飞书）** | 支持 | ✅ |
| **Zalo** | 支持 | ✅ |
| **Nostr** | 支持 | ✅ |
| **QQ Bot** | 支持 | ✅ |

## 快速配置示例

### Telegram（最快）

```bash
# 1. 通过 BotFather 创建 Bot，获取 token
# 2. 登录
openclaw channels login --channel telegram --bot-token "123456:ABC..."

# 3. 配置
openclaw channels status
```

### WhatsApp

```bash
# 扫码登录
openclaw channels login --channel whatsapp
```

### Discord

1. 在 Discord Developer Portal 创建 Application
2. 添加 Bot 账号
3. 启用 Message Content Intent
4. 邀请 Bot 到服务器

## 渠道配置结构

```json5
{
  channels: {
    telegram: {
      botToken: "123456:ABC...",
      dmPolicy: "pairing",  // pairing | allowlist
      allowFrom: [],
    },
    whatsapp: {
      allowFrom: ["+15551234567"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## 安全策略

- `dmPolicy: "pairing"` — 新用户需配对审批
- `dmPolicy: "allowlist"` — 只允许白名单用户
- 群组默认需要 @mention 才能触发智能体

## 相关概念

- [[Telegram 配置]]
- [[WhatsApp 配置]]
- [[Discord 配置]]
- [[渠道路由]]
- [[设备配对与安全]]
