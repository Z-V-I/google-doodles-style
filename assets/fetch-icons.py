#!/usr/bin/env python3
"""补齐两个图标 sprite。

本仓库刻意不带 `assets/vendor/glue-icons.svg` 与 `assets/vendor/icons.svg`
（Google 图标资产，单独排除）。模板和预览页里的 `<use href="/static/…#…">`
需要它们，缺了不会报错 —— 只是图标位置空一块。

    python assets/fetch-icons.py

从上游镜像仓库 google-doodles-mirror 取回、**校验 sha256 后**再落盘。
校验不过就拒绝写入并退出非 0，不会留下半成品文件。

只用标准库，无需 pip install。
"""

from __future__ import annotations

import gzip
import hashlib
import pathlib
import sys
import urllib.error
import urllib.request

# 上游：github.com/Z-V-I/google-doodles-mirror
# _google_clone/ 是未经改造的原站副本，两个 sprite 同时存在于 _clone_search/。
_RAW = (
    "https://raw.githubusercontent.com/"
    "Z-V-I/google-doodles-mirror/main/_google_clone/"
)

TARGETS = [
    {
        "name": "glue-icons.svg",
        "remote": "0f99e02819f0bba398fbcbeff94c8a0eb698e988148884f15cb92c39c17487d7.glue-icons.svg",
        "size": 15738,
        "sha256": "5a3c1c892187f493e32b51a241a4069520147e0294062a5ac67f930774d8cba5",
        "note": "通用图标（44 个 id）",
    },
    {
        "name": "icons.svg",
        "remote": "37ae077da8a25b6950c926233ed752617048c50792204bc7b9d6332bbb7a3a5f.icons.svg",
        "size": 149861,
        "sha256": "37ae077da8a25b6950c926233ed752617048c50792204bc7b9d6332bbb7a3a5f",
        "note": "Doodles 专用图标（34 个 id）",
    },
]

DEST = pathlib.Path(__file__).resolve().parent / "vendor"


def fetch(url: str, timeout: int = 90) -> bytes:
    """取回字节流。

    某些代理会**透明地** gzip 压缩响应体却不在 Content-Encoding 里声明，
    这种情况下 urllib 不会自动解压，所以这里按魔数自己判断。
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "google-doodles-style/fetch-icons", "Accept-Encoding": "identity"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    if raw[:2] == b"\x1f\x8b":  # gzip 魔数
        raw = gzip.decompress(raw)
    return raw


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    failed = 0

    for t in TARGETS:
        out = DEST / t["name"]
        print(f"[{t['name']}] {t['note']}")

        if out.exists():
            have = out.read_bytes()
            if hashlib.sha256(have).hexdigest() == t["sha256"]:
                print("  ✓ 已存在且校验一致，跳过")
                continue
            print(f"  ! 已存在的文件校验不符（{len(have)} B），将重新下载")

        try:
            blob = fetch(_RAW + t["remote"])
        except urllib.error.HTTPError as e:
            print(f"  ✗ 下载失败：HTTP {e.code} {e.reason}")
            failed += 1
            continue
        except (urllib.error.URLError, OSError) as e:
            print(f"  ✗ 下载失败：{e}")
            failed += 1
            continue

        got = hashlib.sha256(blob).hexdigest()
        if len(blob) != t["size"] or got != t["sha256"]:
            print(f"  ✗ 校验不过，拒绝写入（上游可能已改动）")
            print(f"      期望 {t['size']} B / {t['sha256']}")
            print(f"      实得 {len(blob)} B / {got}")
            failed += 1
            continue

        out.write_bytes(blob)  # 只有校验通过才落盘
        print(f"  ✓ 已写入 {out}（{len(blob)} B）")

    print()
    if failed:
        print(f"{failed} 个文件没拿到。检查网络，或按 real-assets.md §0.2 手动取。")
        return 1

    print("图标 sprite 就绪。跑 `python assets/build_preview.py` 可重新生成预览页。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
