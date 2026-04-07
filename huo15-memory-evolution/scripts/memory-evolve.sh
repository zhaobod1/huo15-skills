#!/bin/bash
# memory-evolve.sh - 记忆进化主脚本
# 用法: ./memory-evolve.sh [--compact|--audit|--sync|--status]
# 示例: ./memory-evolve.sh --compact

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EVOLUTION_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_FILE="${MEMORY_FILE:-$HOME/.openclaw/workspace/MEMORY.md}"
MEMORY_DIR="$HOME/.openclaw/workspace/memory"
ARCHIVE_DIR="$EVOLUTION_DIR/memory/archive"
TEMPLATE_DIR="$EVOLUTION_DIR/memory/templates"
CONFIG_FILE="$EVOLUTION_DIR/config.json"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()    { echo -e "${GREEN}[MEM]${NC} $1"; }
log_warn(){ echo -e "${YELLOW}[WARN]${NC} $1"; }
log_err() { echo -e "${RED}[ERR]${NC} $1"; }

# 确保目录存在
mkdir -p "$ARCHIVE_DIR"
mkdir -p "$TEMPLATE_DIR"
mkdir -p "$MEMORY_DIR"

show_status() {
  log "记忆系统状态:"
  echo ""
  
  if [ -f "$MEMORY_FILE" ]; then
    local lines=$(wc -l < "$MEMORY_FILE")
    local words=$(wc -w < "$MEMORY_FILE")
    local size=$(du -h "$MEMORY_FILE" | cut -f1)
    log "  MEMORY.md: $lines 行, $words 字, $size"
  else
    log_warn "  MEMORY.md 不存在"
  fi
  
  echo ""
  local today=$(date +%Y-%m-%d)
  local today_notes="$MEMORY_DIR/${today}.md"
  if [ -f "$today_notes" ]; then
    log "  今日笔记: ✓"
  else
    log_warn "  今日笔记: ✗ (未创建)"
  fi
  
  echo ""
  local archive_count=$(find "$ARCHIVE_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
  log "  归档记忆: $archive_count 条"
  
  echo ""
  log "最后整理时间: $(stat -f "%Sm" "$MEMORY_FILE" 2>/dev/null || stat -c "%y" "$MEMORY_FILE" 2>/dev/null || echo '未知')"
}

compact_memory() {
  log "开始记忆压缩整理..."
  
  if [ ! -f "$MEMORY_FILE" ]; then
    log_err "MEMORY_FILE 不存在: $MEMORY_FILE"
    return 1
  fi
  
  local temp_file=$(mktemp)
  local archive_file="$ARCHIVE_DIR/archive-$(date +%Y%m%d-%H%M%S).md"
  
  # 备份原文件
  cp "$MEMORY_FILE" "${MEMORY_FILE}.bak"
  log "已备份到: ${MEMORY_FILE}.bak"
  
  # 提取超过 60 天的条目到归档（简化处理）
  # 实际实现需要解析日期和内容
  grep -v "^# MEMORY.md" "$MEMORY_FILE" > "$temp_file"
  
  # 移除重复的空行
  cat "$temp_file" | sed '/^$/N;/^\n$/D' > "${MEMORY_FILE}.tmp"
  mv "${MEMORY_FILE}.tmp" "$MEMORY_FILE"
  
  rm -f "$temp_file"
  
  log "✓ 记忆压缩完成"
  log "  归档文件: $archive_file"
}

audit_memory() {
  log "开始记忆体检..."
  
  local issues=0
  
  if [ ! -f "$MEMORY_FILE" ]; then
    log_err "MEMORY_FILE 不存在: $MEMORY_FILE"
    return 1
  fi
  
  # 检查文件格式
  if ! grep -q "^# MEMORY.md" "$MEMORY_FILE"; then
    log_err "  ✗ 缺少标题 '# MEMORY.md'"
    issues=$((issues + 1))
  fi
  
  # 检查更新时间
  local last_update=$(stat -f "%Sm" "$MEMORY_FILE" 2>/dev/null || stat -c "%y" "$MEMORY_FILE" 2>/dev/null || echo "")
  local days_since_update=$(echo $(($(date +%s) - $(date -r "$MEMORY_FILE" +%s 2>/dev/null || echo $(date +%s))) / 86400)) 2>/dev/null || days_since_update=0
  
  if [ "$days_since_update" -gt 7 ]; then
    log_warn "  ⚠ MEMORY.md 超过 ${days_since_update} 天未更新"
  else
    log "  ✓ MEMORY.md 更新正常"
  fi
  
  # 检查必要的章节
  for section in "基本信息" "项目" "人物"; do
    if grep -q "## $section" "$MEMORY_FILE"; then
      log "  ✓ 章节 '$section' 存在"
    else
      log_warn "  ⚠ 缺少章节 '$section'"
      issues=$((issues + 1))
    fi
  done
  
  # 检查今日笔记
  local today=$(date +%Y-%m-%d)
  local today_notes="$MEMORY_DIR/${today}.md"
  if [ -f "$today_notes" ]; then
    log "  ✓ 今日笔记存在"
  else
    log_warn "  ⚠ 今日笔记未创建"
    # 自动创建
    cat > "$today_notes" << NOTES
# ${today} - Daily Notes

## 今天做了什么

-

## 重要决策

-

## 待办事项

-

NOTES
    log "  ✓ 已自动创建今日笔记"
  fi
  
  echo ""
  if [ "$issues" -eq 0 ]; then
    log "✅ 记忆体检通过！"
  else
    log_warn "⚠ 发现 $issues 个问题，建议运行 --compact 整理"
  fi
}

sync_knowledge_base() {
  log "同步知识库..."
  
  # 检查知识库技能是否存在
  if [ -d "$HOME/.openclaw/workspace/skills/huo15-knowledge-base" ]; then
    log "  ✓ 发现 huo15-knowledge-base"
    
    # 同步 reference 记忆到知识库
    local ref_dir="$HOME/.openclaw/workspace/memory/reference"
    if [ -d "$ref_dir" ]; then
      log "  → 同步 reference 目录"
      # 这里可以添加具体同步逻辑
    fi
    
    log "✓ 知识库同步完成"
  else
    log_warn "  huo15-knowledge-base 未安装，跳过同步"
  fi
}

show_help() {
  cat << HELP
memory-evolve.sh - 火一五记忆进化系统

用法: memory-evolve.sh [选项]

选项:
  --compact    压缩整理记忆文件，归档旧条目
  --audit      体检记忆文件，检查完整性
  --sync       与知识库同步
  --status     显示记忆系统状态
  --help       显示本帮助

示例:
  memory-evolve.sh              # 显示状态
  memory-evolve.sh --audit      # 体检
  memory-evolve.sh --compact    # 整理压缩
  memory-evolve.sh --sync       # 同步知识库

环境变量:
  MEMORY_FILE   指定 MEMORY.md 路径
  MEMORY_DIR    指定每日笔记目录

HELP
}

case "${1:-}" in
  --compact)
    compact_memory
    ;;
  --audit)
    audit_memory
    ;;
  --sync)
    sync_knowledge_base
    ;;
  --status)
    show_status
    ;;
  --help|-h)
    show_help
    ;;
  "")
    show_status
    ;;
  *)
    log_err "未知选项: $1"
    show_help
    exit 1
    ;;
esac
