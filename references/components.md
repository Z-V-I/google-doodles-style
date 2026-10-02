# 组件解剖（DOM 结构 + 类名 + 行为）

所有类名与 Google Glue 官方 CSS 一一对应。照抄结构 → 外观即与原站一致。

---

## 1. 页眉 `glue-header`

页眉有**两条完全独立的 bar**，靠 CSS 互斥显示，不是一条 bar 做响应式变形：

```html
<header class="glue-header glue-header--single glue-header--no-cta" aria-expanded="false">
  <a href="#content" class="glue-header__link glue-header__skip-content">Jump to content</a>

  <div class="glue-header__bar glue-header__bar--mobile">   <!-- <1024px 显示 --> </div>
  <div class="glue-header__bar glue-header__bar--desktop glue-header__drawer"
       id="glue-drawer-2465973" style="position: static; top: -64px;">  <!-- ≥1024px --> </div>

  <div class="glue-header__drawer-backdrop" aria-label="close menu"></div>
</header>
```

- `.glue-header--single`：只有一层（没有二级导航）。
- `.glue-header--no-cta`：右侧没有主 CTA 按钮。
- `style="position: static; top: -64px"`：**原站就是这样内联写死的**。桌面 bar 兼作
  移动端抽屉内容，这个内联样式是它的初始收拢位。不要删。

### 品牌锁形组合（page 左侧）

```html
<div class="glue-header__lock-up">
  <div class="glue-header__logo">
    <a class="glue-header__logo-link" href="/" title="Google doodles">
      <div class="glue-header__logo-container">
        <svg class="glue-header__logo-svg" role="presentation" aria-hidden="true">
          <use href="/static/glue-icons.svg#google-color-logo"></use>
        </svg>
      </div>
      <span class="glue-header__logo--product">
        <svg class="glue-header__logo-svg" role="presentation" aria-hidden="true">
          <use href="/static/icons.svg#doodle-logo"></use>
        </svg>
      </span>
    </a>
  </div>
</div>
```

两个 SVG：Google 四色 logo（74×24）+ Doodle 文字标（106×24），横向并排。

### 三层容器分工

`glue-header__tier` 内是三个 `glue-header__container`：

| 位置 | 类名 | 内容 |
| --- | --- | --- |
| 左 | `.glue-header__container` | `glue-header__lock-up` |
| 中 | `.glue-header__container.glue-header__container--linkbar` | `nav.glue-header__link-bar > ul.glue-header__list` |
| 右 | `.glue-header__container` | `.glue-header__supplemental`（搜索图标等） |

> `.glue-header__container--linkbar` 在**移动端是 `display: none`**（它只在桌面 bar 里出现）。

### 埋点属性

每个可点元素都带一组 `data-g-*`，是原站埋点契约。**要复制风格就一起复制**，
否则换回原站 JS 会失去统计维度：

```html
data-g-event-trigger="click"
data-g-event="module_header"
data-g-module_id=""  data-g-module_name="header"  data-g-module_postion=""
data-g-cta_type="button"  data-g-cta_text="Library"  data-g-cta_url="/search/"
data-g-template_id="header_item"  data-g-template_position="1/3"
```

---

## 2. 页脚 `glue-footer`

已按项目要求**重做过**：原站页脚里指向谷歌在线服务的入口（Google logo、About Google、
Google Products、Privacy、Terms、Help、reCAPTCHA 声明）与 "Follow us" 社交图标组
**整块删除**，版权行改成自定义文案。保留下来的只有 `Doodles → Library / About`
两个站内链接与无障碍标题。

