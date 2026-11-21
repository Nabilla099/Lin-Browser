"""Membuat ikon (SVG/PNG/ICO) dan GIF animasi Lin Browser."""
import math
import os
from PIL import Image, ImageDraw, ImageFont

S = 1024
YEL, BLK, RED, BG = (255, 212, 0), (0, 0, 0), (255, 45, 26), (201, 201, 196)
ROOT = os.path.join(os.path.dirname(__file__), "..", "assets")


def ease_out(t):
    return 1 - (1 - t) ** 3


def pop(t):
    c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def clamp(t):
    return max(0.0, min(1.0, t))


def icon(press=0.0, stem=1.0, foot=1.0, dot=1.0, bg=None):
    im = Image.new("RGBA", (S, S), bg + (255,) if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    o = int(96 * press)
    r = lambda x0, y0, x1, y1, c: d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=c)
    r(136, 136, 956, 956, BLK)                           # bayangan
    r(40 + o, 40 + o, 860 + o, 860 + o, BLK)             # bingkai
    r(88 + o, 88 + o, 812 + o, 812 + o, YEL)             # isi
    if stem > 0:
        r(220 + o, 180 + o, 370 + o, 180 + o + int(540 * stem), BLK)
    if foot > 0:
        r(220 + o, 570 + o, 220 + o + int(280 * foot), 720 + o, BLK)
    if dot > 0:
        h = int(65 * dot)
        r(615 - h + o, 655 - h + o, 615 + h + o, 655 + h + o, RED)
    return im


def write_static():
    os.makedirs(f"{ROOT}/icons", exist_ok=True)
    base = icon()
    for s in (16, 32, 48, 64, 128, 256, 512):
        base.resize((s, s), Image.LANCZOS).save(f"{ROOT}/icons/lin-{s}.png")
    base.save(f"{ROOT}/icons/lin.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">'
           '<rect x="136" y="136" width="820" height="820" fill="#000"/>'
           '<rect x="40" y="40" width="820" height="820" fill="#000"/>'
           '<rect x="88" y="88" width="724" height="724" fill="#ffd400"/>'
           '<rect x="220" y="180" width="150" height="540" fill="#000"/>'
           '<rect x="220" y="570" width="280" height="150" fill="#000"/>'
           '<rect x="550" y="590" width="130" height="130" fill="#ff2d1a"/></svg>')
    open(f"{ROOT}/icons/lin.svg", "w").write(svg)


