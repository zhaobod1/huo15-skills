#!/usr/bin/env python3
"""
huo15-img-test — T2I 提示词增强脚本 v2.0

核心升级：
1. 45 风格预设（摄影 / 插画 / 3D / 设计 / 艺术 / 场景 六大类）
2. 意图解析（自动识别主体类型、画幅、构图、情绪）
3. 一致性锁（camera / lighting / palette / aspect 逐项锁定，提升系列一致性）
4. 系列批量模式（-s N：多张图共享相同锁，避免风格漂移）
5. 多模型精细化适配（Midjourney / Stable Diffusion / SDXL / Flux / DALL-E 3）
6. 别名 & 中英混输入（anime / cyberpunk / 赛博朋克 均可）
"""

import sys
import json
import re
import argparse
import hashlib
from typing import Dict, List, Optional, Tuple

VERSION = "2.0.0"

# ─────────────────────────────────────────────────────────
# 通用质量 / 负面词
# ─────────────────────────────────────────────────────────
UNIVERSAL_QUALITY = "masterpiece, best quality, ultra detailed, 8k"
UNIVERSAL_NEG = (
    "low quality, worst quality, lowres, blurry, jpeg artifacts, "
    "watermark, signature, text, logo, username, "
    "bad anatomy, bad hands, extra fingers, missing fingers, "
    "extra limbs, deformed, mutated, disfigured, ugly, "
    "out of frame, cropped, duplicate"
)

# 这些预设天然需要 logo / text / signature，把它们从全局负面词中剔除，避免语义冲突
PRESET_NEG_EXCLUDE: Dict[str, List[str]] = {
    "Logo设计": ["logo", "text"],
    "图标设计": ["logo", "text"],
    "表情包": ["text"],
    "复古海报": ["text"],
    "电影海报": ["text"],
    "专辑封面": ["text"],
    "品牌KV": ["text"],
    "信息图": ["text"],
    "水墨": ["signature"],
    "工笔国画": ["signature"],
    "浮世绘": ["text", "signature"],
    "霓虹灯牌": ["text"],
}


def _filter_neg(universal: str, exclude: List[str]) -> str:
    if not exclude:
        return universal
    tokens = [t.strip() for t in universal.split(",")]
    kept = [t for t in tokens if t.lower() not in {e.lower() for e in exclude}]
    return ", ".join(kept)

# ─────────────────────────────────────────────────────────
# 风格预设 — 每个预设 7 个字段
#   tags     风格标签
#   quality  画质标签
#   neg      负面标签（与 UNIVERSAL_NEG 合并）
#   camera   机位 / 镜头（摄影专用，其它留空）
#   lighting 光影锁
#   palette  色板锁（系列一致性关键）
#   aspect   默认画幅
# ─────────────────────────────────────────────────────────

