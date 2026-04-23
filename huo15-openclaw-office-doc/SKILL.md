---
name: huo15-openclaw-office-doc
displayName: 火一五文档技能
description: 【青岛火一五信息科技有限公司】企业级 Word 文档生成。按内容自动选择文档规范（公文/合同/会议纪要/技术方案/需求文档/工作报告），页眉自动注入本地公司 LOGO 与名称；本地信息缺失时提示用户补录。触发词：写word、写文档、生成word、创建文档、写合同、写方案、写报告、写会议纪要、写需求文档、生成PDF、Word转PDF。
version: 5.3.0
aliases:
  - 火一五文档技能
  - 文档生成
  - Word生成
  - 多规范文档
dependencies:
  python-packages:
    - python-docx
---

# 火一五文档技能 v5.3

> 企业级 Word 文档生成 — 青岛火一五信息科技有限公司

**愿景：** 加速企业向全场景人工智能机器人转变
**理念：** 打破信息孤岛，用一套系统驱动企业增长

---

## 一、核心能力

1. **多规范自动识别** — 根据标题/正文关键词自动挑选最贴合的排版规范。
2. **本地公司信息注入** — 从本地缓存读取公司名、LOGO 等页眉信息；缺失时主动提示用户补录，补录后写入本地并同步到记忆备份。
3. **Markdown 兼容** — 标题、列表、粗体/斜体、GFM 表格、元数据行、分隔线全部兼容。
4. **可复现命令行** — 既支持新版 argparse 调用，也兼容旧位置参数。

---

## 二、文档规范选择

| 规范 | 触发关键词（标题或正文前 500 字） | 页眉风格 | 版本历史 | 审批区 | 典型场景 |
|------|----------------------------------|---------|---------|--------|---------|
| 公文 | 默认（未命中其他关键词） | LOGO + 公司名 + 文档编号 + 密级 | ✅ | ✅ | 正式函件、通知、请示 |
| 合同 | 合同 / 协议 / 协议书 | 公司名居中 | ❌ | ✅ | 商业合同、保密协议 |
| 会议纪要 | 会议纪要 / 纪要 | LOGO + 公司名 | ❌ | ❌ | 会议记录、工作纪要 |
| 技术方案 | 技术方案 / 实施方案 / 解决方案 / 设计文档 | LOGO + 公司名 | ✅ | ✅ | 项目方案、架构设计 |
| 需求文档 | 需求 / 需求规格 / 需求说明 / SRS | LOGO + 公司名 | ✅ | ✅ | SRS、PRD |
| 工作报告 | 工作报告 / 周报 / 月报 / 季报 / 年报 / 述职报告 | LOGO + 公司名 | ❌ | ✅ | 周报、月报、述职 |

> 用户也可以显式指定 `--doc-format <规范>` 覆盖自动识别。

### 标题层级识别

| 规范 | 一级 | 二级 | 三级 |
|------|------|------|------|
| 公文 | 第X章/第X节 | 一、二、三、 | （一）（二） |
| 合同 | 第X章/第X条 | 一、二、 | — |
| 会议纪要 | 【主题】 | 一、二、 | （一）（二） |
| 技术方案 | 一、1. | 1.1 | 1.1.1 |
| 需求文档 | 一、1. | 1.1 | — |
| 工作报告 | 一、 | （一） | — |

> 同时支持标准 Markdown `# / ## / ###`；`---` 作为水平分隔线（转空行）。

---

## 三、本地公司信息工作流（v5.3 新增）

页眉的公司名、LOGO 等信息不再硬编码，按以下优先级解析：

1. **CLI 显式参数** `--company-name` / `--logo-path`
2. **本地缓存** `~/.huo15/company-info.json`（主）
3. **Odoo `res.company`** 自动拉取（第三优先级，可用 `--no-odoo` 关闭）
4. **提示用户补录** — 以上都拿不到时，`create-word-doc.py` 退出码 2，stderr 输出结构化 JSON

### 3.1 Claude 生成文档前的标准流程

> Claude 在调用 `create-word-doc.py` 之前，先跑一遍本节，确保公司信息齐全。

```bash
# ① 检查本地公司信息
python3 scripts/company-info.py check
#   exit 0 + 完整 JSON  → 直接进入生成步骤
#   exit 2 + missing[]  → 进入补录流程
```

**补录流程**（Claude 执行）：

1. 先查 auto-memory 中的 `huo15_company_info.md` / `user_identity.md`，能拼出的字段直接拿来。
2. 仍然缺失时，用 `AskUserQuestion` 询问用户：
   - 公司全称（必填）
   - LOGO 文件路径（必填，默认 `~/.huo15/assets/logo.png`；可让用户粘贴本地路径或 URL）
   - 可选：slogan / 地址 / 电话 / 邮箱 / 官网
