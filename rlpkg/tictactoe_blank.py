import random
from base_game_class import Game


# TIC-TAC TOE CLASS
class TicTacToe(Game):
    def __init__(self, h=3, w=3, k=3):
        self.h = h
        self.w = w
        self.k = k

        board = [[0 for _ in range(3)] for _ in range(3)]

        self.initial = {
            "board": [row[:] for row in board],
            "next": 1
        }

    def next_player(self, state):
        return state["next"]

    def legal_steps(self, state):
        steps = []
        for x in range(self.h):
            for y in range(self.w):
                if state["board"][x][y] == 0:
                    steps.append((x, y))
        return steps

    def goodness(self, state, player):
        board = state["board"]

        if self.check_winner(board, 1):
            return 1 if player == 1 else -1
        if self.check_winner(board, 2):
            return 1 if player == 2 else -1

        return 0

    def is_leaf(self, state):
        board = state["board"]

        if self.check_winner(board, 1) or self.check_winner(board, 2):
            return True

        return len(self.legal_steps(state)) == 0

    def take_step(self, step, state):
        x, y = step

        # illegal move
        if state["board"][x][y] != 0:
            return state

        new_board = [row[:] for row in state["board"]]
        # apply the value of placer
        new_board[x][y] = state["next"]

        return {
            "board": new_board,
            "next": 2 if state["next"] == 1 else 1
        }

    def print(self, state):
        """Let's see the current state."""
        board = state["board"]
        for x in range(self.h):
            for y in range(self.w):
                if board[x][y] == 1:
                    sign = 'X'
                elif board[x][y] == 2:
                    sign = 'O'
                else:
                    sign = '.'
                print(sign, end=' ')
            print()
        print()

    def check_winner(self, board, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for x in range(self.h):
            for y in range(self.w):
                if board[x][y] != player:
                    continue

                for dx, dy in directions:
                    count = 0
                    nx, ny = x, y

                    while 0 <= nx < self.h and 0 <= ny < self.w and board[nx][ny] == player:
                        count += 1
                        nx += dx
                        ny += dy

                    if count >= self.k:
                        return True
        return False


# PLAYERS
def random_player(game, state):
    steps = game.legal_steps(state)
    return random.choice(steps)

def play_game(game, p1, p2):
    state = game.initial

    while True:
        for player_id, player in [(1, p1), (2, p2)]:
            step = player(game, state)
            state = game.take_step(step, state)

            game.print(state)

            if game.is_leaf(state):
                result = game.goodness(state, 1)
                if result == 1:
                    return "Player 1 (X) wins"
                elif result == -1:
                    return "Player 2 (O) wins"
                else:
                    return "Draw"

def human_player(game, state):
    game.print(state)
    move = input("Enter move (x y): ")
    x, y = map(int, move.split())
    return (x, y)


ttt = TicTacToe()
result = play_game(
    ttt,
    human_player,
    human_player
)
print(result)