```html
<footer class="glue-footer">
  <h2 class="glue-visually-hidden">Footer Links</h2>
  <nav class="glue-footer__site-links">
    <div class="glue-footer__site-links-grid glue-footer__site-links-grid--1-col">
      <div class="glue-footer__site-links-column">
        <h3 class="glue-footer__site-links-header">
          <span class="glue-footer__site-links-header-button" id="column-1-toggle">
            <span class="glue-footer__site-links-header-text">Doodles</span>
            <svg role="presentation" aria-hidden="true"
                 class="glue-icon glue-icon--footer glue-expansion-panel__header-arrow">
              <use href="/static/glue-icons.svg#expand-more"></use>
            </svg>
          </span>
        </h3>
        <div class="glue-footer__site-links-list" id="column-1-content">
          <ul class="glue-no-bullet" role="list"> … </ul>
        </div>
      </div>
    </div>
  </nav>
  <section class="glue-footer__global">
    <p class="glue-footer__copyright">Copyright © 2026 → ∞ ZVI and Google will always be together.</p>
  </section>
</footer>
```

要点：
- 页脚分 `__site-links` 与 `__global` 两段，中间有 `1px` 分隔线。
- 移动端把每一列折叠成手风琴（`expand-more` 箭头随展开旋转 180°）。
- 版权文字本身带了一段内联样式（原站行为），字号 `1rem`、字重 `500`、色 `#5f6368`。

> **⚠ 版权行是 `flex: 1 0 auto` —— `flex-shrink` 为 0，它不肯收缩。**
> 原站那句英文短，撑不出来；换成一句长中文就会把整页顶出一条横向滚动条
> （手机上表现为"页面能左右抖"，而且只有这一个元素越界）。
> 覆盖一下即可：
>
> ```css
> .glue-footer__copyright { flex-shrink: 1; min-width: 0; }
> ```
>
> 这一条是实测踩出来的：写中文页面时几乎必中。

---

## 3. 轮播 `glue-carousel`

### 3.1 结构

```html
<div class="glue-carousel"
     aria-label=""
     data-glue-carousel-cards-per-page="1"
     data-glue-carousel-cyclical="true"
     data-glue-carousel-cyclical-aditional-cards="0">
  <div class="glue-carousel__viewport">
    <div class="glue-carousel__list hero-tag-carousel__list"> … </div>
  </div>
</div>
```

> `data-glue-carousel-cyclical-aditional` **拼写就是错的**（原站笔误，少一个 `t`）。
> 照抄，别改 —— 改了 JS 就读不到。

### 3.2 循环模式下的占位符

分页点的 aria-label 里保留了模板变量 `$glue_carousel_page_number$`，
由运行时的 Glue JS 在初始化时替换：

```html
<div class="glue-carousel__navigation"
     aria-label="Go to slide $glue_carousel_page_number$"
     data-glue-carousel-navigation-label="Go to slide $glue_carousel_page_number$"></div>
```

### 3.3 首页 hero 拼贴轮播

```html
<div class="hero-tag-carousel doodle-module floating-buttons" id="section-1">
  <div class="background-pattern-dots">          <!-- 背景点阵装饰 -->
    <div class="glue-carousel"
         data-glue-carousel-cards-per-page="1"
         data-glue-carousel-cyclical="true"
         data-glue-carousel-cyclical-aditional-cards="0">
      <div class="glue-carousel__viewport">

        <div class="glue-carousel__list hero-tag-carousel__list">
          <div class="glue-carousel__item hero-tag-carousel__item"
               id="glue-carousel-1" data-home-slide-index="1" aria-label="Culture">
            <div class="hero-tag-carousel__collage active">
              <a class="hero-tag-carousel__collage-card" href="/doodle/<slug>/">
                <div class="hero-tag-carousel__collage-card-bg"></div>
                <img class="hero-tag-carousel__collage-card-img" src="…" alt="…">
              </a>
              <!-- 共 9 张 -->
            </div>
          </div>
          <!-- 每多一个话题就多一个 item -->
        </div>

        <!-- 主文案层：盖在拼贴上 -->
        <div class="hero-tag-carousel__main glue-text-center">
          <p class="hero-tag-carousel__main-text">Doodles are celebrations of <doodles-tags></doodles-tags></p>
          <div class="hero-tag-carousel__main-cta">
            <span class="hero-tag-carousel__main-cta-wrapper doodle-module theme-green">
              <a class="hero-tag-carousel__main-cta-link theme-word main-outline"
                 data-home-cta-index="1" tabindex="-1" href="/search/">Culture</a>
            </span>
            <!-- 每个话题一个 chip，3 个左右 -->
          </div>
        </div>

      </div>

      <div class="tout-carousel-navigation">
        <button id="prev-mobile-btn" class="glue-button glue-button--high-emphasis glue-button--icon interactive">…</button>
        <div class="glue-carousel__navigation"
             aria-label="Go to slide $glue_carousel_page_number$"></div>
        <button id="next-mobile-btn" class="glue-button glue-button--high-emphasis glue-button--icon interactive">…</button>
      </div>

    </div>
  </div>
</div>
```

