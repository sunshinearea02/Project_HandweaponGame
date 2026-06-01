# 🧟 DARK INVASION — Hand Weapon Mini Game

> Game tembak zombie real-time berbasis deteksi tangan menggunakan OpenCV dan NumPy murni, tanpa framework atau engine game eksternal.

---

## 📋 Deskripsi Proyek

**Dark Invasion** adalah mini game interaktif bertema pertahanan dari serangan zombie yang dikendalikan sepenuhnya menggunakan **gerakan tangan** di depan webcam. Pemain menggerakkan tangan untuk mengarahkan senjata dan melakukan gerakan cepat untuk menembak peluru ke arah zombie yang terus berdatangan.

Proyek ini dikembangkan sebagai tugas mata kuliah dengan ketentuan:
- Hanya menggunakan **Python**, **OpenCV**, dan **NumPy**
- Tidak menggunakan framework atau game engine eksternal
- Seluruh pemrosesan citra diimplementasikan secara manual dari awal

---

## 🎮 Fitur Game

| Fitur | Keterangan |
|---|---|
| **Gesture Detection** | Deteksi gerakan tangan (SHOOT / HOLD) secara real-time |
| **Second Object** | Zombie sebagai objek musuh yang bergerak mendekati pemain |
| **Scoring System** | Skor bertambah setiap zombie berhasil ditembak |
| **Health System** | 5 nyawa, berkurang setiap zombie melewati garis pertahanan |
| **Animasi Zombie** | Sprite animasi multi-frame dari PNG sequence |
| **Perspektif Kedalaman** | Zombie mengecil di kejauhan dan membesar saat mendekat |

---

## 🛠️ Teknologi yang Digunakan

- **Python 3.x**
- **OpenCV** (`cv2`) — I/O kamera, manipulasi frame, render game
- **NumPy** — seluruh pemrosesan piksel dan operasi morfologi
- **os** (built-in Python) — membaca direktori frame zombie

> ⚠️ Tidak menggunakan library eksternal lain seperti Pygame, PIL, TensorFlow, MediaPipe, dsb.

---

## 📁 Struktur Direktori

```
├── main.py                  # File utama game
├── convert_gif.py           # Script konversi GIF → PNG (dijalankan sekali)
├── README.md
└── PROJECT/
    ├── backgroundgame.png   # Background game
    ├── weapon.png           # Sprite senjata (RGBA)
    ├── zombie.gif           # Animasi zombie asli
    └── zombie_frames/       # Hasil konversi PNG per frame
        ├── frame_000.png
        ├── frame_001.png
        └── ...
```

---

## ⚙️ Cara Menjalankan

### 1. Install dependencies
```bash
pip install opencv-python numpy
```

### 2. Konversi GIF zombie ke PNG frames (jalankan sekali saja)
```bash
pip install Pillow   # hanya untuk konversi, tidak dipakai di game
python convert_gif.py
```

Isi `convert_gif.py`:
```python
from PIL import Image
import os

gif = Image.open("PROJECT/zombie.gif")
os.makedirs("PROJECT/zombie_frames", exist_ok=True)

for i in range(gif.n_frames):
    gif.seek(i)
    frame = gif.convert("RGBA")
    frame.save(f"PROJECT/zombie_frames/frame_{i:03d}.png")

print(f"Selesai! {gif.n_frames} frame tersimpan.")
```

> `convert_gif.py` hanya dijalankan **sekali secara offline** untuk menyiapkan aset. File ini **tidak termasuk** dalam program game utama.

### 3. Jalankan game
```bash
python main.py
```

### 4. Kontrol
| Aksi | Cara |
|---|---|
| Mulai game | Tekan `SPACE` di menu |
| Arahkan senjata | Gerakkan tangan kiri-kanan di zona deteksi (kotak pink) |
| Tembak | Gerakkan tangan dengan cepat (gerakan tiba-tiba) |
| Restart | Tekan `R` saat Game Over |
| Keluar | Tekan `ESC` |

