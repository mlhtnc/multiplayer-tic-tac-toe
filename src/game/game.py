from enum import Enum
import sys
 
class GameState(Enum):
    X_WINS = 0
    O_WINS = 1
    DRAW = 2
    NOT_FINISHED = 3
    ILLEGAL_MOVE = 4

class Turn(Enum):
    X = 0
    O = 1

class Game:
    initialCell = "_"

    def __init__(self):
        self.resetGame()

    def resetGame(self):
        self.moveNum = 0
        self.turn = Turn.X
        
        self.board = []
        for r in range(3):
            self.board.append([])
            for c in range(3):
                self.board[r].append(Game.initialCell)

    def __flipTurn(self):
        if self.turn == Turn.X:
            self.turn = Turn.O
        else:
            self.turn = Turn.X

    def move(self, row, col):
        row -= 1
        col -= 1

        if self.board[row][col] != Game.initialCell:
            return GameState.ILLEGAL_MOVE

        if self.turn == Turn.X:
            self.board[row][col] = "X"
        else:
            self.board[row][col] = "O"
        
        self.__flipTurn()
        self.moveNum += 1
        return self.__checkGameState()

    def __checkGameState(self):
        state = GameState.NOT_FINISHED

        state = self.__checkRows()
        if state == GameState.X_WINS or state == GameState.O_WINS:
            return state
        
        state = self.__checkCols()
        if state == GameState.X_WINS or state == GameState.O_WINS:
            return state

        state = self.__checkDiagonals()
        if state == GameState.X_WINS or state == GameState.O_WINS:
            return state

        if state == GameState.NOT_FINISHED and self.moveNum == 9:
            state = GameState.DRAW

        return state

    def __checkRows(self):
        state = None
        for r in range(3):
            v1 = self.board[r][0]
            v2 = self.board[r][1]
            v3 = self.board[r][2]
            
            state = self.__checkIfMatches(v1, v2, v3)
            if state == GameState.X_WINS or state == GameState.O_WINS:
                return state

        return state

    def __checkCols(self):
        state = None
        for c in range(3):
            v1 = self.board[0][c]
            v2 = self.board[1][c]
            v3 = self.board[2][c]
            
            state = self.__checkIfMatches(v1, v2, v3)
            if state == GameState.X_WINS or state == GameState.O_WINS:
                return state

        return state

    def __checkDiagonals(self):
        v1 = self.board[0][0]
        v2 = self.board[1][1]
        v3 = self.board[2][2]

        state = self.__checkIfMatches(v1, v2, v3)
        if state == GameState.X_WINS or state == GameState.O_WINS:
            return state

        v1 = self.board[0][2]
        v2 = self.board[1][1]
        v3 = self.board[2][0]

        state = self.__checkIfMatches(v1, v2, v3)
        if state == GameState.X_WINS or state == GameState.O_WINS:
            return state

        return state

    def __checkIfMatches(self, v1, v2, v3):
        if v1 != Game.initialCell and v1 == v2 and v2 == v3:
            if v1 == 'X':
                return GameState.X_WINS
            else:
                return GameState.O_WINS
        else:
            return GameState.NOT_FINISHED
    
    def printBoard(self):
        print()
        print(">       1 2 3")
        for r in range(3):
            print(f">     {r + 1} ", end = "")
            for c in range(3):
                print(self.board[r][c] + " ", end = "")
            print()
        print()

        sys.stdout.flush()


if __name__ == "__main__":
    g = Game()

    while True:
        print(g.turn)
        print("> Row: ", end = "")
        r = int(input())
        print("> Col: ", end = "")
        c = int(input())
        state = g.move(r, c)

        g.printBoard()
        print(state)

        if state == GameState.DRAW or state == GameState.X_WINS or state == GameState.O_WINS:
            print("Game ended")
            break