"""
Some example strategies for people who want to create a custom, homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""

from __future__ import annotations
import chess
from chess.engine import PlayResult
from engine_wrapper import MinimalEngine
from typing import Any
import random

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

def evaluate(board):
    return countMaterial(board)

class YanNepochoEngine(MinimalEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose a random move."""
        print(evaluate(board))
        return PlayResult(random.choice(list(board.legal_moves)), None)
