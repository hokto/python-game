### 〇×ゲームの実装
### 使用ライブラリ
import sys
import random

MARU = 1
BATU = -1
EMPTY = 0
N = 3 # 〇×ゲームの盤面の大きさ
board = []
winner = None
# 初期化用の関数
def init():
    global board
    board = [[EMPTY for j in range(N)] for i in range(N)]
def next_teban(teban):
    return teban * -1
class AI:
    def __init__(self, player, ai_type,eval_board=None):
        self.teban = player
        if ai_type == 0:
            self.play = self.random
        elif ai_type == 1:
            self.play = self.minmax
            self.eval_board = eval_board
            self.best_x = -1
            self.best_y = -1

    # ランダムに手を打つAI
    def random(self,board):
        x = -1
        y = -1
        while(not(0<=x and x<N and 0<=y and y<=N and board[y][x]==EMPTY)):
            x = random.randint(0,N-1)
            y = random.randint(0,N-1)
        return x,y

    # min-max法
    def minmax(self,board,teban,depth) -> tuple[int,int,int]:
        if depth == 0:
            return self._calc_eval(board,teban),-1,-1
        # 評価値は高ければ高いほど良い手だと判断
        best_score = 100 # MAX_SCORE
        if teban == self.teban:
            best_score = -100 # MIN_SCORE
        best_pos_x = -1
        best_pos_y = -1
        for y in range(N):
            for x in range(N):
                if board[y][x]==EMPTY:
                    board[y][x] = teban
                    score,_,_ = self.minmax(board=board,teban=next_teban(teban),depth=depth-1)
                    if (teban == self.teban and best_score < score) or (teban != self.teban and best_score > score):
                        best_score = score
                        best_pos_x = x
                        best_pos_y = y
                    board[y][x] = EMPTY
        return best_score,best_pos_x,best_pos_y






    # 評価値計算用関数
    # 今はとりあえず評価ボードの和で計算
    def _calc_eval(self,board,teban):
        sum = 0
        for i in range(N):
            for j in range(N):
                if board[i][j] == teban:
                    sum += self.eval_board[i][j]
        return sum

# 盤面描画用の関数
def draw(board):
    for i in range(N):
        for j in range(N):
            if board[i][j] == EMPTY:
                print("　",end="")
            elif board[i][j] == MARU:
                print("〇",end="")
            elif board[i][j] == BATU:
                print("×",end="")
            if j!=N-1:
                print("|",end="")
        print("\n",end="")
        if i!=N-1:
            for k in range(N+1):
                print("ー",end="")
            print("\n",end="")


def is_finish(board):
    global winner
    # 終了条件は3つ.
    # 1. 盤面がすべて埋まっている場合
    # 2. 丸が縦・横・斜めのいずれで3つ連続している場合
    # 3. バツが縦・横・斜めのいずれかで3つ連続している場合

    is_finish_flag = True
    for pos in board:
        if pos != EMPTY:
            is_finish_flag = False
    if is_finish_flag:
        winner = EMPTY
        return True

    # 縦側の判定
    for i in range(N):
        sum = 0
        for j in range(N):
            sum += board[i][j]
        if sum ==3 or sum == -3:
            if sum == 3:
                winner = MARU
            else:
                winner = BATU
            return True

    # 横側の判定
    for j in range(N):
        sum = 0
        for i in range(N):
            sum += board[i][j]
        if sum == 3 or sum == -3:
            if sum == 3:
                winner = MARU
            else:
                winner = BATU
            return True

    # 斜めの判定
    for t in range(2):
        sum = 0
        for k in range(N):
            sum += board[k][k*(-1)**t-t]
        if sum == 3 or sum == -3:
            if sum == 3:
                winner = MARU
            else:
                winner = BATU
            return True
    return False


# メイン関数
def main():
    init()
    now_player = MARU # 先手は〇
    ai_player = None
    eval_board = [[i+j for j in range(N)]for i in range(N)]
    ai = AI(ai_player,ai_type=1,eval_board=eval_board)
    if input("あなたの手番は〇？(Y or N)")=="Y":
        ai_player = MARU
    else:
        ai_player = BATU
    while not is_finish(board):
        draw(board)
        x = -1
        y = -1
        if now_player == MARU:
            print("今の手番は〇")
            x = int(input("x座標の入力:"))
            y = int(input("y座標の入力:"))
        else:
            print("今の手番は×")
            _,x,y = ai.play(board,now_player,depth=5)
        if x==-1 and y==-1:
            print("パスしました")
        elif not(0<=x and x<N and 0<=y and y<N and board[y][x]==EMPTY):
            print("そこにはおけません")
            continue
        else:
            board[y][x] = now_player
        now_player *= -1
    draw(board)
    if winner == MARU:
        print("〇の勝ち")
    elif winner == BATU:
        print("×の勝ち")
    else:
        print("引き分け")

if __name__=="__main__":
    main()