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
WINDOW_HEIGHT = 580
WINDOW_WIDTH = 720

BOARD_X = 200
BOARD_Y = 150
BLOCK_SIZE = 15
SURFACE = Rect(0,0,WINDOW_WIDTH,WINDOW_HEIGHT) # 画面のサイズ(x座標,y座標,幅,高さ)
COLOR = {
    "Black":(0,0,0),
    "LightBlack":(20,20,20),
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
    "LightBlack",
    "LightGray",
    "LightBlue",
    "Blue",
    "Green",
    "Orange",
    "Red",
    "Yellow",
    "Gray"
]

def is_between(row,col):
    if 0 < col and col <= COL and 0 <= row and row <= ROW+2:
        return True
    return False
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
                pygame.draw.rect(surface,COLOR["Black"],Rect(BOARD_X+(self.col+block[1])*BLOCK_SIZE,BOARD_Y+(self.row+block[0])*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))
                pygame.draw.rect(surface,COLOR[BLOCK_COLOR[self.block_type]],Rect(BOARD_X+(self.col+block[1])*BLOCK_SIZE+1,BOARD_Y+(self.row+block[0])*BLOCK_SIZE+1,BLOCK_SIZE-3,BLOCK_SIZE-3))
    
    def movable(self,direction,board):
        drow,dcol = direction
        for coor in self.shape:
            row = self.row + drow + coor[0]
            col = self.col + dcol + coor[1]
            if not is_between(row,col) or board[row][col]!=0:
                return False
        return True

    def move(self,direction,board):
        drow,dcol = direction
        if self.movable(direction,board):
            self.row += drow
            self.col += dcol
# 盤面の描画
def board_draw(surface,board):
    for row in range(ROW+3):
        for col in range(COL+2):
            pygame.draw.rect(surface,COLOR["Black"],Rect(BOARD_X+col*BLOCK_SIZE,BOARD_Y+row*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(surface,COLOR[BLOCK_COLOR[board[row][col]]],Rect(BOARD_X+col*BLOCK_SIZE+1,BOARD_Y+row*BLOCK_SIZE+1,BLOCK_SIZE-2,BLOCK_SIZE-2))
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
        board_draw(surface,board) 
        block.draw(surface)
        pygame.display.update()
        # ステップ3:ピースの移動
        # イベント状態を取得
        for event in pygame.event.get():
            # ウィンドウのバツボタンを押した時
            if event.type == QUIT:
                game_exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    block.move([0,-1],board)
                if event.key == K_RIGHT:
                    block.move([0,1],board)
                # Escキーを押した時
                if event.key == K_ESCAPE:
                    game_exit()

if __name__=="__main__":
    main()
