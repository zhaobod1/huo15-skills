---
name: huo15-openclaw-design-director
displayName: 火一五设计方向顾问技能
description: 当用户没给明确方向时，基于 6 大美学流派 × 24 设计哲学库（含 mobile-native 平台派）生成 3 个反差方向的 Junior pass 简报对比，帮用户快速定流派、定基调、定差异点。配合 huo15-openclaw-frontend-design v4.x 使用，直接读取其 tokens / compare-matrix / redLineWaiver / multi-genre-compare 接力入口。触发词：帮我选设计方向、做几个方向对比、三个风格对比、design direction、设计选型、风格提案、APP 选风格、移动端选方向、iOS 还是安卓、跨端方案选型。
version: 2.0.0
aliases:
  - 火一五设计方向技能
  - 火一五设计方向顾问技能
  - 火一五风格提案技能
  - 火一五方向选型技能
  - 火一五跨端方案技能
  - 火一五设计方向
  - 设计方向
  - 方向选型
  - 风格提案
  - design direction
  - 选风格
  - APP 选风格
  - 跨端选型
---

# 火一五设计方向顾问技能 v2.0

> 多方向设计提案生成 — 青岛火一五信息科技有限公司
> **v2.0 起**：从 5 流派扩到 6 流派含 mobile-native 子集；24 条设计哲学库；与 `huo15-openclaw-frontend-design` v4.x 全量接力（tokens / compare-matrix / multi-genre-compare / redLineWaiver / a11y-checklist）

---

## 一、触发场景

当用户要做一个页面 / 产品 / 品牌 / APP / 小程序，但**没明确美学方向**时：

- "帮我选个设计方向"
- "做三个风格对比"
- "这个 APP 应该做成什么风格"
- "iOS / 安卓 / 鸿蒙 选哪种平台风" ⭐v2.0
- 或在 `huo15-openclaw-frontend-design §三` 被用户选"让你决定"时自动触发

**产出**：3 个反差方向的简报（流派 + tokens 路径 + 差异点 + redLineWaiver）+ 五维对比矩阵 + 推荐方向，按接力消息格式移交给 `frontend-design` 做并行 Junior pass。

---

## 二、设计哲学库（24 条可引用）

### 2.1 极简主义派（5 条）
1. **原研哉（Kenya Hara）** — 白、空、无印良品式的留白美学
2. **Dieter Rams 十诫** — 少即是多，诚实、长寿、环保
3. **Swiss Design / 国际主义** — 网格、无衬线、左对齐
4. **Apple 后乔布斯** — 超大字、超大图、一屏一个重点
5. **Stripe 极简科技** — 渐变 + sans-serif + 大量白

→ 对应 frontend-design 流派：**bold-minimal**

### 2.2 编辑杂志派（4 条）
6. **NYT / 纽约客** — 衬线、纵向栅格、引号做装饰
7. **Monocle 杂志** — 深色衬线 + 米色底 + 分栏
8. **Pentagram 平面** — 超大字排版 + 强烈对比
9. **Hoefler & Co 字体中心主义** — 字体本身就是视觉

→ 对应 frontend-design 流派：**editorial**

### 2.3 前卫实验派（4 条）
10. **Sagmeister 观念先锋** — 手写、大胆、打破规则
11. **David Carson 破坏性排版** — 故意错位、字符切割
12. **Brutalist Web Design** — 粗黑、原始、反精致
13. **Y2K / Vaporwave 复古未来** — 霓虹、CRT、像素

→ 对应 frontend-design 流派：**brutalist** / **retro-future**

### 2.4 东方 / 有机派（4 条）
14. **东方禅意** — 枯山水、空寂、留白 80%
15. **日本民艺（Mingei）** — 手工感、温润、不对称
16. **Field.io 动态几何** — 数字生成艺术
17. **Organic / 有机自然** — 手绘、暖色、柔边

→ 对应 frontend-design 流派：**organic**

### 2.5 信息 / 功能派（3 条）
18. **Tufte 数据可视化** — 数据墨水比、无废装饰
19. **Bauhaus 功能主义** — 形式追随功能、三原色
20. **Edward Tufte 小图密度** — sparkline、紧凑信息层级

