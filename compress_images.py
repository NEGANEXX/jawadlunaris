"""
Compress all images for the Lunaris store:
- Frames: Resize to 1280px wide, JPEG quality 60
- Product images: Convert to WebP, quality 80
"""
from PIL import Image
import os
import glob

FRAMES_DIR = r"c:\Users\him\Desktop\JAWADDDDDD\assets\frames"
IMAGES_DIR = r"c:\Users\him\Desktop\JAWADDDDDD\assets\images"

# ── Compress scroll animation frames ──
print("=== Compressing 240 scroll frames ===")
frame_files = sorted(glob.glob(os.path.join(FRAMES_DIR, "frame_*.jpg")))
total_before = 0
total_after = 0

for i, fp in enumerate(frame_files):
    total_before += os.path.getsize(fp)
    img = Image.open(fp)
    
    # Resize to 1280px wide (keep aspect ratio)
    w, h = img.size
    new_w = 1280
    new_h = int(h * (new_w / w))
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Save with reduced quality
    img.save(fp, "JPEG", quality=55, optimize=True)
    total_after += os.path.getsize(fp)
    
    if (i + 1) % 40 == 0 or i == 0:
        print(f"  Processed {i+1}/{len(frame_files)}")

print(f"  Frames: {total_before/1024/1024:.1f}MB -> {total_after/1024/1024:.1f}MB")

# ── Compress product images (PNG -> WebP) ──
print("\n=== Compressing product images ===")
for fn in os.listdir(IMAGES_DIR):
    if not fn.endswith(".png"):
        continue
    fp = os.path.join(IMAGES_DIR, fn)
    before = os.path.getsize(fp)
    
    img = Image.open(fp)
    # Resize product images to max 800px wide
    w, h = img.size
    if w > 800:
        new_h = int(h * (800 / w))
        img = img.resize((800, new_h), Image.LANCZOS)
    
    # Save as WebP (much smaller)
    webp_path = fp.replace(".png", ".webp")
    img.save(webp_path, "WEBP", quality=80, method=6)
    after = os.path.getsize(webp_path)
    print(f"  {fn}: {before/1024:.0f}KB -> {fn.replace('.png','.webp')}: {after/1024:.0f}KB")

print("\n✅ Done!")
