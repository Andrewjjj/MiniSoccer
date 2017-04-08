import pygame
import random
import math
from Mastermind import *
import time

ip_add = "127.0.0.1"
# ip_add = "172.28.127.17"
port = 6317
# from pygame.locals import *
# import os, sys
playernumber = 1
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
        self.player1Score, self.player2Score = 0,0
        self.goal = 0

    def addSpritesToGroup(self, group, sprites):
        for sprite in sprites:
            group.add(sprite)

    def refresh(self, all_players, all_opponents, ball):
        for player in all_players:
            player.refresh()
        for opponents in all_opponents:
            opponents.refresh()
        ball.refresh()

    def mainLoop(self):

        done = True
        # attaching = False
        all_sprites=pygame.sprite.Group()
        all_players=pygame.sprite.Group()
        all_opponents=pygame.sprite.Group()
        net_bound = pygame.sprite.Group()
        net_score = pygame.sprite.Group()
        # ball_group=pygame.sprite.Group()
        # player2 = Player('player.png', (30,30))
        # self.refresh(playernumber)

        global client, server

        client = MastermindClientTCP(5.0,10.0)
        try:
            client.connect(ip_add,port)
            print("Connected!")
        except MastermindError:
            print("Cannot find a Server; Starting Server!!")
            client.connect(ip_add,port)
            pos_recieved=[]
        if playernumber == 1:
            player1 = Player(True)
            player2 = Player(False)
            player3 = Player(False, True)
            player4 = Player(False, True)
        else:
            player1 = Player(True)
            player2 = Player(False)
            player3 = Player(False, True)
            player4 = Player(False, True)

        scoreLeft = goalnet((10,220), 2)
        scoreRight = goalnet((751,220), 2)
        netLTop = goalnet((10,200), 1)
        netLBot = goalnet((10,320), 1)
        netRTop = goalnet((739,200), 1)
        netRBot = goalnet((739,320), 1)
        netLeft = goalnet((10,200))
        netRight = goalnet((739,200))

        ball = SoccerBall()
        self.addSpritesToGroup(all_sprites, [player1, player2, player3, player4,
                                            ball,
                                            netLeft, netRight,
                                            netLTop, netLBot,
                                            netRTop, netRBot,
                                            scoreLeft, scoreRight])
        self.addSpritesToGroup(all_players, [player1, player2])
        self.addSpritesToGroup(all_opponents, [player3, player4])
        self.addSpritesToGroup(net_bound, [netLTop, netLBot, netRTop, netRBot])
        self.addSpritesToGroup(net_score, [scoreLeft, scoreRight])

        while done:
            if playernumber == 1:
                player1.setPosition((200,100))
                player2.setPosition((200,350))
                player3.setPosition((600,100))
                player4.setPosition((600,350))
            else:
                player1.setPosition((600,100))
                player2.setPosition((600,350))
                player3.setPosition((200,100))
                player4.setPosition((200,350))
            ball.setPosition(self.width, self.height)
            ball.accel_x, ball.accel_y = 0,0


            client.send(["start", playernumber])
            pos_recieved=client.receive()
            while pos_recieved[0] != "go":
                client.send(["start", playernumber])
                pos_recieved=client.receive()


            while done:
                # print(self.player1Score)
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

                #Main Loop to update Characters
                for player in all_players:
                    player.move(ball)
                    player.update(ball, net_bound)
                ball.update(net_bound)
                print((player3.rect.x, player3.rect.y))
                # print(pygame.sprite.collide_rect(ball, scoreLeft))
                if pygame.sprite.collide_rect(ball, scoreLeft):
                    self.player2Score += 1
                    self.goal = 1
                    # client.send(["goal", 2])
                    # self.refresh(all_players, all_opponents, ball)

                elif pygame.sprite.collide_rect(ball, scoreRight):
                    self.player1Score += 1
                    # self.refresh(all_players, all_opponents, ball)
                    self.goal = 2
                    # client.send(["goal", 1])
                    print("GOAL", self.player1Score, self.player2Score)


                #Always 1 in control
                if (player1.control == True and player2.control == True) or (player1.control == False and player2.control == False):
                    if math.hypot(abs(player1.rect.x-ball.rect.x), abs(player1.rect.y-ball.rect.y)) <= math.hypot(abs(player2.rect.x-ball.rect.x), abs(player2.rect.y-ball.rect.y)):
                        player1.control = True
                        player2.control = False
                    else:
                        player1.control = False
                        player2.control = True


                #CLIENT SEND DATA TO SERVER =========================
                #Sending Format = ["Player", player#, (Player1 position x, y), (Player2 position x, y), Posession of the ball, ball position X, ball position Y]
                self.player1pos = (player1.rect.x, player1.rect.y)
                self.player2pos = (player2.rect.x, player2.rect.y)
                if self.goal != 0:
                    client.send(["goal", self.goal])
                    self.goal = 0
                else:
                    client.send(["player", playernumber,self.player1pos,self.player2pos, (player1.posession or player2.posession),ball.rect.x, ball.rect.y])
                #RECEIVE DATA
                #Receiving Format =
                pos_recieved=client.receive()
                print(pos_recieved)
                # pos_recieved[1][0] #player1 pos
                # pos_recieved[1][1] #player2 pos
                # pos_recieved[2][0] #player3 pos
                # pos_recieved[2][1] #player4 pos
                #pos_recieved[3] = Ball Pos


                if pos_recieved[0] == "coord":
                    try:
                        if playernumber == 1:
                            player3.update_opponent(pos_recieved[1][2][0])
                            player4.update_opponent(pos_recieved[1][2][1])
                        else:
                            player3.update_opponent(pos_recieved[1][1][0])
                            player4.update_opponent(pos_recieved[1][1][1])
                    except:
                        pass

                    try:
                        # print(pos_recieved[3][0],pos_recieved[3][1])
                        ball.rect.x, ball.rect.y = pos_recieved[1][3][0],pos_recieved[1][3][1]
                    except:
                        pass
                if pos_recieved[0] == "goal":
                    print("BROKE")
                    # time.sleep(5)
                    #TODO: ADD GOAL
                    break


                    # if pos_recieved[1] == 1:
                    #     self.player1Score += 1
                    # elif pos_recieved[1]==2:
                    #     self.player2Score += 1
                    # self.refresh(all_players, all_opponents, ball)
                    #TODO: refresh

                #Draw all Sprites
                all_sprites.draw(self.screen)
                self.clock.tick(160)
                pygame.display.flip()

