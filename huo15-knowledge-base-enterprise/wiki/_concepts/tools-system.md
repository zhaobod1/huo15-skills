---
type: concept
title: 工具系统
source: openclaw-docs/tools/index.md
date: 2026-04-06
concepts: [工具, 技能, 插件, 浏览器控制, 代码执行, Web搜索]
---

# 工具系统

## 三层架构

OpenClaw 有三层协同工作的组件：

```
技能（Skill）→ 教会智能体何时、如何使用
  ↓
工具（Tool）→ 智能体实际调用的函数
  ↓
插件（Plugin）→ 打包所有能力
```

### 工具（Tools）

工具是智能体可以调用的带类型函数。例如 `exec`、`browser`、`web_search`、`message`。

内置工具（无需安装插件）：

| 工具 | 功能 |
|------|------|
| `exec` / `process` | 运行 Shell 命令、管理后台进程 |
| `code_execution` | 运行沙箱化远程 Python 分析 |
| `browser` | 控制 Chromium 浏览器（导航、点击、截图）|
| `web_search` / `web_fetch` | 搜索网页、获取页面内容 |
| `read` / `write` / `edit` | 工作区文件 I/O |
| `apply_patch` | 多 hunk 文件补丁 |
| `message` | 跨渠道发送消息 |
| `canvas` | 控制节点画布 |
| `nodes` | 发现和定位已配对设备 |
| `cron` / `gateway` | 管理定时任务、重启网关 |
| `image` / `image_generate` | 分析或生成图像 |
| `sessions_*` / `agents_list` | 会话管理、子智能体 |

### 技能（Skills）

技能是注入到系统提示词中的 Markdown 文件（`SKILL.md`），给智能体提供上下文、约束和分步指导。

技能存放位置：
- 工作区 `skills/` 文件夹（每个智能体独有）
- `~/.openclaw/skills/`（共享技能）

### 插件（Plugins）

插件是可以注册任意组合能力的包：渠道、模型提供商、工具、技能、语音、图像生成等。

- **核心插件**：随 OpenClaw 一起发布
- **外部插件**：社区发布在 npm 上

## 工具配置

### 允许/拒绝列表

通过 `tools.allow` / `tools.deny` 控制智能体可以调用哪些工具，拒绝优先于允许：

```json5
{
  tools: {
    allow: ["group:fs", "browser", "web_search"],
    deny: ["exec"],
  },
}
```

### 工具配置文件

`tools.profile` 设置基础允许列表，然后应用 `allow`/`deny`：
```json5
{ tools: { profile: "relaxed" } }
```

## 相关概念

- [[浏览器控制]]
- [[代码执行]]
- [[技能创建]]
- [[插件开发]]
