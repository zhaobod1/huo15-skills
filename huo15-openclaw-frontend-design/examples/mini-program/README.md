# 小程序 Starter — 火一五前端设计技能 v2.2

> 微信 + 支付宝 双端 starter。**浏览器无法直接渲染** wxml / axml，必须用各家 IDE。

## 微信小程序

1. 下载并安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)（Stable v1.06+）
2. 打开工具 → **项目 → 导入项目** → 目录选 `wechat/`
3. AppID 选"测试号"或填自有；项目名留空走默认
4. 点**编译**：左侧模拟器看渲染；点**真机调试**扫码看真机
5. 页面走 `pages/index/index`，全局配置 `app.json`

## 支付宝小程序

1. 下载并安装 [支付宝小程序 IDE](https://opendocs.alipay.com/mini/ide/download)
2. 打开 IDE → **文件 → 打开项目** → 目录选 `alipay/`
3. 点**预览**，扫码用支付宝 App 看真机
4. 配置文件名是 `mini.project.json`（不是 `project.config.json`），别搞混

## 双端同步迭代姿势

1. 先在 `wechat/` 改完 wxml + wxss + 配置（开发体验更顺）
2. 复制到 `alipay/` 改前缀（机械替换，5 分钟）：
   - `wx:for` → `a:for` / `wx:key` → `a:key` / `wx:if` → `a:if`
   - `bindtap` → `onTap` / `bindinput` → `onInput` / `bindsubmit` → `onSubmit`
   - `wxml` → `axml` / `wxss` → `acss`
   - `<page-meta>` 组件支付宝端不支持，改用 `my.setNavigationBar` API（写在 onLoad）
   - `enhanced="true"` 等微信特有属性删掉
   - `app.json`：tabBar 字段 `color/text` → `textColor/name`
3. 双端 ICON / 图片资源建议放 CDN，本地用 base64 占位

## 反 AI Slop 红线（v2.2 新增小程序专属 #14 / #15）

| # | 禁用项 | 替代方案 |
|---|---|---|
| 14 | 直接套 **WeUI / Vant Weapp / TDesign-Mini / Lin-UI** 默认皮 | 自定义 token，至少改 5 个变量再用 |
| 15 | 缺 `<page-meta>` + `safe-area-inset` + `rpx` 适配 | 见本目录 wechat/pages/index/index.wxml |

通用红线 #1 字体豁免：小程序里 `font-family` 优先 PingFang SC / Source Han Sans SC / Noto Sans SC（不能加载 Web Font）。

## 视觉风格

本 starter 延续 ORGANIC 流派的暖色调（米白 + 土橙 + 暖卡片），主题为"手作商品列表"。`hero` + `chips` + 商品 `grid` 三段式，避开千篇一律的"banner + features + cta"。

## 引用关系

- 配色逻辑参考 [`references/colors.md`](../../references/colors.md) §5 ORGANIC（用 hex 表达 oklch 等价值，因小程序基础库 < 3.0 不一定支持 oklch）
- 字体策略参考 [`references/typography.md`](../../references/typography.md) §6 + 小程序豁免说明（见 SKILL.md §四 v2.2 新增段）
