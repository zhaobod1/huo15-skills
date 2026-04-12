---
name: huo15-js-scraper
description: JavaScript渲染网站抓取工具。当需要抓取JS渲染的页面（如企微文档、Vue/React SPA）、绕过反爬、或者普通curl/wget/web_fetch无法获取内容的网站时使用此技能。支持Playwright和scrapling双引擎自动切换。
identifier: huo15-js-scraper
version: 1.0.0
author: 贾维斯
category: web-scraping
---

# huo15-js-scraper

JavaScript渲染网站抓取技能，支持Playwright和scrapling双引擎。

## 快速使用

```bash
# 基本用法（自动选择引擎）
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py <URL>

# 指定选择器
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py <URL> --selector ".content"

# 输出JSON
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py <URL> --output json

# 强制使用scrapling引擎
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py <URL> --engine scrapling
```

## 引擎选择策略

| 场景 | 推荐引擎 |
|------|---------|
| 企微文档 / 微信相关 | Playwright |
| Cloudflare保护站 | scrapling (stealth) |
| Vue/React SPA | Playwright |
| 简单静态页 | scrapling (basic) |
| 未知站 | Playwright（更稳定） |

## Python API

```python
from huo15_js_scraper import scrape

# 方式1：自动选择（推荐）
result = scrape('https://example.com')
print(result['content'])

# 方式2：强制Playwright
result = scrape('https://developer.work.weixin.qq.com/document/path/91756', engine='playwright')
```

## 常见问题

### Q: 企微文档怎么抓？
```bash
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py \
  "https://developer.work.weixin.qq.com/document/path/91756" \
  --wait 5
```

### Q: 提示playwright未安装？
```bash
pip3 install playwright --break-system-packages
playwright install chromium
```

### Q: scrapling安装？
```bash
pip3 install "scrapling[all]" --break-system-packages
scrapling install
```

### Q: 内容为空或获取到跳转页面？
增加 `--wait` 时间，让JS有更多时间渲染：
```bash
python3 ...scrape.py <URL> --wait 5
```

## 依赖安装

```bash
# Playwright（主引擎）
pip3 install playwright --break-system-packages
playwright install chromium

# scrapling（降级引擎）
pip3 install "scrapling[all]" --break-system-packages
scrapling install
```

## 工作原理

1. 优先使用 Playwright（chromium headless）加载页面，等待networkidle
2. 等待指定时间让JS渲染完成
3. 通过CSS选择器提取内容
4. 如果Playwright失败，自动降级到scrapling
