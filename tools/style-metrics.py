#!/usr/bin/env python3
"""风格度量：给一组参考图（正面或负面样本）算同一口径的量化画像。

用途：调整 SKILL 里「反 AI 味参数卡」的阈值时，用新样本重跑本脚本，别凭感觉改。
依赖：Pillow、numpy。

用法：
    python tools/style-metrics.py <图片目录或文件...>

各项含义（对应参数卡）：
    线宽          AI 感样本通常是 1-2px 且几乎等宽；参数卡要求外轮廓 = 短边 0.4%
    灰度三段      中间调占比高 + 极暗占比低 = 没有暗部重音
    局部对比度变异 越小说明全图对比度越均匀 = 缺少焦点层次
    平滑过渡占比   相邻像素差 1-3 的占比高 = 柔化糊感
    细节密度对比   背景高于主体 = 细节堆料
    镜像差异       越小越对称 = 居中对称构图
"""

import pathlib
import sys

import numpy as np
from PIL import Image

BLOCK = 32


def line_width(g):
    gx = np.abs(np.diff(g, axis=1))
    gy = np.abs(np.diff(g, axis=0))
    thr = np.percentile(np.concatenate([gx.ravel(), gy.ravel()]), 97)
    widths = []
    for row in gx >= thr:
        if not row.any():
            continue
        d = np.diff(np.concatenate([[0], row.view(np.int8), [0]]))
        widths.extend((np.where(d == -1)[0] - np.where(d == 1)[0]).tolist())
    w = np.array([x for x in widths if x > 0])
    return w


def metrics(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    g = np.asarray(im.convert("L")).astype(np.float32)
    h, w = g.shape
    short = min(h, w)

    d = np.concatenate([np.abs(np.diff(g, axis=1)).ravel(), np.abs(np.diff(g, axis=0)).ravel()])
    lw = line_width(g)

    q = (a // 16).astype(np.int32)
    codes = q[..., 0] * 256 + q[..., 1] * 16 + q[..., 2]
    counts = np.bincount(codes.ravel())
    cum = np.cumsum(np.sort(counts)[::-1]) / counts.sum()
    n90 = int(np.searchsorted(cum, 0.90) + 1)

    stds = np.array([
        g[i:i + BLOCK, j:j + BLOCK].std()
        for i in range(0, h - BLOCK, BLOCK)
        for j in range(0, w - BLOCK, BLOCK)
    ])

    maxc, minc = a.max(axis=2), a.min(axis=2)
    sat = np.where(maxc == 0, 0, (maxc - minc) / np.maximum(maxc, 1))

    print("--- %s  %dx%d" % (path.name, w, h))
    print("  线宽: 均值 %.2f 中位 %.1f p90 %.1f 最大 %d  (短边 %.1f%%)"
          % (lw.mean(), np.median(lw), np.percentile(lw, 90), lw.max(), 100 * np.median(lw) / short))
    print("  灰度三段: 极暗(<60) %.1f%%  中间调 %.1f%%  亮部(>200) %.1f%%"
          % (100 * (g < 60).mean(), 100 * ((g >= 60) & (g <= 200)).mean(), 100 * (g > 200).mean()))
    print("  局部对比度: 均值 %.1f 变异 %.2f" % (stds.mean(), stds.std() / max(stds.mean(), 1e-6)))
    print("  过渡: 平滑(差1-3) %.1f%%  硬边(>25) %.1f%%" % (100 * ((d >= 1) & (d <= 3)).mean(), 100 * (d > 25).mean()))
    print("  细节密度: 中心 %.2f / 顶部 %.2f" % (
        np.abs(np.diff(g[h // 4:3 * h // 4, w // 4:3 * w // 4], axis=1)).mean(),
        np.abs(np.diff(g[: h // 4, :], axis=1)).mean()))
    print("  镜像差异: 左右 %.1f 上下 %.1f" % (np.abs(a - a[:, ::-1]).mean(), np.abs(a - a[::-1, :]).mean()))
    print("  色阶块: 覆盖 90%% 像素需 %d 块   饱和均值 %.0f  明度均值 %.0f  高饱和 %.1f%%  近灰 %.1f%%"
          % (n90, sat.mean() * 255, g.mean(), 100 * (sat > 0.6).mean(), 100 * (sat < 0.15).mean()))


def main(argv):
    targets = []
    for arg in argv:
        p = pathlib.Path(arg)
        targets.extend(sorted(p.glob("*")) if p.is_dir() else [p])
    imgs = [p for p in targets if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".bmp")]
    if not imgs:
        print(__doc__)
        return 2
    for p in imgs:
        metrics(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
