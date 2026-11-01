"""Everything that prints to the terminal lives here."""

from __future__ import annotations

import os
import sys
from typing import List, Tuple

from mindreader.game import DuelRound, Match, RoundResult

_USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ

COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "dim": "\033[2m",
}
RESET = "\033[0m"


def paint(text: str, color: str) -> str:
    return f"{COLORS[color]}{text}{RESET}" if _USE_COLOR else text


def banner() -> None:
    print(paint(r"""
  __  __ _           _   ____                _
 |  \/  (_)_ __   __| | |  _ \ ___  __ _  __| | ___ _ __
 | |\/| | | '_ \ / _` | | |_) / _ \/ _` |/ _` |/ _ \ '__|
 | |  | | | | | | (_| | |  _ <  __/ (_| | (_| |  __/ |
 |_|  |_|_|_| |_|\__,_| |_| \_\___|\__,_|\__,_|\___|_|   ARENA
""", "cyan"))


def intro(bot, rounds: int) -> None:
    print(f"You vs {bot.emoji} {paint(bot.name, 'bold')}: {bot.description}")
    print(paint(f"{rounds} rounds. Type r / p / s (or q to quit).\n", "dim"))


def show_round(number: int, bot, rnd: RoundResult, taunt: str) -> None:
    if rnd.result > 0:
        verdict = paint("You win!", "green")
    elif rnd.result < 0:
        verdict = paint("Bot wins!", "red")
    else:
        verdict = paint("Tie.", "yellow")
    print(
        f"  Round {number}: you {rnd.player.emoji}  vs  {rnd.bot.emoji} {bot.name}  →  {verdict}")
    print(paint(
        f"  {bot.emoji} \"I was {rnd.confidence:.0%} sure you'd throw {rnd.guess.label}.\" {taunt}\n", "dim"))


def final_score(bot, match: Match) -> None:
    print(paint("═" * 50, "cyan"))
    print(
        f"  You {match.player_score}  ·  {bot.name} {match.bot_score}  ·  Ties {match.ties}")
    score = match.predictability
    if score >= 0.5:
        mood = "You're an open book! 📖"
    elif score >= 0.34:
        mood = "A bit readable. Mix it up a bit more! 🤔"
    else:
        mood = "Unreadable. A true enigma. 🥷👎"
    print(f"  Predictability: {paint(f'{score:.0%}', 'bold')}  {mood}")
    print(paint("═" * 50, "cyan"))


def bot_list(bots) -> None:
    for bot_id, cls in bots.items():
        print(f"  {cls.emoji}  {paint(f'{bot_id:<12}', 'bold')} {
              cls.name}: {cls.description}")


def duel_intro(bot_a, bot_b, rounds: int) -> None:
    print(f"{bot_a.emoji} {paint(bot_a.name, 'bold')}  vs  {bot_b.emoji} {paint(bot_b.name, 'bold')}")
    print(paint(f"{bot_a.name}: {bot_a.description}", "dim"))
    print(paint(f"{bot_b.name}: {bot_b.description}", "dim"))
    print(paint(f"{rounds} rounds. Let the mind games begin!\n", "dim"))


def show_duel_round(number: int, bot_a, bot_b, rnd: DuelRound) -> None:
    """Displays result of a duel round"""

    if rnd.result > 0:
        verdict = paint(f"{bot_a.name} wins!", "green")

    elif rnd.result < 0:
        verdict = paint(f"{bot_b.name} wins!", "red")

    else:
        verdict = paint("Tie.", "yellow")

    print(
        f"  Round {number}: {bot_a.emoji} {bot_a.name} {rnd.a_move.emoji}  vs  "
        f"{bot_b.emoji} {bot_b.name} {rnd.b_move.emoji}  →  {verdict}"
    )

    print(paint(
        f"  {bot_a.emoji} guessed {rnd.a_guess.label} ({rnd.a_confidence:.0%})  ·  "
        f"{bot_b.emoji} guessed {rnd.b_guess.label} ({rnd.b_confidence:.0%})\n",
        "dim",
    ))


def duel_final(bot_a, bot_b, a_wins: int, b_wins: int, ties: int) -> None:
    """Displays final duel stats (duel ended) for each bot"""

    print(paint("═" * 50, "cyan"))
    print(
        f"  {bot_a.emoji} {bot_a.name} {a_wins}  ·  "
        f"{bot_b.emoji} {bot_b.name} {b_wins}  ·  Ties {ties}"
    )

    if a_wins > b_wins:
        winner = paint(f"{bot_a.emoji} {bot_a.name} takes the match! 🏆", "bold")

    elif b_wins > a_wins:
        winner = paint(f"{bot_b.emoji} {bot_b.name} takes the match! 🏆", "bold")

    else:
        winner = paint("A perfect stalemate. 🤝", "bold")
        
    print(f"  {winner}")
    print(paint("═" * 50, "cyan"))


def leaderboard(rows: List[Tuple[str, str, int, int, int]]) -> None:
    """rows: (emoji, name, wins, losses, ties), already sorted."""
    print(paint("\n🏆  TOURNAMENT LEADERBOARD\n", "bold"))
    print(f"  {'#':<3} {'Bot':<24} {'W':>5} {'L':>5} {'T':>5}")
    for place, (emoji, name, wins, losses, ties) in enumerate(rows, 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(place, f"{place}.")
        print(f"  {medal:<3} {emoji} {name:<21} {wins:>5} {losses:>5} {ties:>5}")
    print()
