# tokens.json → tailwind.config.js

> 用 `theme.extend` 注入流派 token，**不要覆盖**默认。

## jq 转换

```bash
jq '{
  theme: {
    extend: {
      colors: .color,
      spacing: (.spacing | with_entries({
        key: .key,
        value: (if (.value | type) == "number" then "\(.value)px" else .value end)
      })),
      borderRadius: (.radius | with_entries({
        key: .key,
        value: (if (.value | type) == "number" then "\(.value)px" else .value end)
      })),
      boxShadow: .shadow,
      transitionDuration: (.motion.duration // {} | with_entries({
        key: .key,
        value: "\(.value)ms"
      })),
      transitionTimingFunction: .motion.easing // {}
    }
  }
}' tokens/bold-minimal.json > generated/tailwind/bold-minimal.tailwind.json
```

## 落地到 tailwind.config.js

```js
import boldMinimal from './generated/tailwind/bold-minimal.tailwind.json' assert { type: 'json' };

export default {
  content: ['./**/*.{html,js,ts,tsx,vue}'],
  theme: {
    extend: {
      ...boldMinimal.theme.extend,
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        body: ['"IBM Plex Sans"', 'sans-serif']
      }
    }
  }
};
```

用法：

```html
<h1 class="font-display text-ink leading-none">少即是<em>极致</em></h1>
<p class="text-mute mt-md">承诺一个方向</p>
<a class="bg-ink text-paper rounded-pill px-lg py-md transition-colors duration-fast ease-standard">查看 →</a>
```

`duration-fast` / `ease-standard` 是 v4.5 motion tokens 通过 `transitionDuration` / `transitionTimingFunction` 注入到 Tailwind 后产生的 utility class。

## 红线提醒

- 不要把 token **覆盖** Tailwind 默认色（避免污染团队既有项目）— 只用 `extend`
- `fontFamily` 必须**显式**列入 `extend`（typography 字段是字符串描述，jq 不能直接转换）
- `radius.lg = 14` 不要无脑当全局 radius — 必须搭配多档（红线 #9）

## OKLCH 兼容

Tailwind v3.4+ 直接支持 oklch，无需额外配置。Tailwind v3.3- 需要 `@property` polyfill 或退到 hex fallback：

```bash
# hex fallback 版
jq '{ theme: { extend: { colors: .colorHex } } }' tokens/bold-minimal.json
```
