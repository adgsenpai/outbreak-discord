#!/usr/bin/env python3
"""Import actual user-provided game screenshots into Discord asset files. No AI artwork."""
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
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
                # Discord artwork is square. Scale the screenshot (up or down) to fit the
                # full 1024px without cropping it, and fill the leftover bands with a
                # darkened, blurred copy of the same image instead of flat black.
                scale=1024/max(image.width,image.height)
                fit=image.resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
                cover_scale=1024/min(image.width,image.height)
                bg=image.resize((round(image.width*cover_scale),round(image.height*cover_scale)),Image.Resampling.BILINEAR)
                left,top=(bg.width-1024)//2,(bg.height-1024)//2
                bg=bg.crop((left,top,left+1024,top+1024)).filter(ImageFilter.GaussianBlur(28))
                square=ImageEnhance.Brightness(bg).enhance(0.45)
                square.paste(fit,((1024-fit.width)//2,(1024-fit.height)//2))
                dest=TARGET/(key+'.png')
                square.save(dest,optimize=True)
                print('READY:',dest)
                found+=1
        except Exception as exc:
            print(f'ERROR: {original}: {exc}')
    print(f'Imported {found}/{len(STAGES)} real stage screenshots')
if __name__=='__main__':main()
