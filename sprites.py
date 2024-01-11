import pygame
from settings import *
import random

vec = pygame.math.Vector2
def scale_img(listi,scale):
    listii = []
    for img in listi:
        new_w = round(scale*img.get_width())
        new_h = round(scale*img.get_height())
        img = pygame.transform.scale(img,(new_w,new_h))
        listii.append(img)
    return listii

class Ground(pygame.sprite.Sprite):
    def __init__(self,game,level,x,y):
        self.groups = game.all_sprites,game.all_draw
        super().__init__(self.groups)
        self.image = level
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.topleft = self.pos
    def draw(self,surf):
        surf.blit(self.image, self.pos)
        self.pos = self.rect.topleft

class Background:

    def __init__(self,game):
        self.base_layer = pygame.transform.scale(game.sky,(WIDTH,HEIGHT))
    
    def draw(self,surf):
        surf.blit(self.base_layer, (0,0))
        

class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_img(self,x,y,w,h):
        img = pygame.Surface((w,h),pygame.SRCALPHA)
        img.blit(self.spritesheet,(0,0) ,(x,y,w,h))
        return img

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites, game.player_group,game.all_draw
        super().__init__(self.groups)
        self.game = game
        self.load_images()
        self.image = self.jump_l[1]
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.jumping = True
        self.state = LEFT
        self.last_dir = LEFT
        self.attacking = False
        self.kicking = False
        self.going_up = False
        self.time_of_jump = 0
        self.doing_damage = False
        self.coins = 0
        self.press_q_text = False
        self.interact = False
        self.is_big = False

       
        self.rect = self.image.get_rect()
        self.hitbox = self.game.player_sheet.get_img(4,56,31,48).get_rect()
        self.dmg_box = pygame.Surface((50,50)).get_rect()
        
        self.pos = vec(300,225)
        self.vel = vec(0,0)

        self.rect.midbottom = self.pos


        self.on_ground = False
         ###########
        self.sewy = False
        self.movingcollide = False
        self.movment2 = 0
        self.movment1 = 0
        self.mate = False
        self.width = self.rect.width
        self.height = self.rect.height
        ###########
    
    def hitbox_collide(self,sprite1,sprite2):
        return sprite1.hitbox.colliderect(sprite2.rect)
    
    def damage_collide(self,sprite1,sprite2):
        return sprite1.dmg_box.colliderect(sprite2.rect)


    def load_images(self):
        self.standing_left = [self.game.player_sheet.get_img(4,56,31,48),
                         self.game.player_sheet.get_img(37,56,31,48),
                         self.game.player_sheet.get_img(70,56,31,48),
                         self.game.player_sheet.get_img(103,56,31,48)]
        self.standing_left_big = scale_img(self.standing_left,PLAYER_SCALE)
        self.standing_right = []
        for frame in self.standing_left:
            self.standing_right.append(pygame.transform.flip(frame,True,False))
        self.standing_right_big = scale_img(self.standing_right,PLAYER_SCALE)

        self.run_left = [self.game.player_sheet.get_img(4,2,30,48),
                         self.game.player_sheet.get_img(36,2,35,47),
                         self.game.player_sheet.get_img(73,2,30,46),
                         self.game.player_sheet.get_img(105,2,33,46)]
        
        self.run_left_big = scale_img(self.run_left,PLAYER_SCALE)

        self.run_right = []
        for frame in self.run_left:
            self.run_right.append(pygame.transform.flip(frame,True,False))
        self.run_right_big = scale_img(self.run_right,PLAYER_SCALE)

        self.jump_l = [self.game.player_sheet.get_img(141,1,37,53),
        self.game.player_sheet.get_img(180,1,42,46),
        self.game.player_sheet.get_img(224,1,45,50)]

        self.jump_l_big = scale_img(self.jump_l,PLAYER_SCALE)

        self.jump_r = []
        for frame in self.jump_l:
            self.jump_r.append(pygame.transform.flip(frame,True,False))
        self.jump_r_big = scale_img(self.jump_r,PLAYER_SCALE)
       

        self.kicking_l = [self.game.player_sheet.get_img(472,2,44,50),
                          self.game.player_sheet.get_img(519,2,47,45)]
        self.kicking_l_big = scale_img(self.kicking_l, PLAYER_SCALE)
        self.kicking_r = []
        for frame in self.kicking_l:
            self.kicking_r.append(pygame.transform.flip(frame,True,False))
        self.kicking_r_big = scale_img(self.kicking_r, PLAYER_SCALE)

        self.punching_l = [self.game.player_sheet.get_img(318,3,29,45),
                         self.game.player_sheet.get_img(350,4,37,44),
                         self.game.player_sheet.get_img(390,2,31,46),
                         self.game.player_sheet.get_img(424,4,45,44)]
        self.punching_l_big = scale_img(self.punching_l, PLAYER_SCALE)
        self.punching_r = []
        for frame in self.punching_l:
            self.punching_r.append(pygame.transform.flip(frame,True,False))
        self.punching_r_big = scale_img(self.punching_r, PLAYER_SCALE)

    def update(self):
        self.acc = vec(0, GRAVITY)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.acc.x = ACC
            self.last_dir = RIGHT
        if keys[pygame.K_a]:
            self.acc.x = -ACC
            self.last_dir = LEFT
        

        #Loftmotstada 
        self.acc.x -= self.vel.x * DRAG 

        old_pos = vec(self.pos)

        # x = 0.5*a*t^2+v_0*t + x_0 (t = 1 rammi)
        self.pos = 0.5*self.acc + self.vel + self.pos

        self.hitbox.midbottom = self.rect.midbottom
        if self.last_dir == RIGHT:
            self.dmg_box.midbottom = self.hitbox.bottomright
        else:
            self.dmg_box.midbottom = self.hitbox.bottomleft
        
        self.vel = self.acc + self.vel
        dx = round(self.pos.x - old_pos.x)
        self.rect.centerx += dx

        self.hitbox.midbottom = self.rect.midbottom
        if self.last_dir == RIGHT:
            self.dmg_box.midbottom = self.hitbox.bottomright
        else:
            self.dmg_box.midbottom = self.hitbox.bottomleft

        hits = pygame.sprite.spritecollide(self, self.game.all_platforms, False, self.hitbox_collide)
        if hits:
            if self.vel.x>0:
                self.hitbox.right = hits[0].rect.left
            elif self.vel.x<0:
                self.hitbox.left = hits[0].rect.right
            self.vel.x = 0

        self.rect.midbottom = self.hitbox.midbottom
        if self.last_dir == RIGHT:
            self.dmg_box.midbottom = self.hitbox.bottomright
        else:
            self.dmg_box.midbottom = self.hitbox.bottomleft

        dy = round(self.pos.y - old_pos.y)
        self.rect.centery += dy

        self.hitbox.midbottom = self.rect.midbottom
        if self.last_dir == RIGHT:
            self.dmg_box.midbottom = self.hitbox.bottomright
        else:
            self.dmg_box.midbottom = self.hitbox.bottomleft
        
        hits = pygame.sprite.spritecollide(self, self.game.all_platforms, False, self.hitbox_collide)
        if hits:
            self.on_ground = True
            if self.vel.y>0:
                self.hitbox.bottom = hits[0].rect.top
                self.jumping = False
            elif self.vel.y<0:
                self.hitbox.top = hits[0].rect.bottom
            self.vel.y = 0
        else:
            self.on_ground = False
        ##############
        for platform in self.game.moving_platforms:
            if platform.rect.colliderect(self.rect.x +dx, self.rect.y, self.width, self.height):
                self.vel.x = 0
                
            if platform.rect.colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                if self.vel.y < 1:
                    self.rect.top = platform.rect.bottom
                    self.vel.y = 1
                    
                else:
                    self.rect.bottom = platform.rect.top 
                    self.vel.y = 0
                    self.sewy = True
                    self.jumping = False
                    self.movingcollide = True
                self.location = platform.rect.top

                self.movment1 = self.movment2
                self.movment2 = platform.rect.centery

        #############################

        hits = pygame.sprite.spritecollide(self, self.game.collectables, True, self.hitbox_collide)
        if hits:
            self.coins +=1
        hits = pygame.sprite.spritecollide(self, self.game.interact, False)
        if hits:
            self.press_q_text = True
        else:
            self.press_q_text = False

        self.rect.midbottom = self.hitbox.midbottom
        if self.last_dir == RIGHT:
            self.dmg_box.midbottom = self.hitbox.bottomright
        else:
            self.dmg_box.midbottom = self.hitbox.bottomleft
        self.pos = vec(self.rect.midbottom)

        dx = round(self.pos.x - old_pos.x)

        self.hitbox.midbottom = self.rect.midbottom
        if self.last_dir == RIGHT:
            self.dmg_box.midbottom = self.hitbox.bottomright
        else:
            self.dmg_box.midbottom = self.hitbox.bottomleft

        if self.pos.x >= WIDTH-BNDRY or self.pos.x <= BNDRY:
            self.game.movement_x+=dx
            for sprite in self.game.all_sprites:
                sprite.rect.centerx -= dx
                
            self.pos = vec(self.rect.midbottom)

        dy = round(self.pos.y - old_pos.y)
        if self.pos.y <= BNDRY or self.pos.y >= HEIGHT-BNDRY:
            for sprite in self.game.all_sprites:
                sprite.rect.centery -= dy
            self.pos = vec(self.rect.midbottom)

        self.hitbox.midbottom = self.rect.midbottom
        if self.last_dir == RIGHT:
            self.dmg_box.midbottom = self.hitbox.bottomright
        else:
            self.dmg_box.midbottom = self.hitbox.bottomleft
         ##############   
        if dy != 0 and not self.movingcollide:
            self.jumping = True
        #############
        if dy>0:
            self.jumping = True
            self.going_up = True
        if dy<0:
            self.going_up = False

        if dx > 0:
            self.state = RIGHT
        elif dx <0:
            self.state =LEFT

        else:
            if self.state != STANDING:
                self.last_update = 0
            self.state = STANDING
        
        ########
        self.rect.centery += 1
        hit = pygame.sprite.spritecollide(self, self.game.moving_platforms, False)
        self.rect.centery -= 1
        if len(hit) > 0:
            self.movingcollide = True
        else:
            self.movingcollide = False
        if self.movingcollide:
            if self.movment1 < self.movment2:
                if self.mate:
                    self.vel.y = 2
                else:
                    self.vel.y = 1
            elif self.movment1 > self.movment2:
                self.vel.y = -1

        self.animate()

    def animate(self):
        now  = pygame.time.get_ticks()
        if self.is_big:
            if self.attacking:
                if self.jumping:
                    self.kicking = True
                if self.kicking:
                    if self.last_dir == RIGHT:
                        self.image = self.kicking_r_big[0]
                        if now-self.game.time_of_attack > 240:
                            self.image = self.kicking_r_big[1]
                        if now-self.game.time_of_attack > 800:
                            self.attacking = False
                            self.kicking = False
                    else:
                        self.image = self.kicking_l_big[0]
                        if now-self.game.time_of_attack > 240:
                            self.image = self.kicking_l_big[1]
                        if now-self.game.time_of_attack > 600:
                            self.attacking = False
                            self.kicking = False
                else:
                    if now-self.last_update >70:
                        self.current_frame = (self.current_frame +1)%len(self.punching_l)
                        self.last_update = now
                    if self.last_dir == RIGHT:
                        self.image = self.punching_r_big[self.current_frame]
                    else:
                        self.image = self.punching_l_big[self.current_frame]
                    if now - self.game.time_of_attack >600:
                        self.attacking = False
                        self.last_update = 0
          ################################
            #elif self.state == STANDING and not self.jumping:
                
                #if now - self.last_update > 1000:
                   # self.current_frame = (self.current_frame +1)%len(self.standing_left)
                    #if self.last_dir == RIGHT:
                      #  self.image = self.standing_right[self.current_frame]
                   # else:
                        #self.image = self.standing_left[self.current_frame]
                   # self.last_update = now
            ###################################

            elif self.jumping:
                if self.last_dir == RIGHT:
                    if now-self.time_of_jump<500:
                        self.image = self.jump_r_big[0]
                    elif self.going_up:
                        self.image = self.jump_r_big[1]
                    else:
                        self.image = self.jump_r_big[2]

                else:
                    if now-self.time_of_jump<500:
                        self.image = self.jump_l_big[0]
                    elif self.going_up:
                        self.image = self.jump_l_big[1]
                    else:
                        self.image = self.jump_l_big[2]

            elif self.state == STANDING:
                
                if now - self.last_update > 1000:
                    self.current_frame = (self.current_frame +1)%len(self.standing_left)
                    if self.last_dir == RIGHT:
                        self.image = self.standing_right_big[self.current_frame]
                    else:
                        self.image = self.standing_left_big[self.current_frame]
                    self.last_update = now

            else:
                if now - self.last_update > 50:
                    self.current_frame = (self.current_frame +1)%len(self.run_left)
                    if self.state == RIGHT:
                        self.image = self.run_right_big[self.current_frame]
                    else:
                        self.image = self.run_left_big[self.current_frame]
                    self.last_update = now

        else:
            if self.attacking:
                if self.jumping:
                    self.kicking = True
                if self.kicking:
                    if self.last_dir == RIGHT:
                        self.image = self.kicking_r[0]
                        if now-self.game.time_of_attack > 240:
                            self.image = self.kicking_r[1]
                        if now-self.game.time_of_attack > 800:
                            self.attacking = False
                            self.kicking = False
                    else:
                        self.image = self.kicking_l[0]
                        if now-self.game.time_of_attack > 240:
                            self.image = self.kicking_l[1]
                        if now-self.game.time_of_attack > 600:
                            self.attacking = False
                            self.kicking = False
                else:
                    if now-self.last_update >70:
                        self.current_frame = (self.current_frame +1)%len(self.punching_l)
                        self.last_update = now
                    if self.last_dir == RIGHT:
                        self.image = self.punching_r[self.current_frame]
                    else:
                        self.image = self.punching_l[self.current_frame]
                    if now - self.game.time_of_attack >600:
                        self.attacking = False
                        self.last_update = 0

            elif self.jumping:
                if self.last_dir == RIGHT:
                    if now-self.time_of_jump<500:
                        self.image = self.jump_r[0]
                    elif self.going_up:
                        self.image = self.jump_r[1]
                    else:
                        self.image = self.jump_r[2]

                else:
                    if now-self.time_of_jump<500:
                        self.image = self.jump_l[0]
                    elif self.going_up:
                        self.image = self.jump_l[1]
                    else:
                        self.image = self.jump_l[2]

            elif self.state == STANDING:
                
                if now - self.last_update > 1000:
                    self.current_frame = (self.current_frame +1)%len(self.standing_left)
                    if self.last_dir == RIGHT:
                        self.image = self.standing_right[self.current_frame]
                    else:
                        self.image = self.standing_left[self.current_frame]
                    self.last_update = now

            else:
                if now - self.last_update > 50:
                    self.current_frame = (self.current_frame +1)%len(self.run_left)
                    if self.state == RIGHT:
                        self.image = self.run_right[self.current_frame]
                    else:
                        self.image = self.run_left[self.current_frame]
                    self.last_update = now
    

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos

    def jump(self):

        self.hitbox.centery += 1
        hits = pygame.sprite.spritecollide(self, self.game.all_platforms, False, self.hitbox_collide)
        if len(hits) > 0:
            self.sewy = True
        self.hitbox.centery -= 1

        if self.sewy:
            if self.jumping == False:
                self.time_of_jump = pygame.time.get_ticks()
            self.jumping = True
            if self.is_big:
                self.vel.y = -20
            else:
                self.vel.y = -13
            self.sewy = False
            self.movingcollide = False
    
    def attack(self):
        self.attacking = True
        



