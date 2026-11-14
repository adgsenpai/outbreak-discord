#!/usr/bin/env python3
"""Render docs/social-preview.png (GitHub social preview, 1280x640).

Usage: companion/.venv/bin/python docs/make_social_preview.py . docs/social-preview.png
Then upload it under the repo Settings -> Social preview.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(sys.argv[1])
OUT = Path(sys.argv[2])
W, H = 1280, 640
STAGES = ['outbreak', 'below_freezing_point', 'the_hive', 'hellfire', 'decisions_decisions',
          'wild_things', 'underbelly', 'flashback', 'desperate_times', 'end_of_the_road']
F = '/usr/share/fonts/truetype/ubuntu/'
bold = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf', s)
med = lambda s: ImageFont.truetype(F + 'Ubuntu-M.ttf', s)
reg = lambda s: ImageFont.truetype(F + 'Ubuntu-R.ttf', s) if Path(F + 'Ubuntu-R.ttf').exists() else ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', s)

# Background: 5x2 mosaic of the stage title cards, blurred and darkened.
bg = Image.new('RGB', (W, H))
tw, th = W // 5, H // 2
for i, k in enumerate(STAGES):
    im = Image.open(REPO / 'assets/real_stage_images' / f'{k}.png').convert('RGB')
    s = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.Resampling.LANCZOS)
    l, t = (im.width - tw) // 2, (im.height - th) // 2
    bg.paste(im.crop((l, t, l + tw, t + th)), ((i % 5) * tw, (i // 5) * th))
bg = bg.filter(ImageFilter.GaussianBlur(3))

# Left-to-right dark gradient so the text is readable, lighter on the right.
shade = Image.new('L', (W, H))
d = ImageDraw.Draw(shade)
for x in range(W):
    a = 235 if x < 560 else int(235 - (x - 560) / (W - 560) * 110)
    d.line([(x, 0), (x, H)], fill=a)
canvas = Image.composite(Image.new('RGB', (W, H), (12, 10, 14)), bg, shade).convert('RGBA')
draw = ImageDraw.Draw(canvas)

# Accent bar
RED = (214, 48, 49)
draw.rectangle([80, 120, 86, 520], fill=RED)

x = 112
draw.text((x, 118), 'RESIDENT EVIL OUTBREAK  ·  FILE #1 & #2', font=med(22), fill=(235, 90, 90))
draw.text((x, 150), 'Outbreak Discord', font=bold(62), fill=(255, 255, 255))
draw.text((x, 226), 'Rich Presence', font=bold(62), fill=(255, 255, 255))
for i, line in enumerate(['Shows the stage you’re playing on', 'outbreakweb.com as your Discord status,', 'with stage art, character and room.']):
    draw.text((x, 330 + i * 34), line, font=reg(26), fill=(205, 205, 215))

# Pills
px, py = x, 452
for label in ['Chrome extension', 'Linux companion', 'All 10 stages']:
    f = med(20)
    w = draw.textlength(label, font=f)
    pill = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle([px, py, px + w + 32, py + 40], radius=20, fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), width=1)
    canvas.alpha_composite(pill)
    draw.text((px + 16, py + 9), label, font=f, fill=(240, 240, 245))
    px += w + 32 + 12

draw.text((x, 522), 'github.com/adgsenpai/outbreak-discord', font=reg(19), fill=(150, 150, 165))

# Right: two real Discord activity cards with a soft shadow.
def card(name, scale):
    im = Image.open(REPO / 'docs/screenshots' / f'{name}.png').convert('RGBA')
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=14, fill=255)
    im.putalpha(m)
    return im, m

for (name, (cx, cy)) in [('hellfire', (770, 110)), ('decisions_decisions', (720, 330))]:
    im, m = card(name, 1.05)
    sh = Image.new('RGBA', (im.width + 80, im.height + 80), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 170), (40, 50), m)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(sh, (cx - 40, cy - 40))
    canvas.alpha_composite(im, (cx, cy))

canvas.convert('RGB').save(OUT, optimize=True)
print(OUT, canvas.size)
