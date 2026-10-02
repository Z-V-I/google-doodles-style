# 设计令牌（全部提取自 doodles.google 原站 index.min.css，未做调整）

来源：`site/static/f90e535b8a14784fb143c98e6c3624c4f0761c2eda4885a3923e4c0a6af066ac.index.min.css`
（548 KB，Google Glue 设计系统的构建产物）

---

## 1. 中性灰阶 `--glue-grey-*`

原站 `:root` 里定义，共 12 档（注意缺 25 与 0 之间的档，命名不连续是原样）。

| 令牌 | 值 | 典型用途 |
| --- | --- | --- |
| `--glue-grey-0`   | `#fff`     | 卡片/页眉底 |
| `--glue-grey-25`  | `#f1f1f1`  | 备用浅底 |
| `--glue-grey-50`  | `#f8f9fa`  | 页脚底 |
| `--glue-grey-100` | `#f1f3f4`  | hover 底 |
| `--glue-grey-200` | `#e8eaed`  | 分隔 |
| `--glue-grey-300` | `#dadce0`  | 描边（中强调按钮） |
| `--glue-grey-400` | `#bdc1c6`  | 禁用态 |
| `--glue-grey-500` | `#9aa0a6`  | 占位文字 |
| `--glue-grey-600` | `#80868b`  | 次级文字 |
| `--glue-grey-700` | `#5f6368`  | 正文辅助色（页脚/版权） |
| `--glue-grey-800` | `#3c4043`  | 标题备选 |
| `--glue-grey-900` | `#202124`  | **正文主色** |

## 2. 主题色阶 `--glue-{blue,green,red,yellow}-*`

每色 10 档（50 起）。**页面实际用得最多的是 600 档**（链接、主按钮）。

| | blue | green | red | yellow |
| --- | --- | --- | --- | --- |
| 50  | `#e8f0fe` | `#e6f4ea` | `#fce8e6` | `#fef7e0` |
| 100 | `#d2e3fc` | `#ceead6` | `#fad2cf` | `#feefc3` |
| 200 | `#aecbfa` | `#a8dab5` | `#f6aea9` | `#fde293` |
| 300 | `#8ab4f8` | `#81c995` | `#f28b82` | `#fdd663` |
| 400 | `#669df6` | `#5bb974` | `#ee675c` | `#fcc934` |
| 500 | `#4285f4` | `#34a853` | `#ea4335` | `#fbbc04` |
| 600 | `#1a73e8` | `#1e8e3e` | `#d93025` | `#f9ab00` |
| 700 | `#1967d2` | `#188038` | `#c5221f` | `#f29900` |
| 800 | `#185abc` | `#137333` | `#b31412` | `#ea8600` |
| 900 | `#174ea6` | `#0d652d` | `#a50e0e` | `#e37400` |

另有 `--glue-purple-100: #ea80fc`、`--glue-purple-900: #681da8`。

**品牌四色** = blue-500 / red-500 / yellow-500 / green-500，即
`#4285f4` `#ea4335` `#fbbc05` `#34a853`。

---

## 3. 涂鸦主题色 `theme-<color>`（19 套）

原站按涂鸦图片的主色给整页套一个 `theme-<color>` 类。每个 theme 提供的
**不是 6 个颜色，而是 21 个** —— 6 个主题色钩子 + 5 档 surface 背景梯（每档 3 个变体）：

```
.theme-X .main                  .theme-X .main-outline            .theme-X .main-fill-svg
.theme-X .interactive           .theme-X .interactive-outline     .theme-X .interactive-fill-svg
.theme-X .surface-1 … .surface-5    （各自另有 -outline / -fill-svg）
```

19 套主题名：

```
blue · brown · dark-blue · emerald · grass · gray · green · light-blue · lime ·
magenta · orange · pink · purple · red · salmon · tan · teal · terracotta · yellow
```

完整的 19×6 色值表、文字对比度实测、按气质选色、数据集 color 字段映射，
全部在 **`references/palette.md`**。这里只强调两条最容易错的：

1. **`theme-*` 是空壳类，不自带任何样式。** 光写 `class="theme-pink"` 不会改变
   任何东西，必须配 `.theme-pink .main { … }` 这样的组合选择器。
