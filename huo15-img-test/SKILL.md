---
name: huo15-img-test
displayName: 火一五文生图提示词增强
description: 文生图提示词增强技能 v2.1 — 输入一句话描述，输出贴近需求、一致性强、专业级的 T2I 提示词。88 款风格预设（10 摄影+3 摄影扩展 / 10 动漫 / 7 插画 / 7 3D / 15 设计 / 4 艺术史 / 17 场景 / 7 游戏艺术 / 7 东方传统）、自动意图识别（主体+时间+天气+季节+构图+情绪+负向需求）、camera/lighting/palette/aspect/seed 五锁、系列批量、角色设定图模式、basic/pro/master 三档画质。适配 Midjourney / Stable Diffusion / SDXL / Flux / DALL-E 3。触发词：文生图、提示词、生成图片、img-test、text to image、enhance prompt、提示词增强、图片一致性、系列图、角色一致、批量出图、原神风、敦煌风、汉服写真、玻璃拟态、角色设定图。
version: 2.1.0
---

# huo15-img-test — 文生图提示词增强 v2.1

**一句话描述 → 贴合需求、一致性强的专业 T2I 提示词。**

## 版本演进

| 维度 | v1 → v2.0 | v2.0 → v2.1 |
|------|-----------|-------------|
| **风格预设** | 17 → **56**（六大类） | 56 → **88**（新增游戏/东方/现代设计/建筑/氛围/动漫子系） |
| **一致性** | 仅风格标签 → camera/lighting/palette/aspect 四锁 + seed + 系列模式 | + **角色设定图模式**（T-pose 多视图给 MJ --cref） |
| **贴近需求** | 意图识别 + 构图/情绪抽词 | + **时间 / 天气 / 季节** 抽词 + **负向需求识别** (不要X/no X) |
| **画质控制** | 固定 masterpiece | + **basic / pro / master 三档** |

## 使用方式

### Agent 调用（推荐）

```
用户: 帮我出一张赛博朋克街头的图
```

Agent 识别到"赛博朋克"触发词，自动调用：

```bash
~/workspace/projects/openclaw/huo15-skills/huo15-img-test/scripts/enhance_prompt.py \
    "赛博朋克街头" -p 赛博朋克 -m Midjourney
```

### 直接调用

```bash
cd ~/workspace/projects/openclaw/huo15-skills/huo15-img-test

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

## 参考文档

`references/t2i-guide.md` — 提示词要素表 / 56 预设对照 / 模型差异 / 一致性技巧。

## 版本历史

见 `CHANGELOG.md`。
