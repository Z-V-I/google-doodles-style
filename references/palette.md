# 配色（palette）

全部数值解析自 doodles.google 原站 `static/*.index.min.css`，未做目测修正。
原文件随 skill 提供：`assets/vendor/glue.min.css`。

---

## 0. 模型：一套主题 = 一条 6 档色梯

Doodles 的配色不是「一个主色 + 灰底」，而是**每一套主题色都自带一条从最浅到最深的色梯**：

```
浅  surface-1  ── 几乎看不出颜色的底（大面积内容区、标题条）
    surface-2  ──
    surface-3  ──  同一色相内做层次
    surface-4  ──
    main       ── 高饱和主色（hero 色带、图片区、区块背景）
    interactive ─ 更深的同色相（按钮、chip、可点元素）
深  surface-5  ── 极深（深色文字块 / 深色页脚）
```

**一套页面只用一个主题。** 用 `theme-pink` 时，`surface-1` 是淡粉 `#f7edf2`，
**不是淡蓝** —— 换主题必须连 surface 一起换，整页才会是同一个色相。

> 这是最容易搞错的一点：很多人会写「主色用主题色，底色统一用浅蓝/浅灰」，
> 结果页面像两种颜色打架。原站不是这么做的。

---

## 1. 六个钩子各用在哪

| 钩子类 | 设在 | 出现位置 |
| --- | --- | --- |
| `.main` | `background-color` | hero 的左右两根色带柱、详情页图片区、整块色底 |
| `.main-outline` | `border-color` | 该区块四周的 1px 黑描边内侧不适用；用于彩色描边块 |
| `.main-fill-svg` | `fill` | 区块内的图标、插画填色 |
| `.interactive` | `background-color` | 实心按钮、被选中的 chip |
| `.interactive-outline` | `border-color` | 空心按钮/chip 的描边 |
| `.interactive-fill-svg` | `fill` | 按钮里的图标 |

同时还有三个同名 surface 系列：`.surface-N`（底色）、`.surface-N-outline`（描边）、
`.surface-N-fill-svg`（填充）。**光写 `class="surface-1"` 不会生效** ——
必须处在带 `theme-X` 的祖先里，或者用全局默认那条梯（见 §7）。

---

## 2. 19 套主题的完整色板

| theme | main | interactive | surface-1 | surface-2 | surface-3 | surface-4 | surface-5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `blue` | `#4285f4` | `#005ac1` | `#edf0ff` | `#d8e2ff` | `#adc6ff` | `#80aaff` | `#001a41` |
| `dark-blue` | `#2e42d1` | `#2e42d1` | `#dae2ff` | `#b9c8ff` | `#919cff` | `#6a70f4` | `#050b45` |
| `light-blue` | `#76d1ff` | `#00739f` | `#daf6ff` | `#bce9ff` | `#82d1ea` | `#70bbe4` | `#102646` |
| `teal` | `#40cec3` | `#007168` | `#e8fbfb` | `#b9e6e5` | `#80d0d0` | `#51bcb8` | `#032925` |
| `emerald` | `#278c68` | `#006d46` | `#d9ffec` | `#99ecce` | `#5bd2a7` | `#3aba8c` | `#00250a` |
| `green` | `#29b571` | `#006e2c` | `#d6fad7` | `#aff8bb` | `#85dd95` | `#66c57a` | `#002108` |
| `grass` | `#70c114` | `#4b8e00` | `#e9fdc9` | `#d5f2a6` | `#bde482` | `#a9d64c` | `#143607` |
| `lime` | `#d9dd0b` | `#a79b00` | `#f6f6e3` | `#efefbe` | `#e7e896` | `#dee170` | `#3c3408` |
| `yellow` | `#fbbc05` | `#fbbc05` | `#ffefd5` | `#ffe3ad` | `#ffda7c` | `#ffc552` | — |
| `orange` | `#ff701f` | `#ff701f` | `#f7e1cb` | `#facc9b` | `#ffca93` | — | `#471406` |
| `terracotta` | `#e26c42` | `#a13f1c` | `#ffede8` | `#ffdbd0` | `#ffb59d` | `#ff8b64` | `#390c00` |
| `red` | `#f94a36` | `#b91e17` | `#ffedea` | `#ffdad5` | `#ffb4a9` | `#ff8a7a` | `#410001` |
| `salmon` | `#ed6798` | `#d81261` | `#fde4ed` | `#f9bad1` | `#f48eb3` | `#ed6798` | `#430829` |
| `pink` | `#ff9bd2` | `#b40082` | `#f7edf2` | `#ecc2d9` | `#e495c0` | `#d26dac` | `#380232` |
| `magenta` | `#ed77ff` | `#ca3be2` | `#ffebff` | `#ffd2ff` | `#f4adff` | `#de87ed` | `#2f0444` |
| `purple` | `#9961ff` | `#762de3` | `#f7edff` | `#ebdcff` | `#d4bbff` | `#bd99ff` | `#260058` |
| `brown` | `#b47943` | `#7c4c1f` | `#ebdec4` | `#e9c7ab` | `#cda889` | `#ae8864` | `#3d2210` |
| `tan` | `#d4baac` | `#765543` | `#f3eee4` | `#e8dfcf` | `#e0d1b6` | `#dfcaa9` | `#3f2b21` |
| `gray` | `#c2c2c2` | `#000` | — | `#f5f5f5` | `#e6e6e6` | `#c2c2c2` | `#262626` |

