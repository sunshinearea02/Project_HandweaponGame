#  DARK INVASION — Hand Weapon Mini Game

Nama : Athaya Khairani Adi
NRP : 5024241007
Mata Kuliah : Pengolahan Citra Video

## Daftar Isi

1. [Deskripsi Game](#-deskripsi-game)
2. [Fitur Game dan Kontrol](#-fitur-game)
3. [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
4. [Alur Program](#-alur-program)
5. [Implementasi Teknis](#-implementasi-teknis)
6. [Cara Menjalankan](#-cara-menjalankan)
7. [Dokumentasi](#-dokumentasi)
8. [Demo Video](#-demo-video)
9. [Struktur Direktori](#-struktur-direktori)

---

## Deskripsi Game

**Dark Invasion** adalah mini game tembak monster berbasis webcam di mana pemain mengendalikan senjata menggunakan gerakan tangan secara real-time. Posisi tangan digunakan untuk mengarahkan senjata ke kiri atau kanan, sedangkan gerakan tangan pose menembak dikenali sebagai perintah untuk menembakkan peluru.

Pada permainan ini, monster akan terus muncul dan bergerak menuju area pertahanan pemain. Pemain harus mengarahkan senjata dan menembak monster sebelum mereka berhasil mencapai garis pertahanan. Setiap monster yang berhasil dikalahkan akan menambah skor, sedangkan monster yang lolos akan mengurangi nyawa pemain. Monster bergerak dengan efek perspektif — mengecil saat jauh dan membesar saat mendekat — menciptakan ilusi kedalaman 3D tanpa engine game apapun.

Game dikembangkan **hanya menggunakan Python, OpenCV, dan NumPy** tanpa framework atau game engine eksternal.

Game ini menerapkan berapa konsep yaitu : 
- **Segmentasi warna kulit** di ruang warna HSV untuk mengisolasi area tangan dari background
- **Operasi morfologi manual** (Opening & Closing) menggunakan NumPy untuk membersihkan hasil segmentasi
- **Analisis kontur** untuk menemukan posisi dan pergerakan tangan
- **Gesture recognition** berbasis perubahan posisi titik tertinggi tangan antar frame untuk menentukan kapan pemain "menembak"
- **Alpha blending manual** untuk menempatkan sprite senjata tepat mengikuti posisi tangan secara real-time

---

## Fitur Game

| Fitur | Keterangan |
|---|---|
| **Gesture Detection** | Deteksi gerakan tangan secara real-time: `SHOOT` (adanya pergerakan) dan `HOLD` (diam) |
| **Second Object** | Monster sebagai objek musuh yang bergerak mendekati pemain dengan efek perspektif|
| **Scoring System** | Skor bertambah setiap monster berhasil ditembak |
| **Health System** | 5 nyawa, berkurang setiap monster melewati garis pertahanan |
| **Weapon Overlay** | Sprite senjata mengikuti posisi tangan secara real-time via alpha blending |
| **Animasi Monster** | Sprite animasi multi-frame dari PNG sequence |
| **Efek Perspektif Monster** | Monster mengecil di kejauhan dan membesar serta mempercepat saat mendekat |

---

### Kontrol
| Aksi | Cara |
|---|---|
| Mulai game | Tekan `SPACE` di menu |
| Arahkan senjata | Gerakkan tangan kiri-kanan di zona deteksi (kotak pink) |
| Tembak | Pose tangan menembak (adanya pergerakan tangan) |
| Restart | Tekan `R` saat Game Over |
| Keluar | Tekan `ESC` |

---

## Teknologi yang Digunakan

| Library | Fungsi |
|---|---|
| **Python 3.x** | Bahasa pemrograman utama |
| **OpenCV (`cv2`)** | Membaca webcam, manipulasi frame, render game, load aset |
| **NumPy** | Seluruh pemrosesan piksel, operasi morfologi, dan kalkulasi matematis |
| **os** *(built-in)* | Membaca direktori frame monster |

> **Tidak menggunakan** library eksternal lain seperti Pygame, PIL/Pillow, TensorFlow, MediaPipe, atau framework game apapun di dalam program utama.

---

## Alur Program
1. **Webcam Capture**  
   Mengambil frame video secara real-time dari webcam.

2. **Flip Frame & Crop ROI**  
   Membalik frame secara horizontal agar pergerakan tangan sesuai dengan arah gerakan pemain, kemudian mengambil area deteksi tangan (Region of Interest).

3. **HSV Conversion**  
   Mengubah ruang warna frame dari BGR ke HSV.

4. **Skin Color Masking**  
   Melakukan segmentasi warna kulit untuk memperoleh area kandidat tangan.

5. **Manual Morphology (Opening & Closing)**  
   Membersihkan noise dan menutup lubang pada mask menggunakan operasi morfologi manual berbasis NumPy.

6. **Hand Contour Detection**  
   Mencari kontur tangan dan menentukan posisi tangan yang terdeteksi.

7. **Gesture Recognition**  
   Menganalisis pergerakan tangan untuk mengenali gesture menembak (*SHOOT*) atau diam (*HOLD*).

8. **Weapon Position Update**  
   Memperbarui posisi senjata agar mengikuti posisi tangan secara real-time.

9. **Game Logic Update**  
   Memperbarui seluruh objek permainan, termasuk peluru, monster, skor, dan nyawa pemain.

10. **Render Game Objects**  
    Menggambar background, senjata, monster, skor, dan nyawa ke dalam frame game.

11. **Display Frame**  
    Menampilkan hasil akhir permainan ke layar dan mengulangi proses untuk frame berikutnya.
---

## Implementasi Teknis
| Komponen | Implementasi |
|-----------|-----------|
| **Akuisisi Video** | Webcam digunakan sebagai sumber input utama. Frame video dibaca secara real-time menggunakan OpenCV untuk mendeteksi tangan pemain. |
| **Segmentasi Tangan** | Tangan dideteksi menggunakan metode skin color masking pada ruang warna HSV untuk memisahkan area tangan dari latar belakang. |
| **Operasi Morfologi** | Opening dan Closing diimplementasikan secara manual menggunakan NumPy untuk menghilangkan noise dan memperbaiki hasil segmentasi. |
| **Deteksi Tangan** | Kontur terbesar pada mask digunakan untuk menentukan posisi tangan yang akan mengendalikan senjata. |
| **Weapon Overlay** | Sprite senjata ditempelkan ke layar menggunakan teknik alpha blending sehingga dapat mengikuti posisi tangan secara real-time. |
| **Gesture Recognition** | Gerakan tangan dianalisis untuk mengenali gesture menembak (*SHOOT*) berdasarkan perubahan posisi tangan antar frame. |
| **Second Object** | Monster berfungsi sebagai objek musuh yang muncul secara berkala dan bergerak menuju area pertahanan pemain. |
| **Scoring System** | Skor bertambah setiap kali monster berhasil ditembak oleh pemain. |
| **Health System** | Nyawa pemain akan berkurang apabila monster berhasil mencapai area pertahanan. |
| **Rendering** | Background, senjata, monster, skor, dan nyawa dirender secara real-time pada setiap frame permainan. |

---

##  Cara Menjalankan

### 1. Install dependencies
```bash
pip install opencv-python numpy
```

### 2. Siapkan aset monster (jalankan sekali saja)

Karena OpenCV tidak mendukung alpha channel GIF secara native, GIF monster perlu dikonversi ke PNG frames terlebih dahulu menggunakan script berikut yang dijalankan :

```bash
pip install Pillow  
python convert_gif.py
```

Isi `convert_gif.py`:
```python
from PIL import Image
import os

gif = Image.open("PROJECT/monster.gif")
os.makedirs("PROJECT/monster_frames", exist_ok=True)

for i in range(gif.n_frames):
    gif.seek(i)
    frame = gif.convert("RGBA")
    frame.save(f"PROJECT/monster_frames/frame_{i:03d}.png")

print(f"Selesai! {gif.n_frames} frame tersimpan.")
```

> `convert_gif.py` hanya dijalankan **sekali untuk menyiapkan aset**. File ini tidak termasuk program game utama, sehingga game tetap murni OpenCV + NumPy.

### 3. Jalankan game
```bash
python main.py
```

### 4. Tips Penggunaan
- Pastikan pencahayaan ruangan cukup terang
- Posisikan tangan di dalam zona deteksi yang ditandai kotak pink di bagian bawah window `Frame`
- Gunakan background yang kontras dengan warna kulit untuk hasil deteksi terbaik
- Tiga window akan terbuka: `Game` (tampilan utama), `Frame` (kamera), `Mask` (debug deteksi)

---
## Dokumemtasi

<p align="center">
  <img src="screenshots/menu.png" width="250">
  <img src="screenshots/gameplay.png" width="250">
  <img src="screenshots/gameover.png" width="250">
</p>
---

## Video Demo
Berikut ink youtube video demontrasi game : 
[Video Demonstrasi Dark Invasion](https://youtu.be/dQw4w9WgXcQ)
---

## Struktur Direktori
```
Project_HandweaponGame/
├── main.py
├── convert_gif.py
├── README.md
├── assets/
│   ├── backgroundgame.png
│   ├── weapon.png
│   ├── monster.gif
│   └── monster_frames/
│       ├── frame_000.png
│       ├── frame_001.png
│       └── ...
└── documentation/
    ├── menu.png
    ├── gameplay.png
    └── gameover.png
```
