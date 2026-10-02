# 原站真实资源：已在 skill 里，以及还要更多时去哪儿取

## 0. 本仓库带了什么、没带什么

### 0.1 随仓库提供

| 资源 | 位置 | 体量 |
| --- | --- | --- |
| Google Sans 全字重（`fonts.css` + 200 个 woff2 语言子集） | `assets/fonts/` | 4.8 MB |
| **原站主样式表本体**（4020 条规则） | `assets/vendor/glue.min.css` | 548 KB |
| Doodle 品牌字标、多色主题标记 | `assets/vendor/logo-doodle-color.svg`、`multicolor.svg` | 32 KB |

**A 档（默认）与 B 档（像素级）都不需要下载任何东西** —— 区别只是 `<link>` 指向
自带的 `doodles-style.css`，还是指向 `vendor/glue.min.css`。**字体两档共用同一份**，
所以 A 档的字形也是真实的 Google Sans，不是 Arial 回退。

> **中文页面注意**：这 200 个 woff2 里**一个 CJK 字形都没有**（26 种
> `unicode-range` 全是拉丁 / 希腊 / 西里尔 / 南亚），中文字符必然落到回退链，
> 跟内联了多少 woff2 无关 —— 见 `design-tokens.md` §5.1。

### 0.2 刻意未提供：两个图标 sprite

| 资源 | 体量 | 为什么没带 |
| --- | --- | --- |
| `glue-icons.svg`（通用图标，44 个 id） | 16 KB | Google 图标资产，单独排除 |
| `icons.svg`（Doodles 专用，34 个 id） | 148 KB | 同上 |

**影响范围**：模板与预览页里的 `<use href="/static/glue-icons.svg#search">`
这类引用会取不到图标 —— **不报错、不提示，只是位置空一块**。
布局、配色、字体、动效都不受影响。

**补齐（一条命令）：**

```bash
python assets/fetch-icons.py
```

脚本从上游镜像仓库下载这两个文件、解压、**校验 sha256 后**写进 `assets/vendor/`。
校验值必须与下表一致，不一致说明上游改过，脚本会拒绝写入而不留半成品：

| 文件 | 大小 | sha256 |
| --- | --- | --- |
| `glue-icons.svg` | 15,738 B | `5a3c1c892187f493e32b51a241a4069520147e0294062a5ac67f930774d8cba5` |
| `icons.svg` | 149,861 B | `37ae077da8a25b6950c926233ed752617048c50792204bc7b9d6332bbb7a3a5f` |

> 镜像站上这两个文件的哈希名就是 **`icons.svg` 自己的 sha256**
> （`37ae077d…`），可以直接当完整性凭据用。

下面记的是这些文件的**原始出处**，以及要更多资源（运行时 JS、涂鸦原图、
互动涂鸦）时该去哪儿取。

---

## 1. 原始出处

| | |
| --- | --- |
| **GitHub 仓库** | <https://github.com/Z-V-I/google-doodles-mirror> （默认分支 `main`，MIT） |
| **在线镜像** | <https://google.zvi.onl> |
| **图片包** | 123 云盘免登录：<https://1812063966.share.123pan.cn/123pan/kD4rVv-k4NcA> |

仓库**只开源代码与页面**（6,503 个文件 / 156 MB），**不含 1.73 GB 涂鸦原图**
（GitHub 单文件上限 100 MiB，仓库建议 1 GB 以内）。

---

## 2. 一条命令跑起来（推荐先做这一步）

```bash
git clone https://github.com/Z-V-I/google-doodles-mirror
cd google-doodles-mirror
python serve.py
# → http://127.0.0.1:8765/
```

`serve.py` 只用标准库，无需第三方包。它额外做了三件事：

1. 复刻原站检索接口 `/live/api/v1/doodles`（原站前端从 Google Cloud 取数据，离线必然失败）。
2. 订阅源按请求头里的真实 Host 改写绝对地址（换端口也不会拿到错地址）。
3. `/rss/images.zip` 服务端用 chunked 编码**边打边发**（1.7 GB 不可能预先落盘）。

全过程**不发起任何外部网络请求**。

---

## 3. 资源清单与原始出处

**✅ 标记的已经随 skill 提供**（见 §0）；没标的需要时从镜像仓库 `site/` 取。
括号里是原文件名 —— 名字那串 sha256 是构建产物哈希，**可以随意重命名**
（只要同步改引用），但内容必须原样。

### 3.1 决定外观的（除两个 sprite 外都已提供 ✅）

