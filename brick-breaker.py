import sys
import pygame
import random
import math
import time
from pygame.locals import *



SURFACE = Rect(0,0,400,580) # 画面のサイズ(x座標,y座標,幅,高さ)
FPS = 60 # fpsの設定
BRICK_Y_NUM = 5 # ブロックの縦方向の個数
BRICK_X_NUM = 5 # ブロックの横方向の個数
BRICK_HEIGHT = 30 # ブロックの縦幅
BRICK_WIDTH = 70 # ブロックの横幅

RACKET_DIF_X = 10 # ラケットの移動速度
SPEED_X = 5 # x軸方向の基準の移動速度 
SPEED_Y = 8 # y軸方向の基準の移動速度

BRICKS_COLOR = [(255,255,255),(255,0,0),(0,255,0),(0,0,255)] # ブロックの色の種類

existing_brick = pygame.sprite.Group() # 存在しているブロックのグループ
racket = None

is_clear = False
is_gameover = False

# ゲームのシーンを定数値で設定
INIT = 0
GAME = 1
RESULT = 2

scene = INIT # 最初のシーンはINIT

# ブロック用のクラス
# Spriteクラスを継承して扱いやすくする
class Brick(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h,color):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(x,y,w,h)
        self.image = pygame.Surface((w,h)) 
        self.image.fill(color)
        
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
    def __init__(self,x,y,r):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(x-r,y-r,2*r,2*r) 
        self.image = pygame.Surface((2*r,2*r))
        self.image.fill((255,255,255))
        
        self.update = self.setup
        
    def setup(self):
        # ランダムで最初にボールの進む方向を決める
        self.speed_x = random.randint(-1,1) * SPEED_X
        self.speed_y = -SPEED_Y
        
        self.update = self.move
        
    def move(self):
        global is_gameover,is_clear,scene
        self.rect.centerx += self.speed_x
        self.rect.centery += self.speed_y
        # 左右の壁に衝突したらx軸の進む方向を反転
        if self.rect.left < SURFACE.left:
            self.rect.left = SURFACE.left
            self.speed_x *= -1

        if self.rect.right > SURFACE.right:
            self.rect.right = SURFACE.right
            self.speed_x *= -1
            
        # 天井に届いたらy軸の進む方向を反転
        if self.rect.top < SURFACE.top:
            self.speed_y *= -1
            
        # 一番下まで落ちたらその時点でゲームオーバー
        if self.rect.bottom > SURFACE.bottom:
            is_gameover = True
            scene = RESULT
            return
        
        # 衝突判定
        collide_briks = pygame.sprite.spritecollide(sprite=self,group=existing_brick,dokill=True)
        
        # 衝突したものがあるなら、ボールの進む向きを再計算
        if(len(collide_briks)>0):
            # ベクトル計算
            dir_x = self.rect.centerx - collide_briks[0].rect.centerx
            dir_y = self.rect.centery - collide_briks[0].rect.centery
            
            # ベクトル正規化 
            nor_dir_x = dir_x / math.sqrt(dir_x**2+dir_y**2)
            nor_dir_y = dir_y / math.sqrt(dir_x**2+dir_y**2)
            
            self.speed_x = nor_dir_x * SPEED_X
            self.speed_y = nor_dir_y * SPEED_Y

        # もし、全てのブロックを破壊出来たらゲームクリア!
        if len(existing_brick.sprites()) == 0:
            is_clear = True
            scene = RESULT
            return
        # 衝突判定し、ラケットと衝突していたら進む方向を再計算
        if(self.rect.colliderect(racket.rect)):
            # ベクトル計算
            dir_x = self.rect.centerx - racket.rect.centerx
            dir_y = self.rect.centery - racket.rect.centery
            
            # ベクトル正規化 
            nor_dir_x = dir_x / math.sqrt(dir_x**2+dir_y**2)
            nor_dir_y = dir_y / math.sqrt(dir_x**2+dir_y**2)
            
            self.speed_x = nor_dir_x * SPEED_X
            self.speed_y = nor_dir_y * SPEED_Y
        if self.speed_y > -1 and self.speed_y < 1:
            if self.speed_y < 0:
                self.speed_y = -1
            else:
                self.speed_y = 1
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
# ゲームの初期化用の関数
# ブロックを生成したり、ラケットを生成したりする
def init():
    global existing_brick
    for y in range(BRICK_Y_NUM):
        for x in range(BRICK_X_NUM):
            brick_color_idx = random.randint(0,len(BRICKS_COLOR)-1)
            existing_brick.add(Brick(x*(BRICK_WIDTH+10),y*(BRICK_HEIGHT+10),BRICK_WIDTH,BRICK_HEIGHT,BRICKS_COLOR[brick_color_idx]))
    
# 終了用の関数
# これを呼び出して画面を閉じる
def exit():
    pygame.quit()
    sys.exit()
    
# 初期化処理用の関数
# 画面の初期化等が終わると、スタート画面に遷移
def main():
    global scene,racket,ball
    pygame.init()
    surface = pygame.display.set_mode(SURFACE.size)
    
    clock = pygame.time.Clock()
    
    draw_font = pygame.font.SysFont("hg教科書体",25)
    init_text1 = draw_font.render("ENTERを押すと",True,(255,255,255))
    init_text2 = draw_font.render("ゲームがスタートします!!",True,(255,255,255))
    clear_text = draw_font.render("ゲームクリア!",True,(255,0,0))
    gameover_text = draw_font.render("ゲームオーバー・・・",True,(255,255,255))
    while True:
        clock.tick(FPS)
        surface.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            exit()
        # シーンで処理分け
        if scene == INIT:
            if pressed_keys[K_RETURN]:
                time.sleep(2)
                init() 
                
                racket =  Racket(200,500,100,10)
                ball = Ball(200,500-10,5)
                scene = GAME
        elif scene == GAME:
            if pressed_keys[K_LEFT]:
                racket.x -= RACKET_DIF_X
            if pressed_keys[K_RIGHT]:
                racket.x += RACKET_DIF_X
        elif scene == RESULT:
            if pressed_keys[K_RETURN]:
                scene = INIT
                
        if scene == INIT:
            surface.blit(init_text1,(50,100))
            surface.blit(init_text2,(50,125))
        elif scene == GAME:
            # オブジェクトの状態を更新
            racket.update()
            ball.update()
            
            # オブジェクトを描画
            existing_brick.draw(surface)
            racket.draw(surface)
            ball.draw(surface)
        elif scene == RESULT:
            if is_clear:
                surface.blit(clear_text,(100,100))
            if is_gameover:
                surface.blit(gameover_text,(100,100))
        pygame.display.update()
        

if __name__=="__main__":
    main()