三个空格是原站**真的没定义**，不是抄漏：`yellow` 没有 `surface-5`、`orange` 没有 `surface-4`、
`gray` 没有 `surface-1`。它们会落到全局默认那条梯（§7），行为正确。

> **`interactive` 不一定比 `main` 深。** `dark-blue`、`orange`、`yellow` 三个是相等的 ——
> 这三种 `main` 本身已经足够深/足够饱和，原站直接复用，没有另造一档。

---

## 3. 哪套主题配什么内容

按色相和明度分组，写页面时先看内容气质再挑：

| 气质 | 可用主题 | 适合的内容 |
| --- | --- | --- |
| **糖果 / 轻快** | `pink` `salmon` `magenta` `purple` | 节日、纪念日、可爱向、软性话题（数据集里 `pink` 占比最高，2273/6375） |
| **科技 / 冷静** | `blue` `dark-blue` `light-blue` `teal` | 产品、工程、工具、知识类；`blue` 是默认安全牌 |
| **自然 / 生长** | `green` `emerald` `grass` | 环保、健康、季节、新事物 |
| **阳光 / 活力** | `yellow` `lime` `orange` `terracotta` | 体育、开学、庆祝、食物 |
| **大地 / 复古** | `brown` `tan` | 历史、文化、手作、怀旧 |
| **强烈 / 情绪** | `red` | 赛事、警示、强烈情感 —— 注意 `red` 很抢眼，整页大面积铺会很累 |
| **中性** | `gray` | 拿不准时的兜底；也是"有内容但不想强调颜色"的选项 |

选色的两条硬规则：

1. **有涂鸦图时，主题跟着图走。** 从图里取主色，去 §2 的表里找最近的色相。
   图是暖红就不要套 `theme-blue`。
2. **无图时按内容挑，但避开最跳的三个**（`lime` `magenta` `yellow`）。
   它们铺满整屏时非常刺眼 —— 原站只在涂鸦图本身就是那个颜色时才用。

---

## 4. 主题色上该放什么颜色的文字（实测对比度）

这条最容易被想当然写错。**结论：19 套主题的 `main` 上，18 套都是黑字对比度更高。**

| theme | main | 白字对比度 | 黑字对比度 | 该用 |
| --- | --- | --- | --- | --- |
| `blue` | `#4285f4` | 3.56 | **5.89** | 黑字 |
| `dark-blue` | `#2e42d1` | **7.46** | 2.82 | **白字**（唯一例外） |
| `light-blue` | `#76d1ff` | 1.70 | **12.33** | 黑字 |
| `teal` | `#40cec3` | 1.94 | **10.83** | 黑字 |
| `emerald` | `#278c68` | 4.17 | **5.04** | 黑字 |
| `green` | `#29b571` | 2.64 | **7.94** | 黑字 |
| `grass` | `#70c114` | 2.25 | **9.33** | 黑字 |
| `lime` | `#d9dd0b` | 1.47 | **14.30** | 黑字 |
| `yellow` | `#fbbc05` | 1.71 | **12.30** | 黑字 |
| `orange` | `#ff701f` | 2.77 | **7.59** | 黑字 |
| `terracotta` | `#e26c42` | 3.25 | **6.46** | 黑字 |
| `red` | `#f94a36` | 3.46 | **6.06** | 黑字 |
| `salmon` | `#ed6798` | 3.00 | **6.99** | 黑字 |
| `pink` | `#ff9bd2` | 1.93 | **10.87** | 黑字 |
| `magenta` | `#ed77ff` | 2.42 | **8.68** | 黑字 |
| `purple` | `#9961ff` | 3.81 | **5.51** | 黑字 |
| `brown` | `#b47943` | 3.65 | **5.76** | 黑字 |
| `tan` | `#d4baac` | 1.84 | **11.42** | 黑字 |
| `gray` | `#c2c2c2` | 1.78 | **11.79** | 黑字 |

**这就是 Doodles 一眼可辨的原因。** 它不用 Material 那套「彩底 + 白字」，
而是「彩底 + 黑字 + 黑描边」—— 因为它的主色全部是明度偏高的粉彩/中世纪色调，
黑字才是对比度高的那一侧。把彩色区块里的字改成白色，风格立刻就散了。

