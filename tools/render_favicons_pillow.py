#!/usr/bin/env python3
from PIL import Image, ImageDraw
import os

BASE = os.path.dirname(__file__)
OUT = os.path.abspath(os.path.join(BASE, '..'))
ICONS_DIR = os.path.join(OUT, 'favicons')
os.makedirs(ICONS_DIR, exist_ok=True)


def cubic_bezier(p0, p1, p2, p3, t):
    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    return (x, y)


def bezier_points(p0, p1, p2, p3, steps=30):
    return [cubic_bezier(p0, p1, p2, p3, i / steps) for i in range(0, steps + 1)]


def draw_icon(size):
    scale = size / 64.0
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_card = (13, 15, 23, 255)
    accent = (202, 162, 255, 255)  # #caa2ff
    accent2 = (138, 227, 217, 255)  # #8ae3d9

    # Rounded card rectangle (based on SVG)
    rect_x = 6 * scale
    rect_y = 4 * scale
    rect_w = 52 * scale
    rect_h = 56 * scale
    rx = 6 * scale
    left = rect_x
    top = rect_y
    right = rect_x + rect_w
    bottom = rect_y + rect_h

    draw.rounded_rectangle([left, top, right, bottom], radius=rx, fill=bg_card)
    stroke_w = max(1, int(round(size * 0.03)))
    draw.rounded_rectangle([left, top, right, bottom], radius=rx, outline=accent, width=stroke_w)

    # Moon: two circles
    cx = 32 * scale
    cy = 24 * scale
    r_outer = 9 * scale
    r_inner = 7 * scale
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=accent)
    draw.ellipse([36 * scale - r_inner, 22 * scale - r_inner, 36 * scale + r_inner, 22 * scale + r_inner], fill=bg_card)

    # Star / sparkle polygon
    star_points = [(44, 14), (45.2, 17), (48, 17), (46, 19), (46.6, 22), (44, 20), (41.4, 22), (42, 19), (40, 17), (42.8, 17)]
    star_points = [(x * scale, y * scale) for x, y in star_points]
    draw.polygon(star_points, fill=accent2)

    # Decorative bezier curve
    p0 = (20 * scale, 44 * scale)
    p1 = (28 * scale, 40 * scale)
    p2 = (36 * scale, 40 * scale)
    p3 = (44 * scale, 44 * scale)
    pts = bezier_points(p0, p1, p2, p3, steps=28)
    curve_width = max(1, int(round(size * 0.03)))
    draw.line(pts, fill=(202, 162, 255, 200), width=curve_width)

    return img


def main():
    sizes = [16, 32, 48, 64, 128, 180, 256]
    paths = {}
    for s in sizes:
        img = draw_icon(s)
        path = os.path.join(ICONS_DIR, f'icon-{s}.png')
        img.save(path, optimize=True)
        print('Wrote', path)
        paths[s] = path

    # create favicon.ico (contains multiple sizes)
    ico_path = os.path.join(ICONS_DIR, 'favicon.ico')
    base_img = Image.open(paths[256])
    base_img.save(ico_path, sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print('Wrote', ico_path)


if __name__ == '__main__':
    main()