3. 写入本地 JSON：
   ```bash
   python3 scripts/company-info.py set \
     --company-name "<公司全称>" \
     --logo-path "<LOGO绝对路径>" \
     --slogan "<口号>"
   ```
4. 同步写入 memory（project 类型）便于跨会话复用：
   - 文件名：`huo15_company_info.md`
   - 正文写出字段与 JSON 路径，方便下次读取确认。

> **不要**把 LOGO 内容本身塞进 memory；memory 里只记"路径 + 关键字段"。

### 3.2 数据字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `company_name` | ✅ | 公司全称，用于页眉与元数据 |
| `logo_path` | ✅ | LOGO 绝对路径；文件需存在且 >1KB 才算有效 |
| `slogan` | — | 口号 / 页眉副标题 |
| `address` | — | 注册 / 办公地址 |
| `phone` | — | 联系电话 |
| `email` | — | 联系邮箱 |
| `website` | — | 官网 URL |

### 3.3 常用命令

```bash
# 查看当前信息 + 缺失字段
python3 scripts/company-info.py get

# 仅检查完整性（SKILL 工作流用；退出码 2 表示需要补录）
python3 scripts/company-info.py check

# 设置/更新字段（支持部分字段）
python3 scripts/company-info.py set --company-name "XX科技" --slogan "YY"

# 清空某些字段
python3 scripts/company-info.py set --clear phone email
```

---

## 四、文档生成调用

### 4.1 推荐调用（argparse）

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
#   --doc-format 技术方案         # 覆盖自动识别
#   --company-name "XX科技"       # 覆盖本地缓存
#   --logo-path /path/to/logo.png
#   --no-odoo                    # 不从 Odoo 回落
```

> `--content` 以 `@` 开头时读取对应路径的文件；否则按字面字符串处理。

### 4.2 Python API

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
    doc_format="auto",   # auto/公文/合同/会议纪要/技术方案/需求文档/工作报告
    # 覆盖本地缓存（可选）
    company_name=None, logo_path=None,
)
```

> 若公司信息缺失会抛 `RuntimeError`，异常 message 是结构化 JSON，Claude 捕获后可直接据此提示用户。

### 4.3 兼容旧位置参数

```bash
python3 scripts/create-word-doc.py <输出> [标题] [正文] [编号] [版本] [密级] [格式]
```

---

## 五、触发词

- 写 word / 写文档 / 写个文档
- 生成 word / 生成文档 / 创建文档
- 导出 word / 导出文档
- 写合同 / 写方案 / 写报告 / 写会议纪要
- 写需求文档 / 写 SRS
- 生成 PDF / Word 转 PDF

---

## 六、Markdown 能力速查

- 标题：`#` `##` `###` … 或中文编号（一、 / 1. / 1.1 / （一） …）
- 列表：`- 项` / `* 项`
- 强调：`**粗体**` / `*斜体*`
- 表格：标准 GFM；允许省略首尾 `|`；支持对齐标记 `:---` / `:---:` / `---:`；支持转义 `\|`；列数不一致会自动补齐
- 分隔线：`---`
- 元数据行：`文档编号：XXX | 版本：V1.0 | 密级：内部 | 日期：2026-04-22` 会自动渲染为两列表格

---

## 七、版本历史

- **v5.3.0（当前）**：
  - 新增：`scripts/company-info.py` — 本地公司信息读写工具（`get/set/check` 三子命令）
  - 新增：公司信息优先级 CLI > 本地 JSON > Odoo > 提示用户，缺字段时以退出码 2 + JSON 报错，便于 Claude 触发补录问答
  - 新增：Claude 补录流程写入 `~/.huo15/company-info.json` 与 auto-memory 双保险
  - 重构：`create-word-doc.py` 改用 argparse；旧位置参数兼容保留
  - 移除：`create-word-doc.py` 内嵌的 Odoo XML-RPC / LOGO 下载逻辑（迁入 `company-info.py`）
- **v5.2.4**：内联 Markdown 加粗/斜体 + 列表 + 标题提取修复
- **v5.2.3**：支持标准 Markdown 标题 `#` / 水平分隔线 `---`
- **v5.2.2**：页眉公司信息 & 元数据行自动转两列表格
- **v5.2.1**：会议纪要格式完善（chapter 保留 `【主题】`，section/article 正确 strip 前缀）
- **v5.2.0**：表格解析关键修复（省略前导 `|` / 列数不一致补齐）
- **v5.0.0**：多规范自动识别（公文/合同/会议纪要/技术方案/需求文档/工作报告）

---

**技术支持：** 青岛火一五信息科技有限公司