STYLE_PRESETS: Dict[str, Dict[str, str]] = {
    # ========== 摄影 Photography ==========
    "写实摄影": {
        "category": "摄影",
        "tags": "photorealistic, hyperrealistic, dslr photography, sharp focus",
        "quality": "raw photo, detailed skin texture, film grain subtle",
        "neg": "cartoon, anime, painting, drawing, illustration, cgi",
        "camera": "Canon EOS R5, 85mm f/1.4 lens, shallow depth of field",
        "lighting": "professional studio lighting, softbox key light, rim light",
        "palette": "natural color grading, balanced exposure",
        "aspect": "3:4",
    },
    "胶片摄影": {
        "category": "摄影",
        "tags": "analog film photography, film grain, analog aesthetic",
        "quality": "kodak portra 400 film stock, scanned film",
        "neg": "digital, oversaturated, hdr, plastic skin",
        "camera": "35mm film camera, 50mm prime, shot on film",
        "lighting": "natural window light, golden hour",
        "palette": "muted earth tones, slightly faded film colors",
        "aspect": "3:2",
    },
    "黑白摄影": {
        "category": "摄影",
        "tags": "black and white photography, monochrome, high contrast",
        "quality": "silver gelatin print, fine art photography, rich grayscale",
        "neg": "color, colorful, saturated, low contrast",
        "camera": "Leica M6, 35mm f/2, classic reportage framing",
        "lighting": "dramatic chiaroscuro, strong directional light",
        "palette": "pure black and white, deep blacks, crisp whites",
        "aspect": "1:1",
    },
    "人像摄影": {
        "category": "摄影",
        "tags": "portrait photography, shallow depth of field, bokeh background",
        "quality": "flawless skin retouch, detailed eyes, catch light",
        "neg": "full body, wide shot, plastic skin, uncanny",
        "camera": "85mm f/1.4, eye-level portrait, rule of thirds",
        "lighting": "rembrandt lighting, soft key with fill",
        "palette": "warm skin tones, complementary backdrop",
        "aspect": "3:4",
    },
    "时尚大片": {
        "category": "摄影",
        "tags": "high fashion editorial, vogue style, avant-garde styling",
        "quality": "magazine cover quality, haute couture",
        "neg": "amateur, casual, snapshot, cluttered set",
        "camera": "medium format, 50mm, full body or waist-up",
        "lighting": "hard strobe with deep shadows, beauty dish",
        "palette": "high-contrast, bold monochromatic set",
        "aspect": "3:4",
    },
    "美食摄影": {
        "category": "摄影",
        "tags": "food photography, overhead flatlay, appetizing presentation",
        "quality": "detailed steam and texture, drool-worthy, michelin plating",
        "neg": "greasy, unappealing, blurry plate, messy",
        "camera": "macro 100mm, 45-degree angle or top-down",
        "lighting": "soft window light from side, subtle rim highlight",
        "palette": "warm appetite-triggering tones, natural food colors",
        "aspect": "1:1",
    },
    "产品摄影": {
        "category": "摄影",
        "tags": "commercial product photography, clean composition, minimal scene",
        "quality": "crisp reflections, seamless background, advertising grade",
        "neg": "cluttered, messy background, amateur lighting",
        "camera": "90mm macro, eye-level product shot",
        "lighting": "large softbox key, gradient sweep background",
        "palette": "neutral white or brand-matched seamless",
        "aspect": "1:1",
    },
    "微距摄影": {
        "category": "摄影",
        "tags": "macro photography, extreme close-up, micro world",
        "quality": "razor sharp details at micro scale, focus stacking",
        "neg": "soft focus, wide view, lack of detail",
        "camera": "100mm macro lens, 1:1 magnification",
        "lighting": "ring flash or twin macro flash, even diffused",
        "palette": "nature-true colors, intense saturation",
        "aspect": "1:1",
    },
    "航拍摄影": {
        "category": "摄影",
        "tags": "aerial photography, drone shot, bird's eye view",
        "quality": "ultra wide sweeping vista, high altitude clarity",
        "neg": "ground level, close-up, people center frame",
        "camera": "drone camera, 24mm equivalent, top-down or 45-degree",
        "lighting": "natural sunlight, long soft shadows",
        "palette": "earth tones with atmospheric blue haze",
        "aspect": "16:9",
    },
    "街拍纪实": {
        "category": "摄影",
        "tags": "street photography, decisive moment, candid documentary",
        "quality": "authentic raw feeling, unposed human story",
        "neg": "staged, fake, overprocessed",
        "camera": "35mm prime, hip-level snap, off-center subject",
        "lighting": "available ambient light, urban neon or sunlight",
        "palette": "slightly desaturated urban tones",
        "aspect": "3:2",
    },

    # ========== 动漫 / 插画 Illustration ==========
    "动漫": {
        "category": "动漫",
        "tags": "anime style, cel shading, clean line art, vibrant anime colors",
        "quality": "detailed anime eyes, pixiv trending, high quality anime",
        "neg": "photorealistic, 3d render, western cartoon, low quality",
        "camera": "",
        "lighting": "anime-style soft light, rim light on hair",
        "palette": "vibrant saturated anime palette",
        "aspect": "3:4",
    },
    "新海诚": {
        "category": "动漫",
        "tags": "Makoto Shinkai style, volumetric cloudscape, realistic anime backgrounds",
        "quality": "your name aesthetic, weathering with you mood, incredibly detailed skyscape",
        "neg": "flat background, dark mood, gritty",
        "camera": "",
        "lighting": "magic hour sunlight streaming, god rays through clouds",
        "palette": "sky blue, warm orange sunset, pink hour",
        "aspect": "16:9",
    },
    "宫崎骏": {
        "category": "动漫",
        "tags": "Studio Ghibli style, hand-painted background, whimsical warmth",
        "quality": "Totoro aesthetic, Spirited Away mood, hayao miyazaki inspired",
        "neg": "dark, edgy, hyperdetailed, cgi",
        "camera": "",
        "lighting": "soft daylight through leaves, gentle diffuse",
        "palette": "pastoral greens, cream, sky blue",
        "aspect": "16:9",
    },
    "美漫": {
        "category": "动漫",
        "tags": "American comic book style, bold ink lines, halftone shading",
        "quality": "marvel / DC inspired, dynamic pose, action panel",
        "neg": "anime, soft shading, watercolor",
        "camera": "",
        "lighting": "dramatic cel lighting, high contrast shadows",
        "palette": "saturated primary colors, comic book palette",
        "aspect": "2:3",
    },
    "Q版": {
        "category": "动漫",
        "tags": "chibi style, super-deformed, cute mascot, 3-head-tall proportions",
        "quality": "adorable, clean vector look, sticker worthy",
        "neg": "realistic proportion, detailed anatomy, dark mood",
        "camera": "",
        "lighting": "even flat light, gentle cel shading",
        "palette": "bright pastel palette, sugary",
        "aspect": "1:1",
    },
    "童话绘本": {
        "category": "动漫",
        "tags": "children's book illustration, storybook style, hand drawn warmth",
        "quality": "gouache texture, paper warmth, beatrix potter meets pixar",
        "neg": "dark, horror, hyper-realistic, edgy",
        "camera": "",
        "lighting": "soft overall illumination, enchanted glow",
        "palette": "warm buttery pastels, cream page base",
        "aspect": "4:3",
    },
    "水彩": {
        "category": "插画",
        "tags": "watercolor painting, wet-on-wet technique, paper texture, soft bleeding edges",
        "quality": "traditional watercolor, transparent wash layers, artistic",
        "neg": "digital vector, hard edges, heavy outlines, 3d",
        "camera": "",
        "lighting": "natural daylight on paper",
        "palette": "translucent pastel layers, white paper showing through",
        "aspect": "1:1",
    },
    "油画": {
        "category": "插画",
        "tags": "oil painting, thick impasto brushstrokes, canvas texture",
        "quality": "museum quality oil on canvas, old master technique",
        "neg": "digital, flat colors, vector, pixel art",
        "camera": "",
        "lighting": "chiaroscuro, warm rembrandt glow",
        "palette": "rich earth tones, deep jewel colors",
        "aspect": "4:5",
    },
    "水墨": {
        "category": "插画",
        "tags": "Chinese ink wash painting, sumi-e, negative space, calligraphic strokes",
        "quality": "zen atmosphere, rice paper texture, ink bleed",
        "neg": "colorful, dense composition, western painting, cartoon",
        "camera": "",
        "lighting": "flat paper light, no harsh shadows",
        "palette": "sumi black on rice-paper beige, occasional vermillion seal",
        "aspect": "3:4",
    },
    "工笔国画": {
        "category": "插画",
        "tags": "Chinese gongbi painting, meticulous fine brush, intricate floral detail",
        "quality": "Song dynasty court painting style, mineral pigment",
        "neg": "loose brushstrokes, abstract, western style",
        "camera": "",
        "lighting": "flat even pigment, no modeling light",
        "palette": "azurite blue, malachite green, cinnabar red, gold leaf",
        "aspect": "3:4",
    },
    "浮世绘": {
        "category": "插画",
        "tags": "Ukiyo-e woodblock print, Edo period, Hokusai / Hiroshige style",
        "quality": "traditional Japanese woodcut, flat color blocks, outlined figures",
        "neg": "modern anime, 3d, photorealistic",
        "camera": "",
        "lighting": "no modeling light, flat graphic",
        "palette": "prussian blue, earth reds, muted greens",
        "aspect": "2:3",
    },
    "线稿": {
        "category": "插画",
        "tags": "clean line art, black ink on white, single weight or dynamic line",
        "quality": "architectural line drawing precision, tattoo flash clarity",
        "neg": "color, shading, painterly, texture",
        "camera": "",
        "lighting": "no lighting, pure linework",
        "palette": "pure black on white",
        "aspect": "1:1",
    },
    "像素艺术": {
        "category": "插画",
        "tags": "pixel art, 16-bit sprite, pixelated, retro game aesthetic",
        "quality": "clean pixel clusters, limited palette, dithering",
        "neg": "anti-aliased, smooth, photorealistic, 3d render, high resolution",
        "camera": "",
        "lighting": "flat pixel shading or 2-tone",
        "palette": "NES / SNES limited palette, 16 colors",
        "aspect": "1:1",
    },

    # ========== 3D / 手工 3D & Craft ==========
    "3DC4D": {
        "category": "3D",
        "tags": "3d render, octane render, c4d style, subsurface scattering, glossy materials",
        "quality": "ray traced reflections, detailed shader, behance trending",
        "neg": "2d flat, sketch, line art",
        "camera": "3d viewport camera, 50mm equivalent",
        "lighting": "hdri environment light, colored accent rims",
        "palette": "vibrant candy colors, pastel gradients",
        "aspect": "1:1",
    },
    "盲盒手办": {
        "category": "3D",
        "tags": "blind box figurine, pop mart style, chibi 3d toy, kawaii collectible",
        "quality": "vinyl toy finish, pristine product shot, pop mart aesthetic",
        "neg": "realistic human, gritty, damaged",
        "camera": "50mm product shot, eye level toy perspective",
        "lighting": "soft studio light, gentle rim, clean shadow",
        "palette": "pastel macaron palette",
        "aspect": "1:1",
    },
    "低多边形": {
        "category": "3D",
        "tags": "low poly 3d, faceted geometry, minimalist polygons",
        "quality": "crisp flat shaded polygons, geometric stylization",
        "neg": "high detail, smooth subdivisions, realistic",
        "camera": "3/4 perspective, isometric-ish",
        "lighting": "flat faceted shading, 2-3 light setup",
        "palette": "limited flat palette, often pastel",
        "aspect": "1:1",
    },
    "等距视图": {
        "category": "3D",
        "tags": "isometric illustration, 2.5d isometric scene, game-dev isometric tile",
        "quality": "clean vector isometric look, detailed miniature diorama",
        "neg": "perspective distortion, top-down, first-person",
        "camera": "true isometric projection, 30-degree angles",
        "lighting": "even diffuse light, directional accent",
        "palette": "bright clean pastel palette",
        "aspect": "1:1",
    },
    "粘土": {
        "category": "3D",
        "tags": "claymation style, stop motion clay, aardman-like tactile figures",
        "quality": "handmade clay texture, fingerprint detail",
        "neg": "clean digital, plastic, smooth 3d",
        "camera": "stop motion rig perspective, slight depth of field",
        "lighting": "warm tungsten key with practical fill",
        "palette": "warm terracotta tones",
        "aspect": "1:1",
    },
    "毛毡手工": {
        "category": "3D",
        "tags": "felted wool craft, needle felt texture, handmade plush character",
        "quality": "fuzzy fiber detail, cute handmade imperfection",
        "neg": "smooth digital render, photorealistic animal",
        "camera": "close macro product shot",
        "lighting": "soft diffuse daylight",
        "palette": "muted natural wool colors",
        "aspect": "1:1",
    },
    "纸艺": {
        "category": "3D",
        "tags": "paper craft, layered paper art, quilling, origami composition",
        "quality": "intricate cut paper layers, shadow depth between layers",
        "neg": "flat 2d, digital illustration",
        "camera": "front-on with slight tilt, shallow depth",
        "lighting": "rim light casting paper-edge shadows",
        "palette": "pastel construction paper colors",
        "aspect": "1:1",
    },

    # ========== 设计 Design ==========
    "极简主义": {
        "category": "设计",
        "tags": "minimalist design, negative space, swiss style, geometric composition",
        "quality": "clean typography-friendly, editorial layout",
        "neg": "cluttered, ornate, busy, excess detail",
        "camera": "",
        "lighting": "flat studio light or ambient, no drama",
        "palette": "monochrome + single accent, lots of white",
        "aspect": "1:1",
    },
    "平面设计": {
        "category": "设计",
        "tags": "flat design, vector graphic, bold shapes, brand illustration",
        "quality": "clean vectors, designer grade composition",
        "neg": "photorealistic, gradient 3d, sketchy",
        "camera": "",
        "lighting": "flat shading, no highlights",
        "palette": "brand-forward 3-color palette",
        "aspect": "1:1",
    },
    "Logo设计": {
        "category": "设计",
        "tags": "logo design, brand mark, vector logotype, scalable emblem",
        "quality": "professional logo, centered composition on clean background",
        "neg": "photorealistic scene, complex background, cluttered",
        "camera": "",
        "lighting": "flat vector, no light gradient",
        "palette": "2-color max, high contrast",
        "aspect": "1:1",
    },
    "图标设计": {
        "category": "设计",
        "tags": "icon design, app icon, rounded square, centered glyph",
        "quality": "apple hig compliant, clean icon grid, crisp at 1024px",
        "neg": "cluttered, off-center, photo, low contrast",
        "camera": "",
        "lighting": "subtle highlight gradient, soft inner glow",
        "palette": "vibrant gradient with 2-3 colors",
        "aspect": "1:1",
    },
    "信息图": {
        "category": "设计",
        "tags": "infographic design, data visualization, icon system, explanatory layout",
        "quality": "clean editorial infographic, behance level",
        "neg": "messy, illustrative painting, photograph",
        "camera": "",
        "lighting": "flat, no drama",
        "palette": "brand palette + grayscale structure",
        "aspect": "3:4",
    },
    "品牌KV": {
        "category": "设计",
        "tags": "brand key visual, advertising campaign hero image, marketing KV",
        "quality": "commercial campaign quality, headline-ready negative space",
        "neg": "casual, amateur, low contrast",
        "camera": "hero wide or 3/4 product hero",
        "lighting": "brand-defined dramatic key, colored rim",
        "palette": "brand palette dominant + accent",
        "aspect": "16:9",
    },
    "专辑封面": {
        "category": "设计",
        "tags": "album cover art, music artwork, square format composition",
        "quality": "iconic album design, strong concept, emotive",
        "neg": "cluttered, literal, stock imagery",
        "camera": "",
        "lighting": "concept-driven, mood-heavy",
        "palette": "2-3 color highly intentional palette",
        "aspect": "1:1",
    },
    "复古海报": {
        "category": "设计",
        "tags": "vintage poster design, 1950s retro, letterpress print, screenprint texture",
        "quality": "saul bass meets mid-century, weathered paper feel",
        "neg": "modern flat design, digital gradient, 3d render",
        "camera": "",
        "lighting": "flat two-tone",
        "palette": "muted primary + cream background",
        "aspect": "3:4",
    },
    "电影海报": {
        "category": "设计",
        "tags": "movie poster, cinematic key art, title-ready composition",
        "quality": "theatrical one-sheet, dramatic hero composition",
        "neg": "casual snapshot, cluttered, amateur",
        "camera": "hero portrait or symmetric icon layout",
        "lighting": "strong single direction light, volumetric",
        "palette": "teal & orange or moody duotone",
        "aspect": "2:3",
    },
    "表情包": {
        "category": "设计",
        "tags": "sticker design, emoji style, expressive meme-ready character",
        "quality": "transparent background ready, bold outline, readable at 128px",
        "neg": "complex scene, photorealistic, subtle",
        "camera": "",
        "lighting": "flat cel shading",
        "palette": "bright saturated 4-color",
        "aspect": "1:1",
    },

    # ========== 艺术史 Art Movement ==========
    "印象派": {
        "category": "艺术",
        "tags": "impressionist painting, visible brushstrokes, plein air, monet inspired",
        "quality": "late 19th century impressionism, atmospheric perspective",
        "neg": "photorealistic, digital, sharp outlines",
        "camera": "",
        "lighting": "dappled natural light, sun-drenched scene",
        "palette": "broken color technique, complementary dabs",
        "aspect": "4:5",
    },
    "后印象派": {
        "category": "艺术",
        "tags": "post-impressionist, van gogh style, expressive brushstroke, emotive color",
        "quality": "starry night swirls, dynamic brush texture",
        "neg": "realistic, photographic, flat",
        "camera": "",
        "lighting": "emotional not physical light",
        "palette": "bold yellows cobalt and burnt sienna",
        "aspect": "4:5",
    },
    "新艺术": {
        "category": "艺术",
        "tags": "art nouveau, alphonse mucha, flowing organic lines, floral ornament border",
        "quality": "belle époque poster, feminine ornate frame",
        "neg": "geometric minimal, modern flat, 3d",
        "camera": "",
        "lighting": "flat even decorative light",
        "palette": "muted golds, soft earth tones, sage",
        "aspect": "2:3",
    },
    "装饰艺术": {
        "category": "艺术",
        "tags": "art deco, 1920s geometric ornament, gatsby aesthetic, gold and black lacquer",
        "quality": "symmetric art deco pattern, streamline moderne elegance",
        "neg": "rustic, organic nouveau, grunge",
        "camera": "",
        "lighting": "strong geometric shadow play",
        "palette": "black gold ivory with emerald accents",
        "aspect": "2:3",
    },

    # ========== 场景 / 氛围 Scene ==========
    "赛博朋克": {
        "category": "场景",
        "tags": "cyberpunk, neon-soaked, blade runner aesthetic, megacity dystopia, holographic ads",
        "quality": "detailed cyberpunk cityscape, rainy night ambiance",
        "neg": "rustic, medieval, natural countryside",
        "camera": "low angle wide, 24mm anamorphic",
        "lighting": "neon magenta and cyan rim, wet reflective streets",
        "palette": "magenta cyan black, neon highlights",
        "aspect": "21:9",
    },
    "蒸汽朋克": {
        "category": "场景",
        "tags": "steampunk, brass gears and copper pipes, victorian industrial, airship era",
        "quality": "intricate clockwork detail, rich leather and patina",
        "neg": "clean sci-fi, modern, plastic",
        "camera": "",
        "lighting": "warm gaslight glow, smoky haze",
        "palette": "brass copper sepia, burgundy leather",
        "aspect": "3:2",
    },
    "科幻": {
        "category": "场景",
        "tags": "sci-fi concept art, futuristic technology, clean spaceship interior, holographic UI",
        "quality": "blade runner 2049 palette, hard-sci-fi plausible",
        "neg": "medieval, fantasy magic, primitive",
        "camera": "cinematic wide, 21:9 framing",
        "lighting": "cool blue practical strips, volumetric haze",
        "palette": "cool blue cyan with warm accent",
        "aspect": "21:9",
    },
    "奇幻": {
        "category": "场景",
        "tags": "epic fantasy art, magical atmosphere, artstation trending, tolkien inspired",
        "quality": "detailed fantasy concept, elven architecture, dragon-scale atmosphere",
        "neg": "modern city, cyberpunk, mundane",
        "camera": "epic wide establishing, 24mm",
        "lighting": "ethereal god rays through mist",
        "palette": "golden hour warm with magical cyan glow",
        "aspect": "16:9",
    },
    "黑暗奇幻": {
        "category": "场景",
        "tags": "dark fantasy, grimdark, eldritch horror atmosphere, berserk aesthetic",
        "quality": "frank frazetta meets zdzisław beksiński",
        "neg": "cheerful, bright, cartoonish",
        "camera": "low angle hero or dread pov",
        "lighting": "blood moon crimson, torch flicker",
        "palette": "black crimson sickly green, rusted iron",
        "aspect": "2:3",
    },
    "国潮": {
        "category": "场景",
        "tags": "guochao Chinese neo-trend, modern hanfu revival, oriental modernism",
        "quality": "contemporary Chinese style illustration, editorial fashion",
        "neg": "western medieval, european style",
        "camera": "",
        "lighting": "warm accent on oriental red-gold",
        "palette": "vermillion jade gold, ink black accents",
        "aspect": "3:4",
    },
    "Y2K": {
        "category": "场景",
        "tags": "Y2K aesthetic, early 2000s digital, chrome bubble UI, frosted plastic",
        "quality": "low-fi cd-rom graphic, holographic stickers",
        "neg": "ultra clean modern, analog retro",
        "camera": "",
        "lighting": "glossy chrome highlights",
        "palette": "baby blue pink lilac, iridescent chrome",
        "aspect": "1:1",
    },
    "Vaporwave": {
        "category": "场景",
        "tags": "vaporwave, retro 80s 90s computer graphics, roman bust, palm tree grid",
        "quality": "synthwave aesthetic, low-fi jpeg nostalgia",
        "neg": "modern clean, natural, high detail",
        "camera": "",
        "lighting": "sunset gradient, neon grid horizon",
        "palette": "hot pink teal purple, retro sunset",
        "aspect": "16:9",
    },
    "霓虹灯牌": {
        "category": "场景",
        "tags": "neon sign typography, glowing tube letters, dark brick wall backdrop",
        "quality": "realistic neon glass tube glow, chromatic bloom",
        "neg": "daylight, printed sign, flat vector",
        "camera": "straight-on product shot, 50mm",
        "lighting": "self-emissive neon, dark ambient",
        "palette": "magenta cyan on deep black",
        "aspect": "3:2",
    },
    "建筑可视化": {
        "category": "场景",
        "tags": "architectural visualization, V-Ray / Lumion render, interior design magazine",
        "quality": "award-winning archviz, photorealistic materials",
        "neg": "sketchy, doodle, distorted perspective",
        "camera": "wide 24mm architectural tilt-corrected",
        "lighting": "realistic sun study plus artificial, product-ready",
        "palette": "natural materials, neutral brand-defined",
        "aspect": "16:9",
    },
    "电影感": {
        "category": "场景",
        "tags": "cinematic film still, anamorphic lens flare, letterboxed framing",
        "quality": "ARRI Alexa quality, professional color grade, movie still",
        "neg": "snapshot, amateur, flat lighting, instagram filter",
        "camera": "anamorphic 2.39:1 framing, low angle hero",
        "lighting": "motivated practical + volumetric haze",
        "palette": "teal & orange cinematic grade",
        "aspect": "21:9",
    },
    "概念艺术": {
        "category": "场景",
        "tags": "concept art, matte painting, production design, pre-visualization",
        "quality": "ILM / weta concept sketch, narrative-driven composition",
        "neg": "finished illustration, cartoon, low detail",
        "camera": "cinematic wide establishing",
        "lighting": "narrative-lit hero with atmosphere",
        "palette": "mood-defined limited palette",
        "aspect": "21:9",
    },
}

