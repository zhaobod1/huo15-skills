---
type: reference
title: CLI 命令参考
source: openclaw-docs/cli/index.md
date: 2026-04-06
concepts: [CLI, 命令行, openclaw, 网关管理, 渠道管理]
---

# CLI 命令参考

## 核心命令

### 网关管理

| 命令 | 说明 |
|------|------|
| `openclaw gateway start` | 启动网关 |
| `openclaw gateway stop` | 停止网关 |
| `openclaw gateway restart` | 重启网关 |
| `openclaw gateway status` | 查看网关状态 |

### 引导配置

| 命令 | 说明 |
|------|------|
| `openclaw onboard` | 引导设置向导 |
| `openclaw onboard --install-daemon` | 安装为系统服务 |

### 控制台

| 命令 | 说明 |
|------|------|
| `openclaw dashboard` | 打开 Web 控制台 |
| `openclaw status` | 查看状态 |

### 渠道管理

| 命令 | 说明 |
|------|------|
| `openclaw channels login --channel <name>` | 登录渠道 |
| `openclaw channels status` | 查看渠道状态 |
| `openclaw channels status --probe` | 探测渠道连接 |

### 智能体管理

| 命令 | 说明 |
|------|------|
| `openclaw agents add <name>` | 添加新智能体 |
| `openclaw agents list` | 列出所有智能体 |
| `openclaw agents list --bindings` | 查看智能体绑定 |
| `openclaw agents remove <name>` | 删除智能体 |

### 会话管理

| 命令 | 说明 |
|------|------|
| `openclaw sessions` | 列出所有会话 |
| `openclaw sessions --json` | JSON 格式输出 |
| `openclaw sessions cleanup --dry-run` | 预览会话清理 |

### 技能管理

| 命令 | 说明 |
|------|------|
| `openclaw skills install <slug>` | 安装技能 |
| `openclaw skills update --all` | 更新所有技能 |

### 配对管理

| 命令 | 说明 |
|------|------|
| `openclaw pairing list` | 列出已配对设备 |
| `openclaw pairing approve <id>` | 审批配对请求 |
| `openclaw pairing revoke <id>` | 撤销配对 |

### 节点管理

| 命令 | 说明 |
|------|------|
| `openclaw nodes list` | 列出已连接节点 |
| `openclaw nodes status` | 节点状态 |

### 配置

| 命令 | 说明 |
|------|------|
| `openclaw config get <key>` | 获取配置项 |
| `openclaw config set <key> <value>` | 设置配置项 |
| `openclaw config edit` | 编辑配置文件 |

### 日志与调试

| 命令 | 说明 |
|------|------|
| `openclaw logs` | 查看日志 |
| `openclaw logs --follow` | 实时跟踪日志 |
| `openclaw doctor` | 运行诊断检查 |

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENCLAW_HOME` | 内部路径解析的主目录 |
| `OPENCLAW_STATE_DIR` | 覆盖状态目录 |
| `OPENCLAW_CONFIG_PATH` | 覆盖配置文件路径 |
| `OPENCLAW_GATEWAY_TOKEN` | 网关认证令牌 |

## 配置文件

主配置：`~/.openclaw/openclaw.json`

详见 [[网关配置]]
