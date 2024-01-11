
import pygame
from settings import *
from sprites import *
import random
from os import path
from menu import Menu
from pygame import mixer
pygame.init()
font = pygame.font.Font("freesansbold.ttf", 16)
Big_font = pygame.font.Font("freesansbold.ttf", 32)
#*** Föll ******



#****** GAME ENGINE ***********
class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
    

        self.running = True
        self.load_data()

        self.menu =Menu(self)

    def load_data(self):
        main_dir = path.dirname(__file__)
        img_dir = path.join(main_dir, "img")
        snd_dir = path.join(main_dir, "snd")
        self.tile_sheet = Spritesheet(path.join(img_dir,"tiles_spritesheet.png"))
        self.player_sheet = Spritesheet(path.join(img_dir,"Player_sheet.png"))
        self.sveppi_sheet = Spritesheet(path.join(img_dir, "Sveppi.png"))
        self.dust1_sheet = Spritesheet(path.join(img_dir, "dust1.png"))
        self.dust2_sheet = Spritesheet(path.join(img_dir, "dust2.png"))

        
        self.needle = pygame.image.load(path.join(img_dir, "nal.png")).convert_alpha()
        self.can = pygame.image.load(path.join(img_dir, "can.png")).convert_alpha()


        self.level_1 = pygame.image.load(path.join(img_dir, "Gillz_map.png")).convert_alpha()
        self.kjallari = pygame.image.load(path.join(img_dir, "kjallari.png")).convert_alpha()
        self.level_2 = pygame.image.load(path.join(img_dir,"poop_map.png")).convert_alpha()
        self.cloud_map = pygame.image.load(path.join(img_dir,"cloud_jump.png")).convert_alpha()
        self.solva_map = pygame.image.load(path.join(img_dir,"sveppa_level.png")).convert_alpha()


        self.sky = pygame.image.load(path.join(img_dir,"mountain.jpg")).convert()
        self.castle = pygame.image.load(path.join(img_dir,"castle.png")).convert_alpha()
        self.castle_open = pygame.image.load(path.join(img_dir,"castle_open.png")).convert_alpha()
        self.gillz_img = pygame.image.load(path.join(img_dir,"Gillz.png")).convert_alpha()
        self.gillz_img_2 = pygame.image.load(path.join(img_dir,"Gillz_2.png")).convert_alpha()
        self.boss_level = pygame.image.load(path.join(img_dir,"boss_level.png")).convert_alpha()

        mixer.music.load(path.join(snd_dir,"Mafar.wav"))
        mixer.music.play(-1)

    def new(self):
        self.background = Background(self)
        self.time_of_start = pygame.time.get_ticks()
        self.time_of_ending = 0
        self.ending = False

        self.player_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_platforms = pygame.sprite.Group()
        self.all_mobs = pygame.sprite.Group()
        self.all_draw = pygame.sprite.Group()
        self.collectables = pygame.sprite.Group()
        self.all_tele = pygame.sprite.Group()
        self.interact = pygame.sprite.Group()
        self.moving_platforms = pygame.sprite.Group()

        self.gillz_map = Ground(self,self.level_1,-35*10,HEIGHT)
        self.kjallari_map = Ground(self,self.kjallari,2500,0)
        self.map_2 = Ground(self,self.level_2,-11000-(13*35),-(8*35))
        self.sky_map = Ground(self,self.cloud_map,-20000,HEIGHT)
        self.solva_mapp = Ground(self,self.solva_map,-30000,HEIGHT)
        

        self.gillz = Gillz(self)
        self.caastle = Castle(self)
        self.player = Player(self)
        self.movement_x = 0

        ###Spawn####
        ###Solva_lvl
        self.player.rect.midbottom = (-29900,1880)
        ###end_of_sky
        #self.player.rect.midbottom = (-16500,600)
        ###Ernis_lvl
        #self.player.rect.midbottom = (-10680,0)
        ###end_of_Ernis_lvl
        #self.player.rect.midbottom = (-4000,0)

        #################
        #Gillz
        
        Enemy(self,self.player,17*35,-35*27-2,[14,21])
        Enemy(self,self.player,38*35,-35*29-2,[36,41])

        #Ernir
        
        for w in range(100):
            pass

        for w in PLATFORMS:
            Platform(self,35*w[0],HEIGHT+w[1]*35,35*w[2],35*w[3])
        
        for w in KJ_PLATFORMS:
            
            Platform(self,2500+35*w[0],w[1]*35,35*w[2],35*w[3])
        
        for w in ERNIR_PLATFORMS:
            Platform(self,-11000+35*w[0],w[1]*35,35*w[2],35*w[3])
        
        for m in MOVING:
            self.platform = Moving_Platform(self, m[0], m[1], m[2], m[3], m[4])
        
        for w in CLOUD_PLATFORMS:
            Platform(self,-20000+35*w[0],HEIGHT+w[1]*35,35*w[2],35*w[3])
        for w in SOLVA_PLATFORMS:
            Platform(self,-30000+35*w[0],HEIGHT+w[1]*35,35*w[2],35*w[3])
            
        
        ######GILLZ
        self.tele = Teleport(self,self.player,[18.8*35,6*35+600,50,35*6],(17*35,HEIGHT),True)
        self.rope = Teleport(self,self.player,[22.8*35,26*35+600,50,35*15],(21*35,15*35+HEIGHT),True)
        self.hurd = Teleport(self,self.player,[18.8*35,15*35+600,50,35*2],(2500+26*35,39*35),True)
        Teleport(self,self.player,[2500+23.8*35,38*35,50,35*2],(20*35,15*35+HEIGHT),True)
        self.respawn = Teleport(self,self.player,[2500,56*35,5000,35*2],(2500+28*35,39*35),False)
        self.boss_tele = Boss_teleport(self,self.player,[35*35,HEIGHT,200,35*4],(10000,0),True)
        ######Ernir
        Teleport(self,self.player,[-11000-13*35,28*35, 50,35*22],((-11000-12*35),(8*35)),True)
        Teleport(self,self.player,[-11000+23*35, 49*35+0.5, 35, 1.5*35],(-11000+261*35, -3*35),True)
        Teleport(self,self.player,[-3000, 5000, 2000, 200],(850,0),False)
        ###SKY
        Teleport(self,self.player,[-20500,2000, 4000,200],(-20000,600),False)
        Teleport(self,self.player,[-16500,2000, 4000,200],(-10680,0),False)
        ###Solva_lvl
        self.stairway_to_heaven = Teleport(self,self.player,[-30000+99*35,HEIGHT+19*35, 50,8*35],(-20000,600),True)
        Teleport(self,self.player,[-31000,4000,8000,8*35],(-29900,1880),False)

        Collectable(self,self.can,35*36+2500,35*21)
        Collectable(self,self.needle,35*8,35*8+HEIGHT)
        Collectable(self,self.can,35*39,35*29+HEIGHT)


        

    def events(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT]:
            shift = True
        else:
            shift = False
        for w in pygame.event.get():
            if w.type == pygame.QUIT:
                self.running = False
            if w.type == pygame.KEYDOWN:
                if w.key == pygame.K_ESCAPE:
                    self.menu.show_menu()
                if w.key == pygame.K_SPACE and self.player.attacking == False:
                    self.player.attack()
                    self.time_of_attack = pygame.time.get_ticks()
                    self.player.current_frame = 0
                    self.player.last_update = pygame.time.get_ticks()
                if w.key == pygame.K_w:
                    self.player.jump()
                if w.key == pygame.K_q:
                    for sprite in self.interact:
                        sprite.interact()

                if w.key == pygame.K_b and shift:
                    if self.player.is_big:
                        self.player.is_big = False
                        self.player.dmg_box = pygame.Surface((50,50)).get_rect()
                        self.player.hitbox = self.player_sheet.get_img(4,56,31,48).get_rect()
                
                    else:
                        self.player.is_big = True
                        self.player.dmg_box = pygame.Surface((100,100)).get_rect()
                        self.player.hitbox = self.player.standing_left_big[0].get_rect()

                
                    
            
    def update(self):
        self.all_sprites.update()
        self.time = -self.time_of_start +pygame.time.get_ticks()

    def draw(self):
        self.background.draw(self.screen)
        self.all_draw.draw(self.screen)
        self.show_text(0,10,"FPS: {}".format(int(self.clock.get_fps())),RED, font,self.screen)
        
        if self.ending:
            self.show_text(WIDTH-750,150,"Þinn tími var : {}s".format(round(self.time_of_ending/1000,2)),WHITE, Big_font,self.screen)    
        else:
            self.show_text(WIDTH-180,30,"Time: {}".format(round(self.time/1000,2)),WHITE, Big_font,self.screen)
        if self.player.press_q_text:
            self.show_text(550,HEIGHT-100,"Ýttu á Q",BLACK, Big_font,self.screen)
        #pygame.draw.rect(self.screen,BLUE,self.boss_tele.rect,1)
        for rect in self.moving_platforms:
            pygame.draw.rect(self.screen, RED, rect)
        #pygame.draw.rect(self.screen,RED,self.stairway_to_heaven.rect,1)
        
        #***Bubbles****
        if self.gillz.bubble_1:
            self.draw_speech_bubble(self.screen,"SIDDUDU, Villtu komast inní kastalann? ", BLACK,WHITE,self.gillz.rect.topleft +vec(200,-20),32)
        elif self.gillz.bubble_2:
            self.draw_speech_bubble(self.screen,"Finndu bara öll hráefnin í skyrið mitt og þá muntu verða nógu sterkur til þess að brjótast inn", BLACK,WHITE,self.gillz.rect.topleft +vec(300,-20),24)
        elif self.gillz.bubble_3:
            self.draw_speech_bubble(self.screen,"Þú þarft {} fleiri hráefni".format(3-self.player.coins), BLACK,WHITE,self.gillz.rect.topleft +vec(180,-20),32)
        elif self.gillz.bubble_4:
            self.draw_speech_bubble(self.screen,"VÓ! Rólegur ÞYKKI", BLACK,WHITE,self.gillz.rect.topleft +vec(160,-20),32)
        pygame.display.flip()
    
    #**********Föll*****

    def draw_speech_bubble(smh,screen, text, text_colour, bg_colour, pos, size):

        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, text_colour)
        text_rect = text_surface.get_rect(midbottom=pos)

        # background
        bg_rect = text_rect.copy()
        bg_rect.inflate_ip(10, 10)

        # Frame
        frame_rect = bg_rect.copy()
        frame_rect.inflate_ip(4, 4)

        pygame.draw.rect(screen, text_colour, frame_rect) 
        pygame.draw.rect(screen, bg_colour, bg_rect)
        screen.blit(text_surface, text_rect)

    def show_text(self,x,y,Text,color,letur,screen):
        texti = letur.render(Text, True, color)
        screen.blit(texti,(x,y))

game = Game()
game.new()
#game.menu.show_menu()

#****** GAME LOOP ************

while game.running:

    game.events()
    game.update()
    game.draw()
    game.clock.tick(FPS)

pygame.quit()