| 用途 | 原文件名 | 大小 | 本仓库内 |
| --- | --- | --- | --- |
| **主样式表** | `static/f90e535b…ac.index.min.css` | 548 KB | ✅ `vendor/glue.min.css` |
| **字体声明** | `fonts/fonts.css` | — | ✅ `fonts/fonts.css` |
| **字体本体** | `fonts/*.woff2`（**200 个**） | 4.8 MB | ✅ `fonts/` |
| **图标 sprite（通用）** | `static/0f99e028…87d7.glue-icons.svg` | 16 KB | ⚠️ 见 §0.2 |
| **图标 sprite（Doodles 专用）** | `static/37ae077d…3a5f.icons.svg` | 148 KB | ⚠️ 见 §0.2 |

> `fonts.css` 用 `@font-face` + `unicode-range` 把 Google Sans / Google Sans Text
> 切成 200 个按语言子集拆分的 woff2。**这 200 个文件是一个整体**，
> 少一个只会让对应语系的字形回退，不报错 —— 排查时容易忽略。
> skill 已完整收录，不用自己拼。

### 3.2 建议一并拿走（要动态效果时才需要）

| 用途 | 原文件名 | 大小 | skill 内 |
| --- | --- | --- | --- |
| 运行时 JS（轮播、折叠面板、抽屉） | `static/9d6cae2b…48.index.min.js` | 228 KB | — |
| Doodle 品牌字标（可换色的 SVG） | `static/06f691de…69.logo-doodle-color.svg` | 32 KB | ✅ `vendor/` |
| 空结果插画 | `static/a1162262…62.not-found.svg` | 4 KB | — |
| 加载动画 | `static/71a12b05…6e.loading.gif` | — | — |
| 页眉点阵/纹理背景 | `static/background.png` | — | — |
| 多色主题标记 | `static/74a8cb76…27.multicolor.svg` | 4 KB | ✅ `vendor/` |
| 社交分享封面 | `static/og-image.png` | — | — |
| favicon 四件套 | `static/favicon-{16,32,64,192}.png` | — | — |
| 品牌 favicon（渐变 G） | `assets/brand/branding/googleg_gradient/{1x,2x}/*.png` | — | — |
| Cookie 通知条 | `vendor/glue/cookienotificationbar/*` | — | — |

### 3.3 运行时依赖（跑互动涂鸦才需要）

`vendor/` 目录下是**被改造过的第三方库**，若你的页面用到对应能力再取：

```
vendor/charts/          Google Charts 全套（11 个文件 / 1.24 MB）
vendor/pixi_v5.min.js   PixiJS 5（374 KB）
vendor/pixi_old.min.js  PixiJS 旧版（437 KB）
vendor/createjs-1.0.0.min.js  CreateJS（242 KB）
vendor/cannon.min.js    物理引擎（132 KB）
vendor/MidiConvert.js   音频
vendor/firebase-*.js    Firebase（旧互动涂鸦会引）
```

以及一批**桩件**（把谷歌在线服务换成空实现，避免发起外部请求）：
`gtm-stub.js`、`recaptcha-stub.js`、`youtube-api.js`、`google-ads-stub.js`、
`glue-cookienotificationbar.js`、`google-charts-loader.js`。

---

## 4. 切换到 B 档（像素级）的三个动作

**除两个图标 sprite 外，文件都在仓库里，不需要下载**（sprite 补法见 §0.2）。
只是把引用从自包含样式换成原站本体：

1. **改 `<head>` 里的样式引用**
   把 `doodles-style.css` 换成 `vendor/glue.min.css`：

   ```html
   <link rel="preload" href="fonts/fonts.css" as="style">
   <link rel="stylesheet" href="fonts/fonts.css">
   <link rel="stylesheet" href="vendor/glue.min.css">
   ```

   顺序不能反。**换了就把自带的 `doodles-style.css` 删掉** ——
   两者有大量同名规则，叠加会互相覆盖，产生难以定位的样式错乱。

2. **sprite 路径要对上**
   原站 HTML 里引用的是哈希文件名：

   ```html
   <use href="/static/0f99e02819f0bba398fbcbeff94c8a0eb698e988148884f15cb92c39c17487d7.glue-icons.svg#search"></use>
   ```

   本仓库的模板里简写成了 `/static/glue-icons.svg#search` 和 `/static/icons.svg#…`，
   而 `fetch-icons.py` 落到 `vendor/` 的正是这个简写名。二选一：
   把引用改成上面那种哈希名，或把 `vendor/` 里的文件重命名成哈希名。
   **别两边都不动。**

3. **图标 id 必须真实存在**

   ```bash
   grep -o 'id="[^"]*"' assets/vendor/glue-icons.svg | sort -u
   ```

   写错的 id **不会报错也不会有任何提示**，只是图标位置空一块。

---

## 5. 图片素材

6,392 张涂鸦原图（1.73 GB）不在仓库里。三种取法：

### 5.1 直接跑镜像（最省事）

