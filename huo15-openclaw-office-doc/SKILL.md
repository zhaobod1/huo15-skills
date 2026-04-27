---
name: huo15-openclaw-office-doc
displayName: 火一五文档技能
description: 【青岛火一五信息科技有限公司】企业级 Word & PDF 文档生成 v7.2。12 类规范（公文/合同/会议纪要/技术方案/需求文档/工作报告/商业计划书/用户手册/培训手册/招投标书/演讲稿/研究报告）。三条路径：Word 直出、原生 PDF 直出、Word→PDF。v7.2 修复：合同页眉改为左对齐（LOGO + 公司名）、`**Key：**` markdown 粗体元数据正确识别（合同编号/签订日期/验收日期/甲乙方/金额等 30+ 关键词扩入白名单）、连续多行 KV 自动归并为 2 列元数据表。触发词：写word、写文档、生成word、创建文档、写合同、写方案、写报告、写会议纪要、写需求文档、写商业计划书、写BP、写用户手册、写培训手册、写招标书、写投标书、写演讲稿、写研究报告、写白皮书、生成PDF、写PDF、Word转PDF。
version: 7.2.0
aliases:
  - 火一五文档技能
  - 文档生成
  - Word生成
  - PDF生成
  - 多规范文档
dependencies:
  python-packages:
    - python-docx
    - reportlab
    - pygments  # 可选；装了即代码块语法高亮
---

# 火一五文档技能 v7.2

> 企业级 Word & 原生 PDF 文档生成 — 青岛火一五信息科技有限公司

**愿景：** 加速企业向全场景人工智能机器人转变
**理念：** 打破信息孤岛，用一套系统驱动企业增长

---

## 一、v7.1 关键变化（业界对标后的工程化升级）

> 调研对象：Pandoc reference-doc、Quarto、Typst、markdocx、pandoc-crossref、docxtpl、msoffcrypto-tool；最终挑了 **ROI 最高的 7 项**落地。

1. **CJK 段落属性 OOXML 直写** — 每个段落注入 `autoSpaceDE/DN/kinsoku/wordWrap/overflowPunct`，让 Word/WPS 自动处理"中英文之间空格""数字与中文之间空格""行首禁则字"等中文排版细节。是 Word 内置能力，不加依赖。
2. **首行缩进字符化** — 用 `firstLineChars=200`（200 = 2 字符）替代 `firstLine=cm`。公文规范要求"首行缩进 2 字符"，cm 在不同字号下视觉就跑偏；字符化后跨字号一致。
3. **Pygments 代码块语法高亮** — 30+ 语言、VS Code Light 主题、关键字 / 函数名 / 字符串 / 注释独立着色；Word 端写带颜色 run，PDF 端写 `<font color>` HTML。无 pygments 时静默回落到等宽灰字。
4. **自动 TOC + 标题书签 + outlineLvl** — 标题 paragraph 注入 `_Toc%08d` 书签 + `outlineLvl`；正式规范（技术方案 / 需求文档 / 用户手册 / 招投标书 / 商业计划书 / 培训手册 / 研究报告）默认在标题之后插 `TOC \\o "1-3"` 字段；`settings.xml` 的 `updateFields=true` 让 Word/WPS 打开时自动刷新。
5. **PDF 原生 outline / 文档大纲** — reportlab 用 `BaseDocTemplate.afterFlowable` 钩子把每个标题写成 `bookmarkPage` + `addOutlineEntry`；PDF 阅读器侧边栏直接显示嵌套大纲，可点击跳转。
6. **文档核心属性 + 文档信息** — `core.xml` 写入 title / author / subject / keywords / category / created / modified；PDF 同步元数据。便于投标书系统、OA 全文检索、合规审计。
7. **多行 Key:Value 元数据自动识别（style B）** — 之前要求用 `|` 分隔的元数据行才能被识别；v7.1 加入"连续多行 `课题：xxx / 日期：xxx / 关键词：xxx`"自动归并为 2 列元数据表格的能力。已知关键词扩到 70+。

---

## 二、v7.0 关键变化（前一版本，保留作背景）

