try:
    import pygame
except ImportError:
    print("Kamu belum memiliki modul pygame")
    sys.exit(1)
from pygame import mixer
import os
import random
import csv
import button
pygame.mixer.init(frequency=44100)
pygame.init()

screen_width = 1000
screen_height = int(screen_width * 0.7)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Atop World Dominesion ')

# FPS
clock = pygame.time.Clock()
FPS = 60

# game variables
GRAVITY = 0.75
SCROLL_THRESH = screen_width // 4
ROWS = 10
COLS = 80
TILE_SIZE = screen_height // ROWS
TILE_TYPES = 33
OPEN_TYPES = 8
screen_scroll = 0
bg_scroll = 0
MAX_LEVELS = 4
level = 1
ANIMATION_COOLDOWN = 200
current_story = 0
start_game = False
start_intro = False
start_story = True
current_ending = 0

# Keyboard aksi
moving_left = False
moving_right = False
shoot = False

#sound effects
jump_fx = pygame.mixer.Sound('Assets/Sound_Effects/Kiki_Suara/loncat.wav')
jump_fx.set_volume(0.5)
shot_fx = pygame.mixer.Sound('Assets/Sound_Effects/Kiki_Suara/nembak.wav')
shot_fx.set_volume(0.5)
backsound = pygame.mixer.Sound('Assets/Music/musik.mp3')
backsound.set_volume(0.2)
button_click = pygame.mixer.Sound('Assets/Sound_Effects/klik-button.mp3')
button_click.set_volume(5)

# load image
# button
start_img = pygame.image.load('Assets/Button/Play.png').convert_alpha()
exit_img = pygame.image.load('Assets/Button/Exit.png').convert_alpha()
retry_img = pygame.image.load('Assets/Button/Retry.png').convert_alpha()

# background level 1

buildings_img = pygame.image.load('Assets/Background/Level_1/buildings.png').convert_alpha()
shadow_img = pygame.image.load('Assets/Background/Level_1/shadow.png').convert_alpha()
sky_img = pygame.image.load('Assets/Background/Level_1/sky_cloud.png').convert_alpha()

buildings_img2 = pygame.image.load('Assets/Background/Level_2/alien.png').convert_alpha()
shadow_img2 = pygame.image.load('Assets/Background/Level_2/buildings.png').convert_alpha()
sky_img2 = pygame.image.load('Assets/Background/Level_2/hell.png').convert_alpha()
        
buildings_img3 = pygame.image.load('Assets/Background/Level_3/smoke.png').convert_alpha()
shadow_img3 = pygame.image.load('Assets/Background/Level_3/broken.png').convert_alpha()
sky_img3 = pygame.image.load('Assets/Background/Level_3/sunset.png').convert_alpha()

buildings_img4 = pygame.image.load('Assets/Background/Level_4/buildings.png').convert_alpha()
shadow_img4 = pygame.image.load('Assets/Background/Level_4/trans.png').convert_alpha()
sky_img4 = pygame.image.load('Assets/Background/Level_4/night.png').convert_alpha()

# Background
open_bg_images = []  # Daftar untuk menyimpan semua gambar latar belakang

# Load semua gambar dari folder Assets/Background/Open
for x in range(OPEN_TYPES):
    img = pygame.image.load(f'Assets/Background/Open/{x}.png')
    img = pygame.transform.scale(img, (screen_width, screen_height))  # Skala gambar agar sesuai dengan ukuran layar
    open_bg_images.append(img)

# Load semua gambar dari folder Assets/Background/Story
Story_list = []
for i in range(6):
    story_image = pygame.image.load(f'Assets/Background/Story/{i}.png').convert()
    Story_list.append(story_image)

Ending_list = []
for i in range(6):
    ending_image = pygame.image.load(f'Assets/Background/Ending/{i}.png').convert()
    Ending_list.append(ending_image)

# Indeks gambar saat ini
current_bg_index = 0

# Fungsi untuk menampilkan latar belakang
def display_background():
    global current_bg_index
    if current_bg_index < len(open_bg_images):
        screen.blit(open_bg_images[current_bg_index], (0, 0))
        current_bg_index = (current_bg_index + 1) % OPEN_TYPES
    else:
        current_bg_index = 0  # Reset to zero if index exceeds the list length

