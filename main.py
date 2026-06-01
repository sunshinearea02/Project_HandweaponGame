import cv2
import numpy as np
import os

from numpy.lib.stride_tricks import sliding_window_view

SKIN_LOWER = np.array([0, 30, 60], dtype=np.uint8)
SKIN_UPPER = np.array([35, 255, 255], dtype=np.uint8)

BACKGROUND = cv2.imread("PROJECT/backgroundgame.png")
BACKGROUND = cv2.resize(BACKGROUND, (800, 600))

cap = cv2.VideoCapture(0)

prev_cx, prev_cy = 0, 0

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)

# gif zombie
zombie_frames = []
frames_dir = "PROJECT/zombie_frames"

frame_files = sorted([
    f for f in os.listdir(frames_dir)
    if f.endswith(".png")
])

for fname in frame_files:
    path = os.path.join(frames_dir, fname)
    frame = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if frame is not None:
        zombie_frames.append(frame)

weapon = cv2.imread("PROJECT/weapon.png", cv2.IMREAD_UNCHANGED)
weapon = cv2.resize(
    weapon,
    (
        int(weapon.shape[1] * 0.2),
        int(weapon.shape[0] * 0.2)
    ),
    interpolation=cv2.INTER_AREA
)

# alpha blending manual untuk gambar RGBA
def overlay_rgba(frame, sprite, x, y):

    if sprite is None:
        return frame

    h, w = sprite.shape[:2]

    x = max(0, min(x, frame.shape[1] - w))
    y = max(0, min(y, frame.shape[0] - h))

    alpha = sprite[:, :, 3] / 255.0

    for c in range(3):
        frame[y:y+h, x:x+w, c] = (
            alpha * sprite[:, :, c] +
            (1 - alpha) * frame[y:y+h, x:x+w, c]
        )

    return frame

def manual_erode(binary_img, kernel_size=3):

    pad = kernel_size // 2

    padded = np.pad(
        binary_img,
        pad,
        mode='constant'
    )

    windows = sliding_window_view(
        padded,
        (kernel_size, kernel_size)
    )

    return windows.min(axis=(2, 3)).astype(np.uint8)


def manual_dilate(binary_img, kernel_size=3):

    pad = kernel_size // 2

    padded = np.pad(
        binary_img,
        pad,
        mode='constant'
    )

    windows = sliding_window_view(
        padded,
        (kernel_size, kernel_size)
    )

    return windows.max(axis=(2, 3)).astype(np.uint8)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = -20

    def update(self):
        self.y += self.speed

    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), 5, (0,0,255), -1)