### `interactive` 上的文字（按钮 / chip 内部）

`interactive` 比 `main` 深，所以这里**大部分要用白字**，但有 5 个例外：

| 用**白字**（14 套） | 用**黑字**（5 套） |
| --- | --- |
| `blue` `brown` `dark-blue` `emerald` `gray` `green` `light-blue` `pink` `purple` `red` `salmon` `tan` `teal` `terracotta` | `grass` `lime` `magenta` `orange` `yellow` |

例外这 5 个的 `interactive` 平均明度仍然偏高（`lime` 是 `#a79b00`、`orange` 是 `#ff701f`），
放白字只有 2.8:1 左右，达不到 AA。

> 写按钮时的判断法：`interactive` 那一列如果看着"发亮"，就用黑字。
> 拿不准就直接取 `#000` —— 原站的按钮绝大多数是黑字或黑描边，
> 这比猜错白字安全得多。

---

## 5. 数据集 `color` 字段 → 主题

原站数据集（`doodles_data.js`）给每条涂鸦标了一个颜色标签，6375 条里只有 11 种取值。
它和 `theme-*` 是**两个命名空间**，需要一张转换表：

| 数据 `color` | 条数 | 建议 theme | 说明 |
| --- | --- | --- | --- |
| `pink` | 2273 | `pink` | 直接对应 |
| `blue` | 1887 | `blue` | 直接对应 |
| `red` | 796 | `red` | 直接对应 |
| `green` | 740 | `green` | 直接对应 |
| `cyan` | 413 | `teal` | theme 里没有 `cyan`；`teal #40cec3` 最接近。偏亮的可用 `light-blue` |
| `orange` | 69 | `orange` | 直接对应 |
| `grey` | 66 | `gray` | 注意数据用英式 `grey`，theme 用美式 `gray` |
| `yellow` | 44 | `yellow` | 直接对应 |
| `white` | 43 | `gray` | 白底无法做色带，退回中性 |
| `purple` | 40 | `purple` | 直接对应 |
| `black` | 4 | `gray` 或 `dark-blue` | 极少数；纯黑铺底会压垮页面，退回中性更稳 |

**theme 有而数据没有的**是 `brown` `dark-blue` `emerald` `grass` `light-blue` `lime`
`magenta` `salmon` `tan` `terracotta` —— 造页面时可以自由用，只是别指望能从数据字段里映射出来。

---

## 6. 检索页的 23 个色圆点

检索页筛选面板里的颜色圆点走的是另一套命名（`circle-color-bg` + `[value=…]`），
**有两个只差一个字符的陷阱值**：

| value | 色值 | 备注 |
| --- | --- | --- |
| `gray` | `#c2c2c2` | 浅灰 |
| `grey` | `#80868b` | **深灰** —— 和 `gray` 是两个不同的值 |
| `light-blue` | `#76d1ff` | 连字符版 = `theme-light-blue` 的主色 |
| `light_blue` | `#aecbfa` | **下划线版** —— 等于 `--glue-blue-200`，完全是另一个色 |
| `black` | `#000` | |
| `white` | `#fff` | |
| `tan` | `#d4baac` | |
| `brown` | `#b47943` | |
| `terracotta` | `#e26c42` | |
| `red` | `#f94a36` | |
| `orange` | `#ff701f` | |
| `yellow` | `#fbbc05` | |
| `lime` | `#d9dd0b` | |
| `grass` | `#70c114` | |
| `green` | `#29b571` | |
| `emerald` | `#278c68` | |
| `teal` | `#40cec3` | |
| `blue` | `#4285f4` | |
| `dark-blue` | `#2e42d1` | |
| `purple` | `#9961ff` | |
| `magenta` | `#ed77ff` | |
| `pink` | `#ff9bd2` | |
| `salmon` | `#ed6798` | |

除 `black` / `white` / `grey` / `light_blue` 四个之外，其余 19 个的色值
**等于同名 theme 的 `main`** —— 也就是说，色圆点就是主题色的展示卡。

> 圆点元素必须是 `<div>`，不能用 `<span>`：它靠
> `height:0 + padding-bottom:calc(100% - 2px)` 撑成正方形，
> 行内元素会忽略宽高，渲染成一条细线。

---

## 7. 没有 theme 包裹时的兜底

不在任何 `theme-*` 里的 `.surface-N` 会用到全局默认值 —— **这条梯取自 `theme-blue`**：

```css
.surface-1 { background-color: #edf0ff; }
.surface-2 { background-color: #d8e2ff; }
.surface-3 { background-color: #adc6ff; }
.surface-4 { background-color: #80aaff; }
.surface-5 { background-color: #001a41; }
```