2. **换主题要连 surface 一起换。** `theme-pink` 的 `surface-1` 是淡粉 `#f7edf2`，
   不是淡蓝 —— 每条主题各有一套自己的 5 档梯。

另外原站还有 4 套与 theme 同构的**品牌强调色** `.brand-accent-1..4`，固定为
Google 四色、不随主题走，用在「要强调但不是涂鸦主色」的区块。

## 4. 表面色 `surface-*`

**surface 不是一套固定色，而是跟着 theme 走的。** 每个 `theme-*` 各带 5 档
（见 §3 与 palette.md §2）。只有**不在任何 theme 里**时，才落到全局默认那条梯 ——
取值正好等于 `theme-blue` 的梯：

| 类 | 全局兜底值 |
| --- | --- |
| `.surface-1` | `#edf0ff` |
| `.surface-2` | `#d8e2ff` |
| `.surface-3` | `#adc6ff` |
| `.surface-4` | `#80aaff` |
| `.surface-5` | `#001a41` |

每档还有 `-outline`（只设 border-color）与 `-fill-svg`（只设 fill）变体。

中性表面是**另一套**，而且在 `.doodle-module` 内取值不同：

| 类 | 全局 | 在 `.doodle-module` 里 |
| --- | --- | --- |
| `.neutral-surface-1` | `#fff` | `#fff` |
| `.neutral-surface-2` | `#f8f9fa` | `#fcfcfc` |
| `.neutral-surface-3` | `#f1f3f4` | `#f5f5f5` |

不要合并成一套；模块内底色比全局略浅是刻意的。

---

## 5. 排版

### 5.1 字体族

原站把字体栈按 CJK 语言拆成 **5 套**（无 / JP / KR / SC / TC），共 24 种组合 ——
同一个字体变体在每个语言下各有一份。规律是**在 Google Sans 后面接对应的
Noto CJK**。简体中文那套：

```css
标题/大字   Google Sans Display, Noto Sans SC, Noto Sans CJK SC, Arial, Helvetica, sans-serif
组件/按钮   Google Sans,         Noto Sans SC, Noto Sans CJK SC, Arial, Helvetica, sans-serif
正文        Google Sans Text, Roboto, Noto Sans SC, Noto Sans CJK SC, Arial, Helvetica, sans-serif
```

把 `SC` 换成 `TC` / `JP` / `KR` 就是另外三套。去掉 Noto 两段就是**纯拉丁那套**
（原站默认，也是 `doodles-style.css` 里 `--font-*` 用的）：

```css
标题/大字   Google Sans Display, Arial, Helvetica, sans-serif
组件/按钮   Google Sans,         Arial, Helvetica, sans-serif
正文        Google Sans Text, Roboto, Arial, Helvetica, sans-serif
品牌 logo   Product Sans, Google Sans, Arial, Helvetica, sans-serif
```

> 注意 Product Sans 那条在中文变体里顺序**不一样**，原站写成
> `Product Sans, Google Sans, Arial, Helvetica, sans-serif, Noto Sans SC, Noto Sans CJK SC`
> —— Arial 排在 Noto 前面。原站自己也不一致，照抄即可，别"顺手统一"。

三个 Google Sans 变体的分工是**固定的**，不能混用：

| 变体 | 用在哪 | 特征 |
| --- | --- | --- |
| `Google Sans Display` | 大标题（h1/h2、`.glue-headline`） | 字面更紧凑，大字号下更有冲击力 |
| `Google Sans` | 导航、按钮、卡片文字、chip | 中等字重语境 |
| `Google Sans Text` | 正文段落 | 小字号可读性优化，字面更开 |

> ⚠️ **Google Sans / Display / Text 不含任何 CJK 字形。**
> `fonts.css` 里 26 种 `unicode-range` 覆盖拉丁、希腊、西里尔、希伯来、阿拉伯、
> 天城文、泰文、高棉文 …… **一条中日韩都没有**。所以中文字符必然落到回退链上 ——
> 中文页面的观感完全由那份回退链决定，跟内联了哪些 woff2 无关。
> 反过来也说明：`--font-display` 这类变量只对拉丁字符（英文、数字、标点）生效。
>
> 实测：`Noto Sans SC` 在 Windows / macOS 上默认都**不装**，Chrome 自带的 Noto
> 也不是以这个 family 名暴露的。所以原站那套 SC 栈在普通机器上会一路落到
> `Arial`，最后交给浏览器的系统中文兜底（Windows 微软雅黑 / macOS 苹方）。
> 想让中文也稳定好看，就在 Noto 之后补一段系统中文黑体 —— 这不是原站行为，
> 是刻意的增强，写页面时注明即可。

