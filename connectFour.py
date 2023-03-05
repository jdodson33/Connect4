# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:07:47 2023

@author: dodsonj
"""
import math
import copy

# Connect four game build utilizing minimax algorithm to allow the computer to make moves
# player = #2, computer = #1

class ConnectFour:
    def __init__(self):
        self.overall_board = []

    def startingPlayer(self):
        import random
        return random.randint(1, 2)

    def generateBoard(self):
        for i in range(6):
            row = []
            for j in range(7):
                row.append(0)
            self.overall_board.append(row)

    def print_board(self):
        print("\033[1;37;48m 0 \033[1;37;48m 1 \033[1;37;48m 2 \033[1;37;48m 3 \
\033[1;37;48m 4 \033[1;37;48m 5 \033[1;37;48m 6 \033[0m")
        for i in self.overall_board:
            row_str = ""
            for j in i:
                if j == 1:
                    # print green
                    row_str += "\033[1;37;42m 1 "
                elif j == 2:
                    # print blue
                    row_str += "\033[1;37;44m 2 "
                else:
                    # print white
                    row_str += "\033[1;37;47m   "

            print(row_str + "\033[0m")

    def validColumns(self, board):
        valid_locations = []
        for i in range(7):
            if board[0][i] == 0:
                valid_locations.append(i)
        return valid_locations

    #   check for the next available row in a given column (aka the piece is dropping down)
    #   -> returns "None" if col is unavailable
    def nextAvailableRow(self, column, board):
        col = [board[x][column] for x in range(6)]
        if col[0] != 0:
            return None
        elif col[-1] == 0:
            return 5

        for i in range(len(col)):
            if col[i] != 0:
                return i - 1

#   place a piece in a given column (utilizing nextAvailable to find the row) - returns None if column is unavailable
    def dropPiece(self, column, player, board):
        row = self.nextAvailableRow(column, board)
        if row is None:
            return board
        board[row][column] = int(player)
        return board

    #   check if a winning move was played
    def winningMove(self, player, board):
        # check horizontal
        for c in range(4):
            for r in range(6):
                if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and \
                        board[r][c + 3] == player:
                    return True

        # check vertical
        for c in range(7):
            for r in range(3):
                if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and \
                        board[r + 3][c] == player:
                    return True

        # check horizontal (left to right)
        for c in range(4):
            for r in range(3):
                if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and \
                        board[r + 3][c + 3] == player:
                    return True

        # check horizontal (right to left)
        for c in range(3, 7):
            for r in range(3):
                if board[r][c] == player and board[r + 1][c - 1] == player and board[r + 2][c - 2] == player and \
                        board[r + 3][c - 3] == player:
                    return True

        return False

    def scorePosition(self, player, board):
        score = 0

        #       place an emphasis on the value of playing in the center column
        center = [board[x][3] for x in range(6)]
        score += (center.count(player) * 3)
        #print(score)
        #       score horizontal
        for r in range(6):
            row = board[r]
            for c in range(4):
                window = row[c:c + 4]
                score += self.evaluateWindow(window, player)
        #print(score)
        #       score verticals
        for c in range(7):
            col = [board[x][c] for x in range(6)]
            for r in range(3):
                window = col[r:r + 4]
                score += self.evaluateWindow(window, player)
        #print(score)
        #       score positive verticals
        for r in range(3):
            for c in range(4):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluateWindow(window, player)
        #print(score)
        #       score negative verticals
        for r in range(3):
            for c in range(4):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluateWindow(window, player)
        #print(score)
        return score

    def evaluateWindow(self, window, player):
        score = 0

        opp = 2
        if player == 2:
            opp = 1

        if window.count(player) == 4:
            score += 10000
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 2000
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 100

        if window.count(opp) == 3 and window.count(0) == 1:
            score -= 500
        elif window.count(opp) == 4 and window.count(0) == 0:
            score -= 5000

        return score

    def isTerminalNode(self, board):
        return self.winningMove(1, board) or self.winningMove(2, board) or len(self.validColumns(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        import random

        valid_locations = self.validColumns(board)
        terminal = self.isTerminalNode(board)
        if depth == 0 or terminal:
            if terminal:
                if self.winningMove(1, board):
                    return None, 9999999999
                elif self.winningMove(2, board):
                    return None, -9999999999
                else:
                    return None, 0
            else:
                return None, self.scorePosition(1, board)

        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = copy.deepcopy(board)
                self.dropPiece(col, 1, b_copy)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = copy.deepcopy(board)
                self.dropPiece(col, 2, b_copy)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value, column = new_score, col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def play(self):

        starting_player = self.startingPlayer()
        print(starting_player)
        self.generateBoard()

        print("This is a game of connect 4. The computer is '1' and the player is '2'")
        self.print_board()

        if starting_player == 2:
            col = input("Please enter a column number from 0 to 6: ")
            self.overall_board = self.dropPiece(int(col), 2, self.overall_board)
            is_player = False
        else:
            col = 3
            self.overall_board = self.dropPiece(int(col), 1, self.overall_board)
            is_player = True

        self.print_board()

        go = True
        while go:

            if is_player:
                col = int(input("Please enter a column number from 0 to 6: "))
                if col not in self.validColumns(self.overall_board):
                    print("This is not a valid input, please enter a new number.")
                    continue
                self.dropPiece(col, 2, self.overall_board)
                is_player = False
                # self.print_board()
                if self.winningMove(2, self.overall_board):
                    #go = False
                    winner = 2
                    break
                elif len(self.validColumns(self.overall_board)) == 0:
                    go, winner = False, None
                    break

            else:
                alpha, beta = -math.inf, math.inf
                board_copy = copy.deepcopy(self.overall_board)
                col = self.minimax(board_copy, 4, alpha, beta, True)[0]
                is_player = True
                self.dropPiece(col, 1, self.overall_board)
                self.print_board()

                if self.winningMove(1, self.overall_board):
                    #go = False
                    winner = 1
                    break
                elif len(self.validColumns(self.overall_board)) == 0:
                    go, winner = False, None
                    break

        if winner is None:
            print("Play again to find the real winner!")
        else:
            print("The winner is " + str(winner) + "!! Congrats")
        self.print_board()


connect4 = ConnectFour()
connect4.play()
