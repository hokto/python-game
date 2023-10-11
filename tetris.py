### pygame_template.pyから作成
### 使用ライブラリ
import sys
import pygame
import random
import math
import time
import copy
from pygame.locals import *

ROW = 20
COL = 10
HEIGHT = 580
WIDTH = 720
BLOCK_SIZE = 15
SURFACE = Rect(0,0,WIDTH,HEIGHT) # 画面のサイズ(x座標,y座標,幅,高さ)
COLOR = {
    "Black":(0,0,0),
    "Red":(255,0,0),
    "Green":(0,255,0),
    "Blue":(0,0,255,),
    "LightBlue":(0,255,255),
    "Yellow":(255,255,0),
    "Orange":(255,130,0),
    "LightGray":(150,150,150),
    "Gray":(50,50,50)
    }
BLOCK_COLOR =[
    "Black",
    "LightGray",
    "LightBlue",
    "Blue",
    "Green",
    "Orange",
    "Red",
    "Yellow",
    "Gray"
]

# ステップ2:枠とピースの描画
class Block:
    def __init__(self,block_type,row,col):
        self.shapes = [
            [], # empty
            [], # wall
            [[0, -1], [0, 0], [0, 1], [0, 2]], # I block
            [[-1, -1], [0, -1], [0, 0], [0, 1]], # J block
            [[0, -1], [0, 0], [0, 1], [-1, 1]], # L block
            [[0, -1], [0, 0], [-1, 0], [-1, 1]], # S blosk
            [[-1, -1], [-1, 0], [0, 0], [0, 1]], # Z block
            [[0, -1], [0, 0], [-1, 0], [0, 1]], # T block
            [[0, 0], [-1, 0], [0, 1], [-1, 1]] # square
        ]
        self.block_type = block_type
        self.shape = copy.deepcopy(self.shapes[self.block_type]) # こうしないと元の配列も変化する(参照コピー)
        self.row = row
        self.col = col
    def draw(self,surface):
        for block in self.shape:
            pygame.draw.rect(surface,COLOR[BLOCK_COLOR[self.block_type]],Rect((self.col+block[1])*BLOCK_SIZE,(self.row+block[0])*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))
        
# ゲーム終了関数
def game_exit():
    pygame.quit()
    sys.exit()
# メイン関数
def main():
    pygame.init()
    surface = pygame.display.set_mode(SURFACE.size)
    block = Block(4,1,5)
    board = [[0 for j in range(COL+2)] for i in range(ROW+3)]
    for col in range(COL+2):
        board[-1][col] = 1
    for row in range(ROW+3):
        board[row][0] = 1
        board[row][-1] = 1
    while True:
        surface.fill(COLOR["Black"])
        for row in range(ROW+3):
            for col in range(COL+2):
                pygame.draw.rect(surface,COLOR[BLOCK_COLOR[board[row][col]]],Rect(col*BLOCK_SIZE,row*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))
                
        block.draw(surface)
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
