# huo15-skills

> 火一五科技所有 Skill 的集中开发仓库，含 60+ Skills。
> 本仓库同时推送 CNB.COOL + GitHub 双端。

## 技术栈
- **格式**: OpenClaw Skill（SKILL.md + assets/ + scripts/）
- **工具**: clawhub CLI 发布
- **Git**: 推 CNB（origin main）→ 推 GitHub（github main）

## 项目结构
```
huo15-skills/
├── CLAUDE.md          # 本文件
├── SKILL.md           # 仓库自身主 Skill
├── skills/            # 所有 Skill 目录
│   ├── huo15-*/       # 各具体技能（odoo/xiaohongshu/office-doc...）
│   └── ...
├── plugins/           # Plugin 插件代码
├── scripts/           # 发布/构建脚本
└── references/        # 参考模板
```

## 发布流程
1. 修改完成 → `git add -A && git commit -m "msg"`
2. `git push origin main`（CNB）
3. `git push github main`（GitHub 镜像）
4. `clawhub publish <slug> --version x.x.x`（发布到 ClawHub）

## 编码规范
- SKILL.md 开头含 YAML frontmatter（name/description/metadata）
- 所有 Skill 保持中文说明 + 实用命令示例
- 新 Skill 必须先验证 `clawhub install <slug>` 能正常安装

## 发布凭据
- ClawHub 账号：jobzhao15 / zhaobod1@163.com
- 发布 token：clh_RlkBsNM1cQUIRaIy8q0OZih3R4GOMgaQMNPw1vP06cw
