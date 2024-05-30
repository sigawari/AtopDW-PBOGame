class atop(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 200
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
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
        animation_types = ['Diam', 'Mati']
        for animation in animation_types:
            #reset gambar berulang-ulang
            temp_list = []
            #menghitung jumlah nomor dalam file di folder
            num_of_frames = len(os.listdir(f'Assets/Characters/Atop/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'Assets/Characters/Atop/{animation}/{i}.png')
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
        #cooldown update
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

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
                if self.char_type == 'Goblin' or self.char_type == 'Demon':
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
            
            return screen_scroll

    def shoot(self):
        if not self.is_demon and self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.8 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            #mengurangi amunisi
            self.ammo -= 1

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