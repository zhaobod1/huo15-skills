---
name: huo15-img-prompt
displayName: 火一五文生图提示词
description: 火一五文生图提示词 v2.6 — 文生图&视频十一件套：(1) enhance_prompt.py 文生图核心；(2) enhance_video.py 视频 9 模型；(3) reverse_prompt.py 参考图反解；(4) render_prompt.py 10 后端直出；(5) claude_polish.py Claude 智能润色 + top-3 推荐；(6) safety_lint.py 平台合规；(7) image_review.py Claude Vision 五维评审；(8) auto_iterate.py 闭环自动迭代；(9) ⭐v2.6 character.py 角色卡持久化（--save-char/--char）；(10) ⭐v2.6 mcp_server.py MCP stdio server（Claude Code/Cursor/Cline/Continue.dev 直接调用 9 工具）；(11) ⭐v2.6 web_ui.py 本地 Web UI（http://127.0.0.1:7155，可视化 88 预设）。⭐v2.6 还加 enhance_prompt.py --obsidian 写入 vault。适配 Midjourney/SD/SDXL/Flux/DALL-E 3。触发词：文生图、火一五文生图提示词、文生视频、提示词、生成图片、img-prompt、enhance prompt、提示词增强、图片一致性、角色一致、角色卡、character card、混合风格、参考图反解、Claude Vision 评审、闭环迭代、自动改 prompt、auto iterate、image review、五维评审、A/B 测试、智能预设推荐、Claude 润色、平台合规、Obsidian 集成、知识库、MCP server、Claude Code、Cursor、Cline、Web UI、本地 GUI、ComfyUI 直出、Replicate、Fal、即梦、可灵、Hailuo、Sora。
version: 2.6.0
aliases:
  - 火一五文生图提示词
  - 火一五文生图技能
  - 火一五文生视频技能
  - 火一五提示词技能
  - 火一五提示词全家桶技能
  - 火一五AI绘画技能
  - 文生图
  - 文生视频
  - 提示词增强
  - 智能润色
  - 平台合规润色
  - img-prompt
---

# 火一五文生图提示词 v2.6

**CLI / IDE / GUI / 笔记 四栖产品。从一行命令到本地 Web UI 到 Claude Code MCP，全场景覆盖。**

## v2.6 = 十一件套

