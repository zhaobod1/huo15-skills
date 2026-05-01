#!/usr/bin/env python3
"""小红书浏览器桥接 — 通过 Chrome CDP 安全浏览和分析笔记内容。

原理：连接用户真实 Chrome 实例（通过 CDP WebSocket），完全复用真实浏览器指纹 +
       登录态 + Cookie + 浏览历史。不是启动新浏览器，而是控制已有的真实浏览器。

为什么安全：
  - 真实 Chrome 指纹：navigator.webdriver=false，无自动化标记
  - 真实 TLS 指纹：Chrome 原生网络栈，非 requests/curl
  - 真实登录态：扫码登录后 Cookie 持久化在 Chrome Profile 中
  - 真实行为：人工浏览速度 + 随机化延迟 + 自然滚动

安全红线（硬编码，不可绕过）：
  - 只读浏览：绝不点赞/评论/关注/发布/私信
  - 拟人延迟：操作间隔 2~10 秒随机
  - 会话限制：单次会话 ≤ 30 次页面操作
  - 不批量抓取：搜索结果只取首页，笔记只取可见内容
  - 熔断机制：遇 403/461/460/406/captcha/滑块 → 立即停 30 分钟
  - 夜间休眠：0:00-6:00 不操作

2026 年风控要点（已规避）：
  - x-s 2.0 JSVMP 签名：不需要，因为走真实浏览器 HTTP 层
  - 动态 xsec_token：浏览器自动处理，不做手动 token 管理
  - TLS 指纹检测：Chrome 原生 TLS，非伪造
  - 行为序列分析：随机延迟 + 不固定操作模式 + 模拟滚动
  - CDP 命令泄露：只发 Runtime.evaluate，不发 Runtime.enable/Console.enable
  - 空 Profile 检测：复用同一 Chrome Profile，积累浏览历史

用法:
    python3 scripts/browser_bridge.py start                     # 启动 CDP Chrome + 打开 XHS
    python3 scripts/browser_bridge.py explore                   # 获取探索页推荐笔记
    python3 scripts/browser_bridge.py search <关键词>            # 搜索笔记
    python3 scripts/browser_bridge.py note <url>                # 打开单篇笔记，获取内容
    python3 scripts/browser_bridge.py analyze <url>             # 对标拆解一篇笔记
    python3 scripts/browser_bridge.py status                    # 检查连接状态
    python3 scripts/browser_bridge.py stop                      # 关闭 CDP Chrome
"""

from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

CDP_PORT = 9222
CDP_HOST = "127.0.0.1"
CHROME_PROFILE = os.path.expanduser("~/.claude/chrome-xhs-profile")
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 安全限制（硬编码）
MAX_OPS_PER_SESSION = 30
MIN_DELAY_SEC = 2
MAX_DELAY_SEC = 10
_session_ops = 0

# 熔断状态（持久化到文件）
_CIRCUIT_BREAKER_FILE = os.path.expanduser("~/.xiaohongshu/.browser_circuit_breaker")


def _check_circuit_breaker():
    """检查熔断状态。如果触发过熔断且未满 30 分钟，拒绝操作。"""
    if os.path.exists(_CIRCUIT_BREAKER_FILE):
        try:
            with open(_CIRCUIT_BREAKER_FILE) as f:
                triggered_at = float(f.read().strip())
            elapsed = time.time() - triggered_at
            if elapsed < 1800:  # 30 分钟
                remaining = int((1800 - elapsed) / 60)
                print(f"ERROR: 熔断保护中，请等待 {remaining} 分钟后重试。")
                print(f"触发时间: {datetime.fromtimestamp(triggered_at).strftime('%H:%M:%S')}")
                sys.exit(1)
            else:
                os.remove(_CIRCUIT_BREAKER_FILE)
        except (ValueError, OSError):
            pass


def _trigger_circuit_breaker(reason: str):
    """触发熔断：写时间戳，30 分钟内禁止所有操作。"""
    os.makedirs(os.path.dirname(_CIRCUIT_BREAKER_FILE), exist_ok=True)
    with open(_CIRCUIT_BREAKER_FILE, 'w') as f:
        f.write(str(time.time()))
    print(f"\n!!! 熔断触发: {reason}")
    print(f"!!! 所有操作已暂停 30 分钟。这是保护你的账号安全的必要措施。")
    print(f"!!! 不要强行绕过。30 分钟后自动恢复。\n")
    sys.exit(1)


def _check_nighttime():
    """夜间休眠检查：0:00-6:00 不操作。"""
    hour = datetime.now().hour
    if 0 <= hour < 6:
        print(f"ERROR: 夜间休眠时段（0:00-6:00），当前 {hour}:00。")
        print("这是保护账号的必要措施——真实用户这个时间也在睡觉。")
        sys.exit(1)


