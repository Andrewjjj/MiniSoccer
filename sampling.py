import pygame
from game import start
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
            return (255, 255, 255)
        else:
            # dim grey
            return (105, 105, 105)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

pygame.init()
screen = pygame.display.set_mode((480, 320))
menu_font = pygame.font.Font(None, 40)
options = [Option("NEW GAME", (150, 105)), Option("INSTRUCTIONS", (120, 155)),
           Option("MUSIC & VOLUME", (105, 205))]
done=True
while done:
    screen.fill((0, 0, 0))
    start()
    for option in options:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True

        else:
            option.hovered = False
        option.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done=False
    pygame.display.flip()
