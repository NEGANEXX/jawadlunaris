import cv2
import os
import numpy as np

video_path = "new_watch.f137.mp4"
output_dir = "assets/frames"
target_frames = 240

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.2, threshold=0):
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
    return sharpened

def enhance_contrast(image):
    # Convert to LAB color space to enhance contrast without changing colors
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L-channel
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
    cl = clahe.apply(l)
    
    # Merge the CLAHE enhanced L-channel with the original A and B channel
    limg = cv2.merge((cl,a,b))
    
    # Convert back to BGR
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final

cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Original video: {total_frames} frames @ {fps} fps")
print("Starting high-quality extraction and enhancement...")

# Trim 2 seconds from start and end
skip_frames = int(2 * fps)
start_frame = skip_frames
end_frame = total_frames - skip_frames

print(f"Trimming 2 seconds (start_frame: {start_frame}, end_frame: {end_frame})")

indices = []
if end_frame > start_frame:
    for i in range(target_frames):
        idx = int(start_frame + i * (end_frame - start_frame) / max(1, (target_frames - 1)))
        indices.append(idx)
else:
    print("Video is too short to trim 4 seconds total!")
    indices = list(range(target_frames))

frame_count = 0
for i, target_frame_idx in enumerate(indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame_idx)
    ret, frame = cap.read()
    if not ret:
        print(f"Warning: Could not read frame {target_frame_idx}. Attempting sequential read.")
        ret, frame = cap.read()
        if not ret:
            print("Sequential read also failed. Stopping extraction.")
            break
            
    # --- ENHANCEMENTS ---
    # 1. Upscale to 1080p using high-quality Lanczos interpolation
    frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
    
    # 2. Enhance contrast
    frame = enhance_contrast(frame)
    
    # 3. Apply unsharp mask to make it crisp
    frame = unsharp_mask(frame)
    
    # 4. Save with maximum JPEG quality
    filename = os.path.join(output_dir, f"frame_{i+1:04d}.jpg")
    cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    
    frame_count += 1
    if frame_count % 24 == 0:
        print(f"Processed {frame_count}/{target_frames} frames...")

cap.release()
print(f"Successfully extracted and enhanced {frame_count} frames to {output_dir}")