class goalnet(pygame.sprite.Sprite):
    def __init__(self, position, hitTest=0):
        # hitTest 0=net, 1=sides, 2=box that determines whether its a goal
        super().__init__()
        if hitTest == 0:
            self.image = pygame.image.load('images/net.jpg')
            # self.image.set_colorkey(pygame.Color(0,0,0))
        elif hitTest == 1:
            self.image = pygame.image.load('images/netbar.png')
        else:
            self.image = pygame.image.load('images/netscore.jpg').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

class Player(pygame.sprite.Sprite):
    def __init__(self, control, opponent=False):
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
        self.noball = True
        self.changeready = False
        self.opponent = opponent
        self.posession = False

    def setPosition(self, position):
        self.rect.x, self.rect.y = position
        self.initialPosition = position

    def refresh(self):
        self.rect.x, self.rect.y = self.initialPosition
        self.accel_x = 0
        self.accel_y = 0
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

    def update(self, ball, net_bound):
        if self.control == False:
            self.image = pygame.image.load('images/player.png')
        else:
            self.image = pygame.image.load('images/currplayer.png')
        if pygame.sprite.collide_rect(ball, self):
            # print("COLLIDE")
            self.posession = True
            self.control = True
        if self.posession == True and abs(self.rect.y-ball.rect.y)<70:
            ball.attach(self.rect.x, self.rect.y, net_bound)
        else:
            self.posession = False
            ball.attached = False
        # print(abs(self.rect.y-ball.rect.y))
        # if abs(self.rect.y-ball.rect.y)<150:
        #     print("2222")
        #     ball.attached = False
        # else:
        #     self.posession = False

    def getPlayer(self, ball):
        if pygame.sprite.collide_rect(ball, self):
            self.control = True
        else:
            self.control = False

    # def opponentMove(self):



class SoccerBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # import math
        self.image = pygame.image.load('images/soccerball.jpg').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.size=self.image.get_rect().size
        self.image.get_rect().size
        self.accel_x, self.accel_y = 0,0
        self.attached = False
        self.mouseX, self.mouseY = 0,0
        self.angleX, self.angleY = 0,0
        self.canKick = True


    def setPosition(self, width, height):
        self.rect.x = width/2-(self.size[0]/2)
        self.rect.y = height/2-(self.size[1]/2)
        self.initialPosition = (self.rect.x, self.rect.y)

    def refresh(self):
        self.rect.x, self.rect.y = self.initialPosition
        self.attached = False
        self.accel_x, self.accel_y = 0,0
    def attach(self, x, y, net_bound):
        import math
        self.attached = True
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        #TODO: FIX THE DIVIDE BY ZERO ERROR
        try:
            self.angleX = math.acos((self.mouseX-x)/math.hypot(self.mouseX-x,self.mouseY-y))
            self.angleY = math.asin((self.mouseY-y)/math.hypot(self.mouseX-x,self.mouseY-y))
        except:
            pass
        if pygame.sprite.spritecollide(self, net_bound, False) == []:
            # self.rect.x = x+math.cos(self.angleX)*50
            self.rect.y = y+math.sin(self.angleY)*50
        self.rect.x = x+math.cos(self.angleX)*50


    def update(self, net_bound):
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
        if pygame.sprite.spritecollide(self, net_bound, False) == []:
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

    def kick(self):
        import math
        self.rect.x += (math.cos(self.angleX)*3)
        self.accel_y += (math.sin(self.angleY)*3)
        self.accel_x += (math.cos(self.angleX)*30)
        self.accel_y += (math.sin(self.angleY)*30)
        self.attached = False

def start():
    MainWindow = gameMain(800, 580, 'images/field.png')
    MainWindow.mainLoop()
if __name__ == "__main__":
    MainWindow = gameMain(800, 580, 'images/field.png')
    MainWindow.mainLoop()
    # Snake1 = Snake()
