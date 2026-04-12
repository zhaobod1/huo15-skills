---
name: huo15_searxng
version: 1.0.0
description: SearXNG 自托管搜索引擎一键部署 - Docker Compose + OpenClaw 配置自动化
homepage: https://github.com/zhaobod1/huo15-skills
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["docker", "git"]
---

# huo15-searxng

SearXNG 自托管搜索引擎一键部署技能。

## 触发词

- "安装 SearXNG"、"部署 SearXNG"
- "searxng"、"SearXNG"
- "自托管搜索"、"私有搜索"
- "搭建搜索"

## 功能

当用户请求安装或部署 SearXNG 时，执行 `scripts/install.sh` 进行自动化部署：

1. 检查 Docker 和 docker compose 环境
2. 检测可用端口（8888 → 8890）
3. 一键部署 SearXNG 容器
4. 等待服务就绪并验证
5. 自动配置 OpenClaw 环境变量

## 使用方式

```
@贾维斯 安装 SearXNG
```

## 前提条件

- Docker 已安装并运行
- docker compose v2 已安装

## 技术细节

- SearXNG 镜像：`searxng/searxng:latest`
- 数据目录：`~/docker/searxng/`
- 默认端口：8888（自动检测冲突并切换）
- OpenClaw 配置：`SEARXNG_BASE_URL` 环境变量
