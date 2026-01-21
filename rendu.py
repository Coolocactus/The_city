import pygame 
from simulation import *


class Render:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen = pygame.display.set_mode((700, 1000))
        self.clock = pygame.time.Clock()
        self.running = True
        self.open_screen = {"menu":(True,True)}
        
        font_24 = pygame.font.Font(None, 24)
        
        #chargement des sprites du menu
        self.background_menu = pygame.image.load("background_menu.jpg")
        self.background_menu = pygame.transform.scale(self.background_menu,(700,1000))
        
        print("__init__ completeted with no error")
        self.main()
        
    def main(self):
        print("starting the main loop")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            if self.open_screen["menu"][0] == True:
                if self.open_screen["menu"][1] == True:
                    self.screen = pygame.display.set_mode((700, 1000))
                    self.open_screen["menu"] = (True,False)
                    
                self.screen.blit(self.background_menu, (0, 0))
                
                #rendu du menu
                
            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60
            
        pygame.quit()
        
    def display_button(self,name,pos,size,color):
        #affichr un joli bouton
        
        
rendu = Render()

                