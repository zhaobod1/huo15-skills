#!/usr/bin/env python3
"""
T2I 提示词增强脚本
输入一句话描述，输出增强后的专业提示词
"""

import sys
import json
import argparse

STYLE_PRESETS = {
    "写实摄影": {
        "tags": "photorealistic, shot on Canon EOS R5, 85mm lens, f/1.8 aperture, professional studio lighting",
        "quality": "masterpiece, best quality, extremely detailed, 8k resolution",
        "neg": "cartoon, anime, painting, drawing, illustration, low quality"
    },
    "胶片摄影": {
        "tags": "film grain, shot on Kodak Portra 400, 35mm lens, natural lighting, cinematic color grading",
        "quality": "masterpiece, best quality, cinematic photography",
        "neg": "digital, filter, overexposed, washed out colors"
    },
    "动漫": {
        "tags": "anime style, vibrant colors, detailed eyes, soft shading, studio Ghibli inspired, cel shading",
        "quality": "masterpiece, best quality, highly detailed, anime art style",
        "neg": "realistic, photographic, 3d render, low quality, worst quality"
    },
    "赛博朋克": {
        "tags": "cyberpunk, neon lights, rain-soaked streets, blade runner aesthetic, holographic ads, fog",
        "quality": "masterpiece, best quality, epic, detailed cyberpunk cityscape",
        "neg": "natural, countryside, low quality, medieval"
    },
    "水彩": {
        "tags": "watercolor painting, soft edges, delicate brushstrokes, paper texture visible, light wash layers",
        "quality": "masterpiece, best quality, beautiful watercolor art",
        "neg": "digital art, pixel art, sharp edges, heavy outlines"
    },
    "油画": {
        "tags": "oil painting, impressionist style, visible brushstrokes, rich texture, museum quality",
        "quality": "masterpiece, best quality, fine art, old master technique",
        "neg": "digital, cartoon, flat colors, low quality"
    },
    "建筑可视化": {
        "tags": "architectural visualization, clean lines, V-Ray render, professional lighting, interior design",
        "quality": "masterpiece, best quality, architectural photography, 4k",
        "neg": "sketch, doodle, low quality, distorted perspective"
    },
    "产品设计": {
        "tags": "product design render, white background, studio lighting, clean, minimal, commercial photography",
        "quality": "masterpiece, best quality, product photography, studio lighting",
        "neg": "cluttered background, amateur photo, low quality"
    },
    "像素艺术": {
        "tags": "pixel art, 16-bit style, vibrant colors, retro game aesthetic, sprite sheet",
        "quality": "masterpiece, best quality, pixel art, game asset",
        "neg": "photorealistic, blurry, anti-aliasing, 3d render"
    },
    "奇幻": {
        "tags": "fantasy art, epic composition, highly detailed, magical atmosphere, artstation trending, ethereal lighting",
        "quality": "masterpiece, best quality, fantasy illustration, intricate details",
        "neg": "modern, realistic, low quality, worst quality"
    },
    "科幻": {
        "tags": "sci-fi, holographic interface, futuristic technology, clean tech aesthetic, blue cyan color scheme",
        "quality": "masterpiece, best quality, sci-fi concept art, detailed",
        "neg": "medieval, fantasy, low quality, primitive technology"
    },
    "复古海报": {
        "tags": "vintage poster design, 1950s style, bold colors, letterpress print texture, retro typography",
        "quality": "masterpiece, best quality, vintage poster art",
        "neg": "modern design, digital, low quality"
    },
    "水墨": {
        "tags": "Chinese ink painting, sumi-e style, minimalist, zen atmosphere, brush and ink on rice paper",
        "quality": "masterpiece, best quality, traditional Chinese art",
        "neg": "colorful, western painting, digital art, cartoon"
    },
    "蒸汽朋克": {
        "tags": "steampunk, brass and copper tones, Victorian era, intricate gears, clockwork machinery, vintagefuturistic",
        "quality": "masterpiece, best quality, steampunk illustration, detailed",
        "neg": "modern, futuristic, low quality, sci-fi without steampunk elements"
    },
    "极简主义": {
        "tags": "minimalist, clean composition, abundant white space, simple, modern design, geometric shapes",
        "quality": "masterpiece, best quality, minimalist design, clean aesthetic",
        "neg": "cluttered, busy, ornate, detailed, complicated"
    },
    "电影感": {
        "tags": "cinematic, film still, anamorphic lens flare, volumetric lighting, cinematic color grading, dramatic shadows",
        "quality": "masterpiece, best quality, cinematic photography, movie still",
        "neg": "snapshot, amateur, low quality, flat lighting"
    },
    "国潮": {
        "tags": "Chinese national style, Chinese traditional elements, modern Chinese fashion, vermillion and gold, hanfu revival",
        "quality": "masterpiece, best quality, Chinese style illustration",
        "neg": "western style, medieval European, low quality"
    },
}


def extract_subject(text: str) -> str:
    """提取主体描述，清理输入"""
    text = text.strip().rstrip(".,，、")
    return text


def build_prompt(subject: str, preset: str, model: str = "通用") -> dict:
    """构建增强后的提示词"""
    preset = preset or "写实摄影"
    preset_data = STYLE_PRESETS.get(preset, STYLE_PRESETS["写实摄影"])

    # 主体处理
    subject_clean = extract_subject(subject)

    # 模型适配
    if model == "Midjourney":
        positive = f"{preset_data['tags']}, {subject_clean}, {preset_data['quality']}"
    elif model == "Stable Diffusion":
        positive = f"{subject_clean}, {preset_data['tags']}, {preset_data['quality']}"
    elif model == "DALL-E":
        positive = f"A {preset} style image showing {subject_clean}. High quality, professional composition."
    else:
        positive = f"{subject_clean}, {preset_data['tags']}, {preset_data['quality']}"

    result = {
        "original": subject,
        "preset": preset,
        "model": model,
        "positive": positive,
        "negative": preset_data["neg"],
    }

    return result


def print_prompt(result: dict):
    """格式化输出"""
    print(f"\n{'='*50}")
    print(f"📌 原始描述: {result['original']}")
    print(f"🎨 预设风格: {result['preset']}")
    print(f"🤖 适配模型: {result['model']}")
    print(f"\n✅ 增强提示词:")
    print(f"{result['positive']}")
    print(f"\n❌ 负面提示词:")
    print(f"{result['negative']}")
    print(f"{'='*50}\n")


def list_presets():
    """列出所有预设"""
    print("\n🎨 可用风格预设:")
    print("-" * 40)
    for i, name in enumerate(STYLE_PRESETS.keys(), 1):
        print(f"  {i:2d}. {name}")
    print()


def main():
    parser = argparse.ArgumentParser(description="T2I 提示词增强工具")
    parser.add_argument("subject", nargs="?", help="要生成图片的主体描述")
    parser.add_argument("-p", "--preset", help="风格预设名称")
    parser.add_argument("-m", "--model", default="通用", help="目标模型 (Midjourney/SD/DALL-E/通用)")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有预设")
    parser.add_argument("-j", "--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    if args.list:
        list_presets()
        return

    if not args.subject:
        print("用法: enhance_prompt.py <主体描述> [-p 预设风格] [-m 模型]")
        print("      enhance_prompt.py -l  # 列出所有预设")
        list_presets()
        sys.exit(1)

    result = build_prompt(args.subject, args.preset, args.model)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_prompt(result)


if __name__ == "__main__":
    main()