**最容易理解错的一点：拼贴不是网格，是 9 张卡各自绝对定位。**

```css
.hero-tag-carousel__collage { display:grid; grid-template-columns:1fr; position:absolute; inset:0; z-index:5 }
.hero-tag-carousel__collage-card {
  position: absolute; width: 250px;              /* 基准 */
  border: 1px solid #000; border-radius: 11px;   /* ≥1024 时 32px */
  grid-column-start: 1; grid-row-start: 1;       /* 全部叠在同一个单元里 */
}
.hero-tag-carousel__collage-card:before { content:""; display:block; padding-top:40%; }  /* 固定 5:2 比例 */
```

落位由 `:first-of-type` … `:nth-of-type(9)` 的 `left/top/right/bottom/width` 决定，
**全是百分比，且在 600 / 1024 两个断点各有取值**（例如第 1 张：基准 `left:1%;top:5%;width:30%`
→ `left:-1.5%;top:24%;width:21.7%` → `left:-11.5%;top:20%;width:21.7%`）。
完整 9 组数值见 `assets/doodles-style.css` 第 11 节。**卡的数量与顺序不能改** —— 
改一张，后面全部的 `nth-of-type` 都会错位。

其它容易漏的：

- 一张拼贴卡 = `<a>` + 背景 `<div>` + 居中 `<img>`，**三件套缺一不可**
  （背景 div 撑满色块，img 用 `max-width/height: 90%` 居中 contain）。
- `.hero-tag-carousel__main` 是**兄弟节点**（不在 item 里），`z-index:10` 压在最上层，
  且 `pointer-events:none` —— 里面的 CTA 链接单独用 `pointer-events:all` 恢复可点。
  漏掉这一步，整个拼贴就点不动了。
- 所有话题 chip 叠在同一个网格单元（`grid-column-start:1; grid-row-start:1`），
  同一时刻只显示一个。原站靠 animation 把非当前的移出可视区。
- 未激活 chip 带 `tabindex="-1"`，键盘 Tab 不会停在看不见的元素上。
- `.floating-buttons` 让左右箭头浮在轮播两侧。
- 分页点那行 `.glue-carousel__navigation` 在 hero 里被 `display:none` 掉。

---

## 4. 涂鸦卡片（两种形态，别混用）

### 4.1 首页/检索页：完整卡片

```html
<div class="doodle-card-wrapper">                 <!-- 黑描边 + 16px 圆角 + overflow:hidden -->
  <a href="/doodle/<slug>/" class="doodle-card-link">
    <div class="doodle-card">                      <!-- hover 放大 + 阴影 -->
      <div class="doodle-card-img">                <!-- 包装器：::before 撑 60% 比例 -->
        <img loading="lazy" src="/img/x.jpg" alt="X">
      </div>
      <div class="doodle-card-content">            <!-- 上描边分隔 -->
        <div class="doodle-card-content__date">Dec 17, 2003</div>
        <div class="doodle-card-content__event">100th Anniversary of Flight</div>
      </div>
    </div>
  </a>
</div>
```

`.doodle-card-img` 用 `::before { padding-top: 60% }` 造比例，
内部的 `img` 是 `position: absolute` + `translate(-50%,-50%)` 居中 contain —— 
**6:4 的比例盒子是固定的**，图片再长也不会把卡片撑变形。

