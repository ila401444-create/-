# Делает все размеры иконки для Android из трёх картинок (foreground/background/monochrome).
# Запускается автоматически при сборке: python3 icon/make.py <папка res>
import os, sys
from PIL import Image, ImageDraw
res = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__))
fg, bg, mono = [Image.open(os.path.join(here, n + '.png')).convert('RGBA') for n in ('foreground', 'background', 'monochrome')]
lay = Image.alpha_composite(bg, fg); P = lay.size[0]; vis = int(P * 72 / 108); off = (P - vis) // 2
legacy = lay.crop((off, off, off + vis, off + vis))
for name, k in {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}.items():
    d = os.path.join(res, 'mipmap-' + name); os.makedirs(d, exist_ok=True)
    a, s = int(108 * k), int(48 * k)
    for im, n in ((fg, 'foreground'), (bg, 'background'), (mono, 'monochrome')):
        im.resize((a, a), Image.LANCZOS).save(os.path.join(d, 'ic_launcher_%s.png' % n))
    sq = legacy.resize((s, s), Image.LANCZOS)
    m = Image.new('L', (s, s), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * .22), fill=255); x = sq.copy(); x.putalpha(m); x.save(os.path.join(d, 'ic_launcher.png'))
    m = Image.new('L', (s, s), 0); ImageDraw.Draw(m).ellipse([0, 0, s - 1, s - 1], fill=255); y = sq.copy(); y.putalpha(m); y.save(os.path.join(d, 'ic_launcher_round.png'))
d = os.path.join(res, 'mipmap-anydpi-v26'); os.makedirs(d, exist_ok=True)
xml = ('<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
       '    <background android:drawable="@mipmap/ic_launcher_background"/>\n    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
       '    <monochrome android:drawable="@mipmap/ic_launcher_monochrome"/>\n</adaptive-icon>\n')
for n in ('ic_launcher', 'ic_launcher_round'):
    open(os.path.join(d, n + '.xml'), 'w').write(xml)
