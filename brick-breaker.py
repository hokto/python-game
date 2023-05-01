import sys
import pygame
from pygame.locals import *



SURFACE = Rect(0,0,400,640) # 画面のサイズ(x座標,y座標,幅,高さ)
FPS = 60 # fpsの設定
BRICK_Y_NUM = 5 # ブロックの縦方向の個数
BRICK_X_NUM = 10 # ブロックの横方向の個数
BRICK_HEIGHT = 15 # ブロックの縦幅
BRICK_WIDTH = 35 # ブロックの横幅

existing_brick = pygame.sprite.Group() # 存在しているブロックのグループ


# ブロック用のクラス
# Spriteクラスを継承して扱いやすくする
class Brick(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super.__init__(self)
        self.rect = Rect(x,y,w,h)
        
# ゲームの初期化用の関数
# ブロックを生成したり、ラケットを生成したりする
def init():
    for y in range(BRICK_Y_NUM):
        for x in range(BRICK_X_NUM):
            existing_brick.add(Brick(x*BRICK_WIDTH,y*BRICK_HEIGHT,BRICK_WIDTH,BRICK_HEIGHT))
    
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
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
                
                

if __name__=="__main__":
    main()