### 5.2 层级（实测值）

| 类 | 字体 | 字号 | 字重 | letter-spacing | line-height |
| --- | --- | --- | --- | --- | --- |
| `.glue-headline` | Display | `32px` | 400 | — | `120%` |
| `.title`（详情页 h1） | Display | `24px`→`40px`→`48px`→`80px` | 400 | — | `120%` |
| `.glue-body--large` | Text | `1.125rem` | 400 | `normal` | `1.5555555556` |
| `.glue-body` | Text | `1rem` | 400 | `.1px` | `1.5` |
| `.glue-caption` | Text | `.875rem` | 400 | `.15px` | `1.7142857143` |
| `.glue-label` | Text | `.6875rem` | 500 | `.5px` | `1.4545454545` |

`.glue-headline` 还有一条容易漏的：`margin-bottom: 32px; width: 70%` —— 标题**只占 70% 宽**，
这是原站刻意的排版留白。

`.glue-label` 带 `text-transform: uppercase`。

---

## 6. 布局

### 6.1 内容栅格 `.glue-page`

三档，以 600 / 1024 为界：

| 视口 | 规则 |
| --- | --- |
| `< 600px` | `margin: 0 28px` |
| `600–1023px` | `margin: 0 40px` |
| `1024–1439px` | `margin: 0 72px` |
| `≥ 1440px` | `margin: 0 auto; max-width: 1296px`（**不再加 padding**） |

**1296px 是内容硬上限**，超出部分由 `.background-padding` 补色块铺满。

注意 `max-width` 那条是在 **1440** 断点才生效的，不是 1024 —— 1024–1439 之间走的是
72px 外边距。页脚的各段（`.glue-footer__site-links` / `__global` / `__upper`）
用的是同一套数值与同一个 1440 断点。

### 6.1.1 三柱子里的 `.background-padding` 默认是隐藏的

```css
.background-padding { display: none; flex: 1 1 calc(50% - 648px); }
@media (min-width: 1440px) { .background-padding { display: block; } }
```

**只有 ≥1440px 才出现。** 1024–1439 之间视口还不够宽，两侧留白由 `.glue-page`
的 72px 外边距负责，不需要柱子。

这条很容易只抄到 `display:none` 那半条就收工 —— 结果整条 hero 都没有底色，
而页面其余部分看起来完全正常，所以特别难往"柱子没显示"上想。
写三柱子区块时先确认 1440 那条 `display:block` 在不在。

### 6.1.2 `.display-flex` 没有全局的"小屏竖排"行为

原站这个类只出现在三处，且行为不一样：

| 上下文 | 行为 |
| --- | --- |
| `.hero-doodle .display-flex` | `display:flex`，**恒为 row**，不随断点变 |
| `.hero-with-subtitle .display-flex` | 同上 |
| `.content-block .display-flex` | base `flex-direction:column` → `600px` 起 `row` |

所以不能写成"全局 column、600px 起 row"。那样会让 hero 的三根柱子在小屏竖着堆起来，
而 `.background-padding` 在小屏本来就是 `display:none`，柱子一竖排就只剩空行。


### 6.2 断点

原站实际使用的媒体查询（按出现次数）：

| 断点 | 次数 | 含义 |
| --- | --- | --- |
| `min-width: 1024px` | 307 | 桌面 |
| `min-width: 600px` | 243 | 平板 |
| `min-width: 1440px` | 144 | 宽屏 |
| `max-width: 599px` | 23 | 移动 |
| `600px–1023px` | 2 | 平板专属 |

> 注意：**没有 768px 断点**。Google Glue 用 600/1024/1440，写响应式时别引入别的值。

### 6.3 页眉高度

- 单层页眉：`64px`（移动端与桌面端都是）
- 双层页眉（tiered，带二级导航）：`128px`
- `.glue-header` 自身 `min-height: 64px`

### 6.4 详情页图片区与标题条

`.hero-doodle .img-container`（图片区）随断点台阶式增长，注意第三档在 **1440**：

