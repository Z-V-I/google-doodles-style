#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_preview.py — 由 templates/ + doodles-style.css 生成预览页与色板页。

用法：
    python build_preview.py

产出（写在同目录下，双击即可打开）：
    preview-home.html           首页 / 落地页
    preview-doodle-detail.html  详情页
    preview-library.html        检索页 / Library
    palette.html                19 套主题 × 6 档色梯的可视化色板

用途：
  1. 改完 doodles-style.css 后跑一次，肉眼确认三个页面没被改坏；
  2. 当作视觉基线 —— 与镜像站（python serve.py → http://127.0.0.1:8765/）
     并排比对，判断还原度；
  3. palette.html 用来挑主题色，它从 doodles-style.css 里**解析**出颜色，
     所以改了样式表它自动跟着变，不存在第二份数据。

预览页里的图片是内联 SVG 占位、图标是内联 sprite，但**字体是真的** ——
页面会 link 同级的 fonts/fonts.css，双击打开就能看到 Google Sans 的字形。
"""
import re
import pathlib
from urllib.parse import quote

HERE = pathlib.Path(__file__).resolve().parent
TPL = HERE / "templates"
CSS = (HERE / "doodles-style.css").read_text(encoding="utf-8")

PLACEHOLDER = """    <!-- 替换点：把 10-home.html / 20-doodle-detail.html / 30-library.html 的主体贴到这里。
         贴之前剥掉模板最外层的 <div class="main-page"> —— 这里已经有一层了。
         嵌套两层不会有任何视觉差异（这个类在原站 CSS 里没有样式），
         但会让遍历 .main-page 直接子元素的脚本全部落空。 -->"""

# 顺序很重要：外壳里的占位符本身是一段注释，如果先剥注释再替换就会静默失配，
# 结果是页面外壳正常、主体全空（踩过一次）。
STRIP_RE = re.compile(r"<!--(?!\[).*?-->", re.S)


def strip_comments(html: str) -> str:
    return STRIP_RE.sub("", html)


def placeholder_img(label: str, w: int = 400, h: int = 300) -> str:
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">'
        f'<rect width="100%" height="100%" fill="#f1f3f4"/>'
        f'<text x="50%" y="50%" fill="#9aa0a6" font-family="sans-serif" font-size="18" '
        f'text-anchor="middle" dominant-baseline="middle">{label}</text></svg>'
    )
    return "data:image/svg+xml;charset=utf-8," + quote(svg)


_SIMPLE = {
    "google-color-logo": '<rect x="1" y="8" width="22" height="8" rx="4" fill="#4285f4"/>',
    "doodle-logo":       '<rect x="1" y="8" width="22" height="8" rx="4" fill="#4285f4"/>',
    "search":            '<circle cx="10.5" cy="10.5" r="6" fill="none" stroke="#5f6368" stroke-width="2"/>'
                         '<path d="M15 15l5 5" stroke="#5f6368" stroke-width="2"/>',
    "expand-more":       '<path d="M7 10l5 5 5-5" fill="none" stroke="#5f6368" stroke-width="2"/>',
    "menu":              '<path d="M4 7h16M4 12h16M4 17h16" stroke="#5f6368" stroke-width="2"/>',
    "stars":             '<path d="M12 4l2.2 5.3 5.8.5-4.4 3.8 1.3 5.7-4.9-3-4.9 3 1.3-5.7L4 9.8l5.8-.5z" '
                         'fill="#fbbc05"/>',
    "refresh":           '<path d="M20 12a8 8 0 1 1-2.3-5.6" fill="none" stroke="#5f6368" stroke-width="2"/>'
                         '<path d="M20 4v5h-5" fill="none" stroke="#5f6368" stroke-width="2"/>',
    "checkmark":         '<path d="M5 12l4.5 4.5L19 7" fill="none" stroke="currentColor" stroke-width="2.4"/>',
    "close":             '<path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2.2"/>',
    "sparkles":          '<path d="M12 3l1.6 5.4L19 10l-5.4 1.6L12 17l-1.6-5.4L5 10l5.4-1.6z" '
                         'fill="currentColor"/>',
}


def sprite(names) -> str:
    parts = []
    for n in names:
        body = _SIMPLE.get(n)
        if body is None:
            body = ('<path d="M5 12h12M12 6l6 6-6 6" fill="none" stroke="currentColor" '
                    'stroke-width="2"/>' if "arrow" in n
                    else '<rect x="5" y="5" width="14" height="14" rx="3" fill="#dadce0"/>')
        parts.append(f'<symbol id="{n}" viewBox="0 0 24 24">{body}</symbol>')
    return '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">' + "".join(parts) + "</svg>"


GLUE_SPRITE = sprite(["google-color-logo", "menu", "search", "expand-more"])
ICON_SPRITE = sprite([
    "doodle-logo", "right-arrow", "right-arrow-doodles",
    "left-white-arrow-tout-carousel", "right-white-arrow-tout-carousel",
    "stars", "refresh", "checkmark", "close", "sparkles",
])


def unwrap_main_page(body: str) -> str:
    """把模板最外层的 <div class="main-page"> 包裹剥掉。

    外壳（00-shell.html）里已经有一个 .main-page 了，模板自己又带一个的话会
    变成两层嵌套。<div class="main-page"> 在原站 CSS 里没有任何样式，所以肉眼
    完全看不出来，但会让"遍历 .main-page 直接子元素"的脚本全部落空 —— 比如
    只想保留某个 section 做单块截图时，会连主体一起隐藏掉（踩过一次）。
    """
    m = re.search(r'<div class="main-page">', body)
    if not m:
        raise SystemExit("主体模板里找不到 <div class=\"main-page\">")
    body = body[m.end():]
    cut = body.rfind("</div>")
    if cut == -1:
        raise SystemExit("主体模板的 .main-page 没有闭合")
    return body[:cut] + body[cut + 6:]


def build(main_file: str, title: str) -> str:
    shell = (TPL / "00-shell.html").read_text(encoding="utf-8")
    body = (TPL / main_file).read_text(encoding="utf-8")

    body = unwrap_main_page(body)
    body = strip_comments(body)                      # 先剥主体的注释
    if PLACEHOLDER not in shell:
        raise SystemExit("00-shell.html 里的替换点不见了，先确认模板没被改过")
    shell = shell.replace(PLACEHOLDER, body)         # 再替换（此时占位符还在）
    shell = strip_comments(shell)

    # 外链全部内联，保证 file:// 直接打开也完整
    shell = re.sub(r'<link rel="preload"[^>]*>', "", shell)
    # 字体不内联 —— fonts/ 就在同级目录，改成相对路径，file:// 下也能加载，
    # 这样预览页里的 Google Sans 字形是真的（原站 200 个 woff2 子集）。
    shell = shell.replace('href="/fonts/fonts.css"', 'href="fonts/fonts.css"')
    shell = re.sub(r'<link rel="stylesheet" href="/static/doodles-style\.css">',
                   "<style>\n" + CSS + "\n</style>", shell)
    shell = re.sub(r'<link rel="(?:apple-touch-icon-precomposed|icon|shortcut icon|canonical)"[^>]*>',
                   "", shell)
    shell = re.sub(r'<script[^>]*src="[^"]*"[^>]*>\s*</script>', "", shell)
    shell = shell.replace("<body>", "<body>\n" + GLUE_SPRITE + "\n" + ICON_SPRITE)

    def swap_img(m):
        tag = m.group(0)
        if "data:image" in tag:
            return tag
        alt = re.search(r'alt="([^"]*)"', tag)
        src = re.search(r'src="[^"]*"', tag)
        if not src:
            return tag
        return tag.replace(src.group(0), 'src="%s"' % placeholder_img((alt.group(1) if alt else "doodle")[:26]))

    shell = re.sub(r"<img[^>]*>", swap_img, shell)

    # sprite 路径 → 本页内联 symbol 的 id
    shell = re.sub(r'href="/static/glue-icons\.svg#', 'href="#', shell)
    shell = re.sub(r'href="/static/icons\.svg#', 'href="#', shell)
    shell = re.sub(r'xlink:href="/static/[^"#]*#', 'xlink:href="#', shell)

    banner = ('<div style="background:#202124;color:#fff;font:500 13px/1.4 system-ui,sans-serif;'
              "padding:8px 16px;text-align:center\">Google Doodles 风格预览 · " + title +
              " · 图片为 SVG 占位，字体与样式为真实资源 · 19 套主题色见 palette.html</div>")
    shell = shell.replace("<body>", "<body>\n" + banner, 1)
    return shell


# --------------------------------------------------------------------------- #
#  palette.html —— 从 doodles-style.css 解析出主题色，生成可视化色板
# --------------------------------------------------------------------------- #

THEME_RE = re.compile(r"\.theme-([a-z-]+) \.(main|interactive|surface-(\d)) \{([^}]*)\}")

# 展示顺序：按色相环排，冷 → 暖 → 中性，比按字母序好找
THEME_ORDER = ["dark-blue", "blue", "light-blue", "teal", "emerald", "green", "grass",
               "lime", "yellow", "orange", "terracotta", "red", "salmon", "pink",
               "magenta", "purple", "brown", "tan", "gray"]

THEME_NOTE = {
    "blue": "默认安全牌，科技/产品",
    "dark-blue": "浓郁庄重，main 上要白字",
    "light-blue": "清爽天空感",
    "teal": "水感，介于蓝绿",
    "emerald": "沉稳的深绿",
    "green": "鲜明、生机",
    "grass": "草绿，偏跳",
    "lime": "柠檬黄绿，最跳之一",
    "yellow": "Google 黄，欢快/警示",
    "orange": "南瓜橙，活力",
    "terracotta": "陶土，复古暖",
    "red": "醒目，大面积铺会累",
    "salmon": "柔和玫红",
    "pink": "糖果粉，数据集里占比最高",
    "magenta": "荧光品红，赛博感",
    "purple": "紫罗兰，创意/神秘",
    "brown": "皮革，大地",
    "tan": "米卡其，最温和",
    "gray": "纯中性，拿不准时的兜底",
}


def _lum(hexcolor: str) -> float:
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def parse_themes() -> dict:
    data = {}
    for name, kind, idx, decl in THEME_RE.findall(CSS):
        m = re.search(r"background-color:\s*([^;]+)", decl)
        if not m:
            continue
        val = m.group(1).strip()
        d = data.setdefault(name, {"surfaces": {}})
        if kind == "main":
            d["main"] = val
        elif kind == "interactive":
            d["interactive"] = val
        else:
            d["surfaces"]["surface-" + idx] = val
    return data


PALETTE_STYLE = """
:root{--ink:#000;--line:#000;--muted:#4a4a4a;--bg:#fff;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:'Google Sans Text','Google Sans',Roboto,Arial,sans-serif;}
h1,h2{font-family:'Google Sans Display','Google Sans',Arial,sans-serif;font-weight:400;margin:0}
header{padding:48px 28px 24px;max-width:1400px;margin:0 auto;
  border-bottom:1px solid var(--line)}
header p{margin:12px 0 0;color:var(--muted);max-width:62ch;line-height:1.55}
header code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.9em;
  background:#f1f3f4;padding:1px 5px;border-radius:4px}
main{max-width:1400px;margin:0 auto;padding:28px}
.tip{border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin-bottom:32px;
  background:#fff;line-height:1.6}
.tip b{font-weight:500}
.grid{display:grid;gap:24px;grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}
.card{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff}
.card>h2{font-size:20px;padding:14px 16px;border-bottom:1px solid var(--line);
  display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.card>h2 span{font-family:'Google Sans Text',sans-serif;font-size:12px;color:var(--muted);
  font-weight:400;text-align:right;line-height:1.3}
.bar{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;
  border-bottom:1px solid var(--line);font-family:'Google Sans',Arial,sans-serif;
  font-size:14px;font-weight:500}
.bar em{font-style:normal;font-size:11px;font-weight:400;opacity:.72;
  font-family:ui-monospace,Menlo,Consolas,monospace}
.steps{display:flex;border-bottom:1px solid var(--line)}
.step{flex:1;height:56px;display:flex;align-items:flex-end;justify-content:center;
  padding-bottom:4px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:9px;
  color:rgba(0,0,0,.55)}
.step.s5{color:rgba(255,255,255,.75)}
.legend{padding:10px 16px;font-size:11.5px;color:var(--muted);line-height:1.5;
  font-family:'Google Sans Text',sans-serif}
footer{max-width:1400px;margin:0 auto;padding:28px;color:var(--muted);font-size:13px;
  border-top:1px solid var(--line)}
"""


def build_palette() -> str:
    themes = parse_themes()
    cards = []
    for name in THEME_ORDER:
        d = themes.get(name)
        if not d:
            continue
        main = d.get("main", "#000")
        inter = d.get("interactive", "#000")
        s = d["surfaces"]

        # main 上该用黑字还是白字：取对比度高的那侧（实测，不是猜的）
        ink_on_main = "#000" if contrast(main, "#000") >= contrast(main, "#fff") else "#fff"
        ink_on_inter = "#000" if contrast(inter, "#000") >= contrast(inter, "#fff") else "#fff"

        steps = []
        for i in range(1, 6):
            c = s.get("surface-%d" % i)
            if c is None:
                steps.append('<div class="step" style="background:repeating-linear-gradient'
                             '(45deg,#fff 0 6px,#e8eaed 6px 12px);color:#5f6368">—</div>')
            else:
                cls = "step s5" if i == 5 else "step"
                steps.append('<div class="%s" style="background:%s">%d</div>' % (cls, c, i))

        cards.append(
            '<article class="card">'
            '<h2>%s<span>%s</span></h2>'
            '<div class="bar" style="background:%s;color:%s">main<em>%s</em></div>'
            '<div class="bar" style="background:%s;color:%s">interactive<em>%s</em></div>'
            '<div class="steps">%s</div>'
            '<p class="legend">surface-1 → 5：%s</p>'
            '</article>'
            % (name, THEME_NOTE.get(name, ""),
               main, ink_on_main, main,
               inter, ink_on_inter, inter,
               "".join(steps),
               " · ".join(s.get("surface-%d" % i, "—") for i in range(1, 6))))

    return (
        '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>Google Doodles 配色板 · 19 套主题</title>\n'
        '<link rel="stylesheet" href="fonts/fonts.css">\n'
        '<style>' + PALETTE_STYLE + '</style>\n</head>\n<body>\n'
        '<header>\n'
        '  <h1>Google Doodles 配色板</h1>\n'
        '  <p>19 套主题，每套自带一条 6 档色梯：<code>main</code> 大面积铺底，'
        '<code>interactive</code> 给按钮和 chip，<code>surface-1..5</code> 由浅到深做层次。'
        '数值逐条解析自原站 <code>index.min.css</code>，本页由 <code>build_preview.py</code> '
        '从 <code>doodles-style.css</code> 直接生成，改了样式表会自动同步。</p>\n'
        '</header>\n'
        '<main>\n'
        '  <div class="tip">色块里的文字颜色是<b>按 WCAG 对比度实测选的</b>，不是凭感觉：'
        '19 套主题的 <code>main</code> 里，18 套都是黑字对比度更高 —— 所以 Doodles 是'
        '「彩底 + 黑字 + 黑描边」，不是 Material 那种「彩底 + 白字」。'
        '唯一例外是 <code>dark-blue</code>。带 <code>—</code> 的格子表示原站没定义这一档，'
        '会落到全局默认（= theme-blue 的梯）。</div>\n'
        '  <div class="grid">\n' + "\n".join(cards) + '\n  </div>\n</main>\n'
        '<footer>切换方式：把区块根元素上的 <code>theme-&lt;color&gt;</code> 换掉即可，'
        '同时确认内部用的是 <code>.main</code> / <code>.interactive</code> / '
        '<code>.surface-N</code> 钩子类。完整选色法则见 references/palette.md。</footer>\n'
        '</body>\n</html>\n'
    )


VARIANTS = [
    ("10-home.html", "首页 / 落地页", "preview-home.html"),
    ("20-doodle-detail.html", "详情页", "preview-doodle-detail.html"),
    ("30-library.html", "检索页 / Library", "preview-library.html"),
]

if __name__ == "__main__":
    for main_file, title, out in VARIANTS:
        html = build(main_file, title)
        (HERE / out).write_text(html, encoding="utf-8")
        start = html.find('class="main-page">')
        print(f"{out:28} {len(html):>7} B   主体长度 {len(html) - start}")

    pal = build_palette()
    (HERE / "palette.html").write_text(pal, encoding="utf-8")
    n = len(parse_themes())
    print(f"{'palette.html':28} {len(pal):>7} B   {n} 套主题")
    print("完成。双击打开任一预览页即可。")
