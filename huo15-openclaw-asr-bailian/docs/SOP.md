# 百炼云端转写 · 怎么用（huo15-openclaw-asr-bailian）

> **一句话**：把录音/视频路径发给龙虾，说「百炼云端转写 + 同意上云」，拿原文 + 纪要。  
> **音频会经公网提交阿里云**，需先配百炼 Key。  
> 不想上云 → 看 [本地版 SOP](../huo15-openclaw-asr/docs/SOP.md)

---

## 复制这句话就能用

```
用百炼云端转写 skill，帮我把「你的文件完整路径」转成文字并写纪要。我同意上云。
```

**例：**

```
用百炼云端转写 skill，帮我把 D:\会议\客户沟通.mp4 转成文字并写纪要。我同意上云。
```

---

## 还能怎么说（按需加一句）

| 你想要 | 加在对话里 |
|--------|------------|
| 现场吵 / 方言多 | 「可以试试 fun-asr 模型」 |
| 分说话人 | 「需要说话人分离」 |
| 已有网上音频链接 | 「音频 URL 是 https://...，直接转写」 |
| 要 Word | 「纪要生成 Word 存下载文件夹」 |
| 改本地不上云 | 「改本地转写，不要上云」→ 本地 SOP |
| `.tty` 录屏 | **不支持**，改 [本地 SOP](../huo15-openclaw-asr/docs/SOP.md) |

---

## 你会拿到什么

- 对话里的 **原文** + **纪要**
- 若你同意保存：**下载** 文件夹里的 `.md` 或 `.docx`（仅纪要）

龙虾会自动用 **`enhance_share_file`** 生成分享链接（`keepermac.huo15.com`），**你不用自己拼 URL**。

---

## 第一次用？必做 1 件事

**配百炼 API Key（只做一次）**

| 项 | 说明 |
|----|------|
| 变量名 | `DASHSCOPE_API_KEY` |
| 去哪拿 | [阿里云百炼](https://help.aliyun.com/zh/model-studio/) → API Key |
| 怎么配 | 写在本机**环境变量**，**不要**发在聊天里 |

**Windows 示例（配完重启 OpenClaw）：**

```powershell
[System.Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "sk-你的Key", "User")
```

另：OpenClaw 里 **enhance 分享插件** 要能用（一般已装好）。  
装 skill：`clawhub install huo15-openclaw-asr-bailian`（见附录）。

---

## 选错 skill？

| 情况 | 用哪个 |
|------|--------|
| 百炼 / 阿里云 / 云端 | **本文** |
| 不想上云、涉密 | [本地 SOP](../huo15-openclaw-asr/docs/SOP.md) |
| `.tty` | [本地 SOP](../huo15-openclaw-asr/docs/SOP.md) |

---

## 附录（可跳过）

### A. 安装 skill

```bash
clawhub install huo15-openclaw-asr-bailian --dir ~/.openclaw/workspace/skills
```

ClawHub：https://clawhub.ai/skills/huo15-openclaw-asr-bailian

### B. 上云是什么意思

1. 龙虾用 `enhance_share_file` 生成 `https://keepermac.huo15.com/plugins/enhance-share/...`  
2. 百炼从该链接拉音频转写  

涉密录音请先确认合规。

### C. 支持哪些文件

**mp3 / mp4 / mkv / mov / wav / m4a** 等一般可直接转，不必先转 MP3。约 ≤ 2GB、≤ 12h。

### D. 命令行（自己跑脚本时）

```bash
pip install dashscope
python scripts/transcribe_bailian.py --file-url "https://keepermac.huo15.com/plugins/enhance-share/..." -o out.txt
```

日常对话使用 **不必**自己敲。见 [scripts/README.md](../scripts/README.md)。

### E. 技术说明（龙虾/开发）

[SKILL.md](../SKILL.md)
