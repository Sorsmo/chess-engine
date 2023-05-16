"""
Some example strategies for people who want to create a custom, homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""

from __future__ import annotations
import chess
from chess.engine import PlayResult
from engine_wrapper import MinimalEngine
from typing import Any

class YanNepochoEngine(MinimalEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose a random move."""
        return PlayResult(None, None)