FONT_PATHS = [
    "/usr/share/fonts/opentype/inter/Inter-Black.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def load_font(px):
    for f in FONT_PATHS:
        if os.path.exists(f):
            return ImageFont.truetype(f, px)
    return ImageFont.load_default()


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def in_out(t):
    t = clamp(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def seg(t, a, b):
    """Progres 0..1 untuk t di antara a dan b (detik)."""
    return clamp((t - a) / (b - a))


def out_back(t, k=1.9):
    t = clamp(t)
    return 1 + (k + 1) * (t - 1) ** 3 + k * (t - 1) ** 2


FPS, DUR = 25, 6.8
SS = 2                      # supersampling untuk tepi halus
OUT = 560                   # ukuran akhir GIF (px)
BG_GIF = (236, 235, 230)


def render(t):
    W = OUT * SS
    im = Image.new("RGB", (W, W), BG_GIF)
    d = ImageDraw.Draw(im)
    isz = int(300 * SS)                     # ukuran ikon
    ox, oy = (W - isz) // 2, int(64 * SS)
    u = isz / S                             # satuan -> px
    R = lambda x0, y0, x1, y1, c: d.rectangle(
        [round(ox + x0 * u), round(oy + y0 * u), round(ox + x1 * u) - 1, round(oy + y1 * u) - 1], fill=c)

    # --- linimasa ---
    appear = out_back(seg(t, 0.15, 0.80), 1.2)           # tile muncul (skala)
    lift = in_out(seg(t, 0.75, 1.25))                    # tile terangkat
    stem = in_out(seg(t, 1.30, 1.95))
    foot = in_out(seg(t, 1.85, 2.35))
    dot = out_back(seg(t, 2.30, 2.90), 2.4)
    ring = seg(t, 2.40, 3.20)
    word = ease_out(seg(t, 3.00, 3.80))
    # idle: tile "bernapas" pelan
    idle = (1 - math.cos(2 * math.pi * seg(t, 3.9, 5.5))) / 2 if 3.9 <= t <= 5.5 else 0
    # keluar
    word_out = in_out(seg(t, 5.55, 6.05))
    dot_out = in_out(seg(t, 5.70, 6.05))
    foot_out = in_out(seg(t, 5.85, 6.20))
    stem_out = in_out(seg(t, 6.00, 6.40))
    press_out = in_out(seg(t, 6.35, 6.60))
    gone = in_out(seg(t, 6.55, 6.80))

    press = (1 - lift) + press_out - idle * 0.07
    press = max(-0.12, min(1.0, press))
    scale = appear * (1 - gone)
    if scale <= 0.001:
        return im.resize((OUT, OUT), Image.LANCZOS)

    # transformasi: skala di sekitar pusat tile
    cx, cy = 450, 450
    def T(v, c):
        return c + (v - c) * scale
    def box(x0, y0, x1, y1, off=0):
        return T(x0 + off, cx), T(y0 + off, cy), T(x1 + off, cx), T(y1 + off, cy)

    o = 96 * press
    # bayangan (tetap di posisi terangkat)
    R(*box(136, 136, 956, 956), BLK)
    # bingkai + isi
    R(*box(40, 40, 860, 860, o), BLK)
    R(*box(88, 88, 812, 812, o), YEL)

    st = stem * (1 - stem_out)
    if st > 0.002:
        R(*box(220, 180, 370, 180 + 540 * st, o), BLK)
    ft = foot * (1 - foot_out)
    if ft > 0.002:
        R(*box(220, 570, 220 + 280 * ft, 720, o), BLK)

    # titik merah + cincin "ping"
    if 0 < ring < 1 and dot_out == 0:
        r_half = 65 + 85 * ease_out(ring)
        th = 14 * (1 - ring)
        col = mix(YEL, RED, (1 - ring) ** 1.3)
        if th > 0.6:
            R(*box(615 - r_half, 655 - r_half, 615 + r_half, 655 + r_half, o), col)
            R(*box(615 - r_half + th, 655 - r_half + th, 615 + r_half - th, 655 + r_half - th, o), YEL)
            # pulihkan huruf L yang tertimpa isi cincin
            if st > 0.002:
                R(*box(220, 180, 370, 180 + 540 * st, o), BLK)
            if ft > 0.002:
                R(*box(220, 570, 220 + 280 * ft, 720, o), BLK)
    dscale = max(0.0, dot) * (1 - dot_out)
    if dscale > 0.01:
        h = 65 * dscale
        R(*box(615 - h, 655 - h, 615 + h, 655 + h, o), RED)

    # wordmark
    wm_vis = word * (1 - word_out)
    if wm_vis > 0.002:
        font = load_font(int(48 * SS))
        text, track = "LIN BROWSER", 8 * SS
        widths = [d.textlength(ch, font=font) for ch in text]
        total = sum(widths) + track * (len(text) - 1)
        tx = (W - total) / 2
        ty = int(404 * SS)
        layer = Image.new("RGB", (W, int(120 * SS)), BG_GIF)
        ld = ImageDraw.Draw(layer)
        x = tx
        for ch, w in zip(text, widths):
            ld.text((x, 0), ch, font=font, fill=BLK)
            x += w + track
        bar_y = int(74 * SS)
        ld.rectangle([tx, bar_y, tx + total, bar_y + 6 * SS], fill=BLK)
        ld.rectangle([tx + total * 0.0, bar_y, tx + total * 0.14, bar_y + 6 * SS], fill=YEL)
        # wipe: tampil dari kiri; saat keluar, menghilang dari kiri juga
        left = tx - 4 + (total + 8) * word_out
        right = tx - 4 + (total + 8) * word
        if right > left + 1:
            crop = layer.crop((int(left), 0, int(right), layer.size[1]))
            im.paste(crop, (int(left), ty))
    return im.resize((OUT, OUT), Image.LANCZOS)


def write_gif():
    n = int(FPS * DUR)
    frames = [render(i / FPS) for i in range(n)]
    # palet bersama dari beberapa frame kunci agar tidak berkedip
    keys = [frames[int(FPS * s)] for s in (1.0, 2.0, 2.6, 3.5, 4.6)]
    mosaic = Image.new("RGB", (OUT * len(keys), OUT))
    for i, k in enumerate(keys):
        mosaic.paste(k, (i * OUT, 0))
    pal = mosaic.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    durs = [int(1000 / FPS)] * n
    durs[-1] = 600                         # jeda kecil sebelum mengulang
    q[0].save(os.path.join(ROOT, "lin-browser.gif"), save_all=True, append_images=q[1:],
              duration=durs, loop=0, optimize=False)


def write_android():
    """Ikon peluncur Android: bitmap per densitas + ikon adaptif (vektor)."""
    out = f"{ROOT}/android"
    base = icon()
    for dens, size in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
        d = f"{out}/mipmap-{dens}"
        os.makedirs(d, exist_ok=True)
        im = base.resize((size, size), Image.LANCZOS)
        im.save(f"{d}/ic_launcher.png")
        im.save(f"{d}/ic_launcher_round.png")

    box, off = 48.0, 30.0                      # ikon 48 dari 108 (zona aman adaptif)
    k = box / 916.0
    pt = lambda v: round(off + (v - 40) * k, 2)
    def rect(x0, y0, x1, y1, color):
        return (f'  <path android:fillColor="{color}" android:pathData="M{pt(x0)},{pt(y0)}'
                f'H{pt(x1)}V{pt(y1)}H{pt(x0)}Z"/>\n')
    body = (rect(136, 136, 956, 956, "#000000") + rect(40, 40, 860, 860, "#000000") +
            rect(88, 88, 812, 812, "#FFD400") + rect(220, 180, 370, 720, "#000000") +
            rect(220, 570, 500, 720, "#000000") + rect(550, 590, 680, 720, "#FF2D1A"))
    head = ('<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
            '    android:width="108dp" android:height="108dp"\n'
            '    android:viewportWidth="108" android:viewportHeight="108">\n')
    full_bg = '  <path android:fillColor="#C9C9C4" android:pathData="M0,0h108v108h-108z"/>\n'
    open(f"{out}/ic_launcher_foreground.xml", "w").write(head + full_bg + body + "</vector>\n")
    mono = "".join(rect(*r_, "#000000") for r_ in (
        (40, 40, 860, 88), (40, 812, 860, 860), (40, 88, 88, 812), (812, 88, 860, 812),
        (220, 180, 370, 720), (220, 570, 500, 720), (550, 590, 680, 720)))
    open(f"{out}/ic_launcher_monochrome.xml", "w").write(head + mono + "</vector>\n")
    open(f"{out}/ic_launcher_background.xml", "w").write(
        head + '  <path android:fillColor="#C9C9C4" android:pathData="M0,0h108v108h-108z"/>\n</vector>\n')


if __name__ == "__main__":
    write_static()
    write_android()
    write_gif()
