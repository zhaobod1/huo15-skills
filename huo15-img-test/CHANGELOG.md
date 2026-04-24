# Changelog

## v2.1.0 — 2026-04-24

**再扩充：更贴近需求 + 更多风格 + 角色一致性。**

### 新增风格预设（+32 款，总 56 → 88）

- **游戏艺术（新类，7）**：原神 / 崩铁星穹 / 英雄联盟 / 暗黑4 / Valorant / Pokemon / 暴雪风
- **东方传统（新类，7）**：敦煌壁画 / 青花瓷 / 民国月份牌 / 年画 / 剪纸 / 和风 / 汉服写真
- **动漫扩展（+4）**：萌系 / 厚涂 / 轻小说封面 / 赛璐璐
- **现代设计（+6）**：玻璃拟态 / 新拟态 / 孟菲斯 / 杂志编排 / 包豪斯 / 奶油风
- **建筑氛围（+3）**：粗野主义 / 北欧极简 / 侘寂
- **摄影扩展（+3）**：暗黑美食 / 日杂 / 街头潮流
- **氛围综合（+2）**：疗愈治愈 / 美式复古

### 新功能

- **角色设定图模式** `--character-sheet` / `-cs`：
  - 自动生成 T-pose + 正面 / 三分之二 / 侧面 / 背面多视图的设定图提示词
  - 专为 Midjourney `--cref`、Stable Diffusion IP-Adapter 做角色参考用
  - 画幅自动锁 16:9
- **时间 / 天气 / 季节 自动抽词**：
  - 14 时间词：清晨 / 黎明 / 黄昏 / 日落 / 深夜 / 蓝调时刻 / 魔法时刻 ...
  - 15 天气词：晴天 / 下雨 / 暴雨 / 下雪 / 暴雪 / 雾天 / 雷雨 ...
  - 10 季节词：春夏秋冬 / 樱花季 / 枫叶季
- **负向需求识别**：识别主体描述中的"不要X / 没有X / 避免X / no X / avoid X / without X"，自动从正向提示中移除并加入负面提示。
- **质量档位** `-t basic / pro / master`：
  - `basic`: `high quality, detailed`（省 token）
  - `pro` (默认): `masterpiece, best quality, ultra detailed, 8k`
  - `master`: 叠加 `hdr, intricate details, sharp focus, award winning, trending on artstation, professional, highly polished`
- **显式负面追加** `--avoid "cluttered, people"`：CLI 级附加负面词。

### 新增别名（+45）

`genshin` / `mihoyo` / `honkai` / `starrail` / `lol` / `diablo` / `valorant` / `pokemon` / `blizzard` / `overwatch` / `dunhuang` / `qinghua` / `porcelain` / `yuefenpai` / `wafu` / `hanfu` / `papercut` / `nianhua` / `moe` / `lightnovel` / `lncover` / `celshaded` / `glassmorphism` / `glass` / `neumorphism` / `memphis` / `editorial` / `bauhaus` / `cream` / `korean` / `brutalism` / `brutalist` / `nordic` / `scandinavian` / `wabisabi` / `zen` / `darkfood` / `muji` / `streetwear` / `hypebeast` / `healing` / `cozy` / `americana` ...

### 改进

- 主体描述中的"不要X"子句会先被 `strip_negative_clauses()` 去除再送入正向提示，避免正向污染。
- `print_prompt()` 输出增加 ⭐ 质量档位、👤 角色设定图模式、🕐 时间、☁️ 天气、🍂 季节、🚫 用户负向 六个新字段展示。
- `list_presets()` 按 8 大类分类展示（新增"游戏" / "东方"分组）。

### 兼容性

- **向下兼容**：v2.0 CLI 命令在 v2.1 完全可用，所有新参数均有默认值。
- **JSON 字段新增**：`quality_tier` / `character_sheet` / `time_of_day` / `weather` / `season` / `user_negatives`（旧字段保留）。

---

## v2.0.0 — 2026-04-24

**大版本升级：一致性 + 贴近需求 + 风格扩充。**

### 新增

- **风格预设 17 → 56**，六大分类：
  - 摄影 10（新增：黑白摄影 / 人像摄影 / 时尚大片 / 美食摄影 / 微距摄影 / 航拍摄影 / 街拍纪实）
  - 动漫 6（新增：新海诚 / 宫崎骏 / 美漫 / Q版 / 童话绘本）
  - 插画 7（新增：工笔国画 / 浮世绘 / 线稿）
  - 3D 7（全部新增：3DC4D / 盲盒手办 / 低多边形 / 等距视图 / 粘土 / 毛毡手工 / 纸艺）
  - 设计 10（新增：平面设计 / Logo设计 / 图标设计 / 信息图 / 品牌KV / 专辑封面 / 电影海报 / 表情包）
  - 艺术史 4（全部新增：印象派 / 后印象派 / 新艺术 / 装饰艺术）
  - 场景氛围 12（新增：黑暗奇幻 / Y2K / Vaporwave / 霓虹灯牌 / 概念艺术）
- **一致性四锁**：每个预设内置 `camera` / `lighting` / `palette` / `aspect` 四项独立锁，系列出图风格不再漂移。
- **系列批量模式** `-s N --variations "A,B,C,D"`：共享 seed + 四锁，主体描述差异化，一次生成一整套。
- **意图识别器**：无需指定 `-p`，脚本从"logo/产品/海报/头像/美食/赛博/水墨..."等关键词自动推荐预设 + 画幅。
- **构图/情绪抽词**：主体描述中的"俯拍/特写/航拍/神秘/温馨/史诗..."自动并入提示词。
- **稳定 seed 建议**：基于 `md5(subject + preset)` 生成 32-bit seed，便于复现。
- **英文 / 同义词别名**：60+ 别名（anime、ghibli、cyberpunk、minimal、3d、logo、neon、vapor…）。
- **多模型精细化适配**：
  - Midjourney 输出 `--ar --stylize`，提示 `--cref/--sref`
  - Stable Diffusion 输出权重语法 `(subject:1.2)`，提示采样器/CFG
  - SDXL 输出推荐尺寸（`1216x832` 等）
  - Flux 输出长句自然语言 + guidance 提示
  - DALL-E 3 输出段落式自然语言
- **JSON 输出** `-j`：结构化一致性锁 + 所有参数，便于下游集成。
- **CLI 增强**：`-a/--aspect`、`--mood`、`--composition`、`--seed`、`-l/--list`、`-v/--version`。

### 修复

- 修复 Logo设计 / 图标设计 / 表情包 / 海报 等预设的**全局负面词包含 "logo/text"** 导致的语义自我否定。
- 修复 水墨 / 工笔国画 / 浮世绘 预设中**负面词包含 "signature"** 与画面印章冲突。

### 破坏性变更

- `build_prompt()` 返回 dict 新增 `aspect` / `seed_suggestion` / `consistency_lock` / `hint` / `version` 字段（向下兼容，原有字段保留）。

---

## v1.0.0 — 2026-04-24（初始版本）

- 17 风格预设（写实摄影 / 胶片摄影 / 动漫 / 赛博朋克 / 水彩 / 油画 / 建筑可视化 / 产品设计 / 像素艺术 / 奇幻 / 科幻 / 复古海报 / 水墨 / 蒸汽朋克 / 极简主义 / 电影感 / 国潮）。
- 支持 Midjourney / SD / DALL-E / 通用 四种输出骨架。
- CLI：`subject -p <preset> -m <model> [-l] [-j]`。