→ 对应 frontend-design 流派：B 端 dashboard 场景常 mix **bold-minimal** + 数据组件

### 2.6 移动平台派 ⭐v2.0（4 条）
21. **Apple Human Interface Guidelines** — large title、segmented control、grouped list、blur navbar、HIG spring 动效
22. **Material Design 3 dynamic color** — seed 派生 primary / secondary / tertiary container；FAB；emphasized easing 4 档
23. **HarmonyOS 灵动色块** — 4 色块同明度多色相（L≈0.78）、大圆角胶囊（24-48px 分级）、fluid easing
24. **微信小程序 Native** — `<page-meta>` + `safe-area-inset` + 原生 tabBar、PingFang SC 字体豁免、rpx 适配

→ 对应 frontend-design 流派：**mobile-native-ios** / **mobile-native-md3** / **mobile-native-harmony** + 小程序四端（微信 / 支付宝 / 抖音 / 快手）

---

## 三、3 方向生成法

### 3.1 方向选取规则

**不要选 3 个相似方向**。从 frontend-design v4.1 [`tokens/_compare-matrix.md`](../huo15-openclaw-frontend-design/tokens/_compare-matrix.md) §反差对位 5 组任选一组：

| 命题 | 流派组合 |
|---|---|
| 理性 vs 感性 vs 实验 | bold-minimal × organic × brutalist |
| 冷峻 vs 温暖 vs 复古 | editorial × organic × retro-future |
| 桌面 vs 移动 vs 跨端 ⭐v2.0 | bold-minimal × mobile-native-ios × mobile-native-harmony |
| 极简 vs 信息密度 vs 装饰 | bold-minimal × editorial × retro-future |
| Web vs iOS vs 鸿蒙 ⭐v2.0 | bold-minimal × mobile-native-ios × mobile-native-harmony |

或按"经典 + 反差 + 中间"自由组合：
- **1 个保守方向**（BOLD-MINIMAL / EDITORIAL）
- **1 个反差方向**（BRUTALIST / RETRO-FUTURE / 移动平台派任一）
- **1 个中间调和**（ORGANIC / mobile-native-md3）

### 3.2 每个方向必给 6 件东西 ⭐v2.0 增加 tokens 路径

```
### 方向 N：<流派名>
- **一句话定位**：[ 为谁做 + 什么感觉 ]
- **核心字体**：display + body 组合（从 tokens.json typography 读）
- **主色 + 强调色**：含 oklch 值（从 tokens.json color 读）
- **关键元素**：3 个会被用户记住的视觉元素
- **frontend-design 资产路径** ⭐v2.0：
  - tokens：`../huo15-openclaw-frontend-design/tokens/<slug>.json`
  - example：`../huo15-openclaw-frontend-design/examples/<dir>/index.html`（Junior pass 起手）
- **redLineWaiver 提醒** ⭐v2.0：本流派的合规豁免（避免 design-critique / 评审环节误判违规）
```

### 3.3 五维对比矩阵

| 维度 | 方向 1 | 方向 2 | 方向 3 |
|------|--------|--------|--------|
| 美学震撼 | ★★★☆☆ | ★★★★★ | ★★☆☆☆ |
| 可用性 | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| 品牌辨识 | ★★☆☆☆ | ★★★★★ | ★★★☆☆ |
| 实现成本 | 低 | 高 | 中 |
| 风险 | 低 | 高（可能不被客户接受） | 中 |
| **a11y 友好度** ⭐v2.0 | 见 [`a11y-checklist.md §流派对照`](../huo15-openclaw-frontend-design/references/a11y-checklist.md) |

### 3.4 推荐表态

**必须**给出一个推荐（不能骑墙）：

```
### 推荐
选 **方向 N**，理由：[结合用户的目的、受众、约束的三句话推理]

### 次选
方向 M，适用场景：[如果方向 N 不被接受的退路]

### 反对
不选方向 K，原因：[为什么这条不合适]
```

---

## 四、工作流

### 阶段 1 · 需求分解
- 复述用户的：**目的 / 受众 / 约束 / 时间预算 / 平台**（Web / 移动 / 跨端 / 小程序）⭐v2.0 加平台维度
- 平台维度决定要不要把 mobile-native 子集纳入候选
- 如果以上任一缺失，先用一轮问答补齐

