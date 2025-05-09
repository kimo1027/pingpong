from pygame import *
from random import choice

# Inisialisasi
init()

# Ukuran jendela
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Pong Sederhana")
back = (200, 255, 255)

# Font
font.init()
font = font.Font(None, 36)

# Kelas dasar untuk sprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Kelas pemain (raket)
class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

# Membuat sprite
racket1 = Player('racket.png', 30, 200, 4, 50, 150)
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

# Variabel permainan
speed_x = choice([-3, 3])
speed_y = choice([-3, 3])
score1 = 0
score2 = 0

# Label kalah
lose1 = font.render('PEMAIN 1 KALAH!', True, (180, 0, 0))
lose2 = font.render('PEMAIN 2 KALAH!', True, (180, 0, 0))

# Status permainan
game = True
finish = False
clock = time.Clock()
FPS = 60

# Fungsi reset bola
def reset_ball():
    global speed_x, speed_y
    ball.rect.x = 200
    ball.rect.y = 200
    speed_x = choice([-3, 3])
    speed_y = choice([-3, 3])

# Loop utama game
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN and e.key == K_r and finish:
            finish = False
            reset_ball()

    if not finish:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # Pantulan dari atas dan bawah
        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1

        # Pantulan dari raket
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1

        # Deteksi kalah
        if ball.rect.x < 0:
            finish = True
            score2 += 1
            window.blit(lose1, (180, 200))
        if ball.rect.x > win_width:
            finish = True
            score1 += 1
            window.blit(lose2, (180, 200))

        # Tampilkan objek
        racket1.reset()
        racket2.reset()
        ball.reset()

        # Tampilkan skor
        score_text = font.render(f"Skor: {score1} - {score2}", True, (0, 0, 0))
        window.blit(score_text, (220, 20))
    else:
        restart_text = font.render("Tekan R untuk main lagi", True, (0, 0, 0))
        window.blit(restart_text, (170, 250))

    display.update()
    clock.tick(FPS)