# tile list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Assets/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# peluru nembak
bullet1_img = pygame.image.load('Assets/Equipments/bullet1.png').convert_alpha()
bullet1_img = pygame.transform.scale(bullet1_img, (int(bullet1_img.get_width() * 2), int(bullet1_img.get_height() * 2)))  # Skala 2x lebih besar
bullet2_img = pygame.image.load('Assets/Equipments/bullet2.png').convert_alpha()
bullet2_img = pygame.transform.scale(bullet2_img, (int(bullet2_img.get_width() * 2), int(bullet2_img.get_height() * 2)))
bullet3_img = pygame.image.load('Assets/Equipments/bullet3.png').convert_alpha()
bullet3_img = pygame.transform.scale(bullet3_img, (int(bullet3_img.get_width() * 2), int(bullet3_img.get_height() * 2)))

# box
health_box_img = pygame.image.load('Assets/Equipments/roti.png').convert_alpha()
ammo_box_img = pygame.image.load('Assets/Tile/27.png').convert_alpha()
item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img
}

# Warna base
BG = (95, 190, 254)
DIRT = (144, 56, 1)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# font
font_type = 'Assets/Ubuntu-Bold.ttf'
font = pygame.font.Font(font_type, 20)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        if level == 1:
            screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(shadow_img, ((x * width) - bg_scroll * 0.6, screen_height - shadow_img.get_height() - 50))
            screen.blit(buildings_img, ((x * width) - bg_scroll * 0.6, screen_height - buildings_img.get_height() - 50))
        elif level == 2:
            screen.blit(sky_img2, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(shadow_img2, ((x * width) - bg_scroll * 0.6, screen_height - shadow_img.get_height() - 50))
            screen.blit(buildings_img2, ((x * width) - bg_scroll * 0.6, screen_height - buildings_img.get_height() - 50))
        elif level == 3:
            screen.blit(sky_img3, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(shadow_img3, ((x * width) - bg_scroll * 0.6, screen_height - shadow_img.get_height() - 50))
            screen.blit(buildings_img3, ((x * width) - bg_scroll * 0.6, screen_height - buildings_img.get_height() - 50))
        elif level == 4:
            screen.blit(sky_img4, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(shadow_img4, ((x * width) - bg_scroll * 0.6, screen_height - shadow_img.get_height() - 50))
            screen.blit(buildings_img4, ((x * width) - bg_scroll * 0.6, screen_height - buildings_img.get_height() - 50))

# Waktu terakhir perubahan gambar latar belakang
last_bg_change_time = 0

def open_bg():
    global last_bg_change_time
    global current_bg_index

    # Memeriksa waktu sekarang
    current_time = pygame.time.get_ticks()

    # Memeriksa apakah sudah waktunya untuk mengubah gambar latar belakang
    if current_time - last_bg_change_time >= ANIMATION_COOLDOWN:
        last_bg_change_time = current_time  # Update waktu terakhir perubahan
        current_bg_index = (current_bg_index + 1) % OPEN_TYPES  # Mengubah gambar ke gambar berikutnya

    # Menampilkan gambar latar belakang yang saat ini dipilih
    screen.blit(open_bg_images[current_bg_index], (0, 0))

def show_story():
    screen.fill(WHITE)
    screen.blit(Story_list[current_story], (0, 0))
    pygame.display.flip()

def story_events():
    global current_story, start_story
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if current_story < len(Story_list) - 1:
                    current_story += 1
                else:
                    start_story = False

def show_ending():
    screen.fill(WHITE)
    screen.blit(Ending_list[current_ending], (0, 0))
    ending_story = pygame.mixer.Sound('Assets/Sound_Effects/akhir-game.mp3')
    ending_story.set_volume(0.5)
    ending_story.play()
    pygame.display.flip()

def ending_events():
    global current_ending, run
    
    # Periksa apakah Atop sudah mati atau health Atop adalah 0
    if not Atop_group or Atop.health == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_ending < len(Ending_list) - 1:
                        current_ending += 1
                    else:
                        run = False

def reset_level():
    Goblin_group.empty()
    Demon_group.empty()
    Atop_group.empty()
    Kiki_group.empty()
    bullet1_group.empty()
    bullet2_group.empty()
    bullet3_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    fire_group.empty()
    exit_group.empty()
    ending_group.empty()

    #empty tile list
    data = []

    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data

class player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, is_demon=False):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 1
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.is_demon = is_demon  # New attribute to check if the character is a demon
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #ai
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False #diam
        self.idling_counter = 0

        #menampilkan semua gambar di folder untuk animasi
        animation_types = ['Diam', 'Lari', 'Loncat', 'Mati']
        for animation in animation_types:
            #reset gambar berulang-ulang
            temp_list = []
            #menghitung jumlah nomor dalam file di folder
            num_of_frames = len(os.listdir(f'Assets/Characters/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'Assets/Characters/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def update(self):
        self.update_animation()
        self.check_alive()
        self.check_fire_collision()  # Add this line
        #cooldown update
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def check_fire_collision(self):
        if pygame.sprite.spritecollide(self, fire_group, False):
            self.health -= 5
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self.update_action(3)  # Mati

    def move(self, moving_left, moving_right):
        #reset movement
        screen_scroll = 0
        dx = 0
        dy = 0

        #set movement kanan atau kiri
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        
        #loncat
        if self.jump == True and self.in_air == False:
            self.vel_y = -17
            self.jump = False
            self.in_air = True
        
        #gravitasi
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #mengecek tabrakan
        # Checking for collision
        for tile in world.obstacle_list:
            # Collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # If the character is a Goblin or Demon, change direction
                if self.char_type == 'Goblin':
                    self.direction *= -1
                    self.move_counter += 1
            # Collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Jump: check for collision if below the ground
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # If above ground
                elif self.vel_y >= 0: 
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        #menegecek collision dengan exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
        
        if pygame.sprite.spritecollide(self, ending_group, False):
            if not Atop_group or Atop.health == 0:
                ending_events()
                show_ending()


        #mengecek apabila karakter keluar dari layar
        if self.char_type == 'Kiki':
            if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
                dx = 0    
        
        #update posisi kotak
        self.rect.x += dx
        self.rect.y += dy

        #update scroll layar
        if self.char_type == 'Kiki':
            if (self.rect.right > screen_width - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - screen_width)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
            
        return screen_scroll, level_complete

    def shoot(self):
        if not self.is_demon and self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 27
            if self.char_type == 'Kiki':
                bullet1 = Bullet1(self.rect.centerx + (0.8 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                bullet1_group.add(bullet1)
            elif self.char_type == 'Goblin':
                bullet2 = Bullet2(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                bullet2_group.add(bullet2)
            elif self.char_type == 'Atop':
                bullet3 = Bullet3(self.rect.centerx + (0.8 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                bullet3_group.add(bullet3)
            #mengurangi amunisi
            self.ammo -= 1
        if self.char_type == 'Kiki':
            shot_fx.play()

    def ai(self):
        if self.alive and Kiki.alive:
            if self.is_demon:
                # Demon walks 
                if self.rect.colliderect(Kiki.rect):
                    Kiki.health -= 1
                    Kiki.check_alive()
                else:
                    if self.idling == False and random.randint(1, 200) == 1:
                        self.update_action(0) #0 itu diam
                        self.idling = True
                        self.idling_counter = 50
                    if self.idling == False:
                        if self.direction == 1:
                            ai_moving_right = True
                        else:
                            ai_moving_right = False
                        ai_moving_left = not ai_moving_right
                        self.move(ai_moving_left, ai_moving_right)
                        self.update_action(1) # lari
                        self.move_counter += 1
                        self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                        if self.move_counter > TILE_SIZE:
                            self.direction *= -1
                            self.move_counter *= -1
                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False
            else:
                # Existing Goblin AI
                if self.idling == False and random.randint(1, 100) == 1:
                    self.update_action(0) #0 itu diam
                    self.idling = True
                    self.idling_counter = 50
                if self.vision.colliderect(Kiki.rect):
                    self.update_action(0) #goblin diam
                    self.shoot()
                else:
                    if self.idling == False:
                        if self.direction == 1:
                            ai_moving_right = True
                        else:
                            ai_moving_right = False
                        ai_moving_left = not ai_moving_right
                        self.move(ai_moving_left, ai_moving_right)
                        self.update_action(1) # lari
                        self.move_counter += 1
                        self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                        if self.move_counter > TILE_SIZE:
                            self.direction *= -1
                            self.move_counter *= -1
                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False
            
        #scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        #update gambar berdasarkan frame sekarang
        self.image = self.animation_list[self.action][self.frame_index]
        #mengecek apabila waktu habis setelah update gambar terakhir
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #apabila animasi telah melewati waktu, reset ke awal
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
    
    def update_action(self, new_action):
        #mengecek apabila aksi sekarang berbeda dengan sebelumnya
        if new_action != self.action:
            self.action = new_action
            #update pengaturan animasi
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        #iterasi setiap nilai
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if (tile >= 0 and tile <= 2): #tanah permukaan
                        self.obstacle_list.append(tile_data)
                    if (tile >= 25 and tile <= 26):
                        self.obstacle_list.append(tile_data)
                    if tile >= 3 and tile <= 6:
                        ending = Ending(img, x * TILE_SIZE, y * TILE_SIZE)
                        ending_group.add(ending)
                    if tile >= 28 and tile <= 31:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    if tile == 32:
                        fire = Fire(img, x * TILE_SIZE, y * TILE_SIZE)
                        fire_group.add(fire)
                    if tile == 24:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    if tile == 9: #memunculkan kikii
                        Kiki = player('Kiki', x * TILE_SIZE, y * TILE_SIZE, 0.5, 7, 20)
                        Kiki_group.add(Kiki)
                        health_bar = HealthBar(10, 10, Kiki.health, Kiki.health)
                    if tile == 10: #memunculkan goblin
                        Goblin = player('Goblin', x * TILE_SIZE, y * TILE_SIZE, 0.4, 4, 20)
                        Goblin_group.add(Goblin)
                    if tile == 11: #memunculkan demon
                        Demon = player('Demon', x * TILE_SIZE, y * TILE_SIZE, 0.4, 4, 0, is_demon=True)
                        Demon_group.add(Demon)
                    if tile == 12: #roti buat health nambah
                        item_box = Item('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    if tile >= 13 and tile <= 23:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    if tile == 27: #nambah amunisi
                        item_box = Item('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    if tile == 7: #memunculkan atop
                        Atop = player('Atop', x * TILE_SIZE, y * TILE_SIZE, 1, 4, 20)
                        Atop_group.add(Atop)

        return Kiki, health_bar
    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Fire(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
            
        def update(self):
            self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll

class Ending(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll

class Item(pygame.sprite.Sprite):
        def __init__(self, item_type, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.item_type = item_type
            self.image = item_boxes[self.item_type]
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
        def update(self):
            #scroll
            self.rect.x += screen_scroll
            #cek apakah dah diambil player lom
            if pygame.sprite.collide_rect(self, Kiki):
                if self.item_type == 'Health':
                    Kiki.health += 25
                    if Kiki.health > Kiki.max_health:
                        Kiki.health = Kiki.max_health
                elif self.item_type == 'Ammo' :
                    Kiki.ammo += 5
                self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    
    def draw(self, health):
        #update health
        self.health = health

        #health rasio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class Bullet1(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet1_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)

        # Check if the bullet is out of screen boundaries
        if self.rect.left > screen_width or self.rect.right < 0:
            self.kill()

        if self.rect.left > screen_width or self.rect.right < 0:
            self.kill()
        # Check collision with world obstacles
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # Check collision with enemies
        for goblin in Goblin_group:
            if pygame.sprite.spritecollide(self, Goblin_group, False):
                if goblin.alive and self.rect.colliderect(goblin.rect):
                    goblin.health -= 45
                    self.kill()

        for demon in Demon_group:
            if pygame.sprite.spritecollide(demon, bullet1_group, False):
                if demon.alive:
                    demon.health -= 50
                    self.kill()

        for atop in Atop_group:
            if pygame.sprite.spritecollide(self, Atop_group, False):
                if atop.alive and self.rect.colliderect(atop.rect):
                    shot_fx.stop()
                    tantrum = pygame.mixer.Sound('Assets/Sound_Effects/Kiki_Suara/kiki-tantrum.wav')
                    tantrum.set_volume(0.5)
                    tantrum.play()
                    atop.health -= 7
                    self.kill()
            else:
                gakena = pygame.mixer.Sound('Assets/Sound_Effects/Atop_Suara/gak-kena.wav')
                gakena.set_volume(0.1)
                gakena.play()

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.image = bullet2_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)

        # Check if the bullet is out of screen boundaries
        if self.rect.left > screen_width or self.rect.right < 0:
            self.kill()

        # Check collision with world obstacles
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # Check collision with Kiki (player)
        for kiki in Kiki_group:
            if pygame.sprite.spritecollide(self, Kiki_group, False):
                if kiki.alive and self.rect.colliderect(kiki.rect):
                    kiki.health -= 7
                    self.kill()

class Bullet3(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 3
        self.image = bullet3_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        api = pygame.mixer.Sound('Assets/Sound_Effects/Atop_Suara/nyembur-api.wav')
        api.set_volume(0.5)
        api.play()

        # Check if the bullet is out of screen boundaries
        if self.rect.left > screen_width or self.rect.right < 0:
            self.kill()

        # Check collision with world obstacles
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # Check collision with Kiki (player)
        for kiki in Kiki_group:
            if pygame.sprite.spritecollide(kiki, bullet3_group, False):
                if kiki.alive:
                    kena = pygame.mixer.Sound('Assets/Sound_Effects/Kiki_Suara/kiki-kena.wav')
                    kena.set_volume(0.7)
                    kena.play()
                    kiki.health -= 10
                    self.kill()
mati = pygame.mixer.Sound('Assets/Sound_Effects/mati.mp3')
mati.set_volume(0.8)
class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0
        self.mati_played = False
    
    def fade(self):  
            fade_complete = False
            self.fade_counter += self.speed
            if self.direction == 1:#whole screen fade
                pygame.draw.rect(screen, self.colour, (0, 0, screen_width, screen_height // 2 - self.fade_counter))
                pygame.draw.rect(screen, self.colour, (0, screen_height // 2 + self.fade_counter, screen_width, screen_height // 2 + self.fade_counter))
            if self.direction == 2:#vertical screen fade down
                if not self.mati_played:
                    mati.play()
                    self.mati_played = True
                pygame.draw.rect(screen, self.colour, (0, 0, screen_width, 0 + self.fade_counter))
            if self.fade_counter >= screen_width:
                fade_complete = True

            return fade_complete

intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, DIRT, 4)

#create buttons
start_button = button.Button(235, 481, start_img, 1)
exit_button = button.Button(578, 481, exit_img, 1)
restart_button = button.Button(406, 318, retry_img, 1)

#sprite groups
Atop_group = pygame.sprite.Group()
Kiki_group = pygame.sprite.Group()
Goblin_group = pygame.sprite.Group()
bullet1_group = pygame.sprite.Group()
bullet2_group = pygame.sprite.Group()
bullet3_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
Demon_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
ending_group = pygame.sprite.Group()

#empty tile list untuk awal
world_data = []

for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)

#load level dan membuat dunia
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
Kiki, health_bar = world.process_data(world_data)

run = True
while run:
    clock.tick(FPS)

    if start_game == False:
        # Memulai musik hanya jika belum dimainkan
        try:
            backsound.play()
        except pygame.error as e:
            print(f"Gagal memutar lagu {e}")
        
        # Menu
        open_bg()
        display_background()

        # Button
        if start_button.draw(screen):
            button_click.play()
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            button_click.play()
            run = False
        
    else:
        backsound.stop()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('Assets/Music/backsound.wav')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        
        if start_story == True:
            story_events()
            show_story()
        if start_story == False:
            draw_bg()
            world.draw()
            health_bar.draw(Kiki.health)
        
            if level == 2 or level == 4:
                draw_text('Ammo: ', font, WHITE, 10, 45)
                for x in range(Kiki.ammo):
                    screen.blit(bullet1_img, (80 + (x * 10), 39))
            else:
                draw_text('Ammo: ', font, BLACK, 10, 45)
                for x in range(Kiki.ammo):
                    screen.blit(bullet1_img, (80 + (x * 10), 39))

            Kiki.update()
            Kiki.draw()

            for Goblin in Goblin_group:
                Goblin.ai()
                Goblin.update()
                Goblin.draw()
            
            for Demon in Demon_group:
                Demon.ai()
                Demon.update()
                Demon.draw()

            for Atop in Atop_group:
                Atop.ai()
                Atop.update()
                Atop.draw()

            bullet1_group.update()
            bullet2_group.update()
            bullet3_group.update()
            item_box_group.update()
            decoration_group.update()
            fire_group.update()
            exit_group.update()
            ending_group.update()
            bullet1_group.draw(screen)
            bullet2_group.draw(screen)
            bullet3_group.draw(screen)
            item_box_group.draw(screen)
            decoration_group.draw(screen)
            fire_group.draw(screen)
            exit_group.draw(screen)
            ending_group.draw(screen)

            if start_intro == True:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            if Kiki.alive:
                if shoot:
                    Kiki.shoot()
                if Kiki.in_air:
                    Kiki.update_action(2) #loncat
                elif moving_left or moving_right:
                    Kiki.update_action(1) #lari
                else:
                    Kiki.update_action(0) #diam
                screen_scroll, level_complete = Kiki.move(moving_left, moving_right)
                bg_scroll -= screen_scroll
            
            #check level complete
                if level_complete and Kiki.alive:
                    start_intro = True
                    level += 1
                    bg_scroll = 0
                    world_data = reset_level()
                    if level <= MAX_LEVELS:
                            #load in level data and create world
                            with open(f'level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            Kiki, health_bar = world.process_data(world_data)	
            else:
                    screen_scroll = 0
                    if death_fade.fade():
                        if restart_button.draw(screen):
                            button_click.play()
                            death_fade.fade_counter = 0
                            start_intro = True
                            bg_scroll = 0
                            world_data = reset_level()
                            #load in level data and create world
                            with open(f'level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            Kiki, health_bar = world.process_data(world_data)          

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and Kiki.alive:
                Kiki.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_KP_ENTER:
                button_click.play()
                show_story()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()

pygame.quit()