# ─────────────────────────────────────────────────────────
# 别名 (英文 / 同义词 → 规范预设名)
# ─────────────────────────────────────────────────────────
ALIASES: Dict[str, str] = {
    # 英文
    "realistic": "写实摄影",
    "photo": "写实摄影",
    "photography": "写实摄影",
    "film": "胶片摄影",
    "analog": "胶片摄影",
    "bw": "黑白摄影",
    "blackwhite": "黑白摄影",
    "monochrome": "黑白摄影",
    "portrait": "人像摄影",
    "fashion": "时尚大片",
    "editorial": "时尚大片",
    "food": "美食摄影",
    "product": "产品摄影",
    "ecommerce": "产品摄影",
    "macro": "微距摄影",
    "aerial": "航拍摄影",
    "drone": "航拍摄影",
    "street": "街拍纪实",
    "documentary": "街拍纪实",
    "anime": "动漫",
    "ghibli": "宫崎骏",
    "miyazaki": "宫崎骏",
    "shinkai": "新海诚",
    "makoto": "新海诚",
    "comic": "美漫",
    "marvel": "美漫",
    "chibi": "Q版",
    "kawaii": "Q版",
    "storybook": "童话绘本",
    "childrensbook": "童话绘本",
    "watercolor": "水彩",
    "oil": "油画",
    "ink": "水墨",
    "sumi": "水墨",
    "gongbi": "工笔国画",
    "ukiyoe": "浮世绘",
    "lineart": "线稿",
    "pixel": "像素艺术",
    "3d": "3DC4D",
    "c4d": "3DC4D",
    "octane": "3DC4D",
    "blindbox": "盲盒手办",
    "popmart": "盲盒手办",
    "lowpoly": "低多边形",
    "isometric": "等距视图",
    "iso": "等距视图",
    "claymation": "粘土",
    "felt": "毛毡手工",
    "papercraft": "纸艺",
    "minimal": "极简主义",
    "minimalist": "极简主义",
    "flat": "平面设计",
    "vector": "平面设计",
    "logo": "Logo设计",
    "icon": "图标设计",
    "infographic": "信息图",
    "kv": "品牌KV",
    "album": "专辑封面",
    "poster": "复古海报",
    "movieposter": "电影海报",
    "sticker": "表情包",
    "emoji": "表情包",
    "impressionist": "印象派",
    "vangogh": "后印象派",
    "postimpressionist": "后印象派",
    "artnouveau": "新艺术",
    "mucha": "新艺术",
    "artdeco": "装饰艺术",
    "cyberpunk": "赛博朋克",
    "steampunk": "蒸汽朋克",
    "scifi": "科幻",
    "fantasy": "奇幻",
    "darkfantasy": "黑暗奇幻",
    "grimdark": "黑暗奇幻",
    "guochao": "国潮",
    "y2k": "Y2K",
    "vaporwave": "Vaporwave",
    "synthwave": "Vaporwave",
    "neon": "霓虹灯牌",
    "archviz": "建筑可视化",
    "architecture": "建筑可视化",
    "cinematic": "电影感",
    "cinema": "电影感",
    "concept": "概念艺术",
    "conceptart": "概念艺术",
}


