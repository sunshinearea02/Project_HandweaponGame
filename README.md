# Handweapon Mini Game — Dark Invasion

##  Deskripsi Project
**Handweapon Mini Game (Dark Invasion)** adalah game berbasis computer vision yang menggunakan deteksi tangan secara real-time sebagai kontrol utama senjata. Pemain mengarahkan weapon dengan posisi tangan dan melakukan gesture cepat untuk menembak zombie yang muncul di layar.

Project ini dikembangkan **murni menggunakan Python, OpenCV, dan NumPy**, tanpa game engine atau framework tambahan.

---

## Fitur Utama

###  Gesture Detection
- Deteksi tangan menggunakan segmentasi warna kulit (HSV)
- Tracking posisi tangan secara real-time
- Gesture:
  - **HOLD** → tidak menembak
  - **SHOOT** → terdeteksi dari perubahan posisi tangan (movement threshold)

###  Second Object System
- Weapon sprite mengikuti posisi tangan
- Zombie sebagai objek musuh:
  - Spawn otomatis
  - Gerakan menuju player
  - Animasi multi-frame (sprite sequence)

### Scoring System
- +1 score setiap zombie berhasil ditembak
- Health system (player life = 5)
- Game Over jika zombie melewati batas pertahanan

---

## Teknologi yang Digunakan
- Python 3
- OpenCV (cv2)
- NumPy
- Webcam (cv2.VideoCapture)

---
## Struktur Folder
```bash
Handweapon-Mini-Game/
│
├── main.py
├── README.md
│
├── assets/
│ ├── backgroundgame.png
│ ├── weapon.png
│ └── zombie_frames/
│ ├── frame_1.png
│ ├── frame_2.png
│ ├── frame_3.png
│ └── ...
│
├── screenshots/
│ ├── gameplay.png
│ ├── menu.png
│ └── gameover.png
│
└── demo/
└── link drive video
```

## Cara Menjalankan
### 1. Install dependency
```bash
pip install opencv-python numpy
```
### 2. Jalankan Program
```bash
python main.py
```
