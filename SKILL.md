---
name: google-doodles-style
description: 复刻 Google Doodles（doodles.google）网页风格与页面结构——Google Glue 设计系统令牌、19 套主题色的完整六档色梯与配色法则（含对比度实测）、页眉/页脚/轮播/卡片/详情页骨架、检索页筛选面板。自带原站构建产物 CSS 与 Google Sans 全字重字体（200 个 woff2 子集），可完全离线。当用户要求「做成谷歌涂鸦那种风格」「复刻 Google 风格页面」「仿 Google Doodles 的网页」「用 Glue 设计系统写页面」「照这个 Google 页面做一版」「配色要像谷歌」时使用。关键词：Google Doodles、doodles.google、Google Glue、Google Sans、复刻 Google 页面、谷歌风格网页、谷歌配色、涂鸦全集、google-doodles-mirror。
agent_created: true
---

# Google Doodles 网页风格复刻

把 doodles.google 的视觉语言与页面结构，一比一搬到用户自己的页面上。

规格来源是真实抓取：上游开源镜像仓库
<https://github.com/Z-V-I/google-doodles-mirror>（MIT）。
里面的 CSS / DOM / 令牌全部来自原站构建产物，不是凭印象仿的 ——
**并且这些构建产物已经打包在本 skill 的 `assets/` 里，不需要联网也不需要那个仓库。**

---

## 先问自己一个问题：要哪一档还原度

| 档位 | 做法 | 还原度 | 依赖 |
| --- | --- | --- | --- |
| **A · 自包含**（默认） | `assets/doodles-style.css` + 模板 + `assets/fonts/` | 布局 / 配色 / 尺寸 / 字体全到位；差原站 JS 驱动的动效 | 零依赖，完全离线 |
| **B · 像素级** | 换成 `assets/vendor/glue.min.css`（原站构建产物本体） | 逐像素一致 | 无（文件已随 skill 提供） |

**A 档和 B 档的资源都在 skill 里了**，区别只是「用重写的自包含样式」还是「用原站那份 548 KB 的 min.css」。

A 档的数值是**逐条从原站 CSS 解析出来的**（不是目测），断点、尺寸、颜色、层叠关系
都与原站一致；字体也是原站那 200 个 Google Sans woff2 子集。肉眼能看出差别的只剩：

- **动效** —— 拼贴切换、卡堆翻页、展开面板的过渡由原站 JS 驱动，A 档只给了静态降级。

所以：**要"看着就是谷歌那个网站"，A 档就够，而且是默认选项；要"逐像素一致"，走 B 档。**

两档**不要混用** —— 原站 CSS 与自带 CSS 有大量同名规则，叠加会互相覆盖。
换档的方式是换 `<link>`，不是两个都链。

---

## 工作流

### 第 1 步 · 读规格（必做，不要跳过）

按需要读，不要一次全读：

- **颜色 / 字体 / 布局数值** → `references/design-tokens.md`
- **配色怎么选、哪个主题配什么内容、文字用什么颜色** → `references/palette.md`（**做任何带颜色决策的页面前都读它**）
- **要写哪个组件** → `references/components.md`
- **要换成原站真实资源 / 想知道资源从哪来** → `references/real-assets.md`

### 第 2 步 · 复制骨架

`assets/templates/00-shell.html` 是**所有路由页共用的外壳**：
`<head>`（含完整 SEO/OG 元信息组）+ `<header>`（移动端/桌面端两条 bar）+ 
`<footer>` + `<div id="content">` + 脚本位。

复制它，然后按页面类型把主体内容换成：

| 页面类型 | 主体模板 |
| --- | --- |
| 首页 / 落地页 | `assets/templates/10-home.html` |
| 详情页 / 单品页 | `assets/templates/20-doodle-detail.html` |
| 检索页 / 列表页 | `assets/templates/30-library.html` |

模板里的 class 名与 DOM 层级是**原站原样**，`references/components.md` 记录了
每处为什么这么写。**照抄结构，不要"优化"** —— 替换成 `<div>`+自定义类名会让
样式全部失效，因为原站 CSS 的选择器是严格绑死这套类名的。

