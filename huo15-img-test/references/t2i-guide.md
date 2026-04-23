# T2I 提示词工程参考

## 提示词核心要素

| 要素 | 说明 | 示例 |
|------|------|------|
| **主体** | 画面核心对象 | a cat, a futuristic building, a woman |
| **材质/介质** | 画面的质感 | oil painting, digital art, photography, watercolor |
| **风格** | 艺术风格 | cyberpunk, impressionist, anime, realistic |
| **光线** | 光照方向和类型 | golden hour, neon glow, soft diffused, dramatic rim light |
| **色彩** | 色调倾向 | warm tones, desaturated, vibrant, monochromatic |
| **构图** | 视角和取景 | close-up, wide angle, bird's eye view, portrait |
| **背景** | 环境设定 | busy city street, empty beach, starfield, studio |
| **质量词** | 画质强化 | masterpiece, best quality, highly detailed, 8k |
| **负面提示词** | 不想出现的 | lowres, bad anatomy, blurry, worst quality |

## 风格预设对照表

| 预设 | 风格标签 | 适用场景 |
|------|---------|---------|
| 写实摄影 | `photorealistic, shot on Canon EOS R5, f/1.8, professional lighting` | 产品、人像、建筑 |
| 胶片摄影 | `film grain, shot on Kodak Portra 400, natural lighting` | 人文、街拍 |
| 动漫 | `anime style, vibrant colors, detailed eyes, studio Ghibli` | 角色、场景 |
| 赛博朋克 | `cyberpunk, neon lights, rain-soaked streets, blade runner aesthetic` | 城市、氛围 |
| 水彩 | `watercolor painting, soft edges, delicate brushstrokes` | 插画、绘本 |
| 油画 | `oil painting, impressionist style, visible brushstrokes` | 艺术创作 |
| 建筑可视化 | `architectural visualization, clean lines, V-Ray render, professional` | 建筑、设计 |
| 产品设计 | `product design render, white background, studio lighting, minimal` | 电商、产品 |
| 像素艺术 | `pixel art, 16-bit, vibrant colors, retro game aesthetic` | 游戏、图标 |
| 奇幻 | `fantasy art, epic composition, detailed, artstation trending` | 场景、角色 |
| 科幻 | `sci-fi, holographic, futuristic UI, clean tech aesthetic` | 概念设计 |
| 复古海报 | `vintage poster design, 1950s style, bold colors, letterpress` | 设计、海报 |
| 水墨 | `Chinese ink painting, sumi-e, minimalist, zen atmosphere` | 东方艺术 |
| 蒸汽朋克 | `steampunk, brass and copper, Victorian era, gears` | 风格、概念 |
| 极简主义 | `minimalist, clean composition, abundant white space, simple` | 设计、图标 |

## 模型差异提示

| 模型 | 提示词偏好 |
|------|-----------|
| **Midjourney** | 逗号分隔，短句优先，风格词放前面 |
| **Stable Diffusion** | 强调权重用 `(word:1.5)`，tag式描述效果好 |
| **DALL-E 3** | 自然语言描述，细节越多越好 |
| **Flux** | 自由格式，对长提示词支持好 |
| **Stable Diffusion XL** | 质量标签堆叠效果明显 |
