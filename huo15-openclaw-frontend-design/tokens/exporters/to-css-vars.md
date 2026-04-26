# tokens.json → CSS Variables

> 把任一 `<slug>.json` 转成可在 `<style>` 顶层使用的 CSS variables。

## 一行 jq 命令（推荐）

```bash
jq -r '
  ":root {",
  (.color | to_entries[] | "  --color-\(.key): \(.value);"),
  (.spacing | to_entries[] | "  --spacing-\(.key): \(.value)px;"),
  (.radius | to_entries[] | "  --radius-\(.key): \(if (.value | type) == "number" then "\(.value)px" else .value end);"),
  (.shadow | to_entries[] | "  --shadow-\(.key): \(.value);"),
  "}"
' tokens/bold-minimal.json
```

## 输出示例（bold-minimal）

```css
:root {
  --color-ink: oklch(0.18 0 0);
  --color-paper: oklch(0.99 0.005 95);
  --color-accent: oklch(0.66 0.20 28);
  --color-mute: oklch(0.45 0 0);
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 32px;
  --spacing-xl: 64px;
  --spacing-2xl: 128px;
  --radius-none: 0px;
  --radius-sm: 2px;
  --radius-md: 8px;
  --radius-lg: 14px;
  --radius-pill: 999px;
  --shadow-subtle: 0 1px 2px oklch(0 0 0 / .05);
  --shadow-card: 0 4px 16px oklch(0 0 0 / .08);
  --shadow-modal: 0 16px 48px oklch(0 0 0 / .15);
}
```

## 批量导出（所有流派）

```bash
mkdir -p generated/css
for f in tokens/*.json; do
  slug=$(basename "$f" .json)
  jq -r '...' "$f" > "generated/css/$slug.css"
done
```

## hex fallback（不支持 oklch 的环境）

```bash
jq -r '
  ":root {",
  (.colorHex | to_entries[] | "  --color-\(.key): \(.value);"),
  "}"
' tokens/bold-minimal.json
```

## 注意

- 本 skill **不内置 spawn**，上述命令是给用户保存到自己项目里跑的（铁律延续 enhance 插件"禁 child_process"）
- `radius.irregular`（organic 流派）值是字符串如 `"48% 52% 55% 45% / 50% 50% 50% 50%"`，jq 上面那行 `if number` 判断已正确处理