def _human_delay(short: bool = False):
    """拟人化随机延迟。"""
    global _session_ops
    _session_ops += 1
    if _session_ops > MAX_OPS_PER_SESSION:
        _trigger_circuit_breaker(f"单次会话已达上限 {MAX_OPS_PER_SESSION} 次操作")

    if short:
        delay = random.uniform(1.0, 3.0)
    else:
        delay = random.uniform(MIN_DELAY_SEC, MAX_DELAY_SEC)
    time.sleep(delay)


def _check_page_errors(result: dict):
    """检测页面返回是否含风控信号。"""
    if "error" in result:
        return
    body = str(result.get("body", "") or result.get("value", ""))
    # 风控关键词检测
    triggers = {
        "460": "Cookie/签名环境不一致（460）",
        "461": "Cookie/签名环境不一致（461）",
        "403 Forbidden": "访问被拒（403）",
        "406": "签名参数错误（406）",
        "captcha": "触发验证码",
        "滑块": "触发滑块验证",
        "请稍后再试": "频率限制触发",
        "300017": "反自动化检测（300017）",
        "访问异常": "访问异常检测",
        "网络异常": "网络异常",
    }
    for key, reason in triggers.items():
        if key.lower() in body.lower():
            _trigger_circuit_breaker(reason)


def _simulate_scroll(ws, times: int = 2):
    """模拟自然滚动行为——真实用户不会打开页面后一动不动。"""
    for _ in range(times):
        ws.send(json.dumps({
            "id": 99,
            "method": "Runtime.evaluate",
            "params": {
                "expression": f"window.scrollBy(0, {random.randint(200, 600)})",
                "returnByValue": True
            }
        }))
        time.sleep(random.uniform(0.5, 1.5))


def _cdp_request(path: str, method: str = "GET") -> dict | list:
    """发送 CDP HTTP 请求。"""
    import urllib.request
    url = f"http://{CDP_HOST}:{CDP_PORT}{path}"
    req = urllib.request.Request(url, method=method)
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except Exception as e:
        print(f"CDP 连接失败: {e}")
        print("请先运行: python3 scripts/browser_bridge.py start")
        sys.exit(1)


def _cdp_execute(expression: str, tab_url_contains: str = "xiaohongshu", timeout: int = 15, scroll: bool = True) -> dict:
    """在匹配的标签页中执行 JavaScript 并返回结果。含风控检测 + 拟人滚动。"""
    import websocket

    _check_circuit_breaker()
    _check_nighttime()

    tabs = _cdp_request("/json")
    if isinstance(tabs, dict):
        tabs = [tabs]
    target = None
    for t in tabs:
        if t.get("type") == "page" and tab_url_contains in t.get("url", ""):
            target = t
            break
    if not target:
        target = _cdp_request(f"/json/new?https://www.xiaohongshu.com/{tab_url_contains}", "PUT")
        time.sleep(random.uniform(3.0, 5.0))

    ws_url = target["webSocketDebuggerUrl"]
    results = {}

    def on_msg(ws, msg):
        m = json.loads(msg)
        if "id" in m:
            results[m["id"]] = m

    def on_open(ws):
        # 模拟滚动后再提取内容（更自然）
        if scroll:
            _simulate_scroll(ws, times=random.randint(1, 3))

        ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": expression, "returnByValue": True}
        }))

    ws = websocket.WebSocketApp(ws_url, on_message=on_msg, on_open=on_open)
    t = threading.Thread(target=ws.run_forever)
    t.daemon = True
    t.start()

    start = time.time()
    while 1 not in results and (time.time() - start) < timeout:
        time.sleep(0.3)
    ws.close()

    if 1 not in results:
        return {"error": "timeout"}
    r = results[1]
    if "error" in r:
        return {"error": r["error"]}
    val = r.get("result", {}).get("result", {}).get("value", "N/A")
    try:
        result = json.loads(val)
    except (json.JSONDecodeError, TypeError):
        result = {"value": str(val)[:1000]}

    # 风控检测
    _check_page_errors(result)
    return result