> **贴之前先剥掉模板最外层的 `<div class="main-page">`。**
> 外壳里已经有一层了，直接贴会变成两层嵌套。这个类在原站 CSS 里
> **没有任何样式**，所以肉眼完全看不出来 —— 但任何"遍历 `.main-page` 直接子元素"
> 的脚本都会全部落空（例如只想显示某个 `section-*` 做单块预览时会连主体一起隐藏）。
> `build_preview.py` 里的 `unwrap_main_page()` 做的就是这件事。

### 第 3 步 · 把内容填成用户的

只改**文字、图片路径、链接、主题色**。结构与类名保持不动。

主题色从 **19 套**里挑一个，加在区块根元素上：`class="doodle-module theme-pink"`。
板块的 id 按 `section-1`、`section-2` … 顺序排。

选色不是随手挑 —— 三条要点（详见 `references/palette.md`）：

- 有涂鸦图/主视觉时，**主题跟着图的主色走**，不要图是暖色却套 `theme-blue`。
- **换主题要连 `surface-*` 一起换**：每套主题自带 5 档 surface，
  `theme-pink` 的 `surface-1` 是淡粉 `#f7edf2`，不是淡蓝。
- **彩色区块里用黑字**：19 套主题的 `main` 上，18 套都是黑字对比度更高
  （只有 `dark-blue` 例外）。这是 Doodles 与 Material 观感分家的地方。

### 第 4 步 · （可选）升级到像素级

用户要"完全一致"时，把 `<link>` 换成原站构建产物 —— **文件已在 skill 里，
不需要任何下载**：

1. `assets/vendor/glue.min.css` —— 原站那份 548 KB / 4020 条规则的样式表本体。
2. `assets/fonts/fonts.css` + 200 个 woff2 —— 直接复用（A 档也用同一套）。
3. `assets/vendor/glue-icons.svg` / `icons.svg` —— 原站两个 sprite。
   ⚠️ **这两个文件没有随本仓库提供**（Google 图标资产，单独排除）。
   一条命令补齐：`python assets/fetch-icons.py` —— 见 `references/real-assets.md` §0.2。
   补齐后，模板里的 `<use>` 指向简写 id（`/static/glue-icons.svg#search`），
   要么让文件名对上，要么把引用改成哈希名。**二选一，别两边都不动。**
4. 图片按 `/img/<slug>.jpg|gif|png` 放；缺图的取法见 `references/real-assets.md`。

**切换时必须删掉 `doodles-style.css` 那一行 `<link>`** —— 两个都链会互相覆盖。

### 第 5 步 · 看效果

**先看预览**（双击即可打开，用来确认模板和样式没被改坏）：

```
assets/preview-home.html            首页
assets/preview-doodle-detail.html   详情页
assets/preview-library.html         检索页
assets/palette.html                 19 套主题色 + 各自 6 档色梯的可视化色板
```

预览页把样式与图标都内联在文件里、图片是 SVG 占位，但**字体走 `assets/fonts/`**，
所以 Google Sans 的字形是真实的。改过 `doodles-style.css` 或模板后，
跑一次 `python assets/build_preview.py` 重新生成。

改配色时先开 `palette.html` 对着挑 —— 比在表格里读十六进制值快得多。

**再看真实页面**：

```bash
python -m http.server 8000
```

要跟原站并排比对时，把镜像站也跑起来：

```bash
cd /path/to/google-doodles-mirror && python serve.py   # → http://127.0.0.1:8765/
```

镜像站用的是原站 CSS + 真实字体 + 真实涂鸦图，那是还原度的天花板，
拿它当基准逐块对照，比凭记忆调整可靠得多。

---

## 不可妥协的 9 条风格规则

这 9 条是"像不像"的分水岭。丢掉任何一条都会立刻变成"某个普通网页"。

1. **描边是纯黑，不是灰色。**
   卡片外框、标题下划线、区块分隔线全是 `border: 1px solid #000`。
   改成 `#dadce0` 就丢了这一版最标志性的"粗黑描边 + 色块"感。

2. **内容硬上限 1296px，两侧用色块铺满。**
   不要用 `100vw` + 负 margin 硬凑。正确做法是三柱子：
   `.background-padding` + `.glue-page.no-margin` + `.background-padding`，
   其中 `flex: 1 1 calc(50% - 648px)`（648 = 1296/2）。两侧柱子的颜色类
   必须与中间一致，否则色带会断。

3. **字体分工固定，不能混用。**
   `Google Sans Display` 只给大标题，`Google Sans` 给组件/按钮/卡片，
   `Google Sans Text` 给正文。三个变体字面不同，混用会"看着有点像但就是不对"。

