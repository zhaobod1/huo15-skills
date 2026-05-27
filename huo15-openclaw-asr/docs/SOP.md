# SOP — huo15-openclaw-asr（本地优先 · 媒体转写与龙虾研判）

| 项 | 内容 |
|----|------|
| **Skill** | `huo15-openclaw-asr` |
| **版本** | 与 `SKILL.md` frontmatter / `_meta.json` 一致 |
| **适用** | OpenClaw Agent、本机 CLI 辅助脚本 |
| **不适用** | 百炼/阿里云云端转写 → 见 [`huo15-openclaw-asr-bailian` SOP](../huo15-openclaw-asr-bailian/docs/SOP.md) |
| **规范源** | [SKILL.md](../SKILL.md)（冲突时以 SKILL 为准） |

---

## 1. 目的

将**音视频**或 **`.tty` 终端录屏**转为：

1. **原文**（逐字/可读转写或终端抽取文本）  
2. **纪要**（严格基于原文的结构化摘要）  
3. **`OPENCLAW_ASR_DELIVERY` 交付块**（供龙虾做类型与后续动作判断）  

可选：经用户同意后落盘 Markdown 或 Word（纪要 Word 走 `huo15-openclaw-office-doc`）。

**隐私原则**：默认**不上云**；用户明确要求云端/百炼时，**切换**至 `huo15-openclaw-asr-bailian`，不在本 skill 内调用百炼 API。

---

## 2. 何时使用本 SOP

| 用户意图 / 输入 | 使用本 SOP |
|-----------------|------------|
| 本地转写、不上云、Whisper / WhisperX | ✔ |
| `.tty` 终端录屏 / 会话日志 | ✔ |
| 百炼、阿里云、云端 ASR、Paraformer | ✘ → bailian SOP |
| 未说明本地还是云端 | 先询问；倾向云端 → bailian SOP |

---

## 3. 前置条件

| 类别 | 要求 |
|------|------|
| **OpenClaw** | 已加载 `huo15-openclaw-asr`（`clawhub install` 或仓库拷贝至 `workspace/skills/`） |
| **ffmpeg** | 在 `PATH` 中（音视频 → MP3） |
| **Whisper** | `pip install openai-whisper`（含 PyTorch；首次会下载 `base` 权重） |
| **Windows** | 同一会话内：`$env:PYTHONIOENCODING = "utf-8"` 再调 `whisper` |
| **WhisperX + 分轨** | `pip install whisperx`；`HF_TOKEN` 或 `--hf_token`；pyannote 门控模型需 HF 同意条款 |
| **Python 脚本** | `scripts/strip_ansi.py` 无第三方依赖；见 [scripts/README.md](../scripts/README.md) |

---

## 4. 标准操作流程（音视频 · Whisper）

```text
[0] 确认路线：本地（本 SOP） / 云端（转 bailian SOP）
[1] 输入分型：.tty → §5；否则继续
[2] ffmpeg 转 MP3（统一中间格式）
[3] whisper --model base（Windows 先设 PYTHONIOENCODING=utf-8）
[4] 转写质量自检（§6）— 未通过则不写定稿纪要
[5] 基于原文生成纪要（SKILL 纪要模板）
[6] 输出 OPENCLAW_ASR_DELIVERY 块
[7] 询问是否保存；若 Word → huo15-openclaw-office-doc
```

### 4.1 转 MP3

**Windows：**

```powershell
powershell -File scripts/transcode_mp3.ps1 -InputPath "path\to\input.mp4" -OutputPath "path\to\out.mp3"
```

**Unix：**

```bash
sh scripts/transcode_mp3.sh path/to/input.mp4 path/to/out.mp3
```

### 4.2 Whisper 转写（默认 base）

```powershell
$env:PYTHONIOENCODING = "utf-8"
whisper "path\to\out.mp3" --model base --language Chinese
```

### 4.3 WhisperX + 说话人分离（可选）

```bash
python scripts/transcribe_with_diarization.py path/to/out.mp3 --model base --language zh
```

原文中须标注说话人分段；完成后仍执行 §6 质量自检（针对可读性与分段合理性）。

---

## 5. 标准操作流程（`.tty`）

1. **探测**：文本 / script 标记 / ttyrec 二进制。  
2. **纯文本**：必要时 `python scripts/strip_ansi.py < file.tty > clean.txt`。  
3. **二进制 ttyrec**：`ttyplay` / `strings` 等；不完整须在 `notes_for_openclaw` 说明。  
4. **不做** Whisper 模型升级质检。  
5. 生成纪要 → 交付块 → 可选落盘（同 §4 步骤 6–7）。

---

## 6. 转写质量自检（Whisper 路径必做）

对照 SKILL 中质量指标表审查 **base** 产出（或最后一次重跑结果）：

- **问题偏多** → 建议 `small` → `medium` 重跑；**通过前不写定稿纪要**。  
- **问题偏少** → 进入纪要 + 交付块 + 可选落盘。

---

## 7. 交付标准

### 7.1 纪要

- 使用 SKILL「纪要模板」；**不得编造**原文未出现的信息。  

### 7.2 交付块（必填）

```yaml
asr_engine: local_whisper   # 或注明 whisperx / tty_extract
source_kind: audio_video | tty
verbatim_text: <全文或见: 路径>
summary_markdown: <纪要>
notes_for_openclaw: <不确定性、敏感提示等>
```

云端转写时**不要**用本 skill 填块，应走 bailian skill 的 `asr_engine: bailian_paraformer`。

### 7.3 落盘（须用户同意）

| 格式 | 文件名 | 内容 |
|------|--------|------|
| Markdown | `ASR_转写_YYYY-MM-DD_HHmmss.md` | 原文 + 纪要 + 交付块 |
| Word | `ASR_纪要_YYYY-MM-DD_HHmmss.docx` | 仅纪要；`huo15-openclaw-office-doc` |

保存目录：用户「下载」文件夹（Windows `%USERPROFILE%\Downloads`）。

---

## 8. 异常与处理

| 现象 | 处理 |
|------|------|
| `UnicodeEncodeError` / GBK | 设置 `PYTHONIOENCODING=utf-8` |
| Whisper OOM / 极慢 | 避免 `turbo`；试 `tiny` 试跑或换机器 |
| HF / pyannote 拉取失败 | 说明降级；见 SKILL WhisperX 节 |
| 用户要云端 | 停止本 SOP，转 [bailian SOP](../huo15-openclaw-asr-bailian/docs/SOP.md) |
| 要 Word 但 office-doc 未装 | 提示安装 skill 或仅输出 Markdown |

---

## 9. 发布与安装（维护人员）

```bash
# 开发仓库
git clone https://github.com/Grunray/huo15-skills
# 或 CNB: https://cnb.cool/huo15/ai/huo15-skills

clawhub install huo15-openclaw-asr --dir ~/.openclaw/workspace/skills
```

发版：`git push` → `clawhub publish <skill-dir> --slug huo15-openclaw-asr --version X.Y.Z`（见仓库根 README）。

---

## 10. 相关文档

| 文档 | 路径 |
|------|------|
| Skill 主规范 | [../SKILL.md](../SKILL.md) |
| 脚本说明 | [../scripts/README.md](../scripts/README.md) |
| 百炼云端 SOP | [../huo15-openclaw-asr-bailian/docs/SOP.md](../huo15-openclaw-asr-bailian/docs/SOP.md) |
| Word 纪要 | `huo15-openclaw-office-doc` |