1. **原生 PDF 直出**（`create-pdf-doc.py`，新增）— 不经过 Word，reportlab 直接写 PDF；与 Word 渲染共用同一份解析器与规范预设；自带 CJK 字体三层回落与两遍渲染的 `第 X 页 / 共 Y 页` 真页码。
2. **Word→PDF 全面重写**（`word-to-pdf.py` v2.0）— 修掉旧版 main 里的 argparse 语法错；多后端策略 `LibreOffice / docx2pdf / Word COM` 自动回落；macOS / Linux / Windows 路径全覆盖；输出后自动校验 PDF 头有效性；默认嵌入字体避免接收方替换字体。
3. **CJK 软换行不再加空格** — 旧版 `' '.join(lines)` 在中文段落里加多余空格；v7.0 在 CJK ↔ CJK 边界自动跳过空格，ASCII ↔ ASCII 仍保留单空格。
4. **硬换行支持** — Markdown 标准的"行尾 2 空格 `  `"和 CommonMark 扩展"行尾反斜杠 `\`"现在都会被识别成 `<w:br/>` / `<br/>`。
5. **页眉强制左对齐** — 直接写 OOXML `<w:jc w:val="left"/>` 并清掉 `Header` 样式继承的 tab stops；旧版在 WPS / 部分 Word 模板上偶发"页眉飘到中间"的问题彻底修复。
6. **新增 6 类规范** — 商业计划书 / 用户手册 / 培训手册 / 招投标书 / 演讲稿 / 研究报告，从 v6 的 6 类升到 12 类。
7. **解析器拆出** — 共享核心 `doc_core.py`：FormatPreset、12 类预设、Block AST 解析、内联 token 拆分、公司信息回落都在这里；Word / PDF 渲染端都从它读，确保两份输出在版式语义上一致。
8. **显式分页符** — `---PAGE---` / `\pagebreak` / `<!-- pagebreak -->` 插入分页。

---

## 二、12 类文档规范

| 规范 | 触发关键词（标题或正文前 800 字） | 默认版本历史 | 默认审批区 | 页眉布局 |
|------|----------------------------------|-----------|----------|---------|
| 公文 | 默认（未命中其他关键词） | ✅ | ✅ | LOGO+公司名+编号+密级（左） |
| 合同 | 合同 / 协议 / 协议书 | ❌ | ❌ | LOGO+公司名（左，简洁） |
| 会议纪要 | 会议纪要 / 纪要 | ❌ | ❌ | LOGO+公司名（左） |
| 技术方案 | 技术方案 / 实施方案 / 解决方案 / 设计文档 / 架构设计 | ✅ | ✅ | LOGO+公司名+编号+密级（左） |
| 需求文档 | 需求规格 / 需求说明 / SRS / PRD / 需求文档 | ✅ | ✅ | LOGO+公司名+编号+密级（左） |
| 工作报告 | 工作报告 / 周报 / 月报 / 季报 / 年报 / 述职报告 / 汇报材料 | ❌ | ❌ | LOGO+公司名（左） |
| **商业计划书** | 商业计划书 / 商业计划 / BP / 融资计划书 / 路演稿 | ✅ | ❌ | LOGO+公司名+编号+密级（左） |
| **用户手册** | 用户手册 / 操作手册 / 使用说明 / 用户指南 / 产品手册 / Manual | ✅ | ❌ | LOGO+公司名（左，简洁） |
| **培训手册** | 培训手册 / 培训教材 / 教学大纲 / 员工手册 / 入职手册 | ✅ | ❌ | LOGO+公司名（左） |
| **招投标书** | 招标书 / 投标书 / 招投标 / 投标文件 / 招标文件 / 响应文件 | ✅ | ✅ | LOGO+公司名+编号+密级（左） |
| **演讲稿** | 演讲稿 / 致辞稿 / 讲话稿 / 主题分享 / 开闭幕辞 / 颁奖辞 | ❌ | ❌ | LOGO+公司名（左，简洁） |
| **研究报告** | 研究报告 / 学术论文 / 调研报告 / 白皮书 / 行业报告 / Whitepaper | ✅ | ❌ | LOGO+公司名+编号+密级（左） |

> 用 `--doc-format <规范>` 覆盖自动识别；`--with-version-history / --no-version-history / --with-approval / --no-approval` 精细控制附加表格。

