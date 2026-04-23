---
name: huo15-img-test
description: 文生图提示词增强技能 — 输入一句话描述，输出专业级 T2I 提示词。支持 17 种风格预设（写实摄影/动漫/建筑/产品/水墨等），适配 Midjourney / Stable Diffusion / DALL-E / Flux 等主流模型。触发词：文生图、提示词、生成图片、img-test、text to image、enhance prompt、提示词增强。
---

# huo15-img-test — 文生图提示词增强

## 功能

将用户的一句话描述转化为结构化、专业级的文生图提示词。

## 使用方式

### 交互模式（推荐）

```
用户: 帮我生成一个赛博朋克城市的提示词
```

Agent 调用 `enhance_prompt.py`，脚本执行后返回增强结果。

### 直接调用脚本

```bash
cd ~/workspace/projects/openclaw/huo15-skills/huo15-img-test
./scripts/enhance_prompt.py "一只赛博朋克风格的猫" -p 赛博朋克 -m Midjourney
```

## 风格预设

| 编号 | 预设名 | 特点 |
|------|--------|------|
| 01 | 写实摄影 | Canon R5, 85mm, 专业影棚光 |
| 02 | 胶片摄影 | Kodak Portra 400, 胶片颗粒 |
| 03 | 动漫 | Ghibli 风格, 精致眼睛 |
| 04 | 赛博朋克 | 霓虹灯, 雨夜, 赛博朋克美学 |
| 05 | 水彩 | 柔和边缘, 纸张质感 |
| 06 | 油画 | 印象派, 笔触可见 |
| 07 | 建筑可视化 | V-Ray, 干净线条 |
| 08 | 产品设计 | 白底, 商业摄影 |
| 09 | 像素艺术 | 16-bit, 复古游戏风 |
| 10 | 奇幻 | 史诗构图, ArtStation 热榜 |
| 11 | 科幻 | 全息, 未来科技感 |
| 12 | 复古海报 | 1950s, letterpress |
| 13 | 水墨 | 中国水墨, 极简禅意 |
| 14 | 蒸汽朋克 | 铜铜色调, 维多利亚, 齿轮 |
| 15 | 极简主义 | 大量留白, 简洁构图 |
| 16 | 电影感 | 电影感, 光晕, 体积光 |
| 17 | 国潮 | 中国传统元素, 朱红金色 |

## 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `-p, --preset` | 风格预设 | 见上表，默认"写实摄影" |
| `-m, --model` | 目标模型 | `Midjourney` / `Stable Diffusion` / `DALL-E` / `Flux` / `通用` |
| `-l, --list` | 列出所有预设 | - |
| `-j, --json` | JSON 格式输出 | - |

## 完整示例

```
用户: 帮我生成一张未来城市的图片，赛博朋克风格

Agent 执行:
./scripts/enhance_prompt.py "未来城市" -p 赛博朋克 -m Midjourney

输出:
✅ 增强提示词:
cyberpunk, neon lights, rain-soaked streets, blade runner aesthetic, holographic ads, fog, future city, masterpiece, best quality, epic, detailed cyberpunk cityscape

❌ 负面提示词:
natural, countryside, low quality, medieval
```

## 参考文档

详细风格标签和模型差异说明见 `references/t2i-guide.md`。