### 4.2 详情页推荐位：极简卡片

```html
<div class="doodle-card-wrapper">
  <a href="/doodle/<slug>/" class="doodle-card-link">
    <img loading="lazy" class="doodle-card-img" src="/img/x.gif" alt="X">   <!-- 直接贴在 img 上 -->
    <div class="doodle-card-title">X</div>
  </a>
</div>
```

**关键差异**：详情页里 `.doodle-card-img` 是**贴在 `<img>` 本身**的，没有包装器、
没有 `.doodle-card`、没有 `.doodle-card-content`，标题用 `.doodle-card-title`。
本 skill 的 CSS 对两种用法都做了适配（见 `doodles-style.css` 里 `img.doodle-card-img` 那条）。

### 4.3 卡片网格

`.cards-stack-grid`（详情页推荐位）：1 / 2 / 4 列（600 / 1024 断点），固定放 8 张。
`.cards-stack-content-list`（首页引言卡堆）：见下一节，**必须正好 5 个**
`.cards-stack-content-square`。

> **⚠ 1024 断点是个"双跳"陷阱。**
> 同一刻，`.cards-stack-grid` 从 2 列跳到 **4 列**，而 `.doodle-card-content`
> 的内边距也从 `28px 32px` 跳到 `32px 40px`。两个一起生效，1024 下每张卡只有
> 约 210px 宽，正文可用宽度只剩 **130px** —— 中文两三个字就换行，英文单词会被
> 从中间断开（`Techno Mechanic / us`）。原站能这么写，是因为它的卡片标题就是短
> 英文，正文根本不进卡片。
>
> **卡片要装一句话时，列数和内边距必须一起改：**
>
> ```css
> @media (min-width: 1024px) {
>   .my-grid .cards-stack-grid    { grid-template-columns: repeat(3, 1fr); }
>   .my-grid .doodle-card-content { padding: 26px 28px 30px; }
> }
> @media (min-width: 1280px) { .my-grid .cards-stack-grid { grid-template-columns: repeat(4, 1fr); } }
> @media (min-width: 1440px) { .my-grid .cards-stack-grid { grid-template-columns: repeat(5, 1fr); } }
> ```
>
> 顺带一个排版的算术：卡片数是 10 的倍数时，**5 列正好两行**，比 4 列留下一行
> 残缺要整齐。

### 4.3.1 卡片里的图片是"缩到 6:4 盒子里"的

```css
.doodle-card-img:before { content: ""; padding-top: 60%; }   /* 盒子固定 3:2 */
.doodle-card-img img { max-height: 90%; max-width: 90%; position: absolute; … }
```

所以一张 4:3 的插画放进去会被**高度限制**（撑满盒高的 90%，宽度只占 80%），
四周留白是原站刻意的效果，不是 bug。

但如果你画的是**半身像 / 会被底边裁切的插画**，那 10% 的余量会变成
"人像底下一道缝"，看着像没对齐：

```css
/* 让它铺满盒高，人像下缘正好贴住 .doodle-card-content 的上边线 */
.my-grid .doodle-card-img img { max-height: 100%; max-width: 100%; }
```

### 4.4 卡片 hover 的三件套

```css
.doodle-card-cta:focus,
.doodle-card-cta:hover {
  background-color: #fff;
  box-shadow: 0 1px 2px 0 rgba(60,64,67,.3), 0 2px 6px 2px rgba(60,64,67,.15);
  transform: scale(1.01);
}
/* transition: all .3s ease-in-out —— 原站用的就是 all + ease-in-out，不是 cubic-bezier */
```

缓存缩放、阴影、底色**三件事同时发生**，只做其中一件或两件会显得"差一口气"。

### 4.5 首页引言卡堆 `.cards-stack`

这是一摞纸的层叠效果，**必须正好 5 个** `.cards-stack-content-square`：

