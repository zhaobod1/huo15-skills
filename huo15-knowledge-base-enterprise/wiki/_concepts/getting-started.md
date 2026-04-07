---
type: concept
title: 安装与入门
source: openclaw-docs/start/getting-started.md
date: 2026-04-06
concepts: [安装, 配置, Node.js, API密钥, 快速开始]
---

# 安装与入门

## 系统要求

- **Node.js**: Node 24（推荐）或 Node 22 LTS（22.14+）
- **API Key**: 从模型提供商获取（Anthropic、OpenAI、Google 等）
- 引导配置会提示输入 API 密钥

检查 Node 版本：
```bash
node --version
```

## 安装方式

### macOS / Linux

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Windows (PowerShell)

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### 其他方式

- npm: `npm install -g openclaw@latest`
- Docker
- Nix

详见 [安装文档](/install)

## 引导配置

```bash
openclaw onboard --install-daemon
```

向导会引导完成：
1. 选择模型提供商
2. 设置 API 密钥
3. 配置 Gateway

## 验证安装

```bash
# 检查网关状态
openclaw gateway status

# 打开控制台
openclaw dashboard
```

## 环境变量（可选）

高级用户或服务账户运行场景：

| 变量 | 说明 |
|------|------|
| `OPENCLAW_HOME` | 内部路径解析的主目录 |
| `OPENCLAW_STATE_DIR` | 覆盖状态目录 |
| `OPENCLAW_CONFIG_PATH` | 覆盖配置文件路径 |

## 下一步

- [[多渠道集成]] — 配置 WhatsApp、Telegram、Discord 等
- [[设备配对与安全]] — 控制谁可以向智能体发消息
- [[网关配置]] — 模型、工具、沙箱和高级设置
- [[工具系统]] — 浏览器、执行、Web 搜索、技能和插件