---

## 🔧 Implementasi Teknis

### 1. Konfigurasi Webcam — `cv2.VideoCapture`

```python
cap = cv2.VideoCapture(0)
```

Frame dari webcam dibaca setiap iterasi loop utama menggunakan `cap.read()`, kemudian di-flip horizontal agar terasa seperti cermin:

```python
ret, frame = cap.read()
frame = cv2.flip(frame, 1)
```

Tampilan game dan kamera ditampilkan menggunakan `cv2.imshow()`, dan aset gambar dimuat dengan `cv2.imread()`.

---

### 2. Skin Color Masking — HSV Color Segmentation

Tangan dideteksi menggunakan **segmentasi berbasis warna kulit** di ruang warna HSV. Pemrosesan dilakukan di ROI (Region of Interest) bagian bawah frame untuk efisiensi:

```python
SKIN_LOWER = np.array([0, 30, 60], dtype=np.uint8)
SKIN_UPPER = np.array([35, 255, 255], dtype=np.uint8)

hsv = cv2.cvtColor(roi_small, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, SKIN_LOWER, SKIN_UPPER)
```

ROI dibatasi pada zona bawah frame (70%–100% tinggi frame) agar deteksi lebih fokus dan efisien:

```python
zone_y1 = int(h * 0.7)
zone_y2 = h
roi = frame_small[zone_y1:zone_y2, zone_x1:zone_x2]
```

Seluruh operasi menggunakan array NumPy secara langsung tanpa fungsi segmentasi eksternal.

---

### 3. Operasi Morfologi Manual — Opening & Closing dengan NumPy

Seluruh operasi morfologi diimplementasikan **dari awal menggunakan NumPy** dengan `sliding_window_view` tanpa menggunakan `cv2.erode` atau `cv2.dilate`.

**Fungsi Erode Manual:**
```python
def manual_erode(binary_img, kernel_size=3):
    pad = kernel_size // 2
    padded = np.pad(binary_img, pad, mode='constant')
    windows = sliding_window_view(padded, (kernel_size, kernel_size))
    return windows.min(axis=(2, 3)).astype(np.uint8)
```

**Fungsi Dilate Manual:**
```python
def manual_dilate(binary_img, kernel_size=3):
    pad = kernel_size // 2
    padded = np.pad(binary_img, pad, mode='constant')
    windows = sliding_window_view(padded, (kernel_size, kernel_size))
    return windows.max(axis=(2, 3)).astype(np.uint8)
```

**Pipeline morfologi yang diterapkan:**

```python
# Opening (erode → dilate): menghilangkan noise kecil
mask = manual_erode(mask, 3)
mask = manual_dilate(mask, 3)

# Closing (dilate → erode): menutup lubang di dalam mask
mask = manual_dilate(mask, 3)
mask = manual_erode(mask, 3)
```

| Operasi | Fungsi |
|---|---|
| **Opening** | Menghilangkan noise kecil / piksel asing di luar area tangan |
| **Closing** | Menutup lubang / celah di dalam area tangan yang terdeteksi |

---

### 4. Weapon Sprite Overlay — Alpha Blending Manual

Senjata ditampilkan di atas background game menggunakan **alpha blending manual** berbasis NumPy tanpa fungsi OpenCV khusus:

```python
def overlay_rgba(frame, sprite, x, y):
    h, w = sprite.shape[:2]
    x = max(0, min(x, frame.shape[1] - w))
    y = max(0, min(y, frame.shape[0] - h))

    alpha = sprite[:, :, 3] / 255.0  # Normalisasi alpha channel

    for c in range(3):
        frame[y:y+h, x:x+w, c] = (
            alpha * sprite[:, :, c] +
            (1 - alpha) * frame[y:y+h, x:x+w, c]
        )
    return frame
```

Rumus alpha blending: `output = alpha × foreground + (1 - alpha) × background`