| 视口 | 高度 | `.media-container` 宽度 |
| --- | --- | --- |
| `< 600px` | `221px` | `375px` |
| `600–1439px` | `316px` | `732px` |
| `≥ 1440px` | `480px` | `940px` |

`.hero-doodle .content-container`（标题条）：

| 视口 | min-height | padding | align-items |
| --- | --- | --- | --- |
| `< 600px` | `195px` | `24px` | `flex-start` |
| `600–1439px` | `253px` | `32px 93px` | `flex-start` |
| `≥ 1440px` | `306px` | `0 80px` | `center` |

标题 `.hero-doodle .content-container .title`（Google Sans Display）：

| 视口 | 字号 | 行高 | 对齐 |
| --- | --- | --- | --- |
| `< 600px` | `40px` | `48px` | 左 |
| `600–1439px` | `64px` | `77px` | 左 |
| `≥ 1440px` | `80px` | `96px` | 居中 |

### 6.5 首页 hero 拼贴轮播

`.hero-tag-carousel .glue-carousel` 的高度是整块拼贴的画布：

| 视口 | 高度 | 其他 |
| --- | --- | --- |
| `< 600px` | `150vw` | — |
| `600–1023px` | `620px` | — |
| `≥ 1024px` | `815px` | `max-width: 1440px` |

`.hero-tag-carousel` 自身 `background-color: #fcfcfc; overflow: hidden`。
9 张拼贴卡各自绝对定位，宽高比由 `:before { padding-top: 40% }` 固定。

---

## 7. 形状与阴影

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 卡片圆角 | `16px` | `.doodle-card-wrapper` / `.doodle-card-cta` |
| 药丸圆角 | `24px` | 按钮、chip |
| hover 阴影 | `0 1px 2px 0 rgba(60,64,67,.3), 0 2px 6px 2px rgba(60,64,67,.15)` | 卡片悬浮 |
| 页眉阴影 | `0 1px 2px 0 rgba(60,64,67,.3), 0 1px 3px 1px rgba(60,64,67,.15)` | 滚动吸顶 |

卡片 hover 的完整效果是**三件事同时发生**，缺一不可：

```css
transform: scale(1.01);
box-shadow: 0 1px 2px 0 rgba(60,64,67,.3), 0 2px 6px 2px rgba(60,64,67,.15);
/* transition: all .3s ease-in-out（原站用的是 all + ease-in-out，不是 cubic-bezier） */
```

---

## 8. 容易踩的坑

1. **描边不是灰色，是纯黑。** 卡片外框、标题下划线、区块分隔线全部是
   `border: 1px solid #000`。这是 Doodles 这一版的标志性风格（粗黑描边 + 色块），
   换成 `#dadce0` 会立刻失去辨识度。

2. **`theme-*` 只提供 `.main` / `.interactive` 这类钩子，不自带任何样式。**
   必须写 `.theme-pink .main { … }` 这样的组合选择器才生效 —— 光加
   `class="theme-pink"` 不会改变任何东西。

3. **字体必须先加载 `fonts/fonts.css`，再加载主样式表。**
   原站 `<head>` 里两者的顺序是固定的，且 fonts.css 额外带了 `rel="preload"`。
   这 200 个 woff2 子集**已经随 skill 提供**（`assets/fonts/`），不需要联网。

4. **`Google Sans` 不是系统字体。** 没有 fonts.css 时会回退到 Arial，
   字形差异在标题上非常明显（原站标题的 `a`/`g` 是双层结构）。
   用 skill 自带的 `assets/fonts/fonts.css` 就不会有问题。

5. **每个 theme 自带 5 档 surface，不是一套固定蓝调。**
   `theme-pink` 的 `surface-1` 是淡粉 `#f7edf2`，只有不在任何 theme 里时
   才用全局那条（= `theme-blue` 的梯）。写页面时若 "主色换了、底色还是蓝的"，
   就是踩了这条。详见 `palette.md` §0。

6. **彩色区块里要用黑字，不是白字。** 19 套主题的 `main` 上，18 套都是
   黑字对比度更高（`dark-blue` 是唯一例外）。这是 Doodles 与 Material 观感
   分道扬镳的地方 —— 换成白字风格立刻就散了。详见 `palette.md` §4。
