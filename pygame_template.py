### 使用ライブラリ
import sys
import pygame
import random
import math
import time
from pygame.locals import *

HEIGHT = 580
WIDTH = 720
SURFACE = Rect(0,0,WIDTH,HEIGHT) # 画面のサイズ(x座標,y座標,幅,高さ)
COLOR = {"Black":(0,0,0)}
# ゲーム終了関数
def game_exit():
    pygame.quit()
    sys.exit()
# メイン関数
def main():
    pygame.init()
    surface = pygame.display.set_mode(SURFACE.size)
    while True:
        surface.fill(COLOR["Black"])
        pygame.display.update()
        pressed_keys = pygame.key.get_pressed() # 押されたキー情報を取得
        for event in pygame.event.get():
            # ウィンドウのバツボタンを押した時
            if event.type == QUIT:
                game_exit()
        # Escキーを押した時
        if pressed_keys[K_ESCAPE]:
            game_exit()
                

if __name__=="__main__":
    main()
