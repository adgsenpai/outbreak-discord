#!/usr/bin/env python3
"""Split the 4-row stage title-card grid (3/3/3/1 layout) into the 10 named stage images.

Usage: python3 crop_stage_grid.py path/to/stage_grid.png
Writes assets/real_stage_images/<stage>.png, then run import_real_stage_art.py.
"""
import sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE / 'assets' / 'real_stage_images'

# Tile boxes measured on the 774x754 reference grid; scaled to the actual image size.
REF_W, REF_H = 774, 754
COLS = [(12, 252), (268, 509), (523, 765)]
ROWS = [(12, 182), (199, 369), (388, 557), (574, 743)]
LAYOUT = [
    ['outbreak', 'below_freezing_point', 'the_hive'],
    ['hellfire', 'decisions_decisions', 'wild_things'],
    ['underbelly', 'flashback', 'desperate_times'],
    [None, 'end_of_the_road', None],
]
INSET = 4  # trim the blue frame


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Image.open(sys.argv[1]).convert('RGB')
    sx, sy = src.width / REF_W, src.height / REF_H
    OUT.mkdir(parents=True, exist_ok=True)
    for r, row in enumerate(LAYOUT):
        y0, y1 = ROWS[r]
        for c, key in enumerate(row):
            if not key:
                continue
            x0, x1 = COLS[c]
            box = (round((x0 + INSET) * sx), round((y0 + INSET) * sy),
                   round((x1 - INSET) * sx), round((y1 - INSET) * sy))
            dest = OUT / f'{key}.png'
            src.crop(box).save(dest)
            print('WROTE', dest)


if __name__ == '__main__':
    main()
