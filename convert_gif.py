# convert_gif.py — jalankan SEKALI, file ini tidak masuk ke project
from PIL import Image
import os

gif = Image.open("PROJECT/zombie.gif")
os.makedirs("PROJECT/zombie_frames", exist_ok=True)

for i in range(gif.n_frames):
    gif.seek(i)
    frame = gif.convert("RGBA")
    frame.save(f"PROJECT/zombie_frames/frame_{i:03d}.png")

print(f"Selesai! {gif.n_frames} frame tersimpan.")