所以 `theme-pink` 里写 `<div class="theme-pink"><div class="surface-1">` 得到淡粉，
而单独写 `<div class="surface-1">` 得到淡蓝 —— 两者都对，取决于你在不在主题里。

**中性的三级表面**是另一套，注意原站定义了两层：

| 类 | 全局 | 在 `.doodle-module` 里 |
| --- | --- | --- |
| `.neutral-surface-1` | `#fff` | `#fff` |
| `.neutral-surface-2` | `#f8f9fa` | `#fcfcfc` |
| `.neutral-surface-3` | `#f1f3f4` | `#f5f5f5` |

不要合并成一套。模块内部的底色比全局略浅，这是刻意的。

---

## 8. 在任意底色上都安全的文字色

原站给了三个语义色，跟着 `.doodle-module` 走，用在色块内部的文字上：

```css
.doodle-module .neutral_on_surface_primary   { color: #000; }     /* 主文字 */
.doodle-module .neutral_on_surface_secondary { color: #4a4a4a; }  /* 次要文字 */
.doodle-module .neutral_on_surface_inactive  { color: #c9c9c9; }  /* 禁用 */
```

注意它们**不含主题色**，是纯中性 —— 彩色区块里的辅助文字用它，不要再去取主题色的深档，
否则会和背景糊在一起。

---

## 9. 背景纹理

三种重复图案，全部用 `rgba(0,0,0,.1)` 画的，所以会**自动带上底下那层主题色的色相**：

```html
<div class="doodle-module theme-pink">
  <div class="background-pattern-square">…</div>  <!-- 方格 -->
  <div class="background-pattern-dots">…</div>    <!-- 圆点 -->
  <div class="background-pattern-stripes">…</div> <!-- 斜纹 -->
</div>
```

公共属性是 `background-position: -2px -2px; background-size: 60px 60px`。
起点偏移 −2px 是为了让图案边缘正好被区块的 1px 黑描边压住。

用纹理的地方**别再叠一层 `surface-*`** —— 纹理是画在底色上的，底色用 `.main` 或
`surface-1` 都行，但同一个元素上同时出现两种背景声明会互相覆盖。

---

## 10. 六个常见错误

1. **只换 `theme-X`，不换 surface。** 结果粉色调页面上出现淡蓝色底 —— 见 §0。
2. **在彩色区块里用白字。** 19 套里 18 套该用黑字 —— 见 §4。
3. **把 `grey` 当成 `gray` 的拼写变体。** 它们分别是 `#80868b` 和 `#c2c2c2`，
   检索页的圆点里两个都存在。同理 `light-blue` ≠ `light_blue` —— 见 §6。
4. **以为 `theme-*` 自带样式。** 它只是个空壳类，必须配 `.main` / `.interactive` /
   `.surface-N` 才生效 —— 见 §1。
5. **一套页面上混多个主题。** 原站的每张详情页只有一个主题。
   需要强调不同区块时，用 `brand-accent-1..4`（固定 Google 四色），不要再插一个 `theme-*`。
6. **把 `theme-X` 和 `surface-N` 写在同一个元素上。** 这个特别容易踩，
   因为写起来很自然：

   ```html
   <!-- ✗ 错：不会生效 -->
   <div class="theme-pink surface-5">…</div>
   ```

   原站的选择器是**后代**形式 `.theme-pink .surface-5 { … }`，同元素不匹配。
   更麻烦的是它**不会完全不生效** —— 会静默落到 §7 那条全局兜底色梯，
   而那套值是 `theme-blue` 的。于是 `surface-5` 拿到的是深蓝 `#001a41`
   而不是深粉 `#380232`，看起来"颜色不对"但完全查不出原因。

   ```html
   <!-- ✓ 对：包一层 -->
   <div class="theme-pink">
     <div class="surface-5">…</div>
   </div>
   ```

   同理，给整块上底色时也要注意：`.main`、`.surface-N` 这些都要处在
   带 `theme-*` 的**祖先**里。给承载底色的那一层加 `padding`
   （而不是给外层 `doodle-module`），否则区块之间会露出白缝。

---

## 11. 品牌强调色 `brand-accent-1..4`

固定为 Google 四色，**不随 `theme-*` 变化**，用在「这一块要强调，但它不是涂鸦主色」的地方：

| 类 | main | interactive |
| --- | --- | --- |
| `.brand-accent-1` | `#4285f4`（蓝） | `#005ac1` |
| `.brand-accent-2` | `#fbbc05`（黄） | `#fbbc05` |
| `.brand-accent-3` | `#f94a36`（红） | `#b91e17` |
| `.brand-accent-4` | `#29b571`（绿） | `#006e2c` |

它们的钩子名与 `theme-*` 完全一样（`.main` / `.interactive` / `.main-outline` …），
所以可以无缝替换一个区块的颜色来源。