def cmd_start():
    """启动 CDP Chrome 并打开小红书。"""
    _check_circuit_breaker()
    _check_nighttime()

    os.makedirs(CHROME_PROFILE, exist_ok=True)

    # 检查是否已运行
    try:
        ver = _cdp_request("/json/version")
        print(f"CDP Chrome 已在运行 ({ver.get('Browser', '?')})。")
        _cdp_request("/json/new?https://www.xiaohongshu.com/explore", "PUT")
        print("已打开小红书探索页。")
        print("\n安全提示:")
        print("  - 只浏览，不操作（点赞/评论/关注/发布）")
        print("  - 浏览速度保持人类节奏")
        print("  - 遇到验证码立即停止，等 30 分钟")
        return
    except Exception:
        pass

    # 关闭旧 CDP 进程（不影响用户正常 Chrome）
    subprocess.run(["pkill", "-f", "Google Chrome.*remote-debugging"], capture_output=True)
    time.sleep(2)

    # 启动 Chrome（注意：不传 --enable-automation，不设 --disable-blink-features）
    subprocess.Popen([
        CHROME_BIN,
        f"--remote-debugging-port={CDP_PORT}",
        "--remote-allow-origins=*",
        f"--user-data-dir={CHROME_PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        "https://www.xiaohongshu.com/explore",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(5)
    try:
        ver = _cdp_request("/json/version")
        print(f"CDP Chrome 已启动 ({ver.get('Browser', '?')})。")
        print("如需扫码登录，请用小红书 App 扫描浏览器中的二维码。")
        print("\n安全提示:")
        print("  - 只浏览，不操作（点赞/评论/关注/发布）")
        print("  - 浏览速度保持人类节奏")
        print("  - 遇到验证码立即停止，等 30 分钟")
    except Exception:
        print("启动失败，请手动尝试。")
        print(f"手动启动命令: \"{CHROME_BIN}\" --remote-debugging-port={CDP_PORT} --remote-allow-origins='*' --user-data-dir=\"{CHROME_PROFILE}\" https://www.xiaohongshu.com/explore")
        sys.exit(1)


def cmd_stop():
    """关闭 CDP Chrome。"""
    subprocess.run(["pkill", "-f", "Google Chrome.*remote-debugging"], capture_output=True)
    print("CDP Chrome 已关闭。")


def cmd_status():
    """检查连接状态和登录状态。"""
    try:
        ver = _cdp_request("/json/version")
        browser = ver.get("Browser", "Unknown")
        print(f"CDP: 已连接 ({browser})")

        result = _cdp_execute("""
            JSON.stringify({
                title: document.title,
                url: window.location.href,
                isLoggedIn: document.body ? !document.body.innerText.includes('手机号登录') : false,
                noteCount: document.querySelectorAll('a[href*=\"/explore/\"]').length
            })
        """)
        if "error" not in result:
            print(f"页面: {result.get('title', '?')}")
            print(f"登录: {'已登录' if result.get('isLoggedIn') else '未登录'}")
            print(f"可见笔记链接: {result.get('noteCount', 0)} 条")
        else:
            print(f"页面读取失败: {result.get('error')}")
    except Exception as e:
        print(f"CDP 未连接: {e}")
        print("请运行: python3 scripts/browser_bridge.py start")


def cmd_explore():
    """获取探索页推荐笔记列表。"""
    _human_delay()
    print("正在获取探索页推荐…")

    result = _cdp_execute("""
        JSON.stringify((function() {
            var notes = [];
            var links = document.querySelectorAll('a[href*=\"/explore/\"]');
            var seen = {};
            for (var i = 0; i < links.length; i++) {
                var a = links[i];
                var text = a.innerText.trim();
                var href = a.href;
                if (text.length > 4 && text.length < 200 && !seen[href]) {
                    seen[href] = true;
                    // 尝试获取互动数据
                    var parent = a.closest('section, div[class*=note], div[class*=card]');
                    var likes = '';
                    if (parent) {
                        var likeEl = parent.querySelector('[class*=like], [class*=count], span');
                        if (likeEl) likes = likeEl.innerText.trim();
                    }
                    notes.push({title: text.substring(0, 100), url: href, likes: likes});
                }
            }
            return {notes: notes.slice(0, 20), total: links.length};
        })())
    """)

    if "error" in result:
        print(f"获取失败: {result['error']}")
        return

    notes = result.get("notes", [])
    if not notes:
        print("未找到笔记。可能需要刷新页面或重新登录。")
        return

    print(f"\n探索页推荐 ({len(notes)} 条):\n")
    for i, n in enumerate(notes):
        likes_str = f" | ❤️ {n['likes']}" if n.get("likes") else ""
        print(f"  {i+1}. {n['title']}{likes_str}")
        print(f"     {n['url'][:80]}")
        print()


def cmd_search(keyword: str):
    """搜索笔记。"""
    _human_delay()
    print(f"搜索: {keyword}")

    # 导航到搜索页
    import urllib.parse
    search_url = f"https://www.xiaohongshu.com/search_result?keyword={urllib.parse.quote(keyword)}"
    _cdp_request(f"/json/new?{search_url}", "PUT")
    time.sleep(4)

    result = _cdp_execute("""
        JSON.stringify((function() {
            var notes = [];
            var links = document.querySelectorAll('a[href*=\"/explore/\"]');
            var seen = {};
            for (var i = 0; i < links.length; i++) {
                var a = links[i];
                var text = a.innerText.trim();
                var href = a.href;
                if (text.length > 4 && text.length < 200 && !seen[href]) {
                    seen[href] = true;
                    var parent = a.closest('section, div[class*=note], div[class*=card]');
                    var likes = '';
                    var author = '';
                    if (parent) {
                        var likeEl = parent.querySelector('[class*=like], [class*=count]');
                        if (likeEl) likes = likeEl.innerText.trim();
                        var authorEl = parent.querySelector('[class*=author], [class*=name], [class*=nickname]');
                        if (authorEl) author = authorEl.innerText.trim();
                    }
                    notes.push({title: text.substring(0, 100), url: href, likes: likes, author: author});
                }
            }
            return {notes: notes.slice(0, 20), keyword: '""" + keyword + """'};
        })())
    """)

    if "error" in result:
        print(f"搜索失败: {result['error']}")
        return

    notes = result.get("notes", [])
    if not notes:
        print("未找到相关笔记。")
        return

    print(f"\n搜索结果「{keyword}」({len(notes)} 条):\n")
    for i, n in enumerate(notes):
        author_str = f"by {n['author']}" if n.get("author") else ""
        likes_str = f" | ❤️ {n['likes']}" if n.get("likes") else ""
        print(f"  {i+1}. {n['title']} {author_str}{likes_str}")
        print(f"     {n['url'][:80]}")
        print()


def cmd_note(url: str):
    """打开单篇笔记，提取内容。"""
    _human_delay()
    print(f"打开笔记: {url[:80]}...")

    _cdp_request(f"/json/new?{url}", "PUT")
    time.sleep(4)

    result = _cdp_execute("""
        JSON.stringify((function() {
            var title = '';
            var titleEl = document.querySelector('#detail-title, [class*=title], h1');
            if (titleEl) title = titleEl.innerText.trim();

            var body = '';
            var bodyEl = document.querySelector('#detail-desc, [class*=desc], [class*=content], [class*=note-text]');
            if (bodyEl) body = bodyEl.innerText.trim();
            if (!body) body = document.body.innerText.substring(0, 2000);

            var author = '';
            var authorEl = document.querySelector('[class*=author], [class*=name], [class*=nickname]');
            if (authorEl) author = authorEl.innerText.trim();

            var likes = '', collects = '', comments = '';
            var interactEls = document.querySelectorAll('[class*=like], [class*=collect], [class*=comment], [class*=count]');

            var hashtags = [];
            var tagEls = document.querySelectorAll('[class*=tag], [class*=topic], a[href*=\"tag\"]');
            for (var i = 0; i < tagEls.length; i++) {
                var t = tagEls[i].innerText.trim();
                if (t && t.length < 30) hashtags.push(t);
            }

            var images = [];
            var imgs = document.querySelectorAll('img[src*=\"xhscdn\"]');
            for (var i = 0; i < Math.min(imgs.length, 5); i++) {
                images.push(imgs[i].src.substring(0, 100));
            }

            return {
                title: title,
                author: author,
                body: body.substring(0, 2000),
                bodyLen: body.length,
                hashtags: hashtags.slice(0, 10),
                imageCount: images.length
            };
        })())
    """, tab_url_contains="explore")

    if "error" in result:
        print(f"获取失败: {result['error']}")
        return

    print(f"\n笔记内容:\n")
    print(f"  标题: {result.get('title', 'N/A')}")
    print(f"  作者: {result.get('author', 'N/A')}")
    print(f"  话题: {' '.join(result.get('hashtags', []))}")
    print(f"  图片数: {result.get('imageCount', 0)}")
    print(f"  正文长度: {result.get('bodyLen', 0)} 字")
    print(f"\n  正文:\n  {result.get('body', 'N/A')[:1500]}")


def cmd_analyze(url: str):
    """对标拆解一篇笔记：提取标题/正文/话题后，用 Allen 6 维诊断。"""
    _human_delay()
    print(f"对标拆解: {url[:80]}...")

    _cdp_request(f"/json/new?{url}", "PUT")
    time.sleep(4)

    result = _cdp_execute("""
        JSON.stringify((function() {
            var title = '';
            var titleEl = document.querySelector('#detail-title, [class*=title], h1');
            if (titleEl) title = titleEl.innerText.trim();

            var body = '';
            var bodyEl = document.querySelector('#detail-desc, [class*=desc], [class*=content], [class*=note-text]');
            if (bodyEl) body = bodyEl.innerText.trim();
            if (!body) body = document.body.innerText.substring(0, 3000);

            var author = '';
            var authorEl = document.querySelector('[class*=author], [class*=name]');
            if (authorEl) author = authorEl.innerText.trim();

            var hashtags = [];
            var tagEls = document.querySelectorAll('[class*=tag], [class*=topic], a[href*=\"tag\"]');
            for (var i = 0; i < tagEls.length; i++) {
                var t = tagEls[i].innerText.trim();
                if (t && t.length < 30) hashtags.push(t);
            }

            return {
                title: title,
                author: author,
                body: body.substring(0, 2000),
                hashtags: hashtags.slice(0, 10),
                url: window.location.href
            };
        })())
    """, tab_url_contains="explore")

    if "error" in result:
        print(f"获取失败: {result['error']}")
        return

    title = result.get('title', 'N/A')
    body = result.get('body', '')
    hashtags = result.get('hashtags', [])
    author = result.get('author', 'N/A')

    print(f"""
╔══════════════════════════════════════════════════════════╗
║            🔍 对标拆解                                    ║
╚══════════════════════════════════════════════════════════╝

📝 标题: {title}
👤 作者: {author}
🏷️  话题: {' '.join(hashtags) if hashtags else '无'}

📄 正文 (前 1500 字):
{body[:1500]}

──────────────────────────────────────────────────────────
📊 Allen 6 维初步诊断:
──────────────────────────────────────────────────────────""")

    # 快速诊断（规则模式）
    checks = {
        "留白度": ("总分总" not in body and "综上所述" not in body and "首先其次" not in body,
                   "有留白感" if "总分总" not in body else "结构过于封闭"),
        "AI 腔": ("众所周知" not in body and "提升" not in body and "赋能" not in body,
                  "无明显 AI 腔" if "众所周知" not in body else "含 AI 高频词"),
        "教 vs 带": ("你应该" not in body and "你必须" not in body and "划重点" not in body,
                     "在带读者而非教读者" if "你应该" not in body else "有教读者腔"),
        "共鸣度": (len(body) > 100 and ("你" in body or "我" in body),
                   "有人称对话感" if "你" in body else "缺少直接对话"),
        "邀请语": ("?" in body or "你呢" in body or "告诉我" in body,
                   "有互动邀请" if "你呢" in body else "可加强互动邀请"),
        "范本范": ("1）" not in body and "2）" not in body and "第一步" not in body,
                   "是范本展示而非攻略" if "1）" not in body else "疑似攻略型"),
    }

    for dim, (passed, msg) in checks.items():
        icon = "✅" if passed else "⚠️"
        print(f"  {icon} {dim}: {msg}")

    print(f"""
──────────────────────────────────────────────────────────
💡 你能学到的:
  1. 标题结构: {'短句爆发型' if len(title) < 20 else '信息完整型'}
  2. 正文风格: {'对话式' if '你' in body else '陈述式'}
  3. 话题策略: {'精准垂直' if len(hashtags) >= 3 else '话题偏少' if hashtags else '无话题标签'}
  4. 互动设计: {'有埋钩子' if '?' in body or '评论' in body else '未设计互动点'}
""")


def main():
    parser = argparse.ArgumentParser(description="小红书浏览器桥接 — CDP 安全浏览")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("start", help="启动 CDP Chrome + 打开小红书")
    sub.add_parser("stop", help="关闭 CDP Chrome")
    sub.add_parser("status", help="检查连接和登录状态")
    sub.add_parser("explore", help="获取探索页推荐笔记")

    p_search = sub.add_parser("search", help="搜索笔记")
    p_search.add_argument("keyword", help="搜索关键词")

    p_note = sub.add_parser("note", help="打开单篇笔记")
    p_note.add_argument("url", help="笔记 URL")

    p_analyze = sub.add_parser("analyze", help="对标拆解一篇笔记")
    p_analyze.add_argument("url", help="笔记 URL")

    args = parser.parse_args()

    if args.cmd == "start":
        cmd_start()
    elif args.cmd == "stop":
        cmd_stop()
    elif args.cmd == "status":
        cmd_status()
    elif args.cmd == "explore":
        cmd_explore()
    elif args.cmd == "search":
        cmd_search(args.keyword)
    elif args.cmd == "note":
        cmd_note(args.url)
    elif args.cmd == "analyze":
        cmd_analyze(args.url)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
