import sys, math, pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE, K_s, Rect

pygame.init()

SURFACE = pygame.display.set_mode((400,300))
FPSCLOCK = pygame.time.Clock()

class Player:
    def __init__(self, top, left):
        self.img = pygame.image.load("player.png")
        self.rect=self.img.get_rect(topleft=(top, left))

    def draw(self):
        SURFACE.blit(self.img, self.rect)

class Inveder:
    def __init__(self,left, top): 
        self.img = pygame.image.load("inveder.gif")
        self.rect=self.img.get_rect(topleft=(left, top))

    def draw(self):
        SURFACE.blit(self.img, self.rect)

class UFO:
    def __init__(self,top, left, dir, speed):
        self.img = pygame.image.load("ufo.gif")
        self.dir = dir 
        self.speed = speed 
        self.rect=self.img.get_rect(topleft=(top, left))
        
    def draw(self):
        SURFACE.blit(self.img, self.rect)

    def move(self):
        if self.rect.centerx < 0 or self.rect.centerx > 400:
            self.dir = 180-self.dir
        if self.rect.centery < 0 or self.rect.centery > 300:
            self.dir = -self.dir

        self.rect.centerx += math.cos(math.radians(self.dir))*self.speed
        self.rect.centery -= math.sin(math.radians(self.dir))*self.speed

class Beam:
    def __init__(self, color, rect):
        self.col = color
        self.rect = rect

    def draw(self):
        pygame.draw.rect(SURFACE, self.col, self.rect)

    def move(self):
        self.rect.centery -= 3


#Playerオブジェクトの生成
player = Player(200,290)

#Invederオブジェクトの生成
top = 5
invs=[]
for j in range(4):
    left = 10
    for i in range(12):
        invs.append(Inveder(left, top))
        left = left+30
    top = top + 28

#UFOオブジェクトの生成
ufo = UFO(100,100,320,10)

pygame.key.set_repeat(30, 30)

beams=[]

myfont = pygame.font.SysFont(None,30)
message_start = myfont.render("Push S KEY!", True, (255,255,0))
message_clear = myfont.render("GAME CLEAR! You win!", True, (255,255,0))

mode = 'START'
reward = 0

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if  event.key == K_s:
                mode='GAME'
            elif event.key == K_LEFT and player.rect.centerx > 0:
                player.rect.centerx -= 1
            elif event.key == K_RIGHT and player.rect.centerx < 400:
                player.rect.centerx += 1
            elif event.key == K_SPACE:
                beam = Beam((255,255,0),Rect(player.rect.centerx, player.rect.centery,1,2))
                beams.append(beam)

    if mode=='START':
        SURFACE.fill((0,0,0))
        SURFACE.blit(message_start,(100,120))

    elif mode=='GAME':

        SURFACE.fill((0,0,0))

        #インベーダーの描画
        for inv in invs:
            inv.draw()

        #プレーヤーの描画
        player.draw()

        #ビームの描画
        for beam in beams:
            beam.move()
            beam.draw()

        #UFOの描画
        if ufo is not None: # ufoオブジェクトがNoneでなければ
            ufo.draw()
            ufo.move()

        #ビームの衝突判定
        for beam in beams:

            #画面から消えたらそのオブジェクトをリストから削除する
            if beam.rect.centery<0:
               beams.remove(beam)

            #ビームとUFOの衝突判定
            if ufo is not None:
                if beam.rect.colliderect(ufo.rect)==True:
                    reward+=10
                    ufo = None #衝突したらufoにNoneを代入する
        
            #ビームとインベーダーとの衝突判定
            for inv in invs:
                if beam.rect.colliderect(inv.rect)==True:
                    reward+=1
                    beams.remove(beam)
                    invs.remove(inv) #衝突したらそのオブジェクトをリストから削除する

        if len(invs)==0:
            mode='CLEAR'

    elif mode == 'CLEAR':
        SURFACE.fill((0,0,0))
        SURFACE.blit(message_clear,(100,120))

    rewardfont = pygame.font.SysFont(None, 20)
    message_reward = rewardfont.render("Your point : {}".format(reward),True,(0,255,255))
    SURFACE.blit(message_reward,(290,280))



    pygame.display.update()
    FPSCLOCK.tick(30) 

