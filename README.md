# google-doodles-style

复刻 [Google Doodles](https://doodles.google) 网页风格的 **Agent Skill** ——
把 Google Glue 设计系统的令牌、配色法则和页面骨架，直接用到你自己的页面上。

不是"凭印象仿"，规格全部来自原站的真实构建产物：19 套主题色的完整六档色梯
（含 WCAG 对比度实测）、`glue-page` / `glue-header` / `glue-footer` / `glue-carousel`
的类名与 DOM 层级、600 / 1024 / 1440 三档断点的实测尺寸。

---

## 装法

**WorkBuddy / Claude Code（推荐）** —— 把整个目录放进 skills 目录即可：

```bash
git clone https://github.com/Z-V-I/google-doodles-style
# ~/.workbuddy/skills/google-doodles-style      （用户级）
# <项目>/.workbuddy/skills/google-doodles-style （项目级）
```

**只想看看效果** —— 直接双击打开，零依赖、零网络：

| 文件 | 内容 |
| --- | --- |
| `assets/palette.html` | 19 套主题 × 每套 6 档色梯的可视化色板（**改配色前先开它**） |
| `assets/preview-home.html` | 首页骨架预览 |
| `assets/preview-doodle-detail.html` | 详情页骨架预览 |
| `assets/preview-library.html` | 检索页骨架预览 |

**先补一次图标**（见下文「图标 sprite」）：

```bash
python assets/fetch-icons.py
```

---

## 两档还原度

| 档位 | 做法 | 还原度 | 依赖 |
| --- | --- | --- | --- |
| **A · 自包含**（默认） | `assets/doodles-style.css` + 模板 + `assets/fonts/` | 布局 / 配色 / 尺寸 / 字体全到位，差原站 JS 驱动的动效 | 零依赖，完全离线 |
| **B · 像素级** | 换成 `assets/vendor/glue.min.css`（原站构建产物本体，548 KB / 4020 条规则） | 逐像素一致 | 同样离线 |

两档**不要混用**，原站 CSS 与自带 CSS 有大量同名规则，叠加会互相覆盖。
换档方式是换 `<link>`，不是两个都链。

---

## 目录

```
SKILL.md                  入口：工作流、9 条风格硬规则、检查清单
references/
  ├── design-tokens.md    令牌实测值（灰阶 / 色阶 / 字体 / 排版 / 布局 / 阴影）
  ├── palette.md          ★ 19 套主题的六档色梯 + 选色法则 + 对比度实测
  ├── components.md       每个组件的 DOM 结构 + 类名 + 踩过的坑
  └── real-assets.md      资源清单、授权边界、B 档切换步骤
assets/
  ├── doodles-style.css   A 档自包含样式表（968 条规则 / 89 个媒体查询）
  ├── palette.html        色板可视化页
  ├── build_preview.py    由 templates + css 重新生成预览页
  ├── fetch-icons.py      补齐两个图标 sprite
  ├── preview-*.html      三个预览页
  ├── templates/          外壳 + 首页 / 详情页 / 检索页主体
  ├── fonts/              Google Sans 全字重：fonts.css + 200 个 woff2 语言子集
  └── vendor/             B 档原站构建产物：glue.min.css + 品牌字标
```

---

## 图标 sprite（需要单独补一次）

`assets/vendor/glue-icons.svg`（16 KB）与 `icons.svg`（148 KB）是 Google 图标资产，
**本仓库刻意没有收录**，对应的 `.gitignore` 也已经写死，跑完脚本不会被误提交。

缺了它们，页面上每个 `<use href="…#…">` 都会**静默取不到** —— 不报错、不提示，
只是图标位置空一块（布局、配色、字体都不受影响）。

```bash
python assets/fetch-icons.py
```

脚本从上游镜像仓库取回这两个文件、**校验 sha256 后**才落盘，校验不过就拒绝写入。
只用标准库，不需要 `pip install`。

---

## 配色是这个 skill 的重点

真正决定"像不像"的不是 Google logo 那四个颜色，而是那 19 套 `theme-*` 主题色，
**尤其是每套自带的 5 档 surface 色梯**：

- `surface-1..5` 会**跟着 `theme-*` 变**。`theme-pink` 的 `surface-1` 是淡粉
  `#f7edf2`，不是淡蓝。用 `theme-pink` 却留着默认淡蓝，页面会像两种颜色打架。
- **彩色区块里用黑字。** 19 套主题的 `main` 上，18 套都是黑字对比度更高，
  只有 `dark-blue` 例外。这是 Doodles 与 Material 观感分家的地方。
- 每套主题共 **21 个钩子**，且选项器是**后代选择器**（`.theme-pink .surface-5`）——
  `.theme-*` 和 `.surface-*` 写在同一个元素上**不会匹配**，会静默落回全局兜底色梯。

完整色值与选色建议见 [`references/palette.md`](references/palette.md)。

---

## 授权与来源

- **本仓库自身的代码与文档是 MIT**（见 [`LICENSE`](LICENSE)），
  与上游 [google-doodles-mirror](https://github.com/Z-V-I/google-doodles-mirror) 一致。
- **Google Sans / Product Sans 字体、Google logo、原站构建产物 CSS、
  Doodles 涂鸦图片，都是 Google 的资产，MIT 不覆盖它们。**
  本仓库带了字体与主样式表是为了让复刻够像、且能完全离线；
  自用与研究没问题，**商业分发或对授权敏感的场景，删掉 `assets/fonts/` 与
  `assets/vendor/` 即可** —— A 档的 `doodles-style.css` 不依赖它们
  （字体只是回退到 Arial，布局与配色完全不受影响）。
- 更多原始出处与取法见 [`references/real-assets.md`](references/real-assets.md) §1。
- 本项目只是对公开页面风格的规格整理，**与 Google 无任何关联，未获其授权或背书**。
