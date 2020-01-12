# Pygame template

# Attributions

# (Heart) Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# (Play)<a href="https://www.freepik.com/free-photos-vectors/Background">Background vector created by freepik - www.freepik.com</a>
# (GameOver)<a href="https://www.freepik.com/free-photos-vectors/background">Background vector created by pikisuperstar - www.freepik.com</a>
# (Backing)Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
# (Graphics)Art by Kenney.nl

# Imports
import  pygame as pg
import random
from os import path

# images / sound
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Constants
WIDTH = 500
HEIGHT = 700
FPS = 60
POWERUP_TIME = 60000

# Define Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GREENISH_BLUE = (0, 255, 180)

# Initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Galaxy Shooters")
clock = pg.time.Clock()

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, CYAN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def spawnmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_status_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREENISH_BLUE, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 370
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power = 1
        self.power_time = pg.time.get_ticks()

    def update(self):
        # Timeout for powerups
        if self.power >= 2 and pg.time.get_ticks() - self.hide_timer > POWERUP_TIME:
            self.power -= 1
            self.power_time = pg.time.get_ticks

        # Unhide if necessary
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_RIGHT]:
            self.speedx = 5
        if keystate[pg.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pg.time.get_ticks()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                laser = Laser(self.rect.centerx, self.rect.top)
                all_sprites.add(laser)
                lasers.add(laser)
                random.choice(shoot_sounds).play()
            if self.power >= 2:
                laser1 = Laser(self.rect.left, self.rect.centery)
                laser2 = Laser(self.rect.right, self.rect.centery)
                all_sprites.add(laser1)
                all_sprites.add(laser2)
                lasers.add(laser1)
                lasers.add(laser2)
                random.choice(shoot_sounds).play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.right < -25 or self.rect.left > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Laser(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Kill it if moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'laser', 'star'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4

    def update(self):
        self.rect.y += self.speedy
        # Kill it if moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()

def show_go_screen():
    screen.blit(background2, background_rect2)
    draw_text(screen, " Guardians of the Galaxy ", 37, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow Keys move, Spacebar to shoot", 29, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press any key to BEGIN", 22, WIDTH / 2, HEIGHT *  3/ 4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False

# Load all game graphics
background = pg.image.load(path.join(img_dir, "2397814.jpg")).convert()
background_rect = background.get_rect()
background2 = pg.image.load(path.join(img_dir, "2474216.jpg")).convert()
background_rect2 = background2.get_rect()
pg.transform.scale(background, (500, 700))
player_img = pg.image.load(path.join(img_dir, "playerShip3_blue.png")).convert()
heart_img = pg.image.load(path.join(img_dir, "heart.png")).convert()
mini_heart_img = pg.transform.scale(heart_img, (23, 23))
mini_heart_img.set_colorkey(BLACK)
laser_img = pg.image.load(path.join(img_dir, "laserBlue01.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
                'meteorBrown_med1.png','meteorBrown_small1.png','meteorBrown_small2.png',
                'meteorBrown_tiny2.png',]
for img in meteor_list:
    meteor_images.append(pg.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(img_dir, 'shield_silver.png')).convert()
powerup_images['laser'] = pg.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['star'] = pg.image.load(path.join(img_dir, 'star_silver.png')).convert()

# Load all game sounds
laser_powerup = pg.mixer.Sound(path.join(snd_dir, 'Laser_Powerup.wav'))
shield_powerup = pg.mixer.Sound(path.join(snd_dir, 'Shield_Powerup.wav'))
shoot_sounds = []
for snd in ['Laser_Shoot.wav', 'Laser_Shoot2.wav']:
    shoot_sounds.append(pg.mixer.Sound(path.join(snd_dir, snd)))
expl_sounds = []
for snd in ['Expl.wav', 'Expl2.wav']:
    expl_sounds.append(pg.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pg.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
pg.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pg.mixer.music.set_volume(0.7)

pg.mixer.music.play(loops = -1)
# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        # Sprite groups
        all_sprites = pg.sprite.Group()
        mobs = pg.sprite.Group()
        lasers = pg.sprite.Group()
        powerups = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            spawnmob()

        score = 0
    # Keep loop running at the right speed
    clock.tick(FPS)
    # Events
    for event in pg.event.get():
        # Check for closing window
        if event.type == pg.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Check to see if a laser hit a mob
    hits = pg.sprite.groupcollide(mobs, lasers, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.92:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        spawnmob()

    # Check to see if a mob hit the player
    hits = pg.sprite.spritecollide(player, mobs, True, pg.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        spawnmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Check to see if player hit a powerup
    hits = pg.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            pow.kill()
            player.shield += random.randrange(10, 30)
            shield_powerup.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'laser':
            player.powerup()
            laser_powerup.play()
        if hit.type == 'star':
            player.lives += 1
            if player.lives >= 3:
                player.lives = 3

    # If the player died and the explosion finished playing
    if player.lives == 0 and not death_expl.alive():
        game_over = True
    # Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, WIDTH / 2, 10)
    draw_shield_status_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, mini_heart_img)
    # *After* drawing everything, flip the display
    pg.display.flip()

pg.quit()