Posisi senjata mengikuti posisi horizontal tangan secara real-time:
```python
weapon_x = int(np.clip(game_x - 10, 0, 800 - weapon.shape[1]))
```

---

### 5. Gesture Recognition — Deteksi Gerakan SHOOT

Gesture dideteksi berdasarkan **perubahan posisi titik teratas tangan** (topmost point) antar frame. Jika perubahan melebihi threshold, gesture diklasifikasikan sebagai `SHOOT`:

```python
topmost = tuple(hand[hand[:,:,1].argmin()][0])

dx = current_top_x - prev_top_x
dy = current_top_y - prev_top_y
movement = np.sqrt(dx*dx + dy*dy)

gesture = "SHOOT" if movement > movement_threshold else "HOLD"
```

**Flag `hand_initialized`** digunakan untuk mencegah tembakan spurious di frame pertama tangan terdeteksi:

```python
if not hand_initialized:
    prev_top_x = current_top_x
    prev_top_y = current_top_y
    hand_initialized = True
else:
    # hitung movement dan tentukan gesture
```

**Smoothing posisi tangan** menggunakan exponential moving average agar gerakan tidak patah-patah:
```python
cx = int(0.7 * prev_cx + 0.3 * cx)
cy = int(0.7 * prev_cy + 0.3 * cy)
```

| Gesture | Kondisi | Efek |
|---|---|---|
| `HOLD` | Tangan diam / bergerak pelan | Senjata mengikuti posisi tangan |
| `SHOOT` | Gerakan tangan tiba-tiba (> threshold) | Menembakkan peluru dari ujung senjata |

---

### 6. Scoring System

Skor bertambah setiap peluru mengenai zombie. Deteksi tumbukan menggunakan perhitungan jarak sederhana berbasis ukuran zombie:

```python
size = int(60 * zombie.scale)

if abs(bullet.x - zombie.x) < size and abs(bullet.y - zombie.y) < size:
    bullets.remove(bullet)
    zombies.remove(zombie)
    score += 1
```

Health berkurang saat zombie mencapai garis pertahanan (`wall_y = 520`):
```python
zombie_bottom = zombie.y + int(60 * zombie.scale)
if zombie_bottom >= wall_y:
    zombies.remove(zombie)
    player_health = max(0, player_health - 1)
```

---

### 7. Sistem Perspektif Zombie

Zombie di-spawn dari tengah background dan membesar seiring mendekat, menciptakan ilusi kedalaman 3D:

```python
self.scale += self.speed        # membesar tiap frame
self.y += int(3 * self.scale)   # makin cepat turun saat besar
self.x += (self.target_x - self.x) * 0.015  # menyebar ke target

# efek kabut: makin transparan saat jauh
alpha *= min(self.scale * 4, 1.0)
```

---

## 🖥️ Tampilan Game

| Window | Isi |
|---|---|
| `Game` | Tampilan game utama (background + zombie + senjata + UI) |
| `Frame` | Feed webcam real-time + zona deteksi + titik tangan |
| `Mask` | Hasil skin color masking HSV (debug) |

---

## 📊 Alur Program

```
Webcam → Flip → Blur → Crop ROI
    → HSV Conversion → Skin Mask
    → Opening (Erode → Dilate)
    → Closing (Dilate → Erode)
    → Contour Detection → Gesture Classification
    → Update Game State (Bullet / Zombie / Score / Health)
    → Render Frame (Background + Weapon + Zombie + HUD)
    → Display
```

---

## 🎥 Demo Video

> 🔗 [Link Video Demonstrasi](#) *(tambahkan link YouTube/Google Drive di sini)*

---

## 📸 Screenshot

> *(Tambahkan screenshot game di sini)*

---

## 👤 Informasi Pengembang

| | |
|---|---|
| **Nama** | *(Nama kamu)* |
| **NIM** | *(NIM kamu)* |
| **Mata Kuliah** | *(Nama mata kuliah)* |
| **Institusi** | *(Nama institusi)* |