# ─────────────────────────────────────────────────────────
# 意图关键词 → (推荐预设, 推荐画幅)
# ─────────────────────────────────────────────────────────
INTENT_KEYWORDS: List[Tuple[str, str, str]] = [
    # (关键词, 推荐预设, 推荐画幅)
    ("logo", "Logo设计", "1:1"),
    ("徽标", "Logo设计", "1:1"),
    ("标志", "Logo设计", "1:1"),
    ("icon", "图标设计", "1:1"),
    ("图标", "图标设计", "1:1"),
    ("app图标", "图标设计", "1:1"),
    ("电影海报", "电影海报", "2:3"),
    ("海报", "复古海报", "3:4"),
    ("poster", "复古海报", "3:4"),
    ("封面", "专辑封面", "1:1"),
    ("专辑", "专辑封面", "1:1"),
    ("表情包", "表情包", "1:1"),
    ("贴纸", "表情包", "1:1"),
    ("信息图", "信息图", "3:4"),
    ("infographic", "信息图", "3:4"),
    ("kv", "品牌KV", "16:9"),
    ("主视觉", "品牌KV", "16:9"),
    ("产品", "产品摄影", "1:1"),
    ("电商", "产品摄影", "1:1"),
    ("商品", "产品摄影", "1:1"),
    ("美食", "美食摄影", "1:1"),
    ("食物", "美食摄影", "1:1"),
    ("菜品", "美食摄影", "1:1"),
    ("头像", "人像摄影", "1:1"),
    ("肖像", "人像摄影", "3:4"),
    ("人像", "人像摄影", "3:4"),
    ("时装", "时尚大片", "3:4"),
    ("时尚", "时尚大片", "3:4"),
    ("街拍", "街拍纪实", "3:2"),
    ("纪实", "街拍纪实", "3:2"),
    ("风景", "写实摄影", "16:9"),
    ("风光", "写实摄影", "16:9"),
    ("建筑", "建筑可视化", "16:9"),
    ("室内", "建筑可视化", "4:3"),
    ("手办", "盲盒手办", "1:1"),
    ("盲盒", "盲盒手办", "1:1"),
    ("玩具", "盲盒手办", "1:1"),
    ("航拍", "航拍摄影", "16:9"),
    ("鸟瞰", "航拍摄影", "16:9"),
    ("微距", "微距摄影", "1:1"),
    ("赛博", "赛博朋克", "21:9"),
    ("cyberpunk", "赛博朋克", "21:9"),
    ("蒸汽朋克", "蒸汽朋克", "3:2"),
    ("科幻", "科幻", "21:9"),
    ("未来", "科幻", "21:9"),
    ("奇幻", "奇幻", "16:9"),
    ("魔幻", "奇幻", "16:9"),
    ("黑暗", "黑暗奇幻", "2:3"),
    ("水墨", "水墨", "3:4"),
    ("国画", "工笔国画", "3:4"),
    ("工笔", "工笔国画", "3:4"),
    ("浮世绘", "浮世绘", "2:3"),
    ("童话", "童话绘本", "4:3"),
    ("绘本", "童话绘本", "4:3"),
    ("宫崎骏", "宫崎骏", "16:9"),
    ("新海诚", "新海诚", "16:9"),
    ("动漫", "动漫", "3:4"),
    ("二次元", "动漫", "3:4"),
    ("q版", "Q版", "1:1"),
    ("Q版", "Q版", "1:1"),
    ("chibi", "Q版", "1:1"),
    ("线稿", "线稿", "1:1"),
    ("像素", "像素艺术", "1:1"),
    ("3d", "3DC4D", "1:1"),
    ("c4d", "3DC4D", "1:1"),
    ("粘土", "粘土", "1:1"),
    ("等距", "等距视图", "1:1"),
    ("国潮", "国潮", "3:4"),
    ("霓虹", "霓虹灯牌", "3:2"),
    ("电影", "电影感", "21:9"),
    ("cinema", "电影感", "21:9"),
    ("concept", "概念艺术", "21:9"),
    ("概念图", "概念艺术", "21:9"),
    ("复古", "复古海报", "3:4"),
    ("vintage", "复古海报", "3:4"),
]

