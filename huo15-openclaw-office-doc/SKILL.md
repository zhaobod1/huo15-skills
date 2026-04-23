---
name: huo15-openclaw-office-doc
displayName: 火一五文档技能
description: 【青岛火一五信息科技有限公司】企业级 Word 文档生成 v6.0。按内容自动挑选规范（公文/合同/会议纪要/技术方案/需求文档/工作报告），页眉始终有公司 LOGO + 名称，页脚始终是"第 X 页 / 共 Y 页"；新增 Block AST 解析、代码块、引用块，修复两列表格与空内容问题。触发词：写word、写文档、生成word、创建文档、写合同、写方案、写报告、写会议纪要、写需求文档、生成PDF、Word转PDF。
version: 6.0.0
aliases:
  - 火一五文档技能
  - 文档生成
  - Word生成
  - 多规范文档
dependencies:
  python-packages:
    - python-docx
---

# 火一五文档技能 v6.0

> 企业级 Word 文档生成 — 青岛火一五信息科技有限公司

**愿景：** 加速企业向全场景人工智能机器人转变
**理念：** 打破信息孤岛，用一套系统驱动企业增长

---

## 一、v6.0 关键变化

1. **Block AST 重写的 Markdown 解析** — 解决了 v5.x "有时正文是空的" / "两列表格不识别" 等零星 bug。
2. **页眉恒为"LOGO + 公司名"** — 无论是哪种规范，都必带 LOGO 与公司全称；公文 / 方案 / 需求还会带上文档编号与密级。
3. **页脚恒为 "第 X 页 / 共 Y 页"** — 用 Word/WPS 原生字段码 (`PAGE` / `NUMPAGES`) 实现，打开文档时自动计算。
4. **代码块 & 引用块** — `` ```lang...``` `` → 等宽灰底段；`> ...` → 左侧橘色竖条 + 灰色段。
5. **版本历史 / 审批表仅在正式规范追加** — 公文、技术方案、需求文档默认追加；合同 / 会议纪要 / 工作报告默认不加，可用 `--with-version-history / --with-approval` 强制。
6. **两列表格修复** — 过去要求至少 3 列才识别，现在只要 `| a | b |` 就会渲染为表格。

---

## 二、支持的文档规范

| 规范 | 触发关键词（标题或正文前 500 字） | 默认版本历史 | 默认审批区 | 典型场景 |
|------|----------------------------------|-----------|----------|---------|
| 公文 | 默认（未命中其他关键词） | ✅ | ✅ | 正式函件、通知、请示 |
| 合同 | 合同 / 协议 / 协议书 | ❌ | ❌ | 商业合同、保密协议（需要签字可手动加 `--with-approval`） |
| 会议纪要 | 会议纪要 / 纪要 | ❌ | ❌ | 会议记录、工作纪要 |
| 技术方案 | 技术方案 / 实施方案 / 解决方案 / 设计文档 | ✅ | ✅ | 项目方案、架构设计 |
| 需求文档 | 需求规格 / 需求说明 / SRS / PRD / 需求文档 | ✅ | ✅ | SRS、PRD |
| 工作报告 | 工作报告 / 周报 / 月报 / 季报 / 年报 / 述职报告 | ❌ | ❌ | 周报、月报、述职 |

> 可用 `--doc-format <规范>` 覆盖自动识别；`--with-version-history / --no-version-history / --with-approval / --no-approval` 精细控制附加表格。

### 标题层级识别

同时支持以下三种层级来源（优先级从高到低）：

1. **标准 Markdown** — `# / ## / ### / ####`
2. **规范专属中文编号** — 不同规范的层级前缀会自动映射到一/二/三级：

| 规范 | 一级 | 二级 | 三级 |
|------|------|------|------|
| 公文 | 第X章/第X节 | 一、二、三、 | （一）（二） |
| 合同 | 第X章/第X条 | 一、二、 | — |
| 会议纪要 | 【主题】 | 一、二、 | （一）（二） |
| 技术方案 | 一、1. | 1.1 | 1.1.1 |
| 需求文档 | 一、1. | 1.1 | — |
| 工作报告 | 一、 | （一） | — |

---

## 三、页眉 / 页脚规范

### 3.1 页眉

- 永远有 LOGO + 公司名。
- 公文 / 技术方案 / 需求文档：LOGO + 公司名 + 文档编号 + 密级。
- 合同：仅公司名，居中。
- 底部配灰色细线。

### 3.2 页脚

- 所有规范统一为 `第 X 页 / 共 Y 页`。
- 使用 `PAGE` 与 `NUMPAGES` OpenXML 字段码，Word / WPS 打开时自动计算；转 PDF 后正确显示。

---

## 四、本地公司信息工作流（v5.3 引入，v6.0 保留）

页眉的公司名、LOGO 按以下优先级解析：

