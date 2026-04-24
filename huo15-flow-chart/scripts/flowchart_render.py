"""把 Mermaid / PlantUML / DOT 代码渲染成 SVG / PNG / PDF。

后端探测顺序（每种 DSL 各自的）：
- Mermaid：`mmdc`（npm @mermaid-js/mermaid-cli） → npx → docker ghcr.io/mermaid-js/mermaid-cli
- PlantUML：`plantuml` → java -jar plantuml.jar → docker plantuml/plantuml
- Graphviz：`dot`

如果所有后端都不可用，会把源码写到 `.mmd/.puml/.dot` 文件里并抛出 RuntimeError，
让用户自己渲染（比如复制到 https://mermaid.live）。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional


SUPPORTED_EXTS = {".svg", ".png", ".pdf", ".mmd", ".puml", ".dot", ".drawio", ".md", ".markdown"}


def render(source: str, output_path: str, engine: str = "mermaid",
           width: Optional[int] = None, height: Optional[int] = None,
           background: Optional[str] = None,
           pdf_fit: bool = True) -> str:
    """核心渲染函数。返回最终产物路径。

    pdf_fit
        输出 .pdf 时是否自动适配画布（不分页、整图一体）。默认 True。
    """
    out = Path(output_path)
    ext = out.suffix.lower()
    if ext not in SUPPORTED_EXTS:
        raise ValueError(f"不支持的扩展名 {ext}；可选 {sorted(SUPPORTED_EXTS)}")

    out.parent.mkdir(parents=True, exist_ok=True)

    # 仅导出源码
    if ext in (".mmd", ".md", ".markdown"):
        out.write_text(source, encoding="utf-8")
        return str(out)
    if ext == ".puml":
        out.write_text(source, encoding="utf-8")
        return str(out)
    if ext == ".dot":
        out.write_text(source, encoding="utf-8")
        return str(out)
    if ext == ".drawio":
        out.write_text(source, encoding="utf-8")
        return str(out)

    if engine == "mermaid":
        return _render_mermaid(source, out, width=width, height=height,
                               background=background, pdf_fit=pdf_fit)
    if engine == "plantuml":
        return _render_plantuml(source, out, pdf_fit=pdf_fit)
    if engine == "dot":
        return _render_dot(source, out)
    raise ValueError(f"未知 engine：{engine}")


# ----- Mermaid -----


def _find_mmdc() -> Optional[list]:
    if shutil.which("mmdc"):
        return ["mmdc"]
    if shutil.which("npx"):
        return ["npx", "-y", "@mermaid-js/mermaid-cli"]
    if shutil.which("docker"):
        return [
            "docker", "run", "--rm", "-u", f"{os.getuid()}:{os.getgid()}",
            "-v", f"{os.getcwd()}:/data",
            "minlag/mermaid-cli", "-"
        ]
    return None


def _render_mermaid(source: str, out: Path, *, width=None, height=None,
                    background=None, pdf_fit: bool = True) -> str:
    cmd_base = _find_mmdc()
    if not cmd_base:
        # 没有 mmdc，把 .mmd 导出
        fallback = out.with_suffix(".mmd")
        fallback.write_text(source, encoding="utf-8")
        raise RuntimeError(
            f"未找到 mmdc / npx / docker，已把 Mermaid 源码保存到 {fallback}。"
            "\n安装任选其一："
            "\n  npm i -g @mermaid-js/mermaid-cli      # 推荐"
            "\n  或用在线编辑器：https://mermaid.live"
        )

    ext = out.suffix.lower()
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "source.mmd"
        src.write_text(source, encoding="utf-8")
        cmd = list(cmd_base) + ["-i", str(src), "-o", str(out)]
        if width:
            cmd += ["-w", str(width)]
        if height:
            cmd += ["-H", str(height)]
        if background:
            cmd += ["-b", background]
        # PDF 导出：让 PDF 自动适配图表大小（单页不分页）
        if ext == ".pdf" and pdf_fit:
            cmd += ["-f"]
        # 设置 puppeteer 的 no-sandbox 配置（常见 Linux CI 报错）
        pup_cfg = Path(td) / "puppeteer.json"
        pup_cfg.write_text(json.dumps({"args": ["--no-sandbox", "--disable-setuid-sandbox"]}))
        cmd += ["-p", str(pup_cfg)]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"mmdc 渲染失败：\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"
            ) from e
    return str(out)


# ----- PlantUML -----


def _find_plantuml() -> Optional[list]:
    if shutil.which("plantuml"):
        return ["plantuml"]
    # 常见 jar 路径
    for candidate in [
        "/opt/homebrew/opt/plantuml/libexec/plantuml.jar",
        "/usr/local/opt/plantuml/libexec/plantuml.jar",
        "/usr/share/plantuml/plantuml.jar",
    ]:
        if os.path.isfile(candidate) and shutil.which("java"):
            return ["java", "-jar", candidate]
    if shutil.which("docker"):
        return ["docker", "run", "--rm", "-i", "plantuml/plantuml", "-pipe"]
    return None


def _render_plantuml(source: str, out: Path, pdf_fit: bool = True) -> str:
    cmd = _find_plantuml()
    if not cmd:
        fallback = out.with_suffix(".puml")
        fallback.write_text(source, encoding="utf-8")
        raise RuntimeError(
            f"未找到 plantuml / java / docker，已把 PlantUML 源码保存到 {fallback}。"
            "\n安装："
            "\n  brew install plantuml     (macOS)"
            "\n  apt install plantuml      (Ubuntu/Debian)"
        )

    ext = out.suffix.lower()
    # PDF 走 SVG → rsvg-convert 流程，保证单页一体输出
    if ext == ".pdf" and pdf_fit and shutil.which("rsvg-convert"):
        return _render_plantuml_pdf_via_svg(source, out, cmd)

    fmt = {".svg": "-tsvg", ".png": "-tpng", ".pdf": "-tpdf"}[ext]
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "source.puml"
        src.write_text(source, encoding="utf-8")
        full_cmd = list(cmd) + [fmt, "-o", str(out.parent.absolute()), str(src)]
        try:
            subprocess.run(full_cmd, check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # 保底：把源码落盘，调用方可以复制到在线编辑器
            fallback = out.with_suffix(".puml")
            fallback.write_text(source, encoding="utf-8")
            stdout = getattr(e, "stdout", "") or ""
            stderr = getattr(e, "stderr", "") or ""
            raise RuntimeError(
                f"plantuml 渲染失败（可能是 docker 镜像未拉 / daemon 未启动）。"
                f"已把 PlantUML 源码落到 {fallback}。"
                f"\nSTDOUT: {stdout}\nSTDERR: {stderr}"
            ) from e
    # plantuml 会输出 source.{fmt}，我们移到指定 out
    produced = Path(out.parent) / src.name.replace(".puml", ext)
    if produced.exists() and produced != out:
        produced.rename(out)
    return str(out)


def _render_plantuml_pdf_via_svg(source: str, out: Path, plantuml_cmd: list) -> str:
    """先用 PlantUML 出 SVG，再用 rsvg-convert 转成单页 PDF（整图一体、不分页）。"""
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "source.puml"
        src.write_text(source, encoding="utf-8")
        # 生成 SVG
        svg_cmd = list(plantuml_cmd) + ["-tsvg", "-o", str(td), str(src)]
        try:
            subprocess.run(svg_cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"plantuml 生成 SVG 失败：\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"
            ) from e
        svg_path = Path(td) / "source.svg"
        if not svg_path.exists():
            raise RuntimeError("plantuml 没有输出预期 SVG")
        # SVG → PDF（rsvg-convert 以 SVG viewBox 为唯一页面尺寸，一定是单页）
        try:
            subprocess.run(
                ["rsvg-convert", "-f", "pdf", "-o", str(out), str(svg_path)],
                check=True, capture_output=True, text=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"rsvg-convert 将 SVG 转 PDF 失败：\nSTDERR: {e.stderr}"
            ) from e
    return str(out)


# ----- Graphviz -----


def _render_dot(source: str, out: Path) -> str:
    if not shutil.which("dot"):
        fallback = out.with_suffix(".dot")
        fallback.write_text(source, encoding="utf-8")
        raise RuntimeError(
            f"未找到 dot (Graphviz)，已把 DOT 源码保存到 {fallback}。"
            "\n安装： brew install graphviz"
        )
    ext = out.suffix.lower()
    fmt = {".svg": "svg", ".png": "png", ".pdf": "pdf"}[ext]
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "source.dot"
        src.write_text(source, encoding="utf-8")
        cmd = ["dot", f"-T{fmt}", str(src), "-o", str(out)]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"dot 渲染失败：\nSTDERR: {e.stderr}"
            ) from e
    return str(out)