4. **断点只有 600 / 1024 / 1440。**
   原站没有 768px 断点。别引入别处抄来的断点值。

5. **`theme-*` 只是钩子，不带样式。**
   必须写 `.theme-pink .main { … }` 这种组合选择器才生效；
   光加 `class="theme-pink"` 什么都不会发生。一套主题共有 **21 个钩子**：
   6 个主题色（`.main` / `.interactive` 各带 `-outline`、`-fill-svg`）
   + 5 档 `surface-N`（各带 `-outline`、`-fill-svg`）。

6. **配色是一整条色梯，不是一个主色。**
   每套主题自带 `main` / `interactive` / `surface-1..5` 六档。
   换主题时要连 surface 一起换 —— 用 `theme-pink` 却留着淡蓝 `surface-1`，
   页面会像两种颜色打架。完整的 19 套色值与选色建议见 `references/palette.md`。

7. **彩色区块里用黑字，不是白字。**
   19 套主题的 `main` 上，18 套都是黑字对比度更高（`dark-blue` 是唯一例外，
   它的 `main` 深到该用白字）。`interactive` 上则多数用白字，但
   `grass` / `lime` / `magenta` / `orange` / `yellow` 这 5 套仍要用黑字。
   拿不准就取 `#000` —— 这是 Doodles 与 Material 观感分家的地方。

8. **图标全部走 SVG sprite `<use>`。**
   不用图标字体、不内联 `<path>`。写错的 id **不报错也不提示**，
   只是位置空一块 —— 拿不准就去 sprite 里 `grep 'id="'` 确认。
   这两个 sprite 未随仓库提供，先跑一次 `python assets/fetch-icons.py` 补齐
   （见 `references/real-assets.md` §0.2）。

9. **卡片 hover 是三件事同时发生**：`scale(1.01)` + 双层阴影 +
   `transition: all .3s ease-in-out`（原站用的就是 `all` + `ease-in-out`，
   不是 `cubic-bezier`）。只做放大或只加阴影都会显得"差一口气"。

---

## 文件地图

```
google-doodles-style/
├── SKILL.md                          入口（本文件）
├── references/
│   ├── design-tokens.md              令牌：灰阶/色阶/字体/排版/布局/阴影 全部实测值
│   ├── palette.md                    ★ 配色：19 套主题的六档色梯 + 选色法则 + 对比度实测
│   ├── components.md                 每个组件的 DOM 结构 + 类名 + 坑
│   └── real-assets.md                原站资源清单、授权边界与替换步骤
└── assets/
    ├── doodles-style.css             A 档自包含样式表
    ├── palette.html                  色板可视化页：19 套主题 × 6 档，开箱即看
    ├── build_preview.py              由 templates + css 重新生成预览页
    ├── fetch-icons.py                补齐两个图标 sprite（未随仓库提供，跑一次即可）
    ├── preview-home.html             预览：首页
    ├── preview-doodle-detail.html    预览：详情页
    ├── preview-library.html          预览：检索页
    ├── fonts/                        原站 Google Sans 字体：fonts.css + 200 个 woff2
    ├── vendor/                       B 档原站构建产物：glue.min.css + logo（图标 sprite 见 fetch-icons.py）
    └── templates/
        ├── 00-shell.html             页面外壳（head + 页眉 + 页脚）
        ├── 10-home.html              首页主体
        ├── 20-doodle-detail.html     详情页主体
        └── 30-library.html           检索页主体
```

规模参考：A 档样式表 2254 行 / 968 条规则 / 89 个媒体查询 / 约 95 KB；
B 档原站 CSS 548 KB；字体 4.8 MB。**总计约 6.0 MB，全部离线可用**
（不含两个图标 sprite —— 补齐后约 6.2 MB，见 `references/real-assets.md` §0.2）。

---

## 写新页面时的检查清单

