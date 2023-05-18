"""
Some example strategies for people who want to create a custom, homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""

from __future__ import annotations
import chess
from chess.engine import PlayResult
from engine_wrapper import MinimalEngine
from typing import Any

# material count function
# pawn(1), knights and bishops(3), rook(5), queen(9)
def countMaterial(board):
    total = 0
    for i in range(64):
        if board.piece_at(i) == None or board.piece_at(i).piece_type == chess.KING:
            continue

        mult = 1
        to_add = 0
        if board.piece_at(i).color == chess.BLACK:
            mult = -1

        if board.piece_at(i).symbol() in ['P', 'p']:
            to_add += 1
        elif board.piece_at(i).symbol() in ['N', 'n', 'B', 'b']:
            to_add += 3
        elif board.piece_at(i).symbol() in ['R', 'r']:
            to_add += 5
        elif board.piece_at(i).symbol() in ['Q', 'q']:
            to_add += 9

        to_add *= mult
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
            evaluation = alphabeta(board, depth-1, alpha, beta, False)
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
            evaluation = alphabeta(board, depth-1, alpha, beta, True)
            board.pop()

            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval

def evaluate(board):
    # check for mate
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -9999
        else:
            return 9999
    return countMaterial(board)

class YanNepochoEngine(MinimalEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        depth = 3

        bestValue = -9999 if board.turn == chess.WHITE else 9999            # set best value to -9999 if white, 9999 if black
        bestMove = None
        for move in board.legal_moves:
            board.push(move)
            evaluation = alphabeta(board, depth-1, -9999, 9999, False)
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