```css
/* 第 4 个留在文档流里当"底板"，1/2/3/5 绝对定位叠在它左后方 */
.cards-stack-content-square:not(:nth-of-type(4)) {
  height: calc(100% - 38px); position: absolute; right: 0; top: 0; width: calc(100% - 52px);
}
.cards-stack-content-square:first-of-type  { transform: translate(0);           z-index: 1; }
.cards-stack-content-square:nth-of-type(2) { transform: translate(-14px, 12px); z-index: 2; }
.cards-stack-content-square:nth-of-type(3) { transform: translate(-32px, 25px); z-index: 3; }
.cards-stack-content-square:nth-of-type(4) { margin: 38px 52px 0 0;             z-index: 4; }
.cards-stack-content-square:nth-of-type(5) { transform: translate(-52px, 38px); z-index: 5; visibility: hidden; }
```

**真正的内容卡放在第 4 个**（在流里的那张），前 3 个留空、第 5 个隐藏。
把内容放到第 1 个会得到一摞错位的空盒子。
内容卡的 `.cards-stack-content-square-item` 需要 `active` 类，否则 `opacity:0`。

卡片圆角 `26px`（比 `.doodle-card` 的 16px 大），`padding: 60px 40px`（≥600 时 `48px 32px`），
容器 `.cards-stack-content-wrapper` 限宽 `421px`。

### 4.6 背景纹理

原站用纯 CSS 渐变画三种底纹，挂在 `.doodle-module` 下：

```css
.doodle-module [class*=background-pattern-] { background-position:-2px -2px; background-size:60px 60px }
.background-pattern-square  { background-image: linear-gradient(90deg,rgba(0,0,0,.1) 2px,transparent 0),
                                                linear-gradient(180deg,rgba(0,0,0,.1) 2px,transparent 0) }
.background-pattern-dots    { background-image: radial-gradient(circle,rgba(0,0,0,.1) 3px,transparent 0) }
.background-pattern-stripes { background-image: repeating-linear-gradient(-45deg,
                                rgba(0,0,0,.1) 50%,rgba(0,0,0,.1) 52.5%,transparent 0,transparent) }
```

网格（square）用在 `.full-bleed-map` 与 `cards-stack`，点阵（dots）用在首页 hero。
注意 `60px` 的 `background-size` 与 `-2px` 的偏移是配套的：格子线正好压在边缘上，
改成别的值会出现一条半截的线。

---

## 5. 详情页 hero `hero-doodle`

三柱子结构是这一版最有辨识度的布局：

```html
<div class="hero-doodle doodle-module theme-pink" id="section-1">

  <!-- 图片区：下描边 -->
  <div class="display-flex border-bottom">
    <div class="background-padding"></div>
    <div class="glue-page no-margin">
      <section class="img-container">
        <div class="media-container">
          <img loading="lazy" src="/img/x.jpg" class="doodle-image" alt="X">
        </div>
      </section>
    </div>
    <div class="background-padding"></div>
  </div>

  <!-- 标题条：背景走 surface-<n> -->
  <div class="display-flex">
    <div class="background-padding surface-1"></div>
    <div class="glue-page no-margin">
      <section class="content-container surface-1">
        <h1 class="title">X</h1>
      </section>
    </div>
    <div class="background-padding surface-1"></div>
  </div>

</div>
```

- `.background-padding { flex: 1 1 calc(50% - 648px) }` —— 648 = 1296/2。
  视口越宽，两个柱子越宽，**中间内容恒为 1296px**。这才是"背景色铺满整屏、
  内容居中"的正确实现，不要用 `100vw` + 负 margin 硬凑。
- **柱子默认 `display: none`，只有 `≥1440px` 才 `display: block`。**
  1024–1439 之间留白由 `.glue-page` 的 72px 外边距负责。只抄 `display:none`
  会让整条 hero 没有底色，而页面其它部分完全正常，极难定位。详见
  `design-tokens.md` 6.1.1。
- 两根柱子上的类必须与中间一致（`surface-1` 出现三次），否则色带会断。
  如果希望整条色带连续（不只是两侧），把同一个颜色类也加到 `.img-container`
  或 `.content-container` 上。