### 阶段 2 · 方向筛选
从 24 条设计哲学库中挑 3 条（按 §3.1 规则组合）

### 阶段 3 · Junior pass 简报生成 ⭐v2.0
本 skill **不直接出 HTML**，而是按下面接力消息格式发给 `frontend-design`，由它跑 [`multi-genre-compare.md`](../huo15-openclaw-frontend-design/references/multi-genre-compare.md) 流程并行出 3 份 Junior pass HTML。

### 阶段 4 · 对比 + 推荐
3 份 Junior pass 截图回流后（frontend-design 自验证用 Chrome MCP 路线），按 §3.3 + §3.4 出报告。

### 阶段 5 · 接力消息格式 ⭐v2.0

```jsonc
// director → frontend-design
{
  "task": "multi-genre-junior-pass",
  "genres": ["bold-minimal", "organic", "brutalist"],
  "context": {
    "client": "<品牌名>",
    "scope": "<目标页面 / 组件类型>",
    "differentiator": "<差异点一句话>",
    "platform": "web | mobile | mini-program | cross"
  },
  "briefs": {
    "bold-minimal": "<本 director 写的简报：定位 + 字体 + 主色 + 关键元素>",
    "organic": "...",
    "brutalist": "..."
  }
}

// frontend-design → director（截图回流）
{
  "task": "multi-genre-junior-pass-done",
  "outputs": [
    { "genre": "bold-minimal", "html": "<rel-path>", "screenshot": "<rel-path>" },
    { "genre": "organic", "html": "<rel-path>", "screenshot": "<rel-path>" },
    { "genre": "brutalist", "html": "<rel-path>", "screenshot": "<rel-path>" }
  ]
}
```

格式与 [`frontend-design/references/multi-genre-compare.md §6`](../huo15-openclaw-frontend-design/references/multi-genre-compare.md) 一致。

---

## 五、与其他 huo15 技能的分工

| 场景 | 归属 |
|------|------|
| 设计方向选型（3 方向对比） | **本技能** |
| 选定方向后做 HTML 原型 | `huo15-openclaw-frontend-design` |
| 评审已有设计 5 维打分 | `huo15-openclaw-design-critique` |
| 抓品牌规范 brand-spec | `huo15-openclaw-brand-protocol` |
| Web / 移动 / 小程序四端 starter / tokens / a11y / motion | `huo15-openclaw-frontend-design` v4.x |

---

## 六、触发词

- 帮我选设计方向 / 选个方向 / 定方向
- 做三个风格对比 / 做几个方向对比 / 出几个风格
- 这个产品应该做成什么风格
- design direction / design proposal
- 设计选型 / 风格提案
- **APP 选风格 / 移动端选方向 / iOS 还是安卓 / 跨端方案选型 / 鸿蒙还是 iOS** ⭐v2.0
- **小程序选哪个风格 / 多端做什么风** ⭐v2.0

---

## 七、版本历史

- **v2.0.0（当前 · 2026-04-27）**：跨端 + 接力升级。流派从 5 扩到 6（加 MOBILE-NATIVE 含 iOS HIG / Material Design 3 / HarmonyOS / 小程序四端）；设计哲学库从 20 条扩到 24 条（新增 §2.6 移动平台派 4 条：HIG / MD3 / HarmonyOS / 微信小程序 Native）；§3.1 方向选取规则加"桌面 / 移动 / 跨端"+"Web / iOS / 鸿蒙"两组反差对位；§3.2 每个方向必给从 5 件扩到 6 件（增 frontend-design tokens 路径 + redLineWaiver 提醒）；§3.3 五维矩阵加 a11y 友好度引用 frontend-design a11y-checklist；§4 工作流阶段 5 移交正式格式化为接力消息 JSON；与 frontend-design v4.x 全量接力 — tokens / compare-matrix / redLineWaiver / multi-genre-compare / a11y-checklist 全部指路。
- **v1.0.0（2026-04-23）**：初始版本。20 条设计哲学库（5 派分类）+ 3 方向生成规则（1 保守 + 1 反差 + 1 中间）+ 五维对比矩阵 + 强制推荐表态（不骑墙）。

---

**技术支持：** 青岛火一五信息科技有限公司
