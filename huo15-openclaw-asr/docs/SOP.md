# 本地转写 · 怎么用（huo15-openclaw-asr）

> **一句话**：把录音/视频/终端录屏发给龙虾，说「本地转写」，拿原文 + 纪要。  
> **不上云**，不用百炼 Key。  
> 要用云端 → 看 [百炼版 SOP](../huo15-openclaw-asr-bailian/docs/SOP.md)

---

## 复制这句话就能用

```
用本地转写 skill，帮我把「你的文件完整路径」转成文字并写纪要，不要上云。
```

**例：**

```
用本地转写 skill，帮我把 D:\录音\周会.mp4 转成文字并写纪要，不要上云。
```

---

## 还能怎么说（按需加一句）

| 你想要 | 加在对话里 |
|--------|------------|
| 会议纪要有行动项 | 「按会议纪要格式写要点和行动项」 |
| 终端录屏 `.tty` | 「这是 .tty 文件，按 skill 提取终端内容」 |
| 多人要分谁说的 | 「需要分说话人，我已配好 HF_TOKEN」（见附录） |
| 要 Word | 「纪要生成 Word 存下载文件夹」 |
| 转写太差 | 「质量不好就按 skill 换更大模型重跑，别硬写纪要」 |
| 改云端 | 「改用百炼云端转写」→ 百炼 SOP |

---

## 你会拿到什么

- 对话里的 **原文** + **纪要**
- 若你同意保存：**下载** 文件夹里的 `.md`（全文）或 `.docx`（仅纪要）

---

## 第一次用？只配这些（可选）

| 要做什么 | 你要不要管 |
|----------|------------|
| 装 skill | 让管理员或自己执行一次 `clawhub install huo15-openclaw-asr`（见附录） |
| 装 ffmpeg | 转 **mp4 等视频** 时龙虾可能需要；没有就说「帮我检查 ffmpeg」 |
| API Key | **不用** |
| 百炼 Key | **不用** |

装好后 **重启 OpenClaw**，直接对话即可。

---

## 选错 skill？

| 情况 | 用哪个 |
|------|--------|
| 不想上云 | **本文（本地）** |
| 要用阿里云/百炼 | [百炼 SOP](../huo15-openclaw-asr-bailian/docs/SOP.md) |
| `.tty` 终端录屏 | **本文（本地）** |

---

## 附录（可跳过）

### A. 安装 skill

```bash
clawhub install huo15-openclaw-asr --dir ~/.openclaw/workspace/skills
```

路径按工作区调整；装完重启 OpenClaw。

### B. 说话人分离（可选）HF_TOKEN

1. [HuggingFace](https://huggingface.co/) 创建 Token  
2. 对 `pyannote/speaker-diarization-3.1` 网页点同意条款  
3. Windows 环境变量示例：

```powershell
[System.Environment]::SetEnvironmentVariable("HF_TOKEN", "你的token", "User")
```

4. 对话里说「需要分说话人转写」

### C. Windows 转写乱码

对话里说：「Windows 环境，转写编码报错请按 skill 处理 UTF-8。」

### D. 技术说明（龙虾/开发）

[SKILL.md](../SKILL.md) · [scripts/README.md](../scripts/README.md)