class Zombie:
    def __init__(self):

        # Spawn dari tengah background
        self.x = np.random.randint(380, 420)
        self.y = 350

        # Tujuan akhir di bawah layar
        self.target_x = np.random.randint(100, 700)

        self.scale = 0.10
        self.speed = 0.004
        self.frame_index = 0

    def update(self):

        # Membesar saat mendekat
        self.scale += self.speed

        # Bergerak turun
        self.y += int(3 * self.scale)

        # Menyebar kiri-kanan
        self.x += (self.target_x - self.x) * 0.015

        self.frame_index += 0.2

        if self.frame_index >= len(zombie_frames):
            self.frame_index = 0

    def draw(self, frame):

        gif_frame = zombie_frames[int(self.frame_index)]

        # Ukuran membesar sesuai jarak
        size = int(280 * self.scale)

        if size <= 5:
            return

        resized = cv2.resize(
            gif_frame,
            (size, size),
            interpolation=cv2.INTER_AREA
        )

        h_img, w_img = resized.shape[:2]

        x1 = int(self.x - w_img // 2)
        y1 = int(self.y - h_img // 2)
        x2 = x1 + w_img
        y2 = y1 + h_img

        if x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
            return

        alpha = resized[:, :, 3] / 255.0

        # Efek kabut/jarak
        alpha *= min(self.scale * 4, 1.0)

        for c in range(3):
            frame[y1:y2, x1:x2, c] = (
                alpha * resized[:, :, c] +
                (1 - alpha) * frame[y1:y2, x1:x2, c]
            )
#game state
bullets = []
zombies = []

score = 0
player_health = 5
game_over = False

shoot_cooldown = 0
spawn_timer = 0

game_state = "MENU"

spawn_delay = 1
max_zombies = 3

# tembok nembak
wall_y= 520

weapon_y = 515


offset_ujung_senjata_x = 110
offset_ujung_senjata_y = 50

prev_top_x = 0
prev_top_y = 0
movement_threshold = 10
hand_initialized = False


while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    frame_small = cv2.GaussianBlur(frame, (5,5), 0)

    h, w, _ = frame_small.shape

    zone_x1 = int(w * 0.10)
    zone_x2 = int(w * 0.90)

    zone_y1 = int(h * 0.7)
    zone_y2 = h

    roi = frame_small[zone_y1:zone_y2,
                    zone_x1:zone_x2]
    
    cv2.rectangle(
    frame,
    (zone_x1, zone_y1),
    (zone_x2, zone_y2),
    (255,0,255),
    2
    )
    
    roi_small = cv2.resize(
        roi,
        None,
        fx=0.5,
        fy=0.5
    )

    hsv = cv2.cvtColor(roi_small, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, SKIN_LOWER, SKIN_UPPER)
    mask = cv2.resize(
        mask,
        (roi.shape[1], roi.shape[0]),
        interpolation=cv2.INTER_NEAREST
    )
    
    mask = manual_erode(mask, 3)
    mask = manual_dilate(mask, 3)

    mask = manual_dilate(mask, 3)
    mask = manual_erode(mask, 3)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    gesture = "HOLD"
    game_x = 400

    if contours:

        hand = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(hand)

        if area > 500:

            M = cv2.moments(hand)

            if M["m00"] != 0:

                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                topmost = tuple(hand[hand[:,:,1].argmin()][0])

                current_top_x = topmost[0]
                current_top_y = topmost[1]

               # SESUDAH
                if not hand_initialized:
                    # frame pertama tangan terdeteksi, langsung set posisi tanpa hitung movement
                    prev_top_x = current_top_x
                    prev_top_y = current_top_y
                    hand_initialized = True
                else:
                    dx = current_top_x - prev_top_x
                    dy = current_top_y - prev_top_y
                    movement = np.sqrt(dx*dx + dy*dy)
                    gesture = "SHOOT" if movement > movement_threshold else "HOLD"

                    prev_top_x = current_top_x
                    prev_top_y = current_top_y

                cx = int(0.7 * prev_cx + 0.3 * cx)
                cy = int(0.7 * prev_cy + 0.3 * cy)

                prev_cx, prev_cy = cx, cy

                raw_x = np.clip(cx, 0, zone_x2 - zone_x1)

                game_x = int(
                    (raw_x / (zone_x2 - zone_x1)) * 800
                )

                draw_x = zone_x1 + cx
                draw_y = zone_y1 + cy

                cv2.circle(frame, (draw_x, draw_y), 10, (0,0,255), -1)
               
    weapon_x = int(np.clip(game_x - 10, 0, 800 - weapon.shape[1]))

    # SHOOT
    if game_state == "PLAY" and not game_over:
        if  gesture == "SHOOT" and shoot_cooldown == 0:
            ujung_x = weapon_x + offset_ujung_senjata_x
            ujung_y = weapon_y - offset_ujung_senjata_y

            bullets.append(Bullet(
                ujung_x,
                ujung_y
            ))
            shoot_cooldown = 8

        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        #spawn zombie
        spawn_timer += 1

        if (
            not game_over
            and spawn_timer >= spawn_delay
            and len(zombies) < max_zombies
        ):

            # spawn 2 zombie sekaligus
            for _ in range(2):
                zombies.append(Zombie())

            spawn_timer = 0

        for bullet in bullets:
            bullet.update()

        for zombie in zombies:
            zombie.update()

        #zombie nabrak tembok
        for zombie in zombies[:]:

            zombie_bottom = zombie.y + int(60 * zombie.scale)

            if zombie_bottom >= wall_y:

                zombies.remove(zombie)

                player_health = max(0, player_health - 1)

                if player_health == 0:
                    game_over = True

       # peluru ke zombie
        for bullet in bullets[:]:
            for zombie in zombies[:]:

                size = int(60 * zombie.scale)

                if abs(bullet.x - zombie.x) < size and abs(bullet.y - zombie.y) < size:
                    bullets.remove(bullet)
                    zombies.remove(zombie)
                    score += 1
                    break

        bullets = [b for b in bullets if b.y > 0]
        zombies = [z for z in zombies if z.y < 600]

    game = BACKGROUND.copy()
    game = overlay_rgba(
            game,
            weapon,
            weapon_x,
            weapon_y,
        )   

    # bantuan buat ngukurnya
    """ cv2.circle(
    game,
    (ujung_x, ujung_y),
    10,
    (0,255,0),
    -1
    ) """
    
    for bullet in bullets:
        bullet.draw(game)

    zombies.sort(key=lambda z: z.scale)
    for zombie in zombies:
        zombie.draw(game)

    cv2.putText(game, f"Score: {score}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(game,
            f"Life: {player_health}",
            (10,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            2)

    frame_display = cv2.resize(frame, (800, 600))

    cv2.putText(frame_display, f"Gesture: {gesture}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)



    if game_over:

        cv2.putText(game,
                    "GAME OVER",
                    (200,300),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0,0,255),
                    5)
        cv2.putText(
        game,
        "Press R to Restart",
        (240,360),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255,255,255),
        2
    )
    if game_state == "MENU":

        game = BACKGROUND.copy()

        cv2.putText(
            game,
            "DARK INVASION",
            (180,170),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.8,
            (255,255,255),
            4
        )

        cv2.putText(
            game,
            "Press SPACE to Start",
            (220,400),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,255),
            3
        )


    cv2.imshow("Frame", frame_display)
    cv2.imshow("Mask", cv2.resize(mask, (400, 300)))
    cv2.imshow("Game", game)

    key = cv2.waitKey(1) & 0xFF
    if key == 32 and game_state == "MENU":
        bullets.clear()
        zombies.clear()

        score = 0
        player_health = 5

        game_over = False

        shoot_cooldown = 0
        spawn_timer = 0

        prev_top_x = 0
        prev_top_y = 0

        prev_cx = 0
        prev_cy = 0
        hand_initialized = False

        game_state = "PLAY"

    if key == 27:
        break

    if key == ord('r') and game_over:

        bullets.clear()
        zombies.clear()

        score = 0
        player_health = 5

        prev_top_x = 0
        prev_top_y = 0

        prev_cx = 0
        prev_cy = 0
        hand_initialized = False

        game_over = False

        shoot_cooldown = 0
        spawn_timer = 0
        game_state = "MENU"

cap.release()
cv2.destroyAllWindows()