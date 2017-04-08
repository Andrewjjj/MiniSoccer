import pygame
from game import *
class Option:

    hovered = False

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            # white color
            return (255, 100, 100)
        else:
            # dim grey
            return (0, 0, 0)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

pygame.init()
screen = pygame.display.set_mode((800, 521))
menu_font = pygame.font.Font(None, 40)
options = [Option("NEW GAME", (315, 355)), Option("INSTRUCTIONS", (285, 405)),
           Option("OPTIONS", (325, 455))]
done=True
background = pygame.image.load("images/background.png")
while done:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    for option in options:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
            option.draw()
            if option.text=="NEW GAME":
                # print("mmmmmm",button)
                if pygame.mouse.get_pressed()[0]:
                    print(pygame.mouse.get_pressed())
                    MainWindow = gameMain(800, 580, 'images/field.png')
                    MainWindow.mainLoop()
                    pass
            elif option.text=="INSTRUCTIONS":
                pass
            elif option.text=="MUSIC & VOLUME":
                pass
        else:
            option.hovered = False
        option.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done=False
    pygame.display.flip()
