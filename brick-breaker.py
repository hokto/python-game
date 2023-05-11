import sys
import pygame
from pygame.locals import *



SURFACE = Rect(0,0,400,640) # 画面のサイズ(x座標,y座標,幅,高さ)
FPS = 60 # fpsの設定
BRICK_Y_NUM = 5 # ブロックの縦方向の個数
BRICK_X_NUM = 10 # ブロックの横方向の個数
BRICK_HEIGHT = 15 # ブロックの縦幅
BRICK_WIDTH = 35 # ブロックの横幅

RACKET_DIF_X = 10

existing_brick = pygame.sprite.Group() # 存在しているブロックのグループ
racket = None

# ブロック用のクラス
# Spriteクラスを継承して扱いやすくする
class Brick(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(x,y,w,h)
        self.image = pygame.Surface((w,h)) 
        self.image.fill((255,255,255))
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)

# ラケット(ボールを打ち返すやつ)用のクラス
# Brickと同様にSpriteを継承し、別の機能を持たせている
class Racket(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        # 中心座標の設定
        self.x = x
        self.y = y
        self.rect = Rect(x-x/2,y-y/2,w,h)
        self.image = pygame.Surface((w,h))
        self.image.fill((255,255,255))
    def update(self):
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.rect.clamp_ip(SURFACE)
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,r,bricks,racket):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(x-r,y-r,2*r,2*r) 
        self.image = pygame.Surface((2*r,2*r))
        self.image.fill((255,255,255))
        
        self.bricks = bricks
        self.racket = racket
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
# ゲームの初期化用の関数
# ブロックを生成したり、ラケットを生成したりする
def init():
    for y in range(BRICK_Y_NUM):
        for x in range(BRICK_X_NUM):
            existing_brick.add(Brick(x*(BRICK_WIDTH+10),y*(BRICK_HEIGHT+10),BRICK_WIDTH,BRICK_HEIGHT))
    
# 終了用の関数
# これを呼び出して画面を閉じる
def exit():
    pygame.quit()
    sys.exit()
    
# 初期化処理用の関数
# 画面の初期化等が終わると、スタート画面に遷移
def main():
    pygame.init()
    surface = pygame.display.set_mode(SURFACE.size)
    init() 
    
    racket =  Racket(200,500,100,10)
    ball = Ball(200,505,5,existing_brick,racket)
    
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        surface.fill((0,0,0))
        # オブジェクトの状態を更新
        #existing_brick.update() 
        racket.update()
        ball.update()
        
        # オブジェクトを描画
        existing_brick.draw(surface)
        racket.draw(surface)
        ball.draw(surface)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_LEFT:
                    racket.x -= RACKET_DIF_X
                if event.key == K_RIGHT:
                    racket.x += RACKET_DIF_X
                
                

if __name__=="__main__":
    main()