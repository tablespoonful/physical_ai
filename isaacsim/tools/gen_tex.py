"""FR3 外装用の tileable テクスチャを手続き生成する (2048px、1 枚 1m)。"""
import numpy as np, sys
from PIL import Image, ImageDraw
out = sys.argv[1]; N = 2048; rng = np.random.default_rng(3)
fx = np.fft.fftfreq(N)[:, None]; fy = np.fft.fftfreq(N)[None, :]; F = np.sqrt(fx**2 + fy**2)
def band(lo_px, hi_px):
    """波長 lo_px〜hi_px の周期ノイズ。平均 0、標準偏差 1。"""
    w = np.exp(-(F * lo_px) ** 2 / 2) * (1 - np.exp(-(F * hi_px) ** 2 / 2))
    n = np.fft.ifft2(np.fft.fft2(rng.standard_normal((N, N))) * w).real
    return (n - n.mean()) / n.std()
def blur(a, s):
    return np.fft.ifft2(np.fft.fft2(a) * np.exp(-2 * (np.pi * F * s) ** 2)).real
def strokes(count, lmin, lmax, width):
    S = 2; im = Image.new("L", (N * S, N * S), 0); d = ImageDraw.Draw(im)
    for _ in range(count):
        x, y = rng.uniform(0, N, 2); a = rng.uniform(0, 2 * np.pi); L = rng.uniform(lmin, lmax); c = rng.normal(0, 0.0025)
        pts = []
        for i in range(24):
            pts.append((x, y)); x += np.cos(a) * L / 24; y += np.sin(a) * L / 24; a += c * L / 24
        v = int(rng.uniform(90, 255))
        for ox in (-N, 0, N):
            for oy in (-N, 0, N):
                d.line([((p[0] + ox) * S, (p[1] + oy) * S) for p in pts], fill=v, width=width)
    return np.asarray(im.resize((N, N), Image.LANCZOS), dtype=np.float32) / 255
fine = strokes(150, 14, 130, 5); long_ = strokes(16, 160, 620, 6)
scratch = np.clip(blur(fine * 0.7 + long_ * 0.9, 0.7), 0, 1)
smudge = band(60, 700); grain = band(1.5, 5); peel = band(4, 14)
wear = np.clip(band(160, 900) - 1.2, 0, 1)            # 局所的な擦れ
rough = np.clip(0.42 + 0.035 * smudge + 0.012 * grain + 0.06 * wear + 0.26 * scratch, 0.05, 0.95)
Image.fromarray((rough * 255).astype(np.uint8), "L").save(f"{out}/fr3_shell_roughness.png")
h = 0.5 * peel + 0.12 * grain - 3.0 * scratch      # 高さ。傷は凹み
dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) / 2; dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) / 2
s = 0.045; nx, ny = -dx * s, dy * s; nz = np.ones_like(nx); l = np.sqrt(nx**2 + ny**2 + nz**2)   # +Y (OpenGL)
Image.fromarray((np.stack([nx / l, ny / l, nz / l], -1) * 0.5 + 0.5).clip(0, 1).__mul__(255).astype(np.uint8), "RGB").save(f"{out}/fr3_shell_normal.png")
lin = np.clip(0.78 + 0.008 * smudge - 0.035 * wear - 0.05 * scratch, 0, 1)[..., None] * np.array([1.0, 1.0, 0.985])
srgb = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)
Image.fromarray((srgb.clip(0, 1) * 255).astype(np.uint8), "RGB").save(f"{out}/fr3_shell_basecolor.png")
print("rough mean", round(float(rough.mean()), 3), "base lin mean", round(float(lin.mean()), 3), "scratch cov %", round(float((scratch > 0.2).mean() * 100), 2))