- 注意 `surface-1` 的**实际颜色由外层的 `theme-X` 决定**：`theme-pink` 下是淡粉
  `#f7edf2`，只有 `theme-blue` 下才是淡蓝 `#edf0ff`。换主题时这里会自动跟着变，
  但如果你把颜色写死成 `#edf0ff`，就会失去这个能力。详见 `palette.md` §0。
- `.glue-page.no-margin` 取消 `glue-page` 在桌面端的 `padding: 0 72px`
  （此处留白已由柱子负责）。

---

## 6. 关键主题 chips `key-themes`

```html
<div class="doodle-module theme-pink key-themes" id="section-3">
  <div class="glue-page">
    <h2 class="key-themes-title">This Doodle's Key Themes</h2>
    <div class="themes-cta-wrapper">
      <div class="themes-wrapper">
        <a class="theme surface-4-outline" href="/search/?topic_tags=Other">Other</a>
      </div>
      <a class="key-themes-cta-link" href="/search/?topic_tags=Aviation"
         data-links='["/search/?topic_tags/Aviation", …]'>
        <div class="key-themes-cta-wrapper">
          <div class="key-themes-cta">Explore a Random Theme</div>
          <svg width="21" height="16" viewBox="0 0 21 16" fill="none" role="img" alt="">
            <use href="/static/icons.svg#right-arrow-doodles"></use>
          </svg>
        </div>
      </a>
    </div>
  </div>
</div>
```

- chip 的类是 `theme` **加上**一个 `surface-N-outline` —— `theme` 负责形状
  （药丸、黑描边），`surface-N-outline` 负责描边色。
- 链接指向 `/search/?topic_tags=<话题>`，话题名**带空格不编码**（原站如此）。
- `data-links` 是"随机主题"按钮的候选池，属性值里的双引号要写成 `&#34;`
  （合法 HTML，且能被 JS 直接 `JSON.parse`）。

> **⚠ `.themes-cta-wrapper` 在 ≥1440px 会变成横向排布。**
> 别往它里面塞"整行宽"的元素（比如一行小标题或一段说明）—— 在 1440 断点上会
> 被当成一个 flex 横向项目，挤成窄窄一条、逐字换行，而且**窄屏下完全正常**，
> 只有宽屏才现形。需要整行的东西放成它的兄弟节点：

```html
<div class="glue-page">
  <p class="eyebrow">…</p>              <!-- ✓ 兄弟节点 -->
  <div class="themes-cta-wrapper"> … </div>
</div>
```

> chips 也可以拿来做**筛选器**（点一位母亲 → 筛出她的孩子）：把 `<a>` 的
> `href` 指向卡片区做锚点跳转，再加 `data-*` 给 JS 用，另配一个 `.is-active`
> 类做选中态。这样能完全复用原站的 chip 样式，不用另造一套按钮。

---

## 7. 检索页 `search-doodle`

BEM 命名，**不是** glue 前缀 —— 这是 Google 给 Doodles 单独写的一套组件。

```
.search-doodle                              根，data-doodle-url="/doodle/"
├── .search-doodle__box                     搜索区
│   ├── .search-doodle__box-form            （带 glue-page，所以有正确的左右留白）
│   ├── .search-doodle__box-icon            放大镜
│   ├── .search-doodle__box-input           name="title_like"
│   ├── .search-doodle__box-input-border    聚焦时的下划线动画条
│   ├── .search-doodle__box-button_search   "Search" + 右箭头
│   ├── .search-doodle__box-button_random   "Surprise me" + sparkles
│   └── .search-doodle__box__tag_wrapper    已选条件 chips + Clear filters
├── .search-doodle__filter-panel            筛选面板
│   └── .glue-expansion-panel               每一组（Date/Topics/Colors/…）
│       ├── .glue-expansion-panel__toggle
│       ├── .glue-expansion-panel__button   data-glue-expansion-panel-toggle-for="<content-id>"
│       ├── .glue-expansion-panel__header-text / __header-counter
│       ├── .glue-expansion-panel__header-arrow
│       └── .glue-expansion-panel__content  id 与上面的 for 对应
├── .search-doodle__results-wrapper         结果网格
├── .search-doodle__results-loading         加载态（loading.gif）
├── .search-doodle__results-empty           空态（not-found.svg + 文案 + CTA）
└── .search-doodle__results-button          Show More
```

