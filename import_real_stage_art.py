#!/usr/bin/env python3
"""Import actual user-provided game screenshots into Discord asset files. No AI artwork."""
from pathlib import Path
from PIL import Image, ImageOps
STAGES = ['outbreak', 'below_freezing_point', 'the_hive', 'hellfire', 'decisions_decisions', 'wild_things', 'underbelly', 'flashback', 'desperate_times', 'end_of_the_road']
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'assets'/'real_stage_images'
TARGET=HERE/'assets'

def main():
    found=0
    for key in STAGES:
        candidates=[SOURCE/(key+ext) for ext in ('.png','.jpg','.jpeg','.webp')]
        original=next((p for p in candidates if p.exists()),None)
        if not original:
            print(f'MISSING: {key} (provide a genuine gameplay screenshot)')
            continue
        try:
            with Image.open(original) as image:
                image=ImageOps.exif_transpose(image).convert('RGB')
                # Discord artwork is best as square; pad without cropping gameplay.
                image.thumbnail((1024,1024),Image.Resampling.LANCZOS)
                square=Image.new('RGB',(1024,1024),(12,12,15))
                square.paste(image,((1024-image.width)//2,(1024-image.height)//2))
                dest=TARGET/(key+'.png')
                square.save(dest,optimize=True)
                print('READY:',dest)
                found+=1
        except Exception as exc:
            print(f'ERROR: {original}: {exc}')
    print(f'Imported {found}/{len(STAGES)} real stage screenshots')
if __name__=='__main__':main()