| 脚本 | 作用 | 一行 demo |
|------|------|-----------|
| `enhance_prompt.py` | 文生图核心 | `enhance_prompt.py "持剑女侠" -p 赛博朋克 --variants 4` |
| `enhance_video.py` | 视频提示词 | `enhance_video.py "汉服少女转身回眸" -p 汉服写真 -m Kling` |
| `reverse_prompt.py` | 参考图反解 | `reverse_prompt.py img.png --mj` |
| `render_prompt.py` | 10 后端直出 | `render_prompt.py "原神少女" -p 原神 --backend jimeng` |
| `claude_polish.py` | Claude 润色 + top-3 推荐 | `claude_polish.py "温柔治愈" --suggest` |
| `safety_lint.py` | 平台合规润色 | `safety_lint.py "战士手中的鲜血" --target dalle` |
| `image_review.py` | Claude Vision 五维评审 | `image_review.py img.png -p "原 prompt"` |
| `auto_iterate.py` | 闭环自动迭代 | `auto_iterate.py "持剑女侠" -p 赛博朋克 --backend dalle --target 7.5` |
| `character.py` ⭐v2.6 | 角色卡持久化 | `enhance_prompt.py "新场景" --char 银发机甲少女` |
| `mcp_server.py` ⭐v2.6 | MCP stdio server | `python3 mcp_server.py` (注册到 ~/.claude/mcp.json) |
| `web_ui.py` ⭐v2.6 | 本地 Web UI | `python3 web_ui.py` (自动开 http://127.0.0.1:7155) |

## 版本演进

| 维度 | v2.3 | v2.4 | v2.5 | v2.6 |
|------|------|------|------|------|
| **风格预设** | 88 | + 参考图链接 | + 智能 top-3 推荐 | 沿用 |
| **一致性** | 沿用 | + session 锁 | + A/B 变体共享 seed | + **角色卡持久化** |
| **贴近需求** | + Claude 润色 | + prompt 压缩 | + Claude 改 prompt | 沿用 |
| **生态闭环** | + 合规重写 | + 10 后端直出 | + VLM 五维评审 | + **Obsidian 写入** |
| **AI 联动** | Claude API | 多轮编辑 | 闭环自动迭代 | + **MCP server** |
| **用户群** | CLI | CLI | CLI | + **IDE + GUI + 笔记** |

## 使用方式

### Agent 调用（推荐）

```
用户: 帮我出一张赛博朋克街头的图
```

Agent 识别到"赛博朋克"触发词，自动调用：

```bash
~/workspace/projects/openclaw/huo15-skills/huo15-img-prompt/scripts/enhance_prompt.py \
    "赛博朋克街头" -p 赛博朋克 -m Midjourney
```

### 直接调用

```bash
cd ~/workspace/projects/openclaw/huo15-skills/huo15-img-prompt

# 基础：指定预设
./scripts/enhance_prompt.py "一只猫" -p 动漫 -m Midjourney

# 自动意图（无需 -p，脚本从关键词推断）
./scripts/enhance_prompt.py "为咖啡品牌设计一个logo"   # → 自动选 Logo设计, 1:1
./scripts/enhance_prompt.py "产品白底图：无线耳机"     # → 自动选 产品摄影, 1:1
./scripts/enhance_prompt.py "微距 一滴露珠"            # → 自动选 微距摄影, 1:1

# 系列一致性（4 张共享 seed + camera/lighting/palette 锁）
./scripts/enhance_prompt.py "红发女侠" -p 动漫 -s 4 \
    --variations "持剑站立,骑马奔驰,弯弓射箭,与龙对视" \
    -m Midjourney

# 英文别名 + 多模型输出
./scripts/enhance_prompt.py "spaceship in nebula" -p scifi -m Flux -a 21:9
./scripts/enhance_prompt.py "minimalist camellia logo" -p logo -m SDXL

# JSON 输出（便于集成）
./scripts/enhance_prompt.py "森林少女" -p ghibli -j
```

## 88 款风格预设

### 【摄影 · 13】
写实摄影 / 胶片摄影 / 黑白摄影 / 人像摄影 / 时尚大片 / 美食摄影 / 产品摄影 / 微距摄影 / 航拍摄影 / 街拍纪实 / **暗黑美食 · 日杂 · 街头潮流** ⭐v2.1

### 【动漫 · 10】
动漫 / 新海诚 / 宫崎骏 / 美漫 / Q版 / 童话绘本 / **萌系 · 厚涂 · 轻小说封面 · 赛璐璐** ⭐v2.1

### 【插画 · 7】
水彩 / 油画 / 水墨 / 工笔国画 / 浮世绘 / 线稿 / 像素艺术

### 【3D · 7】
3DC4D / 盲盒手办 / 低多边形 / 等距视图 / 粘土 / 毛毡手工 / 纸艺

### 【设计 · 15】
极简主义 / 平面设计 / Logo设计 / 图标设计 / 信息图 / 品牌KV / 专辑封面 / 复古海报 / 电影海报 / 表情包 / **玻璃拟态 · 新拟态 · 孟菲斯 · 杂志编排 · 包豪斯 · 奶油风** ⭐v2.1

### 【艺术史 · 4】
印象派 / 后印象派 / 新艺术 / 装饰艺术

### 【场景氛围 · 17】
赛博朋克 / 蒸汽朋克 / 科幻 / 奇幻 / 黑暗奇幻 / 国潮 / Y2K / Vaporwave / 霓虹灯牌 / 建筑可视化 / 电影感 / 概念艺术 / **粗野主义 · 北欧极简 · 侘寂 · 疗愈治愈 · 美式复古** ⭐v2.1

### 【游戏艺术 · 7】⭐ v2.1 新类
原神 / 崩铁星穹 / 英雄联盟 / 暗黑4 / Valorant / Pokemon / 暴雪风

### 【东方传统 · 7】⭐ v2.1 新类
敦煌壁画 / 青花瓷 / 民国月份牌 / 年画 / 剪纸 / 和风 / 汉服写真

> 英文别名支持：`anime`、`ghibli`、`shinkai`、`cyberpunk`、`steampunk`、`scifi`、`minimal`、`logo`、`icon`、`3d`、`c4d`、`octane`、`isometric`、`vangogh`、`artdeco`、`neon`、`vapor`、`y2k`、`genshin`、`lol`、`diablo`、`valorant`、`pokemon`、`dunhuang`、`hanfu`、`wafu`、`glassmorphism`、`neumorphism`、`memphis`、`bauhaus`、`brutalism`、`nordic`、`wabisabi`、`healing`、`cozy`、`americana`、`darkfood`、`muji`、`streetwear`… 运行 `./scripts/enhance_prompt.py -l` 查看完整列表。

## 参数说明

| 参数 | 作用 | 示例 |
|------|------|------|
| `subject` | 主体描述（必填） | `"一只猫"` |
| `-p, --preset` | 风格预设（中文 / 英文别名） | `-p 赛博朋克` / `-p cyberpunk` |
| `-m, --model` | 目标模型 | `Midjourney` / `SD` / `SDXL` / `Flux` / `DALL-E` / `通用` |
| `-a, --aspect` | 画幅 | `1:1` / `3:4` / `16:9` / `21:9` / `9:16` |
| `-t, --tier` ⭐v2.1 | 质量档位 | `basic` / `pro`(默认) / `master` |
| `-cs, --character-sheet` ⭐v2.1 | 角色设定图 T-pose 多视图 | - |
| `--avoid` ⭐v2.1 | 额外负面词，逗号分隔 | `--avoid "cluttered, people"` |
| `--mood` | 情绪覆盖（不给则从主体自动抽） | `--mood 神秘` |
| `--composition` | 构图覆盖 | `--composition 俯拍` |
| `--seed` | 种子（不给则按 subject+preset 哈希生成稳定 seed） | `--seed 42` |
| `-s, --series` | 系列张数 | `-s 4` |
| `--variations` | 系列变体，逗号分隔 | `--variations "A,B,C,D"` |
| `-l, --list` | 列出所有预设 | - |
| `-j, --json` | JSON 输出 | - |

## 自动抽词（v2.1 扩展）

脚本会从主体描述中自动识别以下字段，无需显式参数：

| 维度 | 关键词示例 |
|------|-----------|
| **意图** | logo / 产品 / 海报 / 头像 / 美食 / 汉服 / 敦煌 / 原神 / 玻璃拟态 ... |
| **构图** | 特写 / 近景 / 中景 / 全身 / 俯拍 / 仰拍 / 鸟瞰 / 航拍 / 侧面 / 背面 |
| **情绪** | 温暖 / 冷峻 / 神秘 / 梦幻 / 欢快 / 忧郁 / 史诗 / 高级 / 治愈 / 浪漫 ⭐v2.1：紧张 |
| **时间** ⭐v2.1 | 清晨 / 早晨 / 正午 / 下午 / 黄昏 / 日落 / 夜晚 / 深夜 / 黎明 / 蓝调时刻 |
| **天气** ⭐v2.1 | 晴天 / 多云 / 阴天 / 下雨 / 雨天 / 大雨 / 下雪 / 雪天 / 雾天 / 风暴 / 雷雨 |
| **季节** ⭐v2.1 | 春/夏/秋/冬 / 樱花季 / 枫叶季 |
| **负向需求** ⭐v2.1 | 不要X / 没有X / 避免X / no X / avoid X / without X → 自动入负面 |

## 一致性四锁（核心机制）

每个预设内置以下锁项，所有系列张图共享 ⇒ 风格漂移大幅下降：

| 锁项 | 作用 | 示例（赛博朋克） |
|------|------|----------------|
| `camera` | 镜头焦段 / 视角 | `low angle wide, 24mm anamorphic` |
| `lighting` | 光源 / 光质 | `neon magenta and cyan rim, wet reflective streets` |
| `palette` | 色板 | `magenta cyan black, neon highlights` |
| `aspect` | 画幅 | `21:9` |

系列模式 (`-s N --variations ...`) 额外锁定 **seed**，变换仅发生在主体描述，框架完全不变。

## 模型适配细节

| 模型 | 输出格式 | 特有提示 |
|------|---------|---------|
| **Midjourney** | `主体, 风格, 光影, 色板, 画质 --ar X:Y --stylize 250` | `--cref <url>` 锁角色、`--sref <url>` 锁风格图 |
| **Stable Diffusion** | `(subject:1.2), 风格, ..., 质量` + 负面 | 权重语法 `(word:1.3)`、减弱 `[word]`、DPM++ 2M Karras |
| **SDXL** | 同 SD，尺寸建议 `1024x1024 / 1216x832 / 1536x640 ...` | Refiner 0.2-0.3 |
| **DALL-E 3** | 自然语言段落（已内化负面） | 连续对话中用 "same character / same scene" |
| **Flux** | 长句描述 | guidance 3.5（Dev） / 0（Schnell） |
| **通用** | 逗号分隔 tags | 三大模型通用骨架 |

## 完整示例

```bash
./scripts/enhance_prompt.py "一只戴墨镜的猫在霓虹街头" -p 赛博朋克 -m Midjourney
```

输出：

```
📌 原始描述   : 一只戴墨镜的猫在霓虹街头
🎨 风格预设   : 赛博朋克
🤖 目标模型   : Midjourney
📐 画幅       : 21:9
🎲 种子建议   : 1873940236

✅ 正向提示词：
一只戴墨镜的猫在霓虹街头, cyberpunk, neon-soaked, blade runner aesthetic,
megacity dystopia, holographic ads, low angle wide, 24mm anamorphic,
neon magenta and cyan rim, wet reflective streets,
magenta cyan black, neon highlights,
detailed cyberpunk cityscape, rainy night ambiance,
masterpiece, best quality, ultra detailed, 8k
--ar 21:9 --stylize 250

❌ 负向提示词：
--no rustic, medieval, natural countryside, low quality, worst quality, ...

🔒 一致性锁：
   camera  : low angle wide, 24mm anamorphic
   lighting: neon magenta and cyan rim, wet reflective streets
   palette : magenta cyan black, neon highlights
   aspect  : 21:9

💡 Midjourney tips：
  • 角色/产品系列一致：加 --cref <url> 或 --sref <url>
  • 想要更风格化加 --stylize 500~750；更写实降到 --stylize 50
  • 建议 seed 锁定：--seed 1873940236
```

## v2.6 新功能 ⭐⭐⭐（用户群从 CLI → IDE/GUI/笔记四栖）

### 1. 角色卡持久化 `character.py`

```bash
# Turn 1: 创建角色（带 character-sheet 模式）
enhance_prompt.py "银发机甲少女 twin tails glowing visor" \
    -p 动漫 --character-sheet --save-char 银发机甲少女

# Turn 2 ~ N: 跨调用保持角色一致（自动锁 seed + 注入主体）
enhance_prompt.py "在霓虹街头" --char 银发机甲少女 -p 赛博朋克
enhance_prompt.py "在花海中" --char 银发机甲少女
enhance_prompt.py "持剑战斗" --char 银发机甲少女

# 角色卡管理（独立 CLI）
character.py --list
character.py --show 银发机甲少女
character.py --export 银发机甲少女 > char.json
cat char.json | character.py --import
```

存储：`~/.huo15/characters/<name>.json`，含 use_count + 时间戳 + 五锁。

### 2. Obsidian 集成 `--obsidian`

```bash
# 默认检测 ~/knowledge/huo15 / ~/Documents/Obsidian / ~/Obsidian
enhance_prompt.py "敦煌神女" -p 敦煌壁画 --obsidian

# 指定 vault
OBSIDIAN_VAULT=~/my-vault enhance_prompt.py "..." -p 原神 --obsidian
```

写入 `<vault>/图集/{date}-{subject}-{seed}.md`，含完整 frontmatter（tags/preset/seed/...）+ 正负向提示词 + 一致性锁 + 复现 CLI 命令。

跟 huo15 三层记忆生态吻合（L3 共享 KB wiki）。

### 3. MCP server `mcp_server.py` ⭐ IDE 用户的入口

让 **Claude Code / Cursor / Cline / Continue.dev** 直接调用 9 个工具：

```json
// ~/.claude/mcp.json
{
  "mcpServers": {
    "huo15-img-prompt": {
      "command": "python3",
      "args": ["~/path/to/huo15-img-prompt/scripts/mcp_server.py"]
    }
  }
}
```

暴露的工具：
- `enhance_prompt` / `list_presets` / `preset_examples`
- `suggest_presets` / `polish_prompt` / `safety_lint`
- `review_image` / `list_characters` / `load_character`

实现：手写 JSON-RPC 2.0 over stdio，零第三方依赖。

### 4. 本地 Web UI `web_ui.py` ⭐ 设计师/PM 用户的入口

```bash
python3 web_ui.py             # 默认 http://127.0.0.1:7155
python3 web_ui.py --port 8080
python3 web_ui.py --no-browser
```

特性：
- 单文件 HTML（vanilla JS + Tailwind CDN，零构建）
- Python `http.server.ThreadingHTTPServer` 做后端
- 三栏布局：输入 / 88 预设可视化 / 实时输出
- 角色卡下拉选择 + 一键复制
- 自动开浏览器、Ctrl+C 退出

## v2.5 新功能 ⭐⭐⭐（核心护城河）

### 1. Claude Vision 五维评审 `image_review.py`

```bash
# 单图评审
image_review.py img.png --prompt "原始 prompt"

# 多图排名（同一组 variants 出图后挑最优）
image_review.py renders/*.png --rank
```

输出：
- 五维分数（0-10）：subject_match / composition / lighting / palette / technical
- 加权 overall_score + 三档 verdict（PASS/RETRY/REJECT）
- **可执行修复**：每条 issue 不写"光线不好"，直接给 `add: golden hour rim light, soft fill from camera left`
- 简评模式 `--quick`（只 overall_score，省 token）

### 2. 闭环自动迭代 `auto_iterate.py` ⭐ 杀手级 feature

```
                ┌──────────────┐
                │ user prompt  │
                └──────┬───────┘
                       ↓
            ┌─────────────────────┐
            │  enhance_prompt     │
            └─────────┬───────────┘
                      ↓
            ┌─────────────────────┐
            │  render (10 后端)   │
            └─────────┬───────────┘
                      ↓
            ┌─────────────────────┐
            │  Claude Vision      │
            │  五维评审           │
            └─────────┬───────────┘
                      ↓
                  分数 ≥ 阈值?
                  ↙          ↘
                Y              N (≤ 3 轮)
                ↓               ↓
              完成        ┌────────────┐
                          │ Claude 改   │
                          │ prompt     │
                          └─────┬──────┘
                                ↑
                          (回到 enhance)
```

```bash
auto_iterate.py "持剑女侠" -p 赛博朋克 --backend dalle --target 7.5 --max-rounds 3
```

每轮锁定 seed，便于对比 prompt 改动到底改善了哪一维。Claude 的修改基于上轮 review 的 actionable_fixes，输出 revised_subject + extra_negatives + extra_mood + rationale。

**这个能力 GPT-4o image / Claude Imagen 内部做不到** — 它们是端到端黑盒，没有 prompt-image 闭环数据。

### 3. A/B 变体测试 `--variants N`

```bash
# 同 subject + 同 seed，仅在 mood/composition 上分化出 4 个变体
enhance_prompt.py "持剑女侠" -p 赛博朋克 --variants 4 -j > variants.json

# 出图后挑最优
image_review.py renders/*.png --rank
```

四个差异轴可选：`mood / composition / lighting / stylize`，`--variant-axes mood,lighting` 自定义。

### 4. 智能预设推荐 `--suggest`

```bash
# 模糊描述也能自动匹配预设
enhance_prompt.py "温柔治愈感的画面" --suggest
```

输出：top-3 候选预设 + 每个的 score (0-1) + reason + best_subject_example + mix_suggestion（自动判断是否需要混合）。

解决"温柔"、"高级"、"梦幻"等抽象描述硬关键词匹配不到的痛点。

## v2.4 新功能 ⭐

### 1. render_prompt.py 扩到 10 后端

```bash
# 国际开源
render_prompt.py "侠客" -p 水墨 --backend replicate --remote-model black-forest-labs/flux-schnell
render_prompt.py "猫" -p 动漫 --backend fal --remote-model fal-ai/flux/dev

# 国产模型（中文场景效果好）
render_prompt.py "敦煌神女" -p 敦煌壁画 --backend jimeng    # 字节即梦 / Seedream 3.0
render_prompt.py "汉服少女" -p 汉服写真 --backend kling     # 快手可灵 v1
render_prompt.py "原神少女" -p 原神 --backend hailuo        # 海螺 MiniMax image-01
```

环境变量：`REPLICATE_API_TOKEN` / `FAL_KEY` / `ARK_API_KEY`（火山方舟）/ `KLING_API_KEY` / `MINIMAX_API_KEY`。

### 2. prompt 压缩 `--compact`

```bash
enhance_prompt.py "持剑女侠" -p "赛博朋克+水墨" -m SD --compact
# 🗜  prompt 已压缩: 124→73 tokens (砍 12 段)
```

策略：去重 → 同义合并 → 保头 6 段（主体+camera）→ 按预算砍尾。专治 SDXL CLIP 77 token 截断。

### 3. 88 预设参考图链接 `--examples`

```bash
# 看单个预设的参考图（5 平台搜索 URL）
enhance_prompt.py --examples 敦煌壁画
# 列表模式带链接
enhance_prompt.py -l --with-examples
```

输出 5 平台搜索 URL：Lexica / Civitai / Pinterest / Google Images / Unsplash。零维护，靠搜索 query 永远有效。

### 4. 多轮编辑 `--session` / `--continue`

```bash
# Turn 1: 出图
enhance_prompt.py "猫坐在窗台" -p 写实摄影 --session catwindow

# Turn 2: 改画幅 + 加情绪，seed 自动锁定保证主体一致
enhance_prompt.py --continue catwindow --aspect 16:9 --mood 治愈

# Turn 3: 完全换主体描述但保 seed 测一致性
enhance_prompt.py "猫站起来伸懒腰" --continue catwindow

# 列出所有 session
enhance_prompt.py --list-sessions
```

持久化目录：`~/.huo15/sessions/<name>.json`。CLI 参数 > session 默认值 > 系统默认。

## v2.3 新功能 ⭐

### 5. Claude API 智能润色 `--polish`

```bash
# 直接润色（独立调用）
export ANTHROPIC_API_KEY=sk-ant-xxx
./scripts/claude_polish.py "一个温柔的女孩在花丛中"
./scripts/claude_polish.py "敦煌神女" --pipe   # 输出可直接喂给 enhance_prompt.py 的命令

# 在 enhance_prompt.py 里串联使用（润色 → 88 预设 → 输出）
./scripts/enhance_prompt.py "一个温柔的女孩在花丛中" --polish
./scripts/enhance_prompt.py "雪山下的小屋" --polish --safety MJ -m Midjourney
```

利用 Claude prompt engineering 优势：
- **Prompt caching**：system prompt 用 ephemeral cache，省 90% input token
- **Prefill `{`**：assistant 起手 `{` 强制 JSON 输出，无需 tool use
- **XML 思维链**：让 Claude 内部分步骤（refine/style/camera/safety/negatives）
- **88 预设嵌入 system**：Claude 从清单里挑，不凭记忆
- **零 SDK 依赖**：纯 urllib，避免企业扫描器拦截 anthropic 包

### 6. 平台合规润色 `--safety`

**只做合法艺术创作的平台误判规避，不做 jailbreak。**

```bash
# 独立调用
./scripts/safety_lint.py "战士手中沾满鲜血的剑" --target dalle
./scripts/safety_lint.py "古典维纳斯雕像 nude figure" --target MJ --apply
./scripts/safety_lint.py "如何制作炸弹"   # 命中红线 → exit 2

# 在 enhance_prompt.py 里串联
./scripts/enhance_prompt.py "古风战场鲜血飞溅" --safety dalle
./scripts/enhance_prompt.py "黑暗骑士斩杀恶魔" --safety MJ -p 黑暗奇幻
```

**红线（直接拒答）**：
- ✗ CSAM（未成年 + 性化任意组合）
- ✗ 真人 + 色情/政治污蔑
- ✗ 武器/毒品/爆炸物**制作方法/教程**
- ✗ 自残/自杀**方法诱导**

**黄区（艺术化重写）**：
| 类别 | 例子 | 重写策略 |
|------|------|----------|
| violence | 血、伤口、kill、weapon | crimson splash / battle-scarred / vanquish / ceremonial blade |
| nudity | 裸、naked、sexy | classical figure study / fine art reference / fashion editorial |
| horror | horror、gore、demon | gothic atmospheric tension / mythical creature |
| death | dead、skeleton、skull | memento mori / classical allegory / vanitas |
| real-person | celebrity、明星、politician | fictional character / 80s aesthetic |
| brand | marvel、disney、nike | superhero comic style / classic animated |

**平台分级**：
- DALL-E `max` 严格度
- MJ `high` 中等
- SD/SDXL/Flux `low` 宽松（开源本地）

### 7. Polish + Safety 串联（最强组合）

```bash
# Claude 智能润色 → 平台合规重写 → 88 预设增强
./scripts/enhance_prompt.py "战士在血战之后凝视远方" --polish --safety dalle -j
```

输出 JSON 包含 `claude_polish` 和 `safety_lint` 两个完整 meta 块，可追溯每一步改写过程。

## v2.2 新功能详解

### 1. 混合预设 `-p A+B --mix 0.6`

```bash
# 主预设 60% 权重，副预设 40%
enhance_prompt.py "持剑女侠" -p "赛博朋克+水墨" --mix 0.6 -m Midjourney
enhance_prompt.py "山中神女" -p "原神+敦煌壁画" --mix 0.5 -m SDXL
enhance_prompt.py "极简卡片" -p "玻璃拟态+侘寂" --mix 0.7 -m SD
```

融合策略：
- **tags**：主预设标签前置，副预设按权重补充；SD 自动加权重语法 `(tag:1.16)`
- **camera**：取主预设（避免镜头语言混乱）
- **lighting**：叠加 `主光照, blended with 副光照`
- **palette**：拼接两者
- **aspect**：取主预设默认画幅
- **neg**：合并去重 + PRESET_NEG_EXCLUDE 主辅都生效（避免 logo/text/signature 自我否定）
- **seed**：mix_label `A+B@0.60` 参与 hash，相同混合每次同 seed

### 2. 视频提示词 `enhance_video.py`

```bash
# Sora 8 秒赛博朋克
enhance_video.py "雨夜霓虹街头一只猫漫步" -p 赛博朋克 -m Sora --duration 8

# Kling 慢速跟拍
enhance_video.py "汉服少女转身回眸" -p 汉服写真 -m Kling --motion 慢速跟拍

# 史诗节奏 + 自定义动作
enhance_video.py "宇宙飞船穿越星云" -p scifi -m Runway --pacing 史诗 --action "ship accelerates, lens flare"

# 混合风格 + 海螺 MiniMax
enhance_video.py "山中神女腾云" -p "原神+敦煌壁画" --mix 0.6 -m Hailuo

# 列出所有视频模型规格
enhance_video.py --list-models
```

支持的视频模型：

| 模型 | 上限时长 | 默认画幅 | 提示词风格 |
|------|---------|---------|-----------|
| Sora | 20s (Sora 2 Pro) | 16:9 | 长自然语言 |
| Kling 可灵 | 10s (1080p Pro) | 16:9 | 中文优秀，前置主体 |
| Runway Gen-3/4 | 10s | 16:9 | 英文最佳 |
| Pika | 10s | 16:9 | 标签式 + `-gs/-motion` |
| Luma DreamMachine | 9s | 16:9 | 自然语言 + 关键帧 |
| Hailuo MiniMax | 10s | 16:9 | 中英双语 + 参考人物 |
| 即梦 Seedance | 12s | 16:9 | 中文多镜头剧情 |
| 通义 Wan2.1 | 8s | 16:9 | 阿里开源 14B/1.3B |

输出包含：正向 / 负向（视频专属：flicker、motion blur、identity drift）/ 三段式关键帧 / 一致性六锁（+ motion）。

### 3. 参考图反解 `reverse_prompt.py`

```bash
# 自动识别 A1111/ComfyUI/NovelAI metadata
reverse_prompt.py /path/to/image.png

# 远程 URL
reverse_prompt.py https://example.com/img.png

# 直接给 Midjourney 复用 prompt（一行）
reverse_prompt.py img.png --mj

# 强制 VLM 模板（图无 metadata）
reverse_prompt.py img.png --vlm

# JSON pipe 给 enhance_prompt.py
reverse_prompt.py img.png -j > recipe.json
```

三层反解：
1. **PNG metadata**：手写 `tEXt`/`iTXt` 解析，零 PIL 依赖
2. **A1111 / ComfyUI / NovelAI 三大格式自动识别**
3. **VLM fallback**：图无 metadata 时输出标准 prompt 给 GPT-4o/Claude/Gemini/Qwen-VL

启发式预设猜测：35+ 关键词映射（cyberpunk → 赛博朋克 / ghibli → 宫崎骏 / dunhuang → 敦煌壁画 ...）。

### 4. 直出图片 `render_prompt.py`

```bash
# Dry-run（只输出 recipe，不出图）
render_prompt.py "敦煌神女" -p 敦煌壁画 --backend none -j

# AUTOMATIC1111 / Forge SD WebUI
render_prompt.py "赛博朋克猫" -p 赛博朋克 --backend sd-webui

# ComfyUI（用内置 SDXL workflow）
render_prompt.py "原神少女" -p 原神 --backend comfyui

# ComfyUI（自定义 workflow）
render_prompt.py "原神少女" -p 原神 --backend comfyui --workflow ./workflows/sdxl.json

# DALL-E 3
render_prompt.py "极简logo" -p Logo设计 --backend dalle --size 1024x1024
```

特点：
- **零第三方依赖**：纯 urllib，避免企业扫描器命中
- **环境变量覆盖**：`COMFYUI_URL` / `SDWEBUI_URL` / `OPENAI_API_KEY`
- **支持混合预设直出**

## 参考文档

`references/t2i-guide.md` — 提示词要素表 / 88 预设对照 / 模型差异 / 一致性技巧。

## 版本历史

见 `CHANGELOG.md`。