`serve.py` 起来后，图片按原站路径可直接访问：
`/img/<slug>.jpg`、`/img/<slug>.gif`、`/img/<slug>.png`。

> 仓库 clone 下来时 `site/img/` 是空的，**图片位置会是空的**是预期行为。

### 5.2 打包下载

- **123 云盘（免登录）**：<https://1812063966.share.123pan.cn/123pan/kD4rVv-k4NcA>
- **SHA-256**：`64cd53407dcd75b49b58b47e5179dde22515d4d9d69a15082a305f4e0927d99a`
- 包内：`images/`（6392 张）+ `manifest.csv` + `manifest.json` + `README.txt`

解压后把 `images/` 里的文件放进 `site/img/`。**1.7 GB 的文件在网络往返里出错的概率不低，
下载完建议核对一次 SHA-256。**

### 5.3 逐张取（只要少量图时）

订阅源里每条都带 `<enclosure>`，那就是图片本体的直接地址：

```
/rss.xml              全量 6,375 条
/rss/latest.xml       最新 100 条
/rss/doodles.csv      元数据导出（标题/日期/年份/主色/话题/格式/地区/图片/详情页/介绍）
/rss/doodles.json     同上，JSON 格式
```

### 5.4 其余素材（字体/原站 CSS+JS/互动涂鸦/故事书/CMS 图，约 400 MB）

按站内路径从镜像站直接取，例如 `https://google.zvi.onl/fonts/…`、`/games/…`。

---

## 6. 数据集格式

生成列表页/详情页需要涂鸦元数据。仓库根目录有两份等价数据：

**`doodles_data.js`**（2.8 MB，浏览器可直接 `<script>` 引入）：

```js
window.DOODLES = [{
  "slug": "100th-anniversary-of-flight",
  "title": "100th Anniversary of Flight",
  "date": "December 17, 2003",
  "description": "Learn more about the creation of … Doodle and discover the story behind the unique artwork.",
  "regions": [],
  "image_file": "100th-anniversary-of-flight.jpg",
  "url": "https://doodles.google/doodle/100th-anniversary-of-flight/",
  "color": "red",
  "topics": ["Other"],
  "format": "still",
  "dateISO": "2003-12-17"
}, …];
```

**`涂鸦目录.csv`**（1.7 MB，带 BOM）：

```
序号,标题,日期,描述,主色,话题,格式,本地图片,页面链接
```

字段与页面元素的对应关系：

| 数据字段 | 映射到 |
| --- | --- |
| `color` | 区块的主题色。**数据只有 11 种取值，theme 有 19 套**，中间要过一层映射表 —— 见 `palette.md` §5，直接拼 `theme-<color>` 会漏掉 `cyan` / `grey` / `white` / `black` 这四种 |
| `format` | `form_tags` 筛选项（`still` / `animated` / …） |
| `topics` | `topic_tags` 筛选项 + 详情页 chips |
| `regions` | `nationality_tags` 筛选项 |
| `image_file` | → `/img/<image_file>` |
| `slug` | → `/doodle/<slug>/` |

`color` 的完整分布（6375 条）：`pink` 2273 · `blue` 1887 · `red` 796 · `green` 740 ·
`cyan` 413 · `orange` 69 · `grey` 66 · `yellow` 44 · `white` 43 · `purple` 40 · `black` 4。

---

## 7. 仓库的路由形状（照抄可得到正确的 URL 结构）

```
/                        首页（当日/精选涂鸦轮播）
/search/                 检索页（关键词/主题/颜色/形态/年份筛选 + 分页）
/about/                  关于页（涂鸦历史时间轴，含图表）
/doodle/<slug>/          详情页 ×6,375
/games/…  /storybooks/   互动涂鸦 163 个 + 故事书 22 个
/rss/  /rss.xml          订阅模式页 + 全量订阅源
/live/api/v1/doodles     数据接口
```

---

## 8. 授权提醒

- **仓库自身的代码与文档是 MIT**（`LICENSE`），与上游 `google-doodles-mirror` 一致。
- **Google Sans / Product Sans 字体、Google logo、原站主样式表、图标 sprite、
  Doodles 涂鸦图片，都是 Google 资产，MIT 不覆盖它们。**

  本仓库**有意只带了字体与主样式表**（为了让复刻够像、且离线可用），
  **两个图标 sprite 已单独排除**（见 §0.2），脚本按需从上游镜像取。

  自用与研究没问题；**商业分发、或对授权敏感的场景，删掉
  `assets/fonts/` 与 `assets/vendor/` 即可** —— A 档的 `doodles-style.css`
  不依赖它们（字体只是回退到 Arial，布局与配色完全不受影响）。

- 本仓库是**风格规格的整理**，与 Google 无任何关联，未获 Google 授权或背书。