### 标题层级识别（每种规范独立）

每种规范都有自己的章节编号正则；同时支持标准 Markdown `# / ## / ### / ####`。例如：

| 规范 | 一级（chapter） | 二级（section） | 三级（article） |
|------|---------------|---------------|----------------|
| 公文 | 第X章/第X节 | 一、二、三、 | （一）（二） |
| 合同 | 第X章/第X条 | 一、二、 | — |
| 商业计划书 | 第X部分/一、二、 | 1.1 | 1.1.1 |
| 用户手册 | 第X章 | X. | X.X |
| 培训手册 | 模块X/单元X/第X课 | 一、二、 | X.X |
| 招投标书 | 第X章/篇/部分 | 一、二、 | （一）（二） |
| 研究报告 | 摘要/Abstract/引言/结论/参考文献/一、 | X. | X.X |

---

## 三、页眉 / 页脚规范

### 3.1 页眉

- **company**（默认）：LOGO + 公司名 + 文档编号 + 密级，**左对齐**
- **minimal**（合同 / 用户手册 / 演讲稿）：LOGO + 公司名，**左对齐**，不显示编号 / 密级
- **centered**（保留备选，当前无规范默认走此项）：仅公司名，居中
- 底部统一灰线 `#888888`

> v7.0 直接写 OOXML `<w:jc>` 并清 `<w:tabs>`，避免 WPS / 部分 Word 模板的样式继承覆盖。

### 3.2 页脚

- 所有规范统一为 `第 X 页 / 共 Y 页`，居中
- Word：`PAGE` / `NUMPAGES` 字段码（打开时自动计算）
- PDF：两遍渲染（NumberedCanvas）拿到真总页数

---

## 四、本地公司信息工作流

页眉的公司名、LOGO 按以下优先级解析：

1. **CLI 显式参数** `--company-name` / `--logo-path`
2. **本地缓存** `~/.huo15/company-info.json`
3. **Odoo `res.company`** 自动拉取（可用 `--no-odoo` 关闭）
4. **退出码 2 + 结构化 JSON** — 以上都拿不到时让 Claude 触发补录流程

### 4.1 标准流程（生成前）

```bash
python3 scripts/company-info.py check
#   exit 0 + 完整 JSON  → 直接生成
#   exit 2 + missing[]  → 进入补录
```

**补录流程**（Claude 执行）：

1. 先查 auto-memory 中的 `huo15_company_info.md` / `user_identity.md`
2. 仍缺失时用 `AskUserQuestion` 询问：公司全称、LOGO 路径、可选 slogan / 地址 / 电话 / 邮箱 / 官网
3. 写入：
   ```bash
   python3 scripts/company-info.py set \
     --company-name "<公司全称>" --logo-path "<LOGO绝对路径>"
   ```
4. 同步写入 memory（`huo15_company_info.md`）

---

## 五、命令行

### 5.1 Word 直出

```bash
python3 scripts/create-word-doc.py \
  --output 方案.docx \
  --title "技术方案：XXX系统" \
  --content @/tmp/content.md \
  --doc-number "HG-FA-2026-001" \
  --version "V1.0" \
  --classification "内部" \
  --author "辉火云管家·贾维斯"
# 可选：
#   --doc-format 技术方案    # 12 类规范任选；'auto' 自动识别
#   --company-name "XX科技"
#   --logo-path /path/to/logo.png
#   --no-odoo
#   --with-version-history / --no-version-history
#   --with-approval / --no-approval
```

### 5.2 PDF 直出（原生）

```bash
python3 scripts/create-pdf-doc.py \
  --output 方案.pdf \
  --title "技术方案：XXX系统" \
  --content @/tmp/content.md \
  --doc-format 技术方案 \
  --doc-number "HG-FA-2026-001"
```

> 原生 PDF 不依赖 LibreOffice / Office；只要装了 `reportlab` 与系统 CJK 字体即可。
> macOS 自带 Songti.ttc / STHeiti.ttc；Linux 推荐 Noto CJK；Windows 可用 SimSun / SimHei。

### 5.3 Word → PDF（保留 Word 原版式，再转）

