---
name: huo15-flow-chart
displayName: 火一五流程图技能
description: 规范 + 时尚的流程图、泳道图、系统架构图、C4 架构图、时序图、状态图、ER 图、甘特图生成。输入 YAML/JSON 规格或直接 Mermaid/PlantUML/DOT 源码，输出 SVG/PNG/PDF/draw.io；内置 10 种风格；支持 draw.io 源文件导出 + C4-PlantUML + 架构分层 Tier。触发词：流程图、泳道图、时序图、状态图、ER 图、系统架构图、C4 图、画流程图、生成流程图。
version: 1.2.0
aliases:
  - 火一五流程图
  - 火一五流程图技能
  - 流程图
  - 流程图生成
  - 画流程图
  - 泳道图
  - 时序图
  - 状态图
  - 甘特图
  - ER图
  - 架构图
  - 系统架构图
  - C4 架构图
  - flowchart
  - flow-chart
  - diagram
  - mermaid
  - draw.io
dependencies:
  python-packages:
    - pyyaml
  external:
    - name: "@mermaid-js/mermaid-cli"
      install: "npm i -g @mermaid-js/mermaid-cli"
      notes: "渲染 Mermaid 时用（mmdc 命令）"
    - name: plantuml
      install: "brew install plantuml"
      notes: "PlantUML / C4-PlantUML 渲染（泳道图和 C4 图必须）"
    - name: graphviz
      install: "brew install graphviz"
      notes: "Graphviz DOT 渲染（可选）"
---

# 火一五流程图技能 v1.2.0

> 规范 + 时尚的流程图 / 架构图 / 泳道图 / C4 架构图 / 时序图生成器 — 青岛火一五信息科技有限公司

---

## 一、核心能力

### 1.1 支持的图表类型

| type                 | 用途                    | 渲染引擎          | draw.io |
|---------------------|-----------------------|-----------------|---------|
| `flowchart`          | 普通流程图                | Mermaid         | ✅       |
| `architecture`        | 系统架构图（支持 Tier 分层）  | Mermaid         | ✅       |
| `swimlane`           | 真·泳道图（PlantUML）     | PlantUML        | ❌       |
| `swimlane_mermaid`   | 泳道风格（Mermaid，不需要 Java）| Mermaid | ✅ |
| `sequence`           | 时序图                  | Mermaid/PlantUML | ✅       |
| `state`              | 状态图                  | Mermaid         | ✅       |
| `gantt`              | 甘特图                  | Mermaid         | ✅       |
| `er`                 | ER 图                  | Mermaid         | ✅       |
| `class`              | UML 类图                | Mermaid         | ✅       |
| `journey`            | 用户旅程                 | Mermaid         | ✅       |
| `pie`                | 饼图                   | Mermaid         | ✅       |
| `c4_context`          | C4 上下文图（L1）          | Mermaid / **PlantUML** | ✅ |
| `c4_container`        | C4 容器图（L2）            | Mermaid / **PlantUML** | ✅ |
| `mindmap`            | 简单思维导图               | Mermaid         | ✅       |

### 1.2 输出格式

