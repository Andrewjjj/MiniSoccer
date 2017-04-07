import pygame
import random
import math
from Mastermind import *

ip_add = "127.0.0.1"
port = 6317
# from pygame.locals import *
# import os, sys
playernumber = 2
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

pygame.init()


class gameMain:

    def __init__(self, width, height, image):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = pygame.image.load(image)
        self.clock = pygame.time.Clock()
        self.player1pos = ()
        self.player2pos = ()

    def mainLoop(self):
        done = True
        # attaching = False
        all_sprites=pygame.sprite.Group()
        all_players=pygame.sprite.Group()
        all_opponents=pygame.sprite.Group()
        # ball_group=pygame.sprite.Group()
        # player2 = Player('player.png', (30,30))

        if playernumber == 1:
            player1 = Player(True, (200,100))
            player2 = Player(False, (200,350))
            player3 = Player(False, (600, 100), True)
            player4 = Player(False, (600, 350), True)
        else:
            player1 = Player(True, (600,100))
            player2 = Player(False, (600,350))
            player3 = Player(False, (200, 100), True)
            player4 = Player(False, (200, 350), True)
        netLeft = goalnet((0,300))

        ball = SoccerBall(self.width, self.height)
        all_sprites.add(player1)
        all_sprites.add(player2)
        all_sprites.add(player3)
        all_sprites.add(player4)
        all_sprites.add(netLeft)
        all_players.add(player1)
        all_players.add(player2)
        all_opponents.add(player3)
        all_opponents.add(player4)
        all_sprites.add(ball)

        # all_players.add(player1)
        # all_players.add(player2)
        # ball_group.add(ball)

        global client, server

        client = MastermindClientTCP(5.0,10.0)
        try:
            client.connect(ip_add,port)
            print("Connected!")
        except MastermindError:
            print("Cannot find a Server; Starting Server!!")
            client.connect(ip_add,port)
            # server =
        # i=0
        pos_recieved=[]
        i=0

        while done:
            self.screen.blit(self.background_image,(0,0))
            # player
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Disconnecting")
                    client.disconnect()
                    done=False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done=False

            #Data
            if pygame.sprite.spritecollide(ball, all_opponents, False):
                player1.posession = False
                player2.posession = False
            for player in all_players:
                player.move(ball)
                player.update(ball)
            ball.update()
            collision=pygame.sprite.spritecollide(ball, all_players, False)
            # print(collision)
            #Always 1 in control
            if (player1.control == True and player2.control == True) or (player1.control == False and player2.control == False):
                if math.hypot(abs(player1.rect.x-ball.rect.x), abs(player1.rect.y-ball.rect.y)) <= math.hypot(abs(player2.rect.x-ball.rect.x), abs(player2.rect.y-ball.rect.y)):
                    player1.control = True
                    player2.control = False
                else:
                    player1.control = False
                    player2.control = True

            #CLIENT SERVER SENDING =========================
            self.player1pos = (player1.rect.x, player1.rect.y)
            self.player2pos = (player2.rect.x, player2.rect.y)
            # (player1.posession or player2.posession)
            client.send(["player", playernumber,self.player1pos,self.player2pos, (player1.posession or player2.posession),ball.rect.x, ball.rect.y])
            # print(self.player1pos)
            print("ATTACHED:",ball.attached, (player1.posession or player2.posession))
            pos_recieved=client.receive()
            # print("DATA RECIEVED:",pos_recieved)
            print(pygame.sprite.collide_rect(ball, player1),pygame.sprite.collide_rect(ball, player2))

            # pos_recieved[1][0] #player1 pos
            # pos_recieved[1][1] #player2 pos
            # pos_recieved[2][0] #player3 pos
            # pos_recieved[2][1] #player4 pos
            #pos_recieved[3] = Ball Pos
            try:
                if playernumber == 1:
                    player3.update_opponent(pos_recieved[2][0])
                    player4.update_opponent(pos_recieved[2][1])
                else:
                    player3.update_opponent(pos_recieved[1][0])
                    player4.update_opponent(pos_recieved[1][1])
                i+=1
            except:
                pass

            try:
                # print(pos_recieved[3][0],pos_recieved[3][1])
                ball.rect.x, ball.rect.y = pos_recieved[3][0],pos_recieved[3][1]
            except:
                pass
            all_sprites.draw(self.screen)
            self.clock.tick(60)
            pygame.display.flip()