```bash
python3 scripts/word-to-pdf.py 方案.docx -o 方案.pdf
# 批量
python3 scripts/word-to-pdf.py "*.docx" --output-dir ./pdf/
# 列出可用后端
python3 scripts/word-to-pdf.py --list-backends
# 指定后端 / 不嵌入字体
python3 scripts/word-to-pdf.py 方案.docx --backend libreoffice --no-embed-fonts
```

后端优先级：`libreoffice → docx2pdf → word_com`，自动回落，转换后校验 PDF 头。

### 5.4 何时用哪条路径？

| 场景 | 推荐 |
|------|------|
| 只交付 Word；可能再编辑 | `create-word-doc.py` |
| 只交付 PDF；不需要 Word；要可控版式 | `create-pdf-doc.py`（原生，最快） |
| 同时要 Word 和 PDF；版式必须一致 | `create-word-doc.py` + `word-to-pdf.py` |
| 已有 docx 想转 PDF | `word-to-pdf.py` |

---

## 六、Markdown 能力速查

| 元素 | 写法 | 说明 |
|------|------|------|
| 标题 | `#`~`######` | 也支持规范专属编号（一、 / 1. / 1.1 / 第X章） |
| 段落软换行 | 直接换行 | CJK ↔ CJK 不插入空格；ASCII 仍保留空格 |
| 段落硬换行 | 行尾 `  ` 或 `\` | 同段内强制换行 |
| 列表 | `- item` / `* item` / `1. item` | |
| 强调 | `**粗**` / `*斜*` / `` `inline code` `` | |
| 表格 | 标准 GFM | 缺前导 `|` / 转义 `\|` / 2 列起即可识别 |
| 代码块 | `` ``` ``...`` ``` `` | 等宽灰底；带语言标签 |
| 引用块 | `> ...` | 左侧橘色竖条 + 灰色段 |
| 分隔线 | `---` / `***` / `___` | |
| 元数据行 | `文档编号：XX | 版本：V1.0 | 密级：内部 | 日期：2026-04-27` | 自动两列表格 |
| 分页符 | `---PAGE---` / `\pagebreak` / `<!-- pagebreak -->` | 强制下一页 |
| 空内容 | — | 写"（无正文内容）"灰字占位 |

---

## 七、Python API

```python
# Word
from create_word_doc import create_word_doc
create_word_doc(
    output_path="文档.docx",
    title="技术方案：XXX系统",
    content=md_text,
    doc_number="HG-FA-2026-001",
    version="V1.0",
    classification="内部",
    author="辉火云管家·贾维斯",
    doc_format="auto",            # 12 类规范名 / 'auto'
)

# PDF
from create_pdf_doc import create_pdf_doc
create_pdf_doc(output_path="文档.pdf", title="...", content=md_text,
               doc_format="商业计划书")

# Word → PDF
from word_to_pdf import convert_to_pdf
ok, path = convert_to_pdf("方案.docx", "方案.pdf",
                          backend="auto", keep_fonts=True)