class Platform(pygame.sprite.Sprite):

    def __init__(self, game,x,y,width,height):
        self.groups = game.all_platforms,game.all_sprites
        super().__init__(self.groups)
        self.rect = pygame.Surface((width,height)).get_rect()
        self.rect.topleft = vec(x,y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, player,x,y,bndry):
        self.groups = game.all_sprites,game.all_mobs,game.all_draw
        super().__init__(self.groups)
        self.x = x
        self.game = game
        self.player = player
        self.load_images()
        self.image = self.standing_l[0]
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.state = LEFT
        self.player_dir = LEFT
        self.just_stopped = True
        self.in_range = False
        self.attacking= False
        self.time_of_attack = 0
        self.counter = 0
        self.time_of_last_attack = 0
        self.just_damaged = False
        self.is_dead = False
        self.time_of_death = 0
        self.bndry = bndry


        self.rect = self.image.get_rect()
        self.hitbox = self.image.get_rect()
        self.atk_box = self.atk_l[2].get_rect()

        self.pos = vec(x,HEIGHT-y)
        self.vel = vec(2,0)

        self.rect.midbottom = self.pos
        self.atk_box.midbottom = self.rect.midbottom

    def atk_collide(self,sprite1,sprite2):
        return sprite1.atk_box.colliderect(sprite2.hitbox)
    def damage_collide(self,sprite1,sprite2):
        return sprite1.rect.colliderect(sprite2.dmg_box)

    def load_images(self):

        self.standing_l = [self.game.sveppi_sheet.get_img(61,27,57,58)]
        self.standing_r = []
        self.standing_r.append(pygame.transform.flip(self.standing_l[0],True,False))

        self.walking_l = [self.game.sveppi_sheet.get_img(54,114,56,58),
                            self.game.sveppi_sheet.get_img(129,109,56,57),
                            self.game.sveppi_sheet.get_img(204,120,53,57),
                            self.game.sveppi_sheet.get_img(280,119,56,58)]
        self.walking_r = []
        for frame in self.walking_l:
            self.walking_r.append(pygame.transform.flip(frame,True,False))
        
        self.dmg_l = [self.game.sveppi_sheet.get_img(390,28,48,57),
                        self.game.sveppi_sheet.get_img(370,138,78,39)]
        self.dmg_r = []
        for frame in self.dmg_l:
            self.dmg_r.append(pygame.transform.flip(frame,True,False))
        
        self.atk_l = [self.game.sveppi_sheet.get_img(19,202,52,57),
                    self.game.sveppi_sheet.get_img(84,202,98,57),
                    self.game.sveppi_sheet.get_img(196,196,85,63),
                    self.game.sveppi_sheet.get_img(296,196,117,63),
                    self.game.sveppi_sheet.get_img(433,203,48,56)]
        self.atk_r = []
        for frame in self.atk_l:
            self.atk_r.append(pygame.transform.flip(frame,True,False))

        self.dust = []
        for n in range(7):
            self.dust.append(self.game.dust1_sheet.get_img(n*228,0,228,200))
        for n in range(7):
            self.dust.append(self.game.dust2_sheet.get_img(n*228,0,228,200))

        self.dust = scale_img(self.dust, 0.4)
    def update(self):
        now  = pygame.time.get_ticks()
        self.pos = vec(self.rect.midbottom)
        self.movement_x = (self.rect.midbottom[0])+self.game.movement_x
        if not self.is_dead:
            if not self.attacking:
                hits = pygame.sprite.spritecollide(self, self.game.player_group, False, self.damage_collide)
                if hits and self.game.player.attacking:
                    self.is_dead = True
                    self.attacking = False
                    self.time_of_death = now

                self.just_damaged = True
                if abs(self.player.hitbox.centery - self.rect.centery) <= 200 and abs(self.player.hitbox.centerx - self.rect.centerx) <= 450:
                    self.in_range = True
                    if abs(self.player.hitbox.centery - self.rect.centery) <= 60 and abs(self.player.hitbox.centerx - self.rect.centerx) <= 60 and now-self.time_of_last_attack > 3000:
                        self.time_of_attack = now
                        self.current_frame = 0
                        self.attacking = True
                        self.just_damaged = False
                        self.atk_box.midbottom = self.rect.midbottom
                    elif abs(self.player.hitbox.centerx - self.rect.centerx) <= 20:
                        self.in_range = False
                    else:
                        if self.state == RIGHT and self.movement_x<self.bndry[1]*35-28:
                            self.pos += self.vel
                        elif self.bndry[0]*35<=self.movement_x:
                            self.pos -= self.vel
                        

                else:
                    self.in_range = False
                if self.player.hitbox.centerx >= self.rect.centerx:
                    self.state = RIGHT
                else:
                    self.state = LEFT
            else:
                hits = pygame.sprite.spritecollide(self, self.game.player_group, False, self.atk_collide)
                if hits and not self.just_damaged:
                    self.just_damaged = True
                    if self.game.player.last_dir == RIGHT:
                        self.game.player.vel.x = -13
                    else:
                        self.game.player.vel.x = 13
            self.rect.midbottom = self.pos
            self.atk_box.midbottom = self.rect.midbottom
            
            self.animate()
        else:
            if self.state == RIGHT:
                if now - self.time_of_death <500:
                    self.image = self.dmg_r[0]
                if 500 < now - self.time_of_death <800:
                    self.image = self.dmg_r[1]
                    self.rect = self.image.get_rect()
                    self.rect.midbottom = self.pos
    
            else:
                if now - self.time_of_death <500:
                    self.image = self.dmg_l[0]
                if 500 < now - self.time_of_death <800:
                    self.image = self.dmg_l[1]
                    self.rect = self.image.get_rect()
                    self.rect.midbottom = self.pos

            if now - self.time_of_death >800:
                if 800< now - self.time_of_death < 818:
                    self.rect.midbottom -= vec(0,25)
                if now - self.last_update>50:
                    if self.counter == 13:
                        self.kill()
                    self.image = self.dust[self.counter]
                    self.counter+=1                        
                    self.last_update = now
    def animate(self):
        now  = pygame.time.get_ticks()
        if self.attacking:
            if now - self.last_update > 100:
                if self.current_frame == len(self.atk_l)-1:
                    self.attacking = False
                    self.time_of_last_attack = now

                if self.state == RIGHT:
                    self.image = self.atk_r[self.current_frame]
                    
                else:
                    self.image = self.atk_l[self.current_frame]
                self.last_update = now
                self.current_frame += 1



        elif self.in_range:
            self.just_stopped = True
            if now - self.last_update > 100:
                self.current_frame = (self.current_frame +1)%len(self.walking_l)
                if self.state == RIGHT:
                    self.image = self.walking_r[self.current_frame]
                else:
                    self.image = self.walking_l[self.current_frame]
                self.last_update = now
            

        else:
            if self.just_stopped:
                self.just_stopped = False
                self.last_update = 0
            if now-self.last_update >= 1000:
                x = random.randint(0,1)
                if x == 0:
                    self.image = self.standing_r[0]
                else:
                    self.image = self.standing_l[0]
                self.last_update = now