| 格式   | 类型   | 说明 |
|--------|--------|------|
| `.svg` | 矢量图  | 浏览器直接打开，最推荐 |
| `.png` | 位图    | 适合 PPT / 文档 |
| `.pdf` | 矢量 PDF | 适合打印 |
| `.mmd` | Mermaid 源码 | 复制到 [mermaid.live](https://mermaid.live) 编辑 |
| `.puml` | PlantUML 源码 | 复制到 PlantUML 编辑器 |
| `.drawio` | **draw.io 源文件** | 用 draw.io 桌面版打开，精美编辑 |
| `.dot` | Graphviz DOT 源码 | 复杂网络拓扑 |

### 1.3 十种风格

| key | 名称 | 色调 | 适用场景 | 中文别名 |
|------|-----|------|---------|---------|
| `modern`      | 现代商务   | 深蓝灰 + 橙 | 日常文档、PPT | 现代、商务 |
| `classic`     | 经典稳重   | 蓝紫 + 杏黄 | 正式汇报、咨询 | 经典、稳重 |
| `dark`        | 暗色霓虹   | 深底 + 青粉 | 演示大屏、技术分享 | 暗色、黑色、霓虹 |
| `xiaohongshu` | 小红书暖奶油 | 红 + 米白   | 小红书封面、种草图 | 小红书、奶油、xhs |
| `ocean`       | 海洋蓝     | 天蓝 + 橙 | SaaS 产品、技术架构 | 海洋、蓝、蓝色 |
| `forest`      | 森林绿     | 墨绿 + 琥珀 | 环保、农业、健康 | 森林、绿、自然 |
| `sunset`      | 夕阳暖橙   | 赤橙 + 青 | 运营活动、温暖叙事 | 夕阳、暖橙、橙 |
| `minimal`     | 极简素雅   | 纯黑白灰 | 学术论文、出版物 | 极简、素雅、学术、论文、黑白 |
| `pastel`      | 马卡龙粉嫩 | 粉蓝紫 | 儿童教育、女性向 | 马卡龙、粉嫩、粉、儿童 |
| `github`      | 极客 GitHub | 黑白 + 强调蓝绿 | 开源文档、README | 极客、程序员、gh |

### 1.4 draw.io 精美增强

- 导出 `.drawio` 源文件，用 draw.io 桌面版打开
- draw.io 支持：渐变填充、投影、圆角、图标嵌入
- draw.io 支持 Google Fonts（Mermaid 不支持的中文字体）
- 配合 `--theme` / `--font` / `--shadow` 参数生成精美效果

---

## 二、快速开始

### 2.1 准备渲染器

```bash
# 方案 A：Mermaid（推荐，覆盖 90% 场景）
npm i -g @mermaid-js/mermaid-cli

# 方案 B：PlantUML（C4-PlantUML / 泳道图必须）
brew install plantuml        # macOS
# apt install plantuml       # Ubuntu/Debian

# 方案 C：Graphviz（网络拓扑可选）
brew install graphviz

# Python 依赖
pip install pyyaml
```

### 2.2 最短上手

```bash
# 从 YAML 规格生成 PNG（默认 modern 风格）
python3 scripts/create-flow-chart.py \
  -i examples/architecture.yaml \
  -o /tmp/arch.png

# 泳道图（真·PlantUML）
python3 scripts/create-flow-chart.py \
  -i examples/swimlane.yaml \
  -o /tmp/lane.svg

# 导出 draw.io 源文件（精美编辑）
python3 scripts/create-flow-chart.py \
  -i examples/architecture.yaml \
  -o /tmp/arch.drawio

# 同时导出多种格式（一键到位）
python3 scripts/create-flow-chart.py \
  -i examples/architecture.yaml \
  -o /tmp/arch.png \
  --export-formats svg,pdf,mmd,drawio

# draw.io 精美主题（带投影）
python3 scripts/create-flow-chart.py \
  -i examples/architecture.yaml \
  -o /tmp/arch.png \
  --theme modern --font "Microsoft YaHei" --shadow

# C4-PlantUML（专业 C4 图）
python3 scripts/create-flow-chart.py \
  -i examples/c4_context.yaml \
  -o /tmp/c4.puml \
  --engine plantuml
```

---

## 三、YAML 规格速查

### 3.1 流程图 `flowchart`

```yaml
type: flowchart
title: 用户下单流程
direction: TB          # TB | LR | BT | RL

nodes:
  - { id: start, label: 开始, shape: stadium }
  - { id: check, label: 是否有商品?, shape: diamond }
  - { id: pay,   label: 结算付款 }

edges:
  - { from: start, to: check }
  - { from: check, to: pay, label: 是 }
```

**形状**：`rect` / `round` / `stadium` / `diamond`（判断） / `hexagon` / `circle` / `cylinder`（数据库） / `subroutine` / `parallelogram` / `trapezoid`

**边类型**：`solid`（实线）/ `dashed`（虚线）/ `thick`（粗线）/ `dotted`（点线）/ `bidir`（双向）

### 3.2 系统架构图 `architecture`（支持 Tier 分层）

**方式一：groups 分组**
```yaml
type: architecture
title: 火一五 SaaS 系统架构
groups:
  - { id: frontend, label: 前端层,  children: [web, mobile] }
  - { id: backend,  label: 业务层,  children: [svc_user, svc_order] }
  - { id: data,     label: 数据层,  children: [pg, redis] }
nodes:
  - { id: web, label: Web 门户 }
  - { id: pg,  label: PostgreSQL, shape: cylinder }
edges:
  - [web, svc_user]
  - [svc_user, pg]
```

**方式二：tiers 分层（推荐，层次更清晰）**
```yaml
type: architecture
title: 系统架构（Tier 分层）
tiers:
  - { id: edge, label: 边缘层 }
  - { id: biz,  label: 业务层 }
  - { id: data, label: 数据层 }
nodes:
  - { id: cdn,   label: CDN,       tier: edge }
  - { id: api,   label: API 网关,   tier: biz }
  - { id: pg,    label: PostgreSQL, tier: data, shape: cylinder }
edges:
  - [cdn, api]
  - [api, pg]
```

### 3.3 泳道图 `swimlane`（真·PlantUML）

```yaml
type: swimlane
title: 采购审批流程
lanes:
  - name: 申请人
    steps:
      - { id: A1, label: 填写采购申请 }
      - { id: A2, label: 提交审批 }
  - name: 部门经理
    steps:
      - { id: B1, label: 初审 }
edges:
  - [A1, A2]
  - [A2, B1]
```

### 3.4 时序图 `sequence`

```yaml
type: sequence
title: 用户登录
auto_number: true
nodes:
  - { id: U,  label: 用户,   shape: actor }
  - { id: FE, label: 前端 }
  - { id: BE, label: 后端 }
edges:
  - { from: U,  to: FE, label: 点击登录 }
  - { from: FE, to: BE, label: POST /login }
  - { from: BE, to: FE, label: JWT token, kind: dashed }
notes:
  - { position: over, over: BE, text: "首次登录自动建账" }
```

### 3.5 状态图 `state`

```yaml
type: state
title: 订单状态机
direction: LR
nodes:
  - { id: Pending, label: 待付款 }
  - { id: Paid,    label: 已付款 }
edges:
  - { from: "[*]", to: Pending, label: 下单 }
  - { from: Pending, to: Paid, label: 付款 }
```

### 3.6 甘特图 `gantt`

```yaml
type: gantt
title: Q2 路线图
dateFormat: YYYY-MM-DD
axisFormat: "%m-%d"
sections:
  - name: 基建
    tasks:
      - { name: 服务器扩容, id: i1, status: done,   start: 2026-04-01, duration: 5d }
      - { name: 监控升级,   id: i2, status: active, start: 2026-04-06, duration: 10d }
```

状态值：`done` / `active` / `crit`（关键路径红）/ `milestone`（里程碑）/ 留空即未开始。

### 3.7 C4 架构图 `c4_context` / `c4_container`

**Mermaid 引擎（默认）**
```yaml
type: c4_context
title: 火一五 SaaS 上下文图
nodes:
  - { id: customer, label: 企业客户\n使用 SaaS,  shape: person }
  - { id: huo15,    label: 火一五 SaaS\n企业数字化平台,  shape: system }
  - { id: wecom,    label: 企业微信\nIM,               shape: system_ext }
edges:
  - { from: customer, to: huo15, label: 使用 }
  - { from: huo15,    to: wecom, label: OAuth }
```

**PlantUML 引擎（C4-PlantUML，更专业）**
```bash
python3 scripts/create-flow-chart.py \
  -i examples/c4_context.yaml \
  -o /tmp/c4.puml \
  --engine plantuml
```

C4 shape：`person` / `person_ext` / `system` / `system_ext` / `container` / `container_db` / `component`。

### 3.8 ER 图 / UML 类图 / 用户旅程 / 饼图

- `er` — ER 图，label 用 `\n` 分隔字段
- `class` — UML 类图，edge kind 支持 `extends` / `implements` / `composition` / `aggregation` / `dependency`
- `journey` — 用户旅程，用 `sections[].tasks[]`
- `pie` — 饼图，用 `items` 数组

---

## 四、命令行参数

| 参数 | 说明 |
|------|------|
| `-i, --input` | 输入文件（yaml/json/mmd/puml/dot） |
| `-o, --output` | 输出路径（.svg/.png/.pdf/.mmd/.puml/.dot/.drawio） |
| `--export-formats` | 附加输出格式，逗号分隔。如 `svg,pdf,mmd,drawio` |
| `--export-dir` | 源文件输出目录，默认与主输出同目录 |
| `--style` | 风格：modern/classic/dark/xiaohongshu/ocean/forest/sunset/minimal/pastel/github |
| `--theme` | draw.io 主题（与 --style 对应，影响 draw.io 导出效果） |
| `--font` | 字体名称，默认 PingFang SC（Mac）/ Microsoft YaHei（Win） |
| `--shadow` | 为 draw.io 节点添加投影效果 |
| `--engine` | 强制渲染引擎：mermaid / plantuml / dot / drawio / auto |
| `--width, --height` | 输出尺寸（像素） |
| `--background` | 背景色，默认用 style 的 background |
| `--dump-source` | 只打印源码到 stdout，不渲染（仅 draw.io 输出时生效） |

---

## 五、Python API

```python
import sys; sys.path.insert(0, 'scripts')

from flowchart_core import parse, to_mermaid, to_plantuml, to_drawio
from flowchart_render import render
from styles import get_style, to_mermaid_init_directive, to_plantuml_skinparam

fc = parse('spec.yaml')
style = get_style('xiaohongshu')

# Mermaid
code = to_mermaid(fc, to_mermaid_init_directive(style))
render(code, '/tmp/out.svg', engine='mermaid')

# draw.io（精美源文件）
drawio_xml = to_drawio(fc, style=style, theme='xiaohongshu', font_family='Microsoft YaHei')
render(drawio_xml, '/tmp/out.drawio', engine='mermaid')

# C4-PlantUML
puml = to_plantuml(fc, to_plantuml_skinparam(style))
render(puml, '/tmp/out.puml', engine='plantuml')
```

主要接口：

| 函数 | 说明 |
|------|------|
| `parse(path_or_text, hint='auto')` | YAML/JSON/Mermaid/PlantUML/DOT → FlowChart |
| `to_mermaid(fc, init_directive)` | → Mermaid 源码 |
| `to_plantuml(fc, skinparam)` | → PlantUML/C4-PlantUML 源码 |
| `to_dot(fc, style)` | → Graphviz DOT |
| `to_drawio(fc, style, theme, font_family)` | → draw.io XML 源码（v1.2.0 新增）|
| `render(source, out, engine)` | 调用 mmdc/plantuml/dot 渲染 |
| `get_style(key)` | 获取 Style 对象（中文别名也能识别）|
| `to_mermaid_init_directive(style)` | 返回 `%%{init: ...}%%` 行 |
| `to_plantuml_skinparam(style)` | 返回 PlantUML skinparam 配色指令 |

---

## 六、与其他技能的边界

| 需求 | 用哪个技能 |
|------|----------|
| 自由层级的思维导图，要导出 XMind | **huo15-mind-map** |
| 流程图 / 架构图 / 泳道图 / 时序图 / C4 图 | **huo15-flow-chart**（本技能）|
| **精美架构图**（渐变/投影/圆角），本地编辑 | **huo15-flow-chart** + draw.io 导出 |
| 工程制图 / 原型图 | 不在范围内，建议 draw.io / Figma |
| 数据仪表盘 | 用图表库（Chart.js / ECharts / matplotlib） |

---

## 七、触发词

- 流程图 / 画流程图 / 生成流程图 / 做一张流程图
- 泳道图 / 跨职能流程图 / swim lane
- 系统架构图 / 架构图 / C4 图 / C4 上下文 / C4 容器
- **draw.io 架构图** / 导出 draw.io / draw.io 源文件
- **C4-PlantUML** / C4 图 PlantUML 格式
- 时序图 / 序列图 / sequence diagram
- 状态图 / 状态机 / state diagram
- ER 图 / 实体关系图
- 甘特图 / gantt
- Mermaid / PlantUML
- **架构分层** / Tier 分层 / 多层架构图

---

## 八、版本历史

- **v1.2.0（当前）** — draw.io 导出 + C4-PlantUML + Tier 分层
  - ✅ 新增 `.drawio` 源文件导出（draw.io 桌面版打开，精美编辑）
  - ✅ 新增 `--theme` / `--font` / `--shadow` 参数（draw.io 精美效果）
  - ✅ 新增 `--export-formats`（一键导出多种格式，兼容旧名 `--also`）
  - ✅ 新增 C4-PlantUML 引擎（`--engine plantuml` 输出专业 C4 图）
  - ✅ 新增 `tiers` 分层字段（architecture 类型专用，层次更清晰）
  - ✅ 新增 `node.tier` 属性（替代 group 归类，tiers 模式下使用）
  - ✅ `to_drawio()` Python API（可直接集成到其他工具）
  - ✅ 修复 `.drawio` 导出时 `return` 缺失 bug

- **v1.1.0** — 扩展 6 种风格
  - 新增：`ocean` / `forest` / `sunset` / `minimal` / `pastel` / `github`

- **v1.0.0** — 首版
  - 支持 13 种图表（flowchart / architecture / swimlane / swimlane_mermaid / sequence / state / gantt / er / class / journey / pie / c4_context / c4_container）
  - 3 种输入（YAML/JSON、Mermaid、PlantUML）、6 种输出（svg/png/pdf/mmd/puml/dot）
  - 4 种风格：modern / classic / dark / xiaohongshu

---

**技术支持：** 青岛火一五信息科技有限公司