- [ ] 用了 `00-shell.html` 的外壳，没漏掉 `<main id="content">`
- [ ] 全页只有一个 `.main-page`（模板最外层那层要剥掉，否则是两层嵌套）
- [ ] 区块 id 按 `section-1`、`section-2` … 单调递增
- [ ] 每个内容区块都带 `doodle-module` 和 `theme-<color>`
- [ ] 需要色块的地方写了 `.main` / `.main-outline` / `.interactive`（不是只加 theme 类）
- [ ] **`theme-*` 与 `surface-N` / `.main` 不在同一个元素上**（要包一层，同元素不匹配会静默落到全局淡蓝梯）
- [ ] **全页只有一个主题**，且色相和主视觉一致
- [ ] **换了主题的地方，`surface-*` 也跟着换了**（不是留着默认的淡蓝）
- [ ] **彩色底上放的是黑字**（`dark-blue` 等少数例外见 `palette.md` §4）
- [ ] 承载底色的那一层自己带 `padding`（不是给外层 `doodle-module`），否则区块间露白缝
- [ ] 两根 `.background-padding` 的颜色类与中间一致
- [ ] 用了三柱子的区块，样式表里有 `@media (min-width:1440px){ .background-padding{display:block} }`
- [ ] 所有图标是 SVG sprite `<use>`，且 id 在 sprite 里**真实存在**（见 `components.md` §8.2 —— 写错不报错，只是空一块）
- [ ] 卡片是「wrapper + link + card + img + content」五件套
- [ ] **卡片里要放正文（不是三五个字的标题）时，`.cards-stack-grid` 的列数和
      `.doodle-card-content` 的内边距一起改了** —— 1024 断点这两条会同时跳，
      不改的话正文可用宽度只剩 130px（见 `components.md` §4.3）
- [ ] 插画若是 `src="data:image/svg+xml,…"` 内联的，里面**没有 `<text>`**
      —— `<img>` 里的 SVG 是独立文档，取不到内联的 Google Sans
      （见 `components.md` §8.3）
- [ ] **中文页面**：页脚版权行覆盖了 `.glue-footer__copyright{flex-shrink:1;min-width:0}`
      —— 原站那行是 `flex:1 0 auto`，长中文会顶出横向滚动条（见 `components.md` §2）
- [ ] 图片都带 `loading="lazy"` 和描述性 `alt`
- [ ] 只用了 600 / 1024 / 1440 三个断点
- [ ] 页面链的是 `fonts/fonts.css` **在前**、主样式表在后
- [ ] **中文页面**：字体栈里补了 CJK 回退（原站那套 `Noto Sans SC` 在 Windows/macOS 上通常没装）

---

## 常见误判

- **"配色抄 Google 四色就够了"** —— 不够。真正决定观感的是那 19 套
  `theme-*` 涂鸦主题色，**尤其是每套自带的 5 档 surface 色梯**，
  以及大量使用纯黑描边 + 色块拼接的构图，不是 logo 那四个颜色。
  只想抄四个颜色、底色统一用灰，做出来会像"普通企业站"。

- **"surface 是一套固定色"** —— 不是。`surface-1..5` 会随 `theme-*` 变，
  只有不在任何主题里时才落到全局兜底（取值 = `theme-blue` 那条梯）。
  这条曾经在本 skill 里写错过一次，见 `palette.md` §0 与 §7。

- **"字体里带了 Google Sans，中文也会用上"** —— 不会。Google Sans 系列
  **一个 CJK 字形都没有**（`fonts.css` 的 26 种 `unicode-range` 里没有中日韩），
  中文字符必然落到回退链。中文页面的观感完全由回退链决定，
  跟内联了多少 woff2 无关 —— 见 `design-tokens.md` §5.1。

- **"原站 sprite 直接内联就行"** —— 不行。原站写的是 `<defs><svg id="x">`，
  内联进 HTML 后 `<use>` 不按 `viewBox` 缩放，图标会忽然变大或错位。
  必须先转成 `<symbol>` —— 见 `components.md` §8.1。

- **"`glue-` 前缀的类都可以随便用"** —— 不行。Glue 是 Google 内部设计系统，
  它的 CSS 是**按需构建**的：只有原站页面真实用到的规则才在那 548 KB 里。
  想用没见过的 `glue-*` 类，先去 `assets/vendor/glue.min.css` 里 grep 确认它存在。

- **"页脚照原站抄"** —— 原站页脚含指向谷歌在线服务的入口和社交图标组，
  镜像版已按需求整块删除并换掉版权行。要复刻镜像版的页脚，用模板里的那版。

- **提到配色时注意**：Google 品牌色里的绿是 `#34a853`、红是 `#ea4335`，
  这套是 Google 自己的品牌规范，与中文股票涨跌色约定无关，不要套用红涨绿跌。