class Teleport(pygame.sprite.Sprite):

    def __init__(self, game, player,start,ending,q):

        if q == True:
            self.groups = game.all_sprites, game.all_tele, game.interact
        else:
            self.groups = game.all_sprites, game.all_tele
        super().__init__(self.groups)
        self.game = game
        self.start = start
        self.player = player
        self.ending = vec(ending)
        self.org_ending = vec(ending)
        self.rect = pygame.Surface((start[2],start[3])).get_rect()
        self.rect.bottomleft = vec(start[0],start[1])
        self.q = q
        
    def update(self):
        #self.ending.x = self.org_ending.x - (self.start[0]-self.rect.bottomleft[0])
        #self.ending.y = self.org_ending.y - (self.start[1]-self.rect.bottomleft[1])
        self.ending = self.org_ending - ((self.start[0]-self.rect.bottomleft[0]),(self.start[1]-self.rect.bottomleft[1]))
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
        if hits and not self.q:
            self.player.rect.midbottom = vec(self.ending)
    def interact(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
        if hits:
            self.player.rect.midbottom = vec(self.ending)
class Boss_teleport(pygame.sprite.Sprite):

    def __init__(self, game, player,start,ending,q):
        self.groups = game.all_sprites, game.all_tele, game.interact
        super().__init__(self.groups)
        self.game = game
        self.start = start
        self.player = player
        self.ending = vec(ending)
        self.org_ending = vec(ending)
        self.rect = pygame.Surface((start[2],start[3])).get_rect()
        self.rect.bottomleft = vec(start[0],start[1])
        self.q = q
        
    def update(self):
        #self.ending.x = self.org_ending.x - (self.start[0]-self.rect.bottomleft[0])
        #self.ending.y = self.org_ending.y - (self.start[1]-self.rect.bottomleft[1])
        self.ending = self.org_ending - ((self.start[0]-self.rect.bottomleft[0]),(self.start[1]-self.rect.bottomleft[1]))
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
        if hits and not self.q:
            self.player.rect.midbottom = vec(self.ending)
    def interact(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
        if hits and self.game.caastle.is_open:
            self.player.rect.midbottom = vec(self.ending)
            self.game.background.base_layer = self.game.boss_level
            self.game.time_of_ending = self.game.time
            self.game.ending = True

class Collectable(pygame.sprite.Sprite):

    def __init__(self, game,img, x, y):
        self.groups = game.collectables, game.all_sprites,game.all_draw
        super().__init__(self.groups)
        self.game = game
        self.image = pygame.transform.scale(img,(70,70))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = vec(x, y)
        self.last_update = 0
        self.dir = RIGHT
    def update(self):
        now  = pygame.time.get_ticks()
        
        if now-self.last_update>=500:
            if self.dir == RIGHT:
                self.dir = LEFT
            else:
                self.dir = RIGHT
            self.last_update = now

        if self.dir == RIGHT:
            self.rect.midbottom += vec(0,1)
        else:
            self.rect.midbottom -= vec(0,1)

class Castle(pygame.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites,game.all_draw
        super().__init__(self.groups)
        self.image = game.castle
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.bottomleft = vec(28*35,HEIGHT+10)
        self.is_open = False
        
    
    def damage_collide(self,sprite1,sprite2):
        return sprite1.rect.colliderect(sprite2.dmg_box)

    def update(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False, self.damage_collide)
        if hits and self.game.player.attacking and self.game.player.is_big and not self.is_open:
            self.image = self.game.castle_open
            self.is_open = True
class Gillz(pygame.sprite.Sprite):
    def hitbox_collide(self,sprite1,sprite2):
        return sprite1.hitbox.colliderect(sprite2.rect)
    def __init__(self, game):
        self.groups = game.all_sprites,game.all_draw,game.interact
        super().__init__(self.groups)
        self.gillz_1 = pygame.transform.scale(game.gillz_img,(120,120))
        self.gillz_2 = pygame.transform.scale(game.gillz_img_2,(120,120))
        self.image = self.gillz_1
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Surface((350,100)).get_rect()
        self.rect.bottomleft = vec(4*35,HEIGHT)
        self.hitbox.midbottom = self.rect.midbottom
        self.game = game
        self.bubble_1 = False
        self.bubble_2 = False
        self.bubble_3 = False
        self.bubble_4 = False
        self.q = 0
        self.last_update = 0
        self.img = 1
    def update(self):
        now = pygame.time.get_ticks()
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False, self.hitbox_collide)
        if hits and self.q == 0:
            self.bubble_1 = True
        elif hits and self.q == 1:
            self.bubble_2 = True
            self.bubble_1 = False
        elif hits and self.q>=2 and self.game.player.coins >= 3:
            self.bubble_4 = True
            self.bubble_3 = False
            self.bubble_2 = False
            self.game.player.is_big = True
            self.game.player.dmg_box = pygame.Surface((100,100)).get_rect()
            self.game.player.hitbox = self.game.player.standing_left_big[0].get_rect()
        elif hits and self.q >= 2:
            self.bubble_3 = True
            self.bubble_2 = False
        
        else:
            self.bubble_1 = False
            self.bubble_2 = False
            self.bubble_3 = False
            self.bubble_4 = False
        self.hitbox.midbottom = self.rect.midbottom
        if now-self.last_update>400:
            if self.img == 1:
                self.image = self.gillz_2
                self.last_update = now
                self.img = 2
            else:
                self.image = self.gillz_1
                self.last_update = now
                self.img = 1

        
    def interact(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False,self.hitbox_collide)
        if hits:
            self.q +=1
class Moving_Platform(pygame.sprite.Sprite):

    #(x,y) -> efra vinstra horn
    def __init__(self, game, x, y, width, height, bottom):
        self.groups = game.all_sprites, game.moving_platforms
        super().__init__(self.groups)
        x = -11000 +x * 35
        y = y * 35
        width = width * 35
        height = height * 35
        self.platform = 0
        self.start = 0
        self.end = bottom * 35
        self.moving = 1
        
        self.image = pygame.Surface((width, height),pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = vec(x, y)


    def update(self):
        self.platform += self.moving
        if self.platform >= self.end:
            self.moving = -1
        elif self.platform <= self.start:
            self.moving = 1

        self.rect.centery += self.moving