# ─────────────────────────────────────────────────────────
# 构图关键词
# ─────────────────────────────────────────────────────────
COMPOSITION_KEYWORDS: Dict[str, str] = {
    "特写": "extreme close-up shot",
    "近景": "close-up shot",
    "中景": "medium shot",
    "全身": "full body shot",
    "半身": "medium shot, waist up",
    "远景": "wide shot, establishing shot",
    "全景": "panoramic view",
    "俯拍": "top-down view",
    "俯视": "top-down view",
    "仰拍": "low angle shot, looking up",
    "仰视": "low angle shot, looking up",
    "鸟瞰": "bird's eye view, aerial",
    "平视": "eye-level shot",
    "正面": "front view",
    "侧面": "side profile view",
    "背面": "back view",
    "三分之二": "three-quarter view",
}

# ─────────────────────────────────────────────────────────
# 情绪关键词
# ─────────────────────────────────────────────────────────
MOOD_KEYWORDS: Dict[str, str] = {
    "温暖": "warm cozy atmosphere, golden tones",
    "温馨": "warm cozy atmosphere, golden tones",
    "冷峻": "cold atmosphere, steely blue tones",
    "神秘": "mysterious mood, foggy, dim lighting",
    "梦幻": "dreamy ethereal mood, soft glow, bokeh",
    "欢快": "joyful vibrant, bright cheerful colors",
    "忧郁": "melancholic mood, muted cool palette",
    "压抑": "oppressive mood, deep shadows, heavy atmosphere",
    "史诗": "epic grandeur, cinematic scale",
    "高级": "luxury sophistication, premium materials",
    "治愈": "healing soft ambiance, soothing",
    "清新": "fresh airy light pastel",
    "紧张": "tense suspense mood, high contrast",
    "浪漫": "romantic soft pink glow",
}