### 7.1 筛选控件的真实取值（别自己编）

话题复选框的 `value` 不是原始标签，而是**原站 API 的词表**，规则是
「非字母数字一律折叠成空格再转小写」：

| 界面显示 | `value` |
| --- | --- |
| Football/Soccer | `football soccer` |
| Plants & Flowers | `plants flowers` |
| Children's Day | `children s day` |

详情页 chip 与本地数据用的是**原始标签**（带 `/` 和 `&`），两边不一致会导致
**筛选静默失效** —— 勾了没反应也不报错。比较时两侧都要过同一条归一化规则。

### 7.2 接口契约

`GET /live/api/v1/doodles`

| 参数 | 说明 |
| --- | --- |
| `title_like`（或 `q`） | 标题子串，大小写不敏感 |
| `color_tags` | 主色，逗号分隔 |
| `topic_tags` | 话题，逗号分隔 |
| `form_tags` | 形态（still/animated/…） |
| `nationality_tags` | 地区 |
| `date_like_year` / `_month` / `_day` | 日期 |
| `page` / `limit` | 分页 |
| `art_style_tags` / `sort_tags` | 原站有、本地数据无对应维度；传了**不缩小结果集**而不是返回空 |

> 月份比较要去掉前导零再比（`'05'` ≡ `'5'`）。
> 早期实现用 `str(v) not in (wanted, "%02d" % v)` → 当 `v >= 10` 时
> `"%02d" % v == str(v)` 恒成立，筛选整个失效且界面上看不出来。

---

## 8. 图标：全部走 SVG sprite

**没有任何一个图标是内联 SVG 路径或图标字体**，统一是：

```html
<svg class="glue-icon glue-icon--24px" role="presentation" aria-hidden="true">
  <use href="/static/<hash>.glue-icons.svg#<name>"></use>
</svg>
```

两个 sprite 文件（原站构建产物的哈希名）：

| 文件 | 大小 | 常用 id |
| --- | --- | --- |
| `<hash>.glue-icons.svg` | 16 KB | `menu` `search` `expand-more` `google-color-logo` `google-solid-logo` `help` `instagram` `post-facebook` `post-linkedin` `x` `video-youtube` |
| `<hash>.icons.svg` | 148 KB | `doodle-logo` `celebration` `refresh` `stars` `tick` `right-arrow` `right-arrow-doodles` `left-arrow-tout-carousel` `left-white-arrow-tout-carousel` `right-arrow-tout-carousel` `right-white-arrow-tout-carousel` `arrow-white` `checkmark` `plus` `sparkles` |

> ⚠️ **这两个 sprite 未随本仓库提供**（Google 图标资产，单独排除）。
> 先跑一次 `python assets/fetch-icons.py` 补齐，否则页面上每一个 `<use>`
> 都会静默取不到 —— 不报错、不提示，只是空一块。见 `real-assets.md` §0.2。

尺寸类：`glue-icon--18px` / `--20px` / `--24px` / `--32px` / `glue-icon--footer`。

> 部分老标记用 `xlink:href`，新标记用 `href`。两者都能工作；
> 沿用原站时保持原样即可，新写建议统一用 `href`。

### 8.1 内联进单文件 HTML 时**必须**把 `<svg id>` 转成 `<symbol>`

原站 sprite 的内部结构不是 `<symbol>`，而是 `<defs>` 里嵌一堆 `<svg id="x" viewBox="…">`：

```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <defs>
    <svg id="menu" viewBox="0 0 24 24"><path d="…"></path></svg>
    <svg id="expand-more" viewBox="0 0 24 24"><path d="…"></path></svg>
  </defs>
</svg>
```

