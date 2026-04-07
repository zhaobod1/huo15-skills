---
type: concept
title: 网关架构
source: openclaw-docs/concepts/architecture.md
date: 2026-04-06
concepts: [WebSocket, 网关协议, 设备配对, 远程访问, 协议类型]
---

# 网关架构

## 概述

一个单一的**长连接 Gateway（网关）** 拥有所有消息渠道（WhatsApp、Telegram、Slack、Discord、Signal、iMessage、WebChat）。控制平面客户端（macOS 应用、CLI、Web UI、自动化脚本）通过 **WebSocket** 连接到网关，默认地址 `127.0.0.1:18789`。

**节点**（macOS/iOS/Android/无头）也通过 WebSocket 连接，但声明 `role: node`，并声明自己的能力/命令。

每台宿主机只运行一个 Gateway；它是唯一打开 WhatsApp 会话的组件。

## 核心组件

### Gateway（守护进程）

- 维护提供商连接
- 暴露带类型的 WS API（请求、响应、服务端推送事件）
- 验证入站帧是否符合 JSON Schema
- 发送事件：`agent`、`chat`、`presence`、`health`、`heartbeat`、`cron`

### 客户端（macOS / CLI / Web 管理端）

- 每客户端一个 WS 连接
- 发送请求：`health`、`status`、`send`、`agent`、`system-presence`
- 订阅事件：`tick`、`agent`、`presence`、`shutdown`

### 节点（移动设备 / 无头节点）

- 以 `role: "node"` 连接同一 WS 服务器
- 连接时提供设备身份；配对是**基于设备**的
- 暴露命令：`canvas.*`、`camera.*`、`screen.record`、`location.get`

## 连接生命周期

```
Client → Gateway: req:connect
Gateway → Client: res (ok)
Gateway → Client: event:presence
Gateway → Client: event:tick

Client → Gateway: req:agent
Gateway → Client: res:agent (ack: runId, status: accepted)
Gateway → Client: event:agent (streaming)
Gateway → Client: res:agent (final: runId, status, summary)
```

## 协议要点

- **传输**: WebSocket，JSON 负载的文本帧
- **首帧必须**是 `connect`
- 认证：若设置了 `OPENCLAW_GATEWAY_TOKEN`（或 `--token`），`connect.params.auth.token` 必须匹配
- 幂等键：副作用方法（`send`、`agent`）需要幂等键以安全重试

## 设备配对与本地信任

- 所有 WS 客户端在 `connect` 时包含**设备身份**
- 新设备 ID 需要配对审批；Gateway 颁发**设备令牌**供后续连接使用
- **本地**连接（回环或网关宿主机的同一 tailnet 地址）可自动审批
- 所有连接必须对 `connect.challenge` nonce 签名
- **非本地**连接仍需明确审批

## 远程访问

- **首选**: Tailscale 或 VPN
- **备选**: SSH 隧道

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

## 操作命令

| 操作 | 命令 |
|------|------|
| 启动 | `openclaw gateway`（前台运行，日志输出到 stdout）|
| 健康检查 | WS 上的 `health` 请求 |
| 进程管理 | launchd/systemd 自动重启 |

## 相关概念

- [[OpenClaw 概述]]
- [[多渠道集成]]
- [[多智能体路由]]
- [[安全模型]]
