---
type: concept
title: 技能系统
source: openclaw-docs/tools/skills.md
date: 2026-04-06
concepts: [技能, SKILL.md, ClawHub, 技能加载, 技能优先级]
---

# 技能系统

## 概念

技能（Skill）是包含 `SKILL.md` 的目录，通过 YAML frontmatter 和指令教会智能体如何使用工具。

OpenClaw 使用 **AgentSkills 兼容**的技能目录格式。

## 技能位置与优先级

OpenClaw 从以下来源加载技能（优先级从高到低）：

1. `skills.load.extraDirs` 配置的额外文件夹
2. 捆绑技能（随安装附带）
3. 托管/本地技能 `~/.openclaw/skills`
4. 个人智能体技能 `~/.agents/skills`
5. 项目智能体技能 `<workspace>/.agents/skills`
6. 工作区技能 `<workspace>/skills`

**同名称技能优先级**：`<workspace>/skills` > `.agents/skills` > `~/.agents/skills` > `~/.openclaw/skills` > 捆绑技能 > extraDirs

## 多智能体场景

- **每个智能体独有技能**：放在对应工作区的 `<workspace>/skills/`
- **共享技能**：`~/.openclaw/skills/` 对所有智能体可见
- **额外共享目录**：`skills.load.extraDirs` 配置

## ClawHub

ClawHub 是 OpenClaw 的公共技能注册表：https://clawhub.com

常用命令：
```bash
# 安装技能到工作区
openclaw skills install <skill-slug>

# 更新所有已安装技能
openclaw skills update --all

# 同步发布更新
clawhub sync --all
```

## 技能文件格式

```yaml
---
name: skill-name
description: 触发条件和功能描述
---

# 技能名称

## 触发词
- 触发条件1
- 触发条件2

## 使用指南
...
```

## 相关概念

- [[工具系统]]
- [[创建技能]]
- [[ClawHub]]
