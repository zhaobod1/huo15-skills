# 5 流派字体对（display + body）

> **禁默认 Inter / Roboto / Arial / system-ui**（参见 SKILL.md §四 红线 #1）。
> 所有推荐字体均来自 [Google Fonts](https://fonts.google.com)、[Adobe Fonts](https://fonts.adobe.com) 或思源系列，license 友好。

## 1. BOLD-MINIMAL

| 角色 | 字体 | 备选 |
|---|---|---|
| display | **Playfair Display** Black Italic | Crimson Pro 900 / Tiempos Display |
| body | **IBM Plex Sans** 400/600 | Söhne / Inter Tight（仅作 fallback，不能首选） |

**反差**：粗衬线 italic ↔ 中性现代无衬线。

## 2. EDITORIAL

| 角色 | 字体 | 备选 |
|---|---|---|
| display | **DM Serif Display** | Cormorant Garamond / Tiempos Headline |
| body | **Source Serif 4** opsz | EB Garamond / 思源宋体 |
| caps | small-caps + letter-spacing .06em | — |

**反差**：display 略 condensed，body 宽松，靠 opsz 自动调节字重。

## 3. BRUTALIST

| 角色 | 字体 | 备选 |
|---|---|---|
| display | **Space Grotesk** 700 | PP Neue Montreal / Druk Wide |
| mono | **JetBrains Mono** 400/800 | Space Mono / IBM Plex Mono |

**反差**：粗 sans 大标题 + mono 元数据 / 导航，等宽字承担"机械感"。

## 4. RETRO-FUTURE

| 角色 | 字体 | 备选 |
|---|---|---|
| display | **Major Mono Display** | Monoton / Audiowide（慎用，易土气） |
| body | **VT323** | Press Start 2P（仅做装饰，不能跑长文） |

**警告**：VT323 可读性弱，正文长度 ≤ 200 字符；超过请退回 IBM Plex Mono。

## 5. ORGANIC

| 角色 | 字体 | 备选 |
|---|---|---|
| display | **Caveat** 600 | Patrick Hand / Reenie Beanie |
| body | **Source Serif 4** | Lora / 思源宋体 |
| 中文配对 | 思源宋体（display 仍用 Caveat 拉手写） | 霞鹜文楷 |

**反差**：手写体只在 hero / 卡片标题 / 注脚，正文一律严肃衬线，避免"小学生作文"。

---

## 通用约束

- 主字 / 副字必须有性格反差：衬线 ↔ 无衬线、或 mono ↔ proportional
- **中文**：思源宋体 / 思源黑体 / 霞鹜文楷 / Noto Serif SC，按流派挑一对（**不要**英文中文混 4 个字族）
- **加载**：`<link rel="preconnect">` 提前连，`display=swap` 避免 FOIT
- 任何"system-ui 兜底就完事"的写法 = 没用本 skill
