from PIL import Image
import os

imgs = ['watch_arabic','watch_rolex_green','watch_blue_jubilee','watch_black_jubilee','watch_white_jubilee','watch_casio_green','watch_dw_black','watch_dw_white']
d = r'c:\Users\him\Desktop\JAWADDDDDD\assets\images'

for n in imgs:
    fp = os.path.join(d, n + '.png')
    img = Image.open(fp)
    w, h = img.size
    if w > 800:
        img = img.resize((800, int(h * (800 / w))), Image.LANCZOS)
    out = os.path.join(d, n + '.webp')
    img.save(out, 'WEBP', quality=80, method=6)
    before = os.path.getsize(fp) // 1024
    after = os.path.getsize(out) // 1024
    print(f'{n}: {before}KB -> {after}KB')

print('Done')
