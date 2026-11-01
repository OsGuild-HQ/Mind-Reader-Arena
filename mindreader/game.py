"""Core game rules. Pure logic only, no printing or input(), so it's easy to test."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Iterator, List, Optional, Tuple


class Move(enum.Enum):
    ROCK = "r"
    PAPER = "p"
    SCISSORS = "s"

    @property
    def emoji(self) -> str:
        return {"r": "✊", "p": "✋", "s": "✌️"}[self.value]

    @property
    def label(self) -> str:
        return self.name.lower()

    @classmethod
    def parse(cls, text: str) -> Optional["Move"]:
        """Turn user input like 'r', 'Rock' or ' paper ' into a Move (None if invalid)."""
        text = text.strip().lower()
        for move in cls:
            if text in (move.value, move.label):
                return move
        return None


# Each move beats the move it maps to.
BEATS = {
    Move.ROCK: Move.SCISSORS,
    Move.PAPER: Move.ROCK,
    Move.SCISSORS: Move.PAPER,
}

# A list of rounds as (opponent_move, my_move) pairs, from the point of view of whoever holds it.
History = List[Tuple[Move, Move]]


def beats(a: Move, b: Move) -> bool:
    return BEATS[a] == b


def counter(move: Move) -> Move:
    """The move that beats `move`."""
    for winner, loser in BEATS.items():
        if loser == move:
            return winner
    raise ValueError(f"nothing beats {move}")


def outcome(a: Move, b: Move) -> int:
    """1 if a wins, -1 if b wins, 0 for a tie."""
    if a == b:
        return 0
    return 1 if beats(a, b) else -1


@dataclass
class RoundResult:
    player: Move
    bot: Move
    guess: Move
    confidence: float
    result: int  # 1 = player won, -1 = bot won, 0 = tie


@dataclass
class DuelRound:
    a_guess: Move
    a_confidence: float
    b_guess: Move
    b_confidence: float
    a_move: Move
    b_move: Move
    result: int  # 1 = a won, -1 = b won, 0 = tie


@dataclass
class Match:
    """Player vs one bot. The bot guesses the player's move and plays its counter."""

    history: History = field(default_factory=list)
    player_score: int = 0
    bot_score: int = 0
    ties: int = 0
    correct_guesses: int = 0

    def play_round(self, player: Move, guess: Move, confidence: float) -> RoundResult:
        bot = counter(guess)
        result = outcome(player, bot)
        if result > 0:
            self.player_score += 1
        elif result < 0:
            self.bot_score += 1
        else:
            self.ties += 1
        if guess == player:
            self.correct_guesses += 1
        self.history.append((player, bot))
        return RoundResult(player, bot, guess, confidence, result)

    @property
    def predictability(self) -> float:
        """How often the bot read your mind (0.0 - 1.0). Random play hovers around 0.33."""
        return self.correct_guesses / len(self.history) if self.history else 0.0


def iter_duel(bot_a, bot_b, rounds: int) -> Iterator[DuelRound]:
    """Bot vs bot, yielding each round's details as it happens."""
    a_history: History = []
    b_history: History = []
    for _ in range(rounds):
        a_guess, a_confidence = bot_a.predict(a_history)
        b_guess, b_confidence = bot_b.predict(b_history)
        a_move = counter(a_guess)
        b_move = counter(b_guess)
        result = outcome(a_move, b_move)
        a_history.append((b_move, a_move))
        b_history.append((a_move, b_move))
        yield DuelRound(a_guess, a_confidence, b_guess, b_confidence, a_move, b_move, result)


def run_duel(bot_a, bot_b, rounds: int) -> Tuple[int, int, int]:
    """Bot vs bot. Returns (a_wins, b_wins, ties)."""
    a_wins = b_wins = ties = 0
    for rnd in iter_duel(bot_a, bot_b, rounds):
        if rnd.result > 0:
            a_wins += 1
        elif rnd.result < 0:
            b_wins += 1
        else:
            ties += 1
    return a_wins, b_wins, ties
