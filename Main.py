import pygame
import socket
from game import start

WHITE = (0,0,0)
class Option:
    def __init__(self, text, position, value, hoverable, color=(0,0,0), fontsize=40):
        self.text = text
        self.black = color
        self.red = (255,100,255)
        self.hovered = False
        self.menuFont = pygame.font.Font(None, fontsize)
        self.rend = self.menuFont.render(self.text, True, (0,0,0))
        self.rect = self.rend.get_rect()
        self.rect.center = position
        self.value = value
        self.hoverable = hoverable

        # self.rect.x, self.rect.y = position
    def update(self,screen):

        if self.hoverable and self.rect.collidepoint(pygame.mouse.get_pos()):
            # print("A")
            self.hovered = True
        else:
            # print("B")
            self.hovered = False

        self.rend = self.menuFont.render(self.text, True, self.get_color())
        screen.blit(self.rend, self.rect)
    def get_color(self):
        if self.hovered:
            return self.red
        else:
            return self.black
    def checkpress(self):
        if self.hovered and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((800,521))
        # self.menu_font = pygame.font.Font(None, 40)
        self.background_image = pygame.image.load('images/background.png')
        self.hovered = False
        self.choice = False
        self.page = 0
        self.ip_address = "Gettting IP Adress"
        self.setip = False
        self.ip_input = ""
    def MainMenu(self):
        # self.screen.blit(self.background_image,(0,0))

        try:
            self.ip_address = socket.gethostbyname(socket.gethostname())
        except:
            self.ip_address = "Cannot get your IP. Manually Do it"
            self.setip = True
        done = True
        while done:


            # self.screen.fill(pygame.Color("black"))
            self.screen.blit(self.background_image,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done = False
                elif event.type == pygame.KEYDOWN and self.page == 1:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.ip_input) > 0:
                            self.ip_input = self.ip_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.page = 4
                    else:
                        try:
                        # print(event.unicode)
                            self.ip_input += str(event.unicode)
                        except:
                            pass
                # print(event)
            if self.page == 0:
                options = [Option("New Game", (400, 350), 1, True),
                            Option("Instructions", (400, 400), 2, True),
                            Option("Options", (400, 450), 3, True)]
            #Start Game
            elif self.page == 1:

                if len(self.ip_input) == 0:
                    options = [
                                Option("Your IP Adress is:", (400, 100), 0, False),
                                Option(self.ip_address, (400,150), 0, False, (100, 255, 255)),
                                Option("Input your partner's IP adress", (400, 225), 0, False),
                                Option("0.0.0.0", (400, 275), 0, False, (100, 100, 255)),
                                Option("Start Game", (400, 450), 4, True, (0, 76, 255)),
                                Option("Go back", (250, 450), 0, True)]
                else:
                    options = [
                                Option("Your IP Adress is:", (400, 100), 0, False),
                                Option(self.ip_address, (400,150), 0, False, (100, 255, 255)),
                                # Option("Instructions on how ")
                                Option("Input your partner's IP adress", (400, 225), 0, False),
                                Option(self.ip_input, (400, 275), 0, False,(100, 100, 255)),
                                Option("Start Game", (400, 450), 4, True, (0, 76, 255)),
                                Option("Go back", (250, 450), 0, True)]
                print("TOT",self.ip_input)
                # #TODO: FIX
                # if self.setip == True:
                #     options.append(Option("Click to Set IP", (400, 350), 5, True))
                # else:
                #     options.append()
                # print(self.ip_address)

            #Instructions
            elif self.page == 2:
                options = [Option("Keys: W,A,S,D to Move", (400, 200), 0, False),
                            Option("Space bar to Shoot", (400, 250), 0, False),
                            Option("Mouse to Aim", (400, 300), 0, False),

                            Option("Go back", (250, 450), 0, True)]

            #Options
            elif self.page == 3:
                options = [
                            Option("Made by", (400, 250), 0, False),
                            # Option(self.ip_address, (400,150), 0, False, (100, 255, 255)),
                            Option("Andrew Park and Aman Anand", (400, 300), 0, False),
                            # Option(self.ip_input, (400, 275), 0, False,(100, 100, 255)),
                            # Option("Start Game", (400, 450), 4, True, (0, 76, 255)),
                            Option("Go back", (250, 450), 0, True)]

            #Get Partner's IP Address
            elif self.page == 4:
                # options = [Option("Enter your opponent's IP address", (400, 250), 0, False),
                #             ,
                #             Option("Start Game", (400, 350), 5, True)]
                # keys_pressed = pygame.key.pressed()
                # keys_pressed = pygame.key.get_pressed()
                start(self.ip_input)

            #Start Game
            elif self.page == 5:

                pass
            for option in options:
                option.update(self.screen)
                # if option.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed[0]:
                #     print("A")


                self.choice = option.checkpress()
                if self.choice == True:
                    self.page = option.value

                    break
            print(self.page)
                # for option in options:
                #     option.update(self.screen)

                # print(options)
            # print(ip_address)
            # option.draw()
            pygame.display.flip()

pygame.init()

# if __init__ == "__main__":
menu=Menu()
menu.MainMenu()
# background
# # menu_selection = [menu()
# while done:
