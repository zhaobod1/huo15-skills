# huo15-searxng

> SearXNG 自托管搜索引擎一键部署 - Docker Compose + OpenClaw 配置自动化

## 功能特性

- 🔍 **一键部署**：Docker Compose 自动部署 SearXNG 实例
- 🔄 **端口冲突自动处理**：8888 → 8889 → 8890 自动检测可用端口
- ⚙️ **OpenClaw 无缝集成**：自动配置 `SEARXNG_BASE_URL` 环境变量
- ✅ **健康检查**：启动后自动验证服务可用性

## 前提条件

- Docker Desktop (macOS) / Docker Engine (Linux)
- docker compose v2 (`docker compose` 命令)

## 快速开始

### 安装 Skill

```bash
clawhub install huo15-searxng --dir ~/.openclaw/workspace/skills
```

### 部署 SearXNG

```bash
@贾维斯 安装 SearXNG
```

或手动执行安装脚本：

```bash
bash ~/.openclaw/workspace/skills/huo15-searxng/scripts/install.sh
```

## 工作原理

```
安装脚本流程：
1. 检查 Docker + docker compose v2
2. 端口 8888-8890 可用性检测
3. 渲染 docker-compose.yml
4. docker compose up -d
5. 健康检查 (HTTP 200)
6. 配置 SEARXNG_BASE_URL
7. 输出完成信息
```

## 目录结构

```
huo15-searxng/
├── SKILL.md              # Skill 定义
├── README.md             # 本文档
├── scripts/
│   ├── install.sh        # 核心安装脚本
│   ├── env.sh            # 环境变量加载
│   └── status.sh         # 状态检查
└── templates/
    └── docker-compose.yml.template
```

## 配置说明

### 环境变量

安装后自动添加以下环境变量到 `~/.zshrc`：

```bash
export SEARXNG_BASE_URL="http://localhost:8888"
```

### OpenClaw 配置

OpenClaw 自动检测 `SEARXNG_BASE_URL` 环境变量，无需手动配置。

如需手动配置，编辑 `~/.openclaw/openclaw.json`：

```json
{
  "plugins": {
    "entries": {
      "searxng": {
        "config": {
          "webSearch": {
            "baseUrl": "http://localhost:8888"
          }
        }
      }
    }
  }
}
```

## 常用命令

| 操作 | 命令 |
|------|------|
| 查看状态 | `bash ~/.openclaw/workspace/skills/huo15-searxng/scripts/status.sh` |
| 查看日志 | `docker logs searxng` |
| 重启服务 | `cd ~/docker/searxng && docker compose restart` |
| 停止服务 | `cd ~/docker/searxng && docker compose down` |
| 卸载 | `rm -rf ~/docker/searxng` + 删除 `~/.zshrc` 中的 SEARXNG_BASE_URL |

## 端口说明

| 端口 | 说明 |
|------|------|
| 8888 | 默认端口 |
| 8889 | 备用端口 1 |
| 8890 | 备用端口 2 |

脚本会按顺序检测，找到第一个可用端口为止。

## 故障排除

### Docker 未安装

```bash
# macOS
brew install --cask docker

# Linux (Ubuntu)
curl -fsSL https://get.docker.com | sh
```

### 端口全部占用

手动指定端口后重新安装：

```bash
cd ~/docker/searxng
# 编辑 docker-compose.yml 修改端口
docker compose up -d
# 手动设置环境变量
export SEARXNG_BASE_URL="http://localhost:你指定的端口"
```

### SearXNG 启动失败

```bash
docker logs searxng
docker compose -f ~/docker/searxng/docker-compose.yml logs
```

## 技术参考

- [SearXNG 官方文档](https://docs.searxng.org/)
- [OpenClaw SearXNG 配置](https://docs.openclaw.ai/tools/searxng-search)
- [SearXNG GitHub](https://github.com/searxng/searxng)

## License

MIT