1. **CLI 显式参数** `--company-name` / `--logo-path`
2. **本地缓存** `~/.huo15/company-info.json`（主）
3. **Odoo `res.company`** 自动拉取（第三优先级，可用 `--no-odoo` 关闭）
4. **提示用户补录** — 以上都拿不到时，`create-word-doc.py` 退出码 2，stderr 输出结构化 JSON

### 4.1 Claude 生成文档前的标准流程

```bash
# ① 检查本地公司信息
python3 scripts/company-info.py check
#   exit 0 + 完整 JSON  → 直接进入生成步骤
#   exit 2 + missing[]  → 进入补录流程
```

**补录流程**（Claude 执行）：

1. 先查 auto-memory 中的 `huo15_company_info.md` / `user_identity.md`。
2. 仍缺失时，用 `AskUserQuestion` 询问：
   - 公司全称（必填）
   - LOGO 文件路径（必填，默认 `~/.huo15/assets/logo.png`）
   - 可选 slogan / 地址 / 电话 / 邮箱 / 官网
3. 写入本地：
   ```bash
   python3 scripts/company-info.py set \
     --company-name "<公司全称>" --logo-path "<LOGO绝对路径>"
   ```
4. 同步写入 memory（`huo15_company_info.md`），下次会话可复用。

> **不要**把 LOGO 图像本身塞进 memory；memory 里只记"路径 + 关键字段"。

### 4.2 数据字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `company_name` | ✅ | 公司全称 |
| `logo_path` | ✅ | LOGO 绝对路径；文件需存在且 >1KB 才算有效 |
| `slogan` / `address` / `phone` / `email` / `website` | — | 补充信息 |

---

## 五、命令行

### 5.1 推荐调用（argparse）

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
#   --doc-format 技术方案             # 覆盖自动识别
#   --company-name "XX科技"           # 覆盖本地缓存
#   --logo-path /path/to/logo.png
#   --no-odoo                         # 不回落 Odoo
#   --with-version-history            # 非正式规范也追加版本历史
#   --with-approval                   # 强制追加审批表
#   --no-version-history / --no-approval  # 正式规范关闭附加表
```

> `--content` 以 `@` 开头时读取对应路径文件；否则按字面字符串处理。

### 5.2 Python API

```python
from create_word_doc import create_word_doc

create_word_doc(
    output_path="文档.docx",
    title="技术方案：XXX系统",
    content=md_text,
    doc_number="HG-FA-2026-001",
    version="V1.0",
    classification="内部",
    author="辉火云管家·贾维斯",
    doc_format="auto",
    # 覆盖本地缓存（可选）
    company_name=None, logo_path=None,
    # 强制附加（可选；True/False/None）
    force_version_history=None, force_approval=None,
)
```

> 若公司信息缺失会抛 `RuntimeError`，异常 message 是结构化 JSON，Claude 捕获后可直接据此提示用户。

### 5.3 兼容旧位置参数

```bash
python3 scripts/create-word-doc.py <输出> [标题] [正文] [编号] [版本] [密级] [格式]
```

---

## 六、Markdown 能力速查

- **标题** — `#`~`######` / 规范专属中文编号（一、 / 1. / 1.1 / （一） / 第X章 …）
- **列表** — `- item` / `* item` / `1. item`
- **强调** — `**粗体**` / `*斜体*` / `` `inline code` ``
- **表格** — 标准 GFM；允许缺前导 `|`；`:---` / `---:` / `:---:` 对齐；`\|` 转义；2 列起即可识别
- **代码块** — 三个反引号包围，可带语言标签 ``` ```python ```
- **引用块** — `> ...`，连续多行视作同一引用
- **分隔线** — `---` / `***` / `___`（>=3）
- **元数据行** — `文档编号：XXX | 版本：V1.0 | 密级：内部 | 日期：2026-04-23` 自动变成两列表格
- **空内容** — 不会生成完全空白的文档，会放一行 `（无正文内容）`

---

## 七、触发词

- 写 word / 写文档 / 写个文档
- 生成 word / 生成文档 / 创建文档
- 导出 word / 导出文档
- 写合同 / 写方案 / 写报告 / 写会议纪要
- 写需求文档 / 写 SRS / 写 PRD
- 生成 PDF / Word 转 PDF

---

## 八、版本历史

- **v6.0.0（当前）**
  - Block AST Markdown 解析重写，修复偶发"正文为空"与两列表格丢失
  - 页眉恒含 LOGO + 公司名；页脚恒为 `第 X 页 / 共 Y 页`（PAGE / NUMPAGES 字段码）
  - 新增：代码块、引用块渲染；新增 `--with-version-history / --with-approval` 等四个强制开关
  - 规范化：版本历史 / 审批表仅在正式规范（公文/技术方案/需求文档）默认生成
- **v5.3.0**：`company-info.py` 本地公司信息读写工具 + 补录流程
- v5.2.x：GFM 表格解析、内联加粗/斜体、标题提取修复
- v5.0.0：多规范自动识别骨架

---

**技术支持：** 青岛火一五信息科技有限公司