# ─────────────────────────────────────────────────────────
# 画幅 → 模型特定写法
# ─────────────────────────────────────────────────────────
ASPECT_TO_MJ = {
    "1:1": "--ar 1:1",
    "3:4": "--ar 3:4",
    "4:3": "--ar 4:3",
    "3:2": "--ar 3:2",
    "2:3": "--ar 2:3",
    "16:9": "--ar 16:9",
    "9:16": "--ar 9:16",
    "21:9": "--ar 21:9",
    "4:5": "--ar 4:5",
}

ASPECT_TO_SDXL = {
    "1:1": "1024x1024",
    "3:4": "896x1152",
    "4:3": "1152x896",
    "3:2": "1216x832",
    "2:3": "832x1216",
    "16:9": "1344x768",
    "9:16": "768x1344",
    "21:9": "1536x640",
    "4:5": "912x1144",
}


# ─────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────
def resolve_preset(name: Optional[str]) -> str:
    """预设名归一化：支持中文 / 英文别名 / 大小写不敏感。"""
    if not name:
        return ""
    key = name.strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    if key in ALIASES:
        return ALIASES[key]
    for p in STYLE_PRESETS:
        if p.lower() == key or p.lower().replace(" ", "") == key:
            return p
    return name if name in STYLE_PRESETS else ""


