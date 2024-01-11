from settings import *
import pygame
pygame.init()
big_font = pygame.font.Font("freesansbold.ttf", 32)
font = pygame.font.Font("freesansbold.ttf", 16)

class Menu:
    def __init__(self,game):
        self.game = game
        self.is_active = False
        self.current_menu = "Main"

        self.main_opts = ["New Game", "Continue","Quit"]
        self.current_opt = 0


    def menu_events(self):
        for w in pygame.event.get():
            if w.type == pygame.QUIT:
                self.is_active = False
                self.game.running = False
            if self.current_menu == "Main":
                if w.type == pygame.KEYDOWN:
                    if w.key == pygame.K_ESCAPE:
                        self.is_active = False
                    if w.key == pygame.K_s:
                        self.current_opt = (self.current_opt +1)%len(self.main_opts)
                    if w.key == pygame.K_w:
                        self.current_opt = (self.current_opt -1)%len(self.main_opts)
                    if w.key == pygame.K_RETURN:
                        if self.main_opts[self.current_opt] == "New Game":
                            self.game.new()
                            self.is_active = False

                        elif self.main_opts[self.current_opt] == "Continue":
                            self.is_active =False
                        elif self.main_opts[self.current_opt] == "Quit":
                            self.is_active = False
                            self.game.running = False

    def show_menu(self):
        self.is_active = True
       
        while self.is_active:
            
            self.menu_events()

            if self.current_menu == "Main":
                self.main_menu()
            elif self.current_menu == "Quit":
                self.quit_game()
            elif self.current_menu == "Instructions":
                self.instructions()
            elif self.current_menu == "Settings":
                self.settings()


            pygame.display.flip()

    def main_menu(self):

        self.game.screen.fill(BLACK)
        self.game.show_text(515,50,"Main Menu",RED,big_font,self.game.screen)

        counter = 0 
        for opt in self.main_opts:
            self.game.show_text(515,150+70*counter,opt,WHITE,font,self.game.screen)
            counter+=1
        self.game.show_text(480,150+self.current_opt*70,"X",WHITE,font,self.game.screen)
        

        def instructions(self):
            pass
        
        def settins(self):
            pass

        def continue_game(self):
            pass

        def quit_game(self):
            pass
        pass