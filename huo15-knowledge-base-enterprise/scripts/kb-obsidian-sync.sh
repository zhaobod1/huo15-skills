#!/bin/bash
# kb-obsidian-sync.sh — 知识库同步到 Obsidian vault
# 用法:
#   ./scripts/kb-obsidian-sync.sh [--dry-run]
#   ./scripts/kb-obsidian-sync.sh --vault "我的笔记库"

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_ROOT="$(dirname "$SCRIPT_DIR")"
WIKI_DIR="$KB_ROOT/wiki"

DRY_RUN=false
VAULT_NAME=""

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --vault)
      VAULT_NAME="$2"
      shift 2
      ;;
    --help)
      echo "用法: kb-obsidian-sync.sh [--dry-run] [--vault 'vault-name']"
      echo "  --dry-run  预览模式（不实际写入）"
      echo "  --vault    指定 vault 名称（默认使用 obsidian-cli 默认 vault）"
      exit 0
      ;;
    *)
      shift
      ;;
  esac
done

echo "🔄 知识库 → Obsidian 同步"

# Step 1: 找到 Obsidian vault 路径
find_vault() {
  if [ -n "$VAULT_NAME" ]; then
    obsidian-cli print-default --path-only 2>/dev/null || true
    cat ~/Library/Application\ Support/obsidian/obsidian.json 2>/dev/null | \
      python3 -c "import sys,json; d=json.load(sys.stdin); [print(v['path']) for n,v in d.items() if '$VAULT_NAME' in n or v.get('alias','') == '$VAULT_NAME']" 2>/dev/null || true
  else
    obsidian-cli print-default --path-only 2>/dev/null || \
      cat ~/Library/Application\ Support/obsidian/obsidian.json 2>/dev/null | \
      python3 -c "import sys,json; d=json.load(sys.stdin); [print(v['path']) for v in d.values() if v.get('open')]" 2>/dev/null
  fi
}

VAULT_PATH=$(find_vault)

if [ -z "$VAULT_PATH" ]; then
  echo "❌ 未找到 Obsidian vault，请先设置默认 vault: obsidian-cli set-default '<vault-name>'"
  exit 1
fi

echo "📁 Vault: $VAULT_PATH"

OBSIDIAN_KB_DIR="$VAULT_PATH/知识库"
mkdir -p "$OBSIDIAN_KB_DIR"

if [ ! -d "$WIKI_DIR" ]; then
  echo "⚠️  wiki/ 目录不存在，请先运行: ./scripts/compile.sh"
  exit 1
fi

WIKI_COUNT=$(find "$WIKI_DIR" -name "*.md" | wc -l | tr -d ' ')
echo "📤 将同步 $WIKI_COUNT 个文件到 Obsidian..."

sync_file() {
  local src="$1"
  local rel_path="${src#$WIKI_DIR/}"
  local dest="$OBSIDIAN_KB_DIR/$rel_path"
  local dest_dir=$(dirname "$dest")

  mkdir -p "$dest_dir"

  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would sync: $rel_path → $dest"
  else
    if ! head -1 "$src" | grep -q "^---"; then
      local title=$(basename "$src" .md | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1))substr($i,2)} 1')
      local date=$(date +%Y-%m-%d)
      local temp_file=$(mktemp)
      {
        echo "---"
        echo "type: knowledge-base"
        echo "title: \"$title\""
        echo "source: knowledge-base"
        echo "date: $date"
        echo "---"
        echo ""
        cat "$src"
      } > "$temp_file"
      mv "$temp_file" "$dest"
    else
      cp "$src" "$dest"
    fi
    echo "✅ Synced: $rel_path"
  fi
}

export -f sync_file
find "$WIKI_DIR" -name "*.md" -type f | while read -r file; do
  sync_file "$file"
done

echo ""
echo "✅ 同步完成！"
echo "📂 Obsidian 知识库: $OBSIDIAN_KB_DIR"
echo ""
echo "在 Obsidian 中打开 vault，笔记在 '知识库' 文件夹中"