class goalnet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('images/net.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

class Player(pygame.sprite.Sprite):
    def __init__(self, control, position, opponent=False):
        super().__init__()
        if opponent == False:
            self.image = pygame.image.load('images/player.png')
        else:
            self.image = pygame.image.load('images/opponent.png')
        # self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.accel_x = 0
        self.accel_y = 0
        self.control = control
        self.rect.x, self.rect.y = position
        self.noball = True
        self.changeready = False
        self.opponent = opponent
        self.posession = False

    def update_opponent(self, coord):
        self.rect.x = coord[0]
        self.rect.y = coord[1]

    def move(self, ball):
        """ Handles Keys """
        if self.opponent == False:
            key = pygame.key.get_pressed()
            # event = pygame.key.get_focused()
            # print("A",event)
            if self.control == True:
                if key[pygame.K_s]:
                    if self.accel_y < 5:
                        self.accel_y+=1
                if key[pygame.K_w]:
                    if self.accel_y > -5:
                        self.accel_y-=1
                if key[pygame.K_d]:
                    if self.accel_x < 5:
                        self.accel_x += 1;
                if key[pygame.K_a]:
                    if self.accel_x > -5:
                        self.accel_x -= 1;
                if sum(key)==0:
                    # print("NOKEY")
                    if self.accel_x > 0:
                        self.accel_x -= 0.5
                    elif self.accel_x < 0:
                        self.accel_x += 0.5
                    if self.accel_y>0:
                        self.accel_y -= 0.5
                    elif self.accel_y<0:
                        self.accel_y += 0.5

                # if ball.canKick == True:
                if self.posession == True:
                    if key[pygame.K_SPACE]:
                        ball.kick()
                        self.posession = False
                        self.control = False
            #Ball Automove
            else:
                # self.accel_x = 0
                # self.accel_y = 0
                # print(ball.rect.x)
                if ball.rect.x >= self.rect.x:
                    if self.accel_x < 5:
                        self.accel_x += 0.5
                elif ball.rect.x <= self.rect.x:
                    if self.accel_x > -5:
                        self.accel_x -= 0.5
                # if ball.rect.y < self.rect.y:
                #     if ball.rect.y+100 > self.rect.y:
                #         if self.accel_y < 5:
                #             self.accel_y += 0.5
                #             print("A")
                #     elif ball.rect.y+100 < self.rect.y:
                #         if self.accel_y > 5:
                #             self.accel_y -= 0.5
                # print(ball.rect.y, self.rect.y)
                self.accel_y = 0

                # self.rect.x =
            self.rect.x += self.accel_x
            self.rect.y += self.accel_y

            if key[pygame.K_q] and self.noball == True:
                if self.changeready == True:
                    if self.control == True:
                        self.control = False
                    else:
                        self.control = True
                    self.changeready = False
            if not key[pygame.K_q] and self.changeready == False:
                self.changeready = True

            if self.rect.x <= 0:
                self.rect.x = 0
            elif self.rect.x >= 800-self.rect.width:
                self.rect.x = 800-self.rect.width
            if self.rect.y <= 0:
                self.rect.y = 0
            elif self.rect.y >= 521-self.rect.height:
                self.rect.y = 521-self.rect.height

        # print("A",ball.attached)
        #if opponent
        # else:
    def update(self, ball):
        if self.control == False:
            self.image = pygame.image.load('images/player.png')
        else:
            self.image = pygame.image.load('images/currplayer.png')
        if pygame.sprite.collide_rect(ball, self):
            # print("COLLIDE")
            self.posession = True
            self.control = True
        if self.posession == True:
            ball.attach(self.rect.x, self.rect.y)

        # else:
        #     self.posession = False

    def getPlayer(self, ball):
        if pygame.sprite.collide_rect(ball, self):
            self.control = True
        else:
            self.control = False

    # def opponentMove(self):



class SoccerBall(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        # import math
        self.image = pygame.image.load('images/soccerball.jpg').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.size=self.image.get_rect().size
        self.rect.x = width/2-(self.size[0]/2)
        self.rect.y = height/2-(self.size[1]/2)
        self.image.get_rect().size
        self.accel_x, self.accel_y = 0,0
        self.attached = False
        self.mouseX, self.mouseY = 0,0
        self.angleX, self.angleY = 0,0
        self.canKick = True

    def attach(self, x, y):
        import math
        self.attached = True
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        #TODO: FIX THE DIVIDE BY ZERO ERROR
        self.angleX = math.acos((self.mouseX-x)/math.hypot(self.mouseX-x,self.mouseY-y))
        self.angleY = math.asin((self.mouseY-y)/math.hypot(self.mouseX-x,self.mouseY-y))

        self.rect.x = x+math.cos(self.angleX)*50
        self.rect.y = y+math.sin(self.angleY)*50

    def update(self):
        import math
        # #Calculate Position
        # if self.attached == True:


        #Calculate Acceleration
        if self.accel_x != 0:
            if self.accel_x > 10:
                self.accel_x -= int(abs((math.cos(self.angleX)*5)))
            elif self.accel_x < -10:
                self.accel_x += int(abs((math.cos(self.angleX)*5)))
            else:
                self.accel_x = 0
        if self.accel_y != 0:
            if self.accel_y > 10:
                self.accel_y -= int(abs((math.sin(self.angleY)*5)))
            elif self.accel_y < -10:
                self.accel_y += int(abs((math.sin(self.angleY)*5)))
            else:
                self.accel_y = 0

        #Apply ball Position according to mouse
        self.rect.x += self.accel_x
        self.rect.y += self.accel_y
        # print(int(math.cos(self.angleX)*30))
        #BALL BOUNDARIES
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= (800 - self.rect.width):
            self.rect.x = (800 - self.rect.width)
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= (521 - self.rect.height):
            self.rect.y = (521 - self.rect.height)
        key = pygame.key.get_pressed()

        # if key[pygame.K_SPACE] and self.attached == True and self.canKick == True: # down key
        #     attached = False
        #     self.kick()
        #     # self.kick()
        #
        #     self.canKick = False
        #     # print("KICKED")
        # if not key[pygame.K_SPACE] and self.canKick == False:
        #     self.canKick = True

    def kick(self):
        import math
        self.accel_x += (math.cos(self.angleX)*30)
        self.accel_y += (math.sin(self.angleY)*30)
        self.attached = False

def start():
    MainWindow = gameMain(800, 521, 'images/field.png')
    MainWindow.mainLoop()
if __name__ == "__main__":
    MainWindow = gameMain(800, 521, 'images/field.png')
    MainWindow.mainLoop()
    # Snake1 = Snake()
