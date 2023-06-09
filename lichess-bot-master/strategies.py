"""
Some example strategies for people who want to create a custom, homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""

from __future__ import annotations
import chess
from chess.engine import PlayResult
from engine_wrapper import MinimalEngine
from typing import Any
import numpy as np

# material count function
# pawn(1), knight(3), bishop(3.2), rook(5), queen(9)
def countMaterial(board):
    total = 0
    for i in range(64):
        if board.piece_at(i) == None or board.piece_at(i).symbol() in ['K', 'k']:
            continue
        
        to_add = 0

        if board.piece_at(i).symbol() in ['P', 'p']:
            to_add = 100
        elif board.piece_at(i).symbol() in ['N', 'n']:
            to_add = 300
        elif board.piece_at(i).symbol() in ['B', 'b']:
            to_add = 320
        elif board.piece_at(i).symbol() in ['R', 'r']:
            to_add = 500
        elif board.piece_at(i).symbol() in ['Q', 'q']:
            to_add = 900

        if board.piece_at(i).color == chess.BLACK:
            total -= to_add
        else:
            total += to_add
    return total

# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
def alphabeta(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizingPlayer:
        maxEval = -9999
        for move in board.legal_moves:
            board.push(move)
            evaluation = alphabeta(board, depth - 1, alpha, beta, False)
            board.pop()

            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = 9999
        for move in board.legal_moves:
            board.push(move)
            evaluation = alphabeta(board, depth - 1, alpha, beta, True)
            board.pop()

            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval

# calculates basic piece activity
# prioritizes long diagonal bishops, centered knights and pawns
def getPieceActivity(board):
    # A1   B1 ...
    #
    #
    #
    #           ...
    #
    #
    #                   ... G8   H8
    
    
    pawnEval = [
         0,  0,   0,   0,   0,   0,  0,  0,
         5, 10,  10, -20, -20,  10, 10,  5, 
         5, -5, -10,   0,   0, -10, -5,  5,
         0,  0,   0,  20,  20,   0,  0,  0, 
         5,  5,  10,  25,  25,  10,  5,  5,
        10, 10,  20,  30,  30,  20, 10, 10,
        50, 50,  50,  50,  50,  50, 50, 50,
         0,  0,   0,   0,   0,   0,  0,  0
    ]

    knightEval = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,  0,   5,   5,   0,  -20, -40,
        -30,  5,  10,  15,  15,  10,   5,  -30,
        -30,  0,  15,  20,  20,  15,   0,  -30,
        -30,  5,  15,  20,  20,  15,   5,  -30,
        -30,  0,  10,  15,  15,  10,   0,  -30,
        -40, -20,  0,   0,   0,   0, -20,  -40,
        -50, -40,-30, -30, -30, -30, -40,  -50
    ]
    
    bishEval = [
        -20, -10, -10, -10, -10, -10, -10, -20, 
        -10,   5,   0,   0,   0,   0,   5, -10, 
        -10,  10,  10,  10,  10,  10,  10, -10,
        -10,   0,  10,  10,  10,  10,   0, -10, 
        -10,   5,   5,  10,  10,   5,   5, -10, 
        -10,   0,   5,  10,  10,   5,   0, -10, 
        -10,   0,   0,   0,   0,   0,   0, -10, 
        -20, -10, -10, -10, -10, -10, -10, -20
    ]
    
    rookEval = [
         0,  0,  0,  5,  5,  0,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         5, 10, 10, 10, 10, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    ]
    
    queenEval = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10,   0,   5,  0,  0,   0,   0, -10,
        -10,   5,   5,  5,  5,   5,   0, -10,
          0,   0,   5,  5,  5,   5,   0,  -5, 
         -5,   0,   5,  5,  5,   5,   0,  -5,
        -10,   0,   5,  5,  5,   5,   0, -10, 
        -10,   0,   0,  0,  0,   0,   0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ]

    kingEval = [
        20, 30, 10,  0,  0, 10, 30, 20,
        20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
    ]

    rookRev = rookEval[::-1]
    knightRev = knightEval[::-1]
    bishRev = bishEval[::-1]
    queenRev = queenEval[::-1]
    pawnRev = pawnEval[::-1]
    
    total = 0
    for i in range(64):
        if board.piece_at(i) == None or board.piece_at(i).piece_type == chess.KING:
            continue
        
        to_add = 0
        piece_color = board.piece_at(i).color
        if piece_color == chess.WHITE: 
            opp_color = chess.BLACK

            defended = len(board.attackers(piece_color, i)) <= len(board.attackers(opp_color, i))
            
            if board.piece_at(i).piece_type == chess.PAWN:
                if not defended:
                    to_add -= 100
                else:
                    to_add += pawnEval[i]
            elif board.piece_at(i).piece_type == chess.KNIGHT:
                if not defended:
                    to_add -= 300
                else:
                    to_add += knightEval[i]
            elif board.piece_at(i).piece_type == chess.BISHOP:
                if not defended:
                    to_add -= 320
                else:
                    to_add += bishEval[i]
            elif board.piece_at(i).piece_type == chess.ROOK:
                if not defended:
                    to_add -= 500
                else:
                    to_add += rookEval[i]
            elif board.piece_at(i).piece_type == chess.QUEEN:
                if not defended:
                    to_add -= 900
                else:
                    to_add += queenEval[i]

        elif piece_color == chess.BLACK:
            opp_color = chess.WHITE

            defended = len(board.attackers(piece_color, i)) <= len(board.attackers(opp_color, i))

            if board.piece_at(i).piece_type == chess.PAWN:
                if not defended:
                    to_add -= 100
                else:
                    to_add += pawnRev[i]
            elif board.piece_at(i).piece_type == chess.KNIGHT:
                if not defended:
                    to_add -= 300
                else:
                    to_add += knightRev[i]
            elif board.piece_at(i).piece_type == chess.BISHOP:
                if not defended:
                    to_add -= 320
                else:
                    to_add += bishRev[i]
            elif board.piece_at(i).piece_type == chess.ROOK:
                if not defended:
                    to_add -= 500
                else:
                    to_add += rookRev[i]
            elif board.piece_at(i).piece_type == chess.QUEEN:
                if not defended:
                    to_add -= 900
                else:
                    to_add += queenRev[i]

        if board.piece_at(i).color == chess.BLACK:
            total -= to_add
        else:
            total += to_add
    return total

def evaluate(board):
    # check for mate
    evaluation = 0
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -9999
        else:
            return 9999
       
    evaluation += countMaterial(board)
    evaluation += getPieceActivity(board)
    return evaluation

class YanNepochoEngine(MinimalEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        depth = 3

        bestValue = -9999 if board.turn == chess.WHITE else 9999            # set best value to -9999 if white, 9999 if black
        bestMove = None
        for move in board.legal_moves:
            board.push(move)
            evaluation = alphabeta(board, depth - 1, -9999, 9999, False)
            board.pop()

            if board.turn == chess.WHITE:
                if evaluation > bestValue:
                    bestMove = move
                    bestValue = evaluation
            else:
                if evaluation < bestValue:
                    bestMove = move
                    bestValue = evaluation
        
        print("Best move: ", bestMove, " with evaluation: ", bestValue)

        return PlayResult(bestMove, None)
