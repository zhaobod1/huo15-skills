---
type: concept
title: OpenClaw 概述
source: openclaw-docs/index.md
date: 2026-04-06
concepts: [自托管, 多渠道, AI网关, 跨平台, 开源]
---

# OpenClaw 概述

> OpenClaw — 多渠道自托管 AI 助手网关

## 是什么

OpenClaw 是一个**自托管网关**，将各种聊天应用（WhatsApp、Telegram、Discord、iMessage 等）与 AI 编程智能体连接。只需在自己的机器上运行一个 Gateway 进程，即可随时通过手机或电脑与 AI 助手对话。

**谁适合用？** 开发者和技术爱好者——想要一个私人 AI 助手，又能完全掌控自己的数据，不依赖第三方托管服务。

## 核心特点

| 特点 | 说明 |
|------|------|
| **自托管** | 运行在自有硬件上，数据完全可控 |
| **多渠道** | 一个 Gateway 同时服务 WhatsApp、Telegram、Discord 等 |
| **智能体原生** | 为编程智能体构建，支持工具调用、会话、记忆、多智能体路由 |
| **开源** | MIT 许可证，社区驱动 |

## 工作原理

```
聊天应用 + 插件 → Gateway → AI 智能体
                         → CLI 命令行
                         → Web 控制台
                         → macOS 应用
                         → iOS/Android 节点
```

**Gateway（网关）** 是所有会话、路由和渠道连接的核心中枢。

## 系统要求

- **Node.js**: Node 24（推荐）或 Node 22 LTS（22.14+）
- **API Key**: 从模型提供商获取（Anthropic、OpenAI、Google 等）
- **5分钟**即可完成安装和配置

## 快速开始

```bash
# 1. 安装
npm install -g openclaw@latest

# 2. 引导配置
openclaw onboard --install-daemon

# 3. 验证运行状态
openclaw gateway status

# 4. 打开控制台
openclaw dashboard
```

## 控制台地址

- 本地默认: http://127.0.0.1:18789/
- 远程访问: 需配置 Tailscale 或 SSH 隧道

## 配置文件

配置文件位于 `~/.openclaw/openclaw.json`。默认使用内置 Pi 二进制文件（RPC 模式，按发送者隔离会话）。

示例配置：
```json5
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  messages: { groupChat: { mentionPatterns: ["@openclaw"] } },
}
```

## 相关概念

- [[网关架构]] — WebSocket 网关架构和组件
- [[多渠道集成]] — WhatsApp/Telegram/Discord 等渠道配置
- [[多智能体路由]] — 工作区隔离和按智能体会话
- [[会话管理]] — 会话生命周期和内存管理