```

> 缺公司信息时三个入口都抛 `RuntimeError`，message 是结构化 JSON，Claude 据此触发补录。

---

## 八、触发词

- 写 word / 写文档 / 写个文档 / 生成 word / 生成文档 / 创建文档
- 导出 word / 导出文档 / 写合同 / 写方案 / 写报告 / 写会议纪要
- 写需求文档 / 写 SRS / 写 PRD
- **写 PDF / 生成 PDF / 导出 PDF / Word 转 PDF**
- 写商业计划书 / 写 BP / 写融资计划书 / 写路演稿
- 写用户手册 / 写操作手册 / 写使用说明 / 写产品手册
- 写培训手册 / 写培训教材 / 写员工手册
- 写招标书 / 写投标书 / 写标书 / 写响应文件
- 写演讲稿 / 写致辞 / 写讲话稿
- 写研究报告 / 写白皮书 / 写学术论文 / 写调研报告

---

## 九、目录结构

```
scripts/
├── doc_core.py          # 共享核心：12 类预设 + Block AST 解析 + 内联 token
├── company-info.py      # 本地公司信息读写 + Odoo 回落
├── create-word-doc.py   # Word 渲染（python-docx + 强制 OOXML jc）
├── create-pdf-doc.py    # 原生 PDF 渲染（reportlab + NumberedCanvas）
└── word-to-pdf.py       # Word → PDF 多后端转换
```

---

## 十一、未来路线（已调研、未实施）

| 功能 | 业界参考 | 优先级 | 复杂度 | 拟引入依赖 |
|------|---------|--------|-------|----------|
| LaTeX → OMML 公式管线 | markdocx / Pandoc | 中 | 中 | latex2mathml + XSLT |
| reference docx 模板继承 | Pandoc / Quarto | 中 | 中 | 仅模板文件 |
| Typst 第四条 PDF 路径（30× 速度） | typst.app + zh-kit | 中 | 中 | typst 二进制 |
| pandoc-crossref 风格交叉引用 `{#fig:xxx}` | pandoc-crossref | 中 | 中 | — |
| 水印 + AES 加密 | msoffcrypto-tool | 低 | 小 | msoffcrypto-tool |
| 修订追踪 / 批注 | docx-revisions | 低 | 大 | docx-revisions |
| docxtpl Jinja2 模板槽 | docxtpl | 低 | 小 | docxtpl |

> 任何一项触发刚需时再上；当前以稳定 + 中文友好 + 易维护为先。

---

## 十、版本历史

- **v7.2.0（当前）**
  - **修复**：合同 / 协议页眉从 `centered`（仅公司名居中）改为 `minimal`（LOGO + 公司名左对齐），与正文左对齐保持一致
  - **修复**：`**合同编号：** HHY-IOT-2025xxx` 这类 markdown 粗体包裹的 Key:Value 现在能被识别。原来三行连写会被 `_smart_join_paragraph` 拼成一段，丢掉换行。现在自动归并为 2 列元数据表。
  - **元数据关键词扩展**：合同编号 / 合同号 / 协议编号 / 订单编号 / 报价编号 / 工单编号 / 发票编号 / 凭证编号 / 签订日期 / 签约日期 / 签署日期 / 生效日期 / 失效日期 / 验收日期 / 交付日期 / 起止日期 / 完成日期 / 甲方 / 乙方 / 丙方 / 签约方 / 发包方 / 承包方 / 采购方 / 供应商 / 金额 / 总价 / 单价 / 数量 / 币种 / 含税 / 税率 / 税额 / 付款方式 / 付款条件 / ContractNo / ContractNumber
  - **`_try_kv_line` 现在剥掉首尾的 markdown 包裹符**（`*` / `~` / `` ` `` / 空白），所以 `*Key:* value`、`` `Key:` value ``、`**Key：** value` 都能被识别
  - Key 长度上限从 16 → 24 字符，覆盖被 markdown 包裹后变长的 key
- **v7.1.0**
  - 业界调研后挑出 7 项落地：CJK 段落属性、字符化首行缩进、Pygments 代码高亮、自动 TOC + 书签、PDF outline、文档核心属性、多行 Key:Value 元数据
  - `doc_core.py` 内置 VS Code Light token 颜色 map，Word / PDF 共用
  - 已知元数据关键词扩到 70+（覆盖课题 / 关键词 / 单位 / 联系人 / 状态 / 期限等）
- **v7.0.0**
  - 解析器拆出 `doc_core.py`，Word / PDF 共用
  - 新增 `create-pdf-doc.py` 原生 PDF 直出（reportlab + 两遍渲染真页码 + CJK 字体三层回落）
  - 新增 6 类规范：商业计划书 / 用户手册 / 培训手册 / 招投标书 / 演讲稿 / 研究报告（共 12 类）
  - 修复 CJK 软换行多余空格；新增 `  ` / `\` 硬换行
  - 强制页眉左对齐（直接写 OOXML jc + 清 tab stops）
  - `word-to-pdf.py` 重写：修语法错、跨平台后端、字体嵌入、自动校验
  - 显式分页符 `---PAGE---` / `\pagebreak`
- **v6.0.0**：Block AST 重写；页眉恒含 LOGO；页脚字段码；代码块 / 引用块
- **v5.3.0**：`company-info.py` 本地公司信息工具
- v5.0.0：多规范自动识别骨架

---

**技术支持：** 青岛火一五信息科技有限公司
