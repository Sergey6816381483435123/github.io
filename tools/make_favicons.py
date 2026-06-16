from PIL import Image
import os

BASE = os.path.dirname(__file__)
OUT = os.path.join(BASE, '..')
SVG = os.path.join(OUT, 'favicon.svg')

# Rendered sizes we want
sizes = [16, 32, 48, 64, 128, 180, 256]

from io import BytesIO
import subprocess

# Use rsvg-convert if available, otherwise try cairosvg

def svg_to_png(svg_path, size):
    # try using cairosvg
    try:
        import cairosvg
        with open(svg_path, 'rb') as f:
            return cairosvg.svg2png(bytestring=f.read(), output_width=size, output_height=size)
    except Exception:
        pass
    # fallback: try rsvg-convert CLI
    try:
        proc = subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg_path], capture_output=True)
        if proc.returncode == 0:
            return proc.stdout
    except Exception:
        pass
    raise RuntimeError('Не удалось конвертировать SVG в PNG — установите cairosvg или rsvg-convert')


def main():
    svg_path = SVG
    if not os.path.exists(svg_path):
        print('favicon.svg не найден')
        return
    os.makedirs(os.path.join(OUT, 'favicons'), exist_ok=True)
    png_data = {}
    for s in sizes:
        data = svg_to_png(svg_path, s)
        path = os.path.join(OUT, 'favicons', f'icon-{s}.png')
        with open(path, 'wb') as f:
            f.write(data)
        print('Wrote', path)
        png_data[s] = path

    # create favicon.ico with PIL
    ico_sizes = [(16,16),(32,32),(48,48)]
    imgs = [Image.open(png_data[s]).convert('RGBA') for s in (16,32,48) if s in png_data]
    ico_path = os.path.join(OUT, 'favicons', 'favicon.ico')
    imgs[0].save(ico_path, sizes=[(i.width, i.height) for i in imgs])
    print('Wrote', ico_path)

if __name__ == '__main__':
    main()