def parse_requirement(text: str) -> Dict[str, str]:
    """从用户输入中解析意图、画幅、构图、情绪。

    返回 dict 字段：
        preset_suggestion  推荐预设（可能为空）
        aspect_suggestion  推荐画幅
        composition        构图片段（英文，可为空）
        mood               情绪片段（英文，可为空）
    """
    lower = text.lower()
    out = {"preset_suggestion": "", "aspect_suggestion": "", "composition": "", "mood": ""}

    for kw, preset, aspect in INTENT_KEYWORDS:
        if kw.lower() in lower:
            out["preset_suggestion"] = preset
            out["aspect_suggestion"] = aspect
            break

    for zh, en in COMPOSITION_KEYWORDS.items():
        if zh in text:
            out["composition"] = en
            break

    for zh, en in MOOD_KEYWORDS.items():
        if zh in text:
            out["mood"] = en
            break

    return out


def sanitize_subject(text: str) -> str:
    """清理主体描述：去除首尾标点和多余空白。"""
    return re.sub(r"\s+", " ", text).strip().rstrip(".,，、。;；")


def stable_seed(subject: str, preset: str) -> int:
    """根据主体 + 预设生成稳定的种子建议（32-bit 正整数）。"""
    h = hashlib.md5(f"{subject}|{preset}".encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def build_prompt(
    subject: str,
    preset: str,
    model: str = "通用",
    aspect: str = "",
    extra_mood: str = "",
    extra_composition: str = "",
    seed: Optional[int] = None,
) -> Dict:
    """构建增强后的提示词。"""
    preset = resolve_preset(preset) or "写实摄影"
    data = STYLE_PRESETS[preset]
    subject_clean = sanitize_subject(subject)

    auto = parse_requirement(subject)
    if not extra_composition:
        extra_composition = auto["composition"]
    if not extra_mood:
        extra_mood = auto["mood"]
    if not aspect:
        aspect = data.get("aspect", "1:1")

    consistency_parts = [
        data["tags"],
        data.get("camera", ""),
        data.get("lighting", ""),
        data.get("palette", ""),
    ]
    consistency = ", ".join([x for x in consistency_parts if x])

    quality_combined = f"{data['quality']}, {UNIVERSAL_QUALITY}"
    universal_neg_filtered = _filter_neg(UNIVERSAL_NEG, PRESET_NEG_EXCLUDE.get(preset, []))
    neg_combined = f"{data['neg']}, {universal_neg_filtered}"
    extras = ", ".join([x for x in [extra_composition, extra_mood] if x])

    # 按模型生成不同形式
    if model in ("Midjourney", "MJ", "mj"):
        core = f"{subject_clean}, {consistency}"
        if extras:
            core = f"{core}, {extras}"
        core = f"{core}, {quality_combined}"
        flags = [ASPECT_TO_MJ.get(aspect, "--ar 1:1"), "--stylize 250"]
        positive = f"{core} {' '.join(flags)}"
        negative = f"--no {neg_combined}"
        hint = (
            "Midjourney tips：\n"
            "  • 角色/产品系列一致：加 --cref <url> 或 --sref <url>\n"
            f"  • 想要更风格化加 --stylize 500~750；更写实降到 --stylize 50\n"
            f"  • 建议 seed 锁定：--seed {seed or stable_seed(subject_clean, preset)}"
        )

    elif model in ("Stable Diffusion", "SD", "sd"):
        positive = (
            f"({subject_clean}:1.2), {consistency}"
            + (f", {extras}" if extras else "")
            + f", {quality_combined}"
        )
        negative = neg_combined
        hint = (
            "Stable Diffusion tips：\n"
            f"  • 强化权重: (word:1.2~1.5), 减弱: [word:0.7]\n"
            f"  • 建议尺寸 (SD 1.5): 512x{{hw_from_aspect}}; (SDXL): {ASPECT_TO_SDXL.get(aspect,'1024x1024')}\n"
            f"  • 采样: DPM++ 2M Karras, 30 steps, CFG 6.5\n"
            f"  • 建议 seed 锁定: {seed or stable_seed(subject_clean, preset)}（系列同 seed 提升一致性）"
        )

    elif model in ("SDXL", "sdxl"):
        positive = (
            f"{subject_clean}, {consistency}"
            + (f", {extras}" if extras else "")
            + f", {quality_combined}"
        )
        negative = neg_combined
        hint = (
            "SDXL tips：\n"
            f"  • 推荐尺寸: {ASPECT_TO_SDXL.get(aspect,'1024x1024')}\n"
            f"  • 采样: DPM++ SDE Karras, 25-30 steps, CFG 5-7\n"
            f"  • Refiner 使用率 0.2-0.3\n"
            f"  • seed: {seed or stable_seed(subject_clean, preset)}"
        )

    elif model in ("DALL-E", "DALL·E", "dalle", "DALLE"):
        parts = [f"A {preset} style image of {subject_clean}"]
        if data.get("camera"):
            parts.append(f"captured with {data['camera']}")
        if data.get("lighting"):
            parts.append(f"lit by {data['lighting']}")
        if data.get("palette"):
            parts.append(f"with a color palette of {data['palette']}")
        if extras:
            parts.append(extras)
        parts.append("highly detailed, professional composition")
        positive = ". ".join(parts) + "."
        negative = "(DALL-E 3 忽略负面提示，已通过正向描述规避)"
        hint = (
            "DALL-E 3 tips：\n"
            "  • 用自然语言句子 + 细节形容词效果最佳\n"
            f"  • 画幅: {aspect} (仅支持 1:1, 16:9, 9:16 在 ChatGPT 内)\n"
            "  • 一致性: 在同一会话连续生成并引用 \"use the same character\""
        )

    elif model in ("Flux", "flux"):
        positive = (
            f"{subject_clean}. {consistency}."
            + (f" {extras}." if extras else "")
            + f" {quality_combined}."
        )
        negative = neg_combined
        hint = (
            "Flux tips：\n"
            "  • 支持长自然语言提示，可加句式结构 \"The subject is...\"\n"
            f"  • 建议 Flux Dev: guidance 3.5; Flux Schnell: guidance 0\n"
            f"  • seed: {seed or stable_seed(subject_clean, preset)}"
        )

    else:  # 通用
        positive = (
            f"{subject_clean}, {consistency}"
            + (f", {extras}" if extras else "")
            + f", {quality_combined}"
        )
        negative = neg_combined
        hint = "通用格式：Midjourney / SD / Flux 皆可直接使用。"

    return {
        "version": VERSION,
        "original": subject,
        "preset": preset,
        "model": model,
        "aspect": aspect,
        "composition": extra_composition,
        "mood": extra_mood,
        "seed_suggestion": seed or stable_seed(subject_clean, preset),
        "positive": positive,
        "negative": negative,
        "hint": hint,
        "consistency_lock": {
            "camera": data.get("camera", ""),
            "lighting": data.get("lighting", ""),
            "palette": data.get("palette", ""),
            "aspect": aspect,
        },
    }


def build_series(
    subject: str, preset: str, model: str, aspect: str, variations: List[str], seed: Optional[int] = None
) -> List[Dict]:
    """系列批量生成：共享 camera/lighting/palette/seed 锁，仅替换主体描述。"""
    if seed is None:
        seed = stable_seed(subject, preset)
    results = []
    for i, v in enumerate(variations, 1):
        full = f"{subject}, {v}" if v and v != subject else subject
        r = build_prompt(full, preset, model, aspect, seed=seed)
        r["series_index"] = i
        r["series_total"] = len(variations)
        results.append(r)
    return results


# ─────────────────────────────────────────────────────────
# 输出
# ─────────────────────────────────────────────────────────
def print_prompt(result: Dict):
    sep = "═" * 60
    print(f"\n{sep}")
    if "series_index" in result:
        print(f"📸 系列生成 [{result['series_index']}/{result['series_total']}]")
    print(f"📌 原始描述   : {result['original']}")
    print(f"🎨 风格预设   : {result['preset']}")
    print(f"🤖 目标模型   : {result['model']}")
    print(f"📐 画幅       : {result['aspect']}")
    if result.get("composition"):
        print(f"🎥 构图       : {result['composition']}")
    if result.get("mood"):
        print(f"🎭 情绪       : {result['mood']}")
    print(f"🎲 种子建议   : {result['seed_suggestion']}")
    print(f"\n✅ 正向提示词：")
    print(f"{result['positive']}")
    print(f"\n❌ 负向提示词：")
    print(f"{result['negative']}")
    print(f"\n🔒 一致性锁：")
    for k, v in result["consistency_lock"].items():
        if v:
            print(f"   {k:8s}: {v}")
    print(f"\n💡 {result['hint']}")
    print(f"{sep}\n")


def list_presets():
    by_cat: Dict[str, List[str]] = {}
    for name, data in STYLE_PRESETS.items():
        by_cat.setdefault(data["category"], []).append(name)
    print(f"\n🎨 可用风格预设 (共 {len(STYLE_PRESETS)} 款)")
    print("─" * 50)
    for cat in ["摄影", "动漫", "插画", "3D", "设计", "艺术", "场景"]:
        if cat not in by_cat:
            continue
        print(f"\n【{cat}】 {len(by_cat[cat])} 款")
        for name in by_cat[cat]:
            print(f"  • {name}")
    print(f"\n💡 同义别名示例：anime, ghibli, cyberpunk, minimal, 3d, logo, neon ...\n")


# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-test v{VERSION} — T2I 提示词增强工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础
  enhance_prompt.py "一只赛博朋克风格的猫" -p 赛博朋克 -m Midjourney

  # 自动意图（省略 -p，脚本自动推荐 Logo设计预设 + 1:1 画幅）
  enhance_prompt.py "为咖啡品牌设计一个logo"

  # 英文别名
  enhance_prompt.py "spaceship in nebula" -p scifi -m Flux -a 21:9

  # 系列一致性（4 张共享 camera/lighting/palette/seed）
  enhance_prompt.py "一个红发女侠" -p 动漫 -s 4 \\
      --variations "持剑站立,骑马奔驰,弯弓射箭,与龙对视"

  # JSON 输出，便于链式集成
  enhance_prompt.py "极简Logo一朵山茶花" -p Logo设计 -j
""",
    )
    parser.add_argument("subject", nargs="?", help="要生成图片的主体描述")
    parser.add_argument("-p", "--preset", help="风格预设（中文 / 英文别名）")
    parser.add_argument(
        "-m", "--model", default="通用",
        help="目标模型: Midjourney / SD / SDXL / DALL-E / Flux / 通用",
    )
    parser.add_argument("-a", "--aspect", default="", help="画幅: 1:1 / 3:4 / 16:9 / 21:9 ...")
    parser.add_argument("--mood", default="", help="情绪覆盖")
    parser.add_argument("--composition", default="", help="构图覆盖")
    parser.add_argument("--seed", type=int, help="种子（不给则哈希生成稳定 seed）")
    parser.add_argument("-s", "--series", type=int, default=1, help="系列张数（配合 --variations 使用）")
    parser.add_argument("--variations", default="", help="系列变体，逗号分隔，如 '持剑,骑马,射箭'")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有预设")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")

    args = parser.parse_args()

    if args.list:
        list_presets()
        return

    if not args.subject:
        parser.print_help()
        sys.exit(1)

    # 自动推荐
    auto = parse_requirement(args.subject)
    preset = args.preset or auto["preset_suggestion"] or "写实摄影"
    aspect = args.aspect or auto["aspect_suggestion"] or STYLE_PRESETS.get(resolve_preset(preset) or "写实摄影", {}).get("aspect", "1:1")

    # 系列模式
    if args.series > 1 or args.variations:
        variations = [v.strip() for v in args.variations.split(",") if v.strip()]
        if not variations:
            variations = [args.subject] * args.series
        elif len(variations) < args.series:
            variations += [variations[-1]] * (args.series - len(variations))
        results = build_series(args.subject, preset, args.model, aspect, variations[: max(args.series, len(variations))], seed=args.seed)
        if args.json:
            print(json.dumps({"version": VERSION, "series": results}, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print_prompt(r)
            print(f"🔐 本系列 {len(results)} 张共享 seed = {results[0]['seed_suggestion']}，一致性锁见每张「🔒」区块。")
        return

    # 单张
    result = build_prompt(
        args.subject, preset, args.model, aspect,
        extra_mood=args.mood, extra_composition=args.composition, seed=args.seed,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_prompt(result)


if __name__ == "__main__":
    main()
