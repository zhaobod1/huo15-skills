#!/bin/bash
# status.sh — 检查 SearXNG 运行状态

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/env.sh" 2>/dev/null || true

DOCKER_DIR="${DOCKER_DIR:-$HOME/docker/searxng}"

echo "🔍 SearXNG 状态检查"
echo "═══════════════════════════════════════════════════"

# 1. 容器状态
echo ""
echo "📦 Docker 容器:"
if docker ps | grep -q searxng; then
    echo "   ✅ searxng 容器运行中"
    docker ps --filter name=searxng --format "   状态: {{.Status}} | 镜像: {{.Image}}"
else
    echo "   ❌ searxng 容器未运行"
fi

# 2. 端口状态
echo ""
echo "🌐 端口检测:"
# 尝试从 docker port 获取实际映射的端口
MAPPED_PORT=$(docker port searxng 2>/dev/null | grep '8080/tcp' | grep -oP '\d+$' || echo "")
if [ -n "$MAPPED_PORT" ]; then
    PORT=$MAPPED_PORT
fi

if nc -z localhost $PORT 2>/dev/null; then
    echo "   ✅ 端口 $PORT 可访问"
else
    echo "   ❌ 端口 $PORT 无法访问"
fi

# 3. 服务状态
echo ""
echo "🔍 服务状态:"
if curl -sf "http://localhost:$PORT/healthz" > /dev/null 2>&1; then
    echo "   ✅ SearXNG 健康检查通过"
else
    echo "   ❌ SearXNG 健康检查失败"
fi

# 4. JSON API 测试
echo ""
echo "🔧 JSON API 测试:"
JSON_RESULT=$(curl -sf "http://localhost:$PORT/search?q=hello&format=json" 2>/dev/null | head -c 200 || echo "")
if echo "$JSON_RESULT" | grep -q '"results"'; then
    echo "   ✅ JSON API 正常"
else
    echo "   ❌ JSON API 异常"
fi

# 5. 环境变量
echo ""
echo "📝 OpenClaw 配置:"
if [ -n "$SEARXNG_BASE_URL" ]; then
    echo "   SEARXNG_BASE_URL=$SEARXNG_BASE_URL"
else
    echo "   ⚠️  SEARXNG_BASE_URL 未设置"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "📚 Docker 配置目录: $DOCKER_DIR"
echo "🔧 常用命令:"
echo "   查看日志: docker logs searxng"
echo "   重启服务: cd $DOCKER_DIR && docker compose restart"
echo ""
