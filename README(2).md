# 🧟 DARK INVASION — Hand Weapon Mini Game

> Mini game tembak monster real-time berbasis deteksi tangan menggunakan OpenCV dan NumPy, dikembangkan untuk mata kuliah **Pengolahan Citra Video**.

---

## 📑 Daftar Isi

1. [Identitas](#-identitas)
2. [Deskripsi Game](#-deskripsi-game)
3. [Screenshot Game](#-screenshot-game)
4. [Fitur Game](#-fitur-game)
5. [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
6. [Alur Program](#-alur-program)
7. [Implementasi Teknis](#-implementasi-teknis)
8. [Cara Menjalankan](#-cara-menjalankan)
9. [Demo Video](#-demo-video)
10. [Struktur Direktori](#-struktur-direktori)

---

## 👤 Identitas

| | |
|---|---|
| **Nama** | *Athaya Khairani Adi* |
| **NRP** | *5024241007* |
| **Mata Kuliah** | Pengolahan Citra Video |

---

## 📋 Deskripsi Game

**Dark Invasion** adalah mini game interaktif bertema pertahanan dari serangan monster yang dikendalikan sepenuhnya menggunakan **gerakan tangan** di depan webcam — tanpa keyboard, mouse, atau controller.

Proyek ini merupakan implementasi nyata dari konsep **Gesture Detection** pada mata kuliah **Pengolahan Citra Video**. Inti dari proyek ini adalah bagaimana sebuah program mampu memahami dan menginterpretasikan gerakan tangan manusia secara real-time melalui kamera, lalu mengubahnya menjadi aksi di dalam game.

Alih-alih menggunakan library deteksi tangan seperti MediaPipe, seluruh pipeline deteksi dibangun dari awal menggunakan teknik pengolahan citra klasik:

- **Segmentasi warna kulit** di ruang warna HSV untuk mengisolasi area tangan dari background
- **Operasi morfologi manual** (Opening & Closing) menggunakan NumPy untuk membersihkan hasil segmentasi
- **Analisis kontur** untuk menemukan posisi dan pergerakan tangan
- **Gesture recognition** berbasis perubahan posisi titik tertinggi tangan antar frame untuk menentukan kapan pemain "menembak"
- **Alpha blending manual** untuk menempatkan sprite senjata tepat mengikuti posisi tangan secara real-time

Pemain menggerakkan tangan kiri-kanan untuk mengarahkan senjata, dan melakukan gerakan tangan tiba-tiba (hentakan) untuk menembakkan peluru ke arah monster yang terus berdatangan dari kejauhan. Monster bergerak dengan efek perspektif — mengecil saat jauh dan membesar saat mendekat — menciptakan ilusi kedalaman 3D tanpa engine game apapun.

Game dikembangkan **hanya menggunakan Python, OpenCV, dan NumPy** tanpa framework atau game engine eksternal.

---

## 📸 Screenshot Game

> *(Tambahkan screenshot game di sini — bisa berupa tampilan menu, gameplay, dan game over)*

| Menu Utama | Gameplay | Game Over |
|---|---|---|
| *(screenshot)* | *(screenshot)* | *(screenshot)* |

---

## 🎮 Fitur Game

| Fitur | Keterangan |
|---|---|
| **Gesture Detection** | Deteksi gerakan tangan secara real-time: `SHOOT` (hentakan cepat) dan `HOLD` (diam) |
| **Second Object** | Monster sebagai objek musuh yang bergerak mendekati pemain dengan efek perspektif |
| **Scoring System** | Skor bertambah setiap monster berhasil ditembak |
| **Health System** | 5 nyawa, berkurang setiap monster melewati garis pertahanan |
| **Weapon Overlay** | Sprite senjata mengikuti posisi tangan secara real-time via alpha blending |
| **Animasi Monster** | Sprite animasi multi-frame dari PNG sequence |
| **Efek Perspektif** | Monster mengecil di kejauhan dan membesar serta mempercepat saat mendekat |
| **Efek Kabut** | Monster tampak transparan saat jauh, makin solid saat mendekat |
| **Anti-Ghost Shoot** | Flag `hand_initialized` mencegah tembakan tidak sengaja di frame pertama |
| **Smoothing Posisi** | Exponential moving average untuk pergerakan senjata yang halus |

---

## 🛠️ Teknologi yang Digunakan

| Library | Fungsi |
|---|---|
| **Python 3.x** | Bahasa pemrograman utama |
| **OpenCV (`cv2`)** | Membaca webcam, manipulasi frame, render game, load aset |
| **NumPy** | Seluruh pemrosesan piksel, operasi morfologi, dan kalkulasi matematis |
| **os** *(built-in)* | Membaca direktori frame monster |

> ⚠️ **Tidak menggunakan** library eksternal lain seperti Pygame, PIL/Pillow, TensorFlow, MediaPipe, atau framework game apapun di dalam program utama.

---

## 📊 Alur Program

```
┌─────────────────────────────────────────────────────────┐
│                     INISIALISASI                        │
│  Load background, weapon sprite, monster frames (PNG)   │
│  Buka koneksi webcam (cv2.VideoCapture)                 │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   LOOP UTAMA (per frame)                │
└──────────────────────────┬──────────────────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │        BACA FRAME WEBCAM        │
          │   cap.read() → flip horizontal  │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │         CROP ROI (zona tangan)  │
          │   70%-100% tinggi frame         │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │      SKIN COLOR MASKING         │
          │   BGR → HSV → inRange (mask)    │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │    MORFOLOGI MANUAL (NumPy)      │
          │  Opening: Erode → Dilate        │
          │  Closing: Dilate → Erode        │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │      DETEKSI KONTUR TANGAN      │
          │   findContours → area terbesar  │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │      GESTURE RECOGNITION        │
          │   Hitung movement topmost point │
          │   movement > threshold → SHOOT  │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │       UPDATE GAME STATE         │
          │  Spawn monster, gerak peluru,   │
          │  cek tumbukan, hitung skor,     │
          │  cek health → game over         │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │         RENDER FRAME            │
          │  Background + Senjata (alpha    │
          │  blending) + Monster + HUD      │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │     TAMPILKAN (cv2.imshow)      │
          │  Window: Game | Frame | Mask    │
          └────────────────┬────────────────┘
                           │
                    ESC ───┘ (keluar)
```

---

## 🔧 Implementasi Teknis

### 1. Konfigurasi Webcam — `cv2.VideoCapture`

Webcam dibuka menggunakan `cv2.VideoCapture(0)` dan frame dibaca setiap iterasi loop. Frame di-flip horizontal agar terasa seperti cermin dan intuitif bagi pemain:

```python
cap = cv2.VideoCapture(0)

ret, frame = cap.read()
frame = cv2.flip(frame, 1)
```

Aset gambar (background dan weapon) dimuat dengan `cv2.imread()`, dan seluruh tampilan dirender dengan `cv2.imshow()`:

```python
BACKGROUND = cv2.imread("PROJECT/backgroundgame.png")
weapon = cv2.imread("PROJECT/weapon.png", cv2.IMREAD_UNCHANGED)

cv2.imshow("Game", game)
cv2.imshow("Frame", frame_display)
cv2.imshow("Mask", mask)
```

---

### 2. Skin Color Masking — Segmentasi HSV

Tangan dideteksi menggunakan **segmentasi berbasis warna kulit** di ruang warna HSV. Deteksi difokuskan hanya pada ROI (Region of Interest) bagian bawah frame (70%–100%) untuk efisiensi dan mengurangi false detection:

```python
SKIN_LOWER = np.array([0, 30, 60], dtype=np.uint8)
SKIN_UPPER = np.array([35, 255, 255], dtype=np.uint8)

# Batasi zona deteksi
zone_y1 = int(h * 0.7)
zone_y2 = h
roi = frame_small[zone_y1:zone_y2, zone_x1:zone_x2]

# Konversi ke HSV dan buat mask
hsv = cv2.cvtColor(roi_small, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, SKIN_LOWER, SKIN_UPPER)
```

Seluruh manipulasi piksel menggunakan operasi array NumPy secara langsung, tanpa fungsi segmentasi eksternal.

---

### 3. Operasi Morfologi Manual — Opening & Closing dengan NumPy

Seluruh operasi morfologi diimplementasikan **dari awal menggunakan NumPy** dengan `sliding_window_view`, tanpa menggunakan `cv2.erode` atau `cv2.dilate`:

**Fungsi Erode Manual** — mengambil nilai minimum di setiap window:
```python
def manual_erode(binary_img, kernel_size=3):
    pad = kernel_size // 2
    padded = np.pad(binary_img, pad, mode='constant')
    windows = sliding_window_view(padded, (kernel_size, kernel_size))
    return windows.min(axis=(2, 3)).astype(np.uint8)
```

**Fungsi Dilate Manual** — mengambil nilai maksimum di setiap window:
```python
def manual_dilate(binary_img, kernel_size=3):
    pad = kernel_size // 2
    padded = np.pad(binary_img, pad, mode='constant')
    windows = sliding_window_view(padded, (kernel_size, kernel_size))
    return windows.max(axis=(2, 3)).astype(np.uint8)
```

**Pipeline morfologi lengkap (Opening + Closing):**
```python
# Opening (Erode → Dilate): hilangkan noise kecil di luar area tangan
mask = manual_erode(mask, 3)
mask = manual_dilate(mask, 3)

# Closing (Dilate → Erode): tutup lubang/celah di dalam area tangan
mask = manual_dilate(mask, 3)
mask = manual_erode(mask, 3)
```

| Operasi | Urutan | Fungsi |
|---|---|---|
| **Opening** | Erode → Dilate | Menghilangkan noise kecil dan piksel asing di luar area tangan |
| **Closing** | Dilate → Erode | Menutup lubang dan celah di dalam area tangan yang terdeteksi |

---

### 4. Weapon Sprite Overlay — Alpha Blending Manual

Sprite senjata (format RGBA) ditempatkan di atas background game menggunakan **alpha blending manual** berbasis NumPy:

```python
def overlay_rgba(frame, sprite, x, y):
    h, w = sprite.shape[:2]
    x = max(0, min(x, frame.shape[1] - w))
    y = max(0, min(y, frame.shape[0] - h))

    alpha = sprite[:, :, 3] / 255.0  # normalisasi alpha [0.0 - 1.0]

    for c in range(3):
        frame[y:y+h, x:x+w, c] = (
            alpha * sprite[:, :, c] +
            (1 - alpha) * frame[y:y+h, x:x+w, c]
        )
    return frame
```

**Rumus:** `output = α × foreground + (1 − α) × background`

Posisi senjata mengikuti posisi horizontal tangan secara real-time, dipetakan dari koordinat ROI ke koordinat layar game (800px):

```python
game_x = int((raw_x / (zone_x2 - zone_x1)) * 800)
weapon_x = int(np.clip(game_x - 10, 0, 800 - weapon.shape[1]))
```

---

### 5. Gesture Recognition — Deteksi Gerakan SHOOT

Gesture dikenali berdasarkan **perubahan posisi titik teratas tangan** (topmost point) antar frame. Pendekatan ini sederhana namun efektif untuk mendeteksi hentakan/gerakan tiba-tiba:

```python
# Cari titik tertinggi tangan (y terkecil)
topmost = tuple(hand[hand[:,:,1].argmin()][0])

# Hitung pergerakan dari frame sebelumnya
dx = current_top_x - prev_top_x
dy = current_top_y - prev_top_y
movement = np.sqrt(dx*dx + dy*dy)

# Klasifikasi gesture
gesture = "SHOOT" if movement > movement_threshold else "HOLD"
```

**Flag `hand_initialized`** mencegah tembakan tidak sengaja saat tangan pertama kali terdeteksi:

```python
if not hand_initialized:
    # Frame pertama: simpan posisi tanpa klasifikasi gesture
    prev_top_x = current_top_x
    prev_top_y = current_top_y
    hand_initialized = True
else:
    # Frame berikutnya: hitung movement dan klasifikasikan
    dx = current_top_x - prev_top_x
    dy = current_top_y - prev_top_y
    movement = np.sqrt(dx*dx + dy*dy)
    gesture = "SHOOT" if movement > movement_threshold else "HOLD"
```

**Exponential Moving Average** untuk smoothing posisi senjata agar tidak patah-patah:
```python
cx = int(0.7 * prev_cx + 0.3 * cx)
cy = int(0.7 * prev_cy + 0.3 * cy)
```

| Gesture | Kondisi | Efek dalam Game |
|---|---|---|
| `HOLD` | Tangan diam atau bergerak pelan | Senjata mengikuti posisi tangan |
| `SHOOT` | Gerakan tangan tiba-tiba melebihi threshold | Peluru ditembakkan dari ujung senjata |

---

### 6. Scoring System & Collision Detection

Skor bertambah saat peluru mengenai monster. Tumbukan dideteksi menggunakan jarak Manhattan berbasis ukuran monster (skala dinamis):

```python
size = int(60 * monster.scale)

if abs(bullet.x - monster.x) < size and abs(bullet.y - monster.y) < size:
    bullets.remove(bullet)
    monsters.remove(monster)
    score += 1
    break
```

Health system berkurang saat monster melewati garis pertahanan:
```python
monster_bottom = monster.y + int(60 * monster.scale)
if monster_bottom >= wall_y:
    monsters.remove(monster)
    player_health = max(0, player_health - 1)
    if player_health == 0:
        game_over = True
```

---

### 7. Sistem Perspektif Monster

Monster di-spawn dari tengah background dengan skala kecil, lalu membesar dan mempercepat seiring mendekat — menciptakan ilusi kedalaman 3D:

```python
self.scale += self.speed             # membesar tiap frame
self.y += int(3 * self.scale)        # kecepatan turun proporsional dengan skala
self.x += (self.target_x - self.x) * 0.015  # menyebar ke target secara smooth

# efek kabut: makin transparan saat masih jauh
alpha *= min(self.scale * 4, 1.0)
```

Monster diurutkan berdasarkan skala sebelum digambar agar yang jauh (kecil) tergambar lebih dulu (depth sorting):
```python
monsters.sort(key=lambda m: m.scale)
for monster in monsters:
    monster.draw(game)
```

---

## ⚙️ Cara Menjalankan

### 1. Install dependencies
```bash
pip install opencv-python numpy
```

### 2. Siapkan aset monster (jalankan sekali saja)

Karena OpenCV tidak mendukung alpha channel GIF secara native, GIF monster perlu dikonversi ke PNG frames terlebih dahulu menggunakan script berikut yang dijalankan **sekali secara offline**:

```bash
pip install Pillow   # hanya untuk konversi aset, tidak dipakai di game
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

### 4. Kontrol

| Aksi | Cara |
|---|---|
| Mulai game | Tekan `SPACE` di menu |
| Arahkan senjata | Gerakkan tangan kiri-kanan di dalam zona deteksi (kotak pink) |
| Tembak | Hentakkan tangan dengan cepat |
| Restart | Tekan `R` saat Game Over |
| Keluar | Tekan `ESC` |

### 5. Tips Penggunaan

- Pastikan pencahayaan ruangan cukup terang
- Posisikan tangan di dalam zona deteksi yang ditandai kotak pink di bagian bawah window `Frame`
- Gunakan background yang kontras dengan warna kulit untuk hasil deteksi terbaik
- Tiga window akan terbuka: `Game` (tampilan utama), `Frame` (kamera), `Mask` (debug deteksi)

---

## 🎥 Demo Video

> 🔗 [Link Video Demonstrasi](#) *(tambahkan link YouTube / Google Drive di sini)*

---

## 📁 Struktur Direktori

```
📦 dark-invasion/
├── 📄 main.py                    # File utama game (OpenCV + NumPy only)
├── 📄 convert_gif.py             # Script konversi GIF → PNG (dijalankan sekali)
├── 📄 README.md                  # Dokumentasi proyek
└── 📂 PROJECT/
    ├── 🖼️  backgroundgame.png    # Background game (800x600)
    ├── 🖼️  weapon.png            # Sprite senjata format RGBA
    ├── 🎞️  monster.gif           # Animasi monster asli
    └── 📂 monster_frames/        # PNG per frame hasil konversi (alpha transparan)
        ├── frame_000.png
        ├── frame_001.png
        └── ...
```