外部引用（`<use href="file.svg#menu">`）这样没问题，但**把 sprite 内联进同一个
HTML 之后，`<use>` 就不按 `viewBox` 缩放了** —— 图标会按被引用 `<svg>` 元素自身的
尺寸渲染（没写 width/height 时是 300×150），症状是"图标忽然巨大或者位置全错"。

所以内联前先做一次转换，属性只保留 `viewBox`：

```python
m = re.search(r'<svg\b[^>]*\bid="' + name + r'"([^>]*)>(.*?)</svg>', text, re.S)
# → <symbol id="…" viewBox="…">…</symbol>
```

各图标的体积（latin 子集之外，这是最该按需取的部分）：

| id | 体积 | id | 体积 |
| --- | --- | --- | --- |
| `google-color-logo` | 1.8 KB | `refresh` | 2.1 KB |
| `menu` / `search` / `close` / `expand-more` | 各 0.1–0.2 KB | `right-arrow-doodles` | 1.1 KB |
| `checkmark` | 1.2 KB | `stars` / `sparkles` | 各 7.5 KB |
| `doodle-logo` | 34.8 KB | `not-found-cat` | 5.1 KB |

> 页眉那个 Google logo 一定要用 `google-color-logo` 真品。手写
> `<text>` 拼四色字母（哪怕用 Arial bold）一眼就能看出不像 ——
> 真品是 1.8 KB 的路径数据，没有理由不用。

### 8.2 两个会静默失败的 id 陷阱

1. **写错的 id 不报错、不提示、控制台也没有警告**，只是那个位置空一块。
   因为 CSS 的 `width/height` 仍然生效在 `<svg>` 外壳上，连"布局坏掉"的迹象都没有。
   新写图标后一定回 sprite 里核对：

   ```bash
   grep -o 'id="[^"]*"' assets/vendor/glue-icons.svg assets/vendor/icons.svg | sort -u
   ```

2. **原站根本没有 `heart` 这个图标。** `glue-icons.svg` 和 `icons.svg` 里都没有心形
   （最接近的是 `celebration`）。需要心形只能自己画，别照着语感写
   `glue-icons.svg#heart` —— 那一定是什么都拿不到。

### 8.3 插画用 data URI 内联时，**不能写 `<text>`**

单文件页面的常见做法是把插画内联成 `src="data:image/svg+xml,…"`。注意
`<img>` 里的 SVG 是**独立文档**，取不到宿主页面的样式表 —— 页面上内联的
Google Sans 它一个字都用不上，`<text>` 会静默落回系统 `sans-serif`。

所以：

- 内联 `<symbol>`（直接写在 HTML 里，用于 `<use>`）→ **能**用页面字体。
  页眉那个文字标就走这条路。
- `data:` / 外部 `.svg` 文件（用于 `<img src>`）→ **不能**用页面字体。
  要字母就先转成 `<path>`，或者干脆把字换成图形。

想在构建时拦一道的话：

```python
for key, svg in art.items():
    if "<text" in svg:
        raise SystemExit(f"{key} 的插画里写了 <text>，data URI 里会掉字体")
```

另外 `data:` URI 里必须把 `#` 转义成 `%23`（`urllib.parse.quote` 默认就会做），
否则 `url(#id)`、`fill="#000"` 会被当成 URL 的 fragment 直接截断。

---

## 9. 埋点、无障碍与其它约定

1. **`aria-hidden="true"` + `role="presentation"` 成对出现**，装饰性 SVG 都带。
2. **跳过链接**：`<a href="#content" class="glue-header__link glue-header__skip-content">Jump to content</a>`，
   而且是页眉里**第一个**可聚焦元素。
3. **正文容器 id 固定为 `content`**：`<main id="content">`。
4. **区块 id 是 `section-<n>`**，n 在整个页面单调递增，用作锚点
   （`/about/#section-4` 这种链接就依赖它）。
5. **`doodle-module`** 是每个内容区块的通用钩子类，出现 9 次（首页）。
6. 图片一律 `loading="lazy"`，`alt` 用涂鸦标题（不是空串）。
