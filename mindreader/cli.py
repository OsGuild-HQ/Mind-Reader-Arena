"""Command line entry point: `mindreader play | bots | tournament`."""

from __future__ import annotations

import argparse
import itertools
import sys
import time

from mindreader import display
from mindreader.bots import all_bots
from mindreader.game import Match, Move, iter_duel, run_duel


def cmd_play(args) -> None:
    bots = all_bots()
    if args.bot not in bots:
        sys.exit(f"Unknown bot '{args.bot}'. Try one of: {', '.join(bots)}")
    bot = bots[args.bot]()
    match = Match()

    display.banner()
    display.intro(bot, args.rounds)
    number = 1
    while number <= args.rounds:
        # The bot commits to its guess BEFORE you choose. No cheating!
        guess, confidence = bot.predict(match.history)
        try:
            text = input(f"Round {number}/{args.rounds}, your move: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.strip().lower() in ("q", "quit"):
            break
        player = Move.parse(text)
        if player is None:
            print(display.paint("  Please type r, p or s.", "yellow"))
            continue
        rnd = match.play_round(player, guess, confidence)
        display.show_round(number, bot, rnd, bot.taunt(won=rnd.result < 0) if rnd.result else "")
        number += 1

    if match.history:
        display.final_score(bot, match)


def cmd_bots(args) -> None:
    display.bot_list(all_bots())


def cmd_duel(args) -> None:
    bots = all_bots()
    for bot_id in (args.bot_a, args.bot_b):
        if bot_id not in bots:
            sys.exit(f"Unknown bot '{bot_id}'. Try one of: {', '.join(bots)}")
    bot_a = bots[args.bot_a]()
    bot_b = bots[args.bot_b]()

    display.banner()
    display.duel_intro(bot_a, bot_b, args.rounds)
    a_wins = b_wins = ties = 0
    delay = args.delay if sys.stdout.isatty() else 0.0
    for number, rnd in enumerate(iter_duel(bot_a, bot_b, args.rounds), 1):
        display.show_duel_round(number, bot_a, bot_b, rnd)
        if rnd.result > 0:
            a_wins += 1
        elif rnd.result < 0:
            b_wins += 1
        else:
            ties += 1
        if delay > 0 and number < args.rounds:
            time.sleep(delay)
    display.duel_final(bot_a, bot_b, a_wins, b_wins, ties)


def cmd_tournament(args) -> None:
    bots = all_bots()
    stats = {bot_id: [0, 0, 0] for bot_id in bots}  # wins, losses, ties
    for a, b in itertools.combinations(bots, 2):
        a_wins, b_wins, ties = run_duel(bots[a](), bots[b](), args.rounds)
        stats[a][0] += a_wins
        stats[a][1] += b_wins
        stats[a][2] += ties
        stats[b][0] += b_wins
        stats[b][1] += a_wins
        stats[b][2] += ties
    rows = [(bots[i].emoji, bots[i].name, *stats[i]) for i in bots]
    rows.sort(key=lambda row: (row[2] - row[3], row[2]), reverse=True)
    display.leaderboard(rows)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(prog="mindreader", description="Rock-Paper-Scissors vs mind-reading bots.")
    sub = parser.add_subparsers(dest="command")

    play = sub.add_parser("play", help="play against a bot (default)")
    play.add_argument("--bot", default="markov", help="bot id, see `mindreader bots`")
    play.add_argument("--rounds", type=int, default=10)
    play.set_defaults(func=cmd_play)

    sub.add_parser("bots", help="list available bots").set_defaults(func=cmd_bots)

    tour = sub.add_parser("tournament", help="every bot vs every other bot")
    tour.add_argument("--rounds", type=int, default=100, help="rounds per duel")
    tour.set_defaults(func=cmd_tournament)

    duel = sub.add_parser("duel", help="watch two bots fight round-by-round")
    duel.add_argument("bot_a", help="first bot id, see `mindreader bots`")
    duel.add_argument("bot_b", help="second bot id, see `mindreader bots`")
    duel.add_argument("--rounds", type=int, default=10)
    duel.add_argument("--delay", type=float, default=0.5, help="seconds between rounds (0 = instant)")
    duel.set_defaults(func=cmd_duel)

    args = parser.parse_args(argv)
    if args.command is None:
        args = parser.parse_args(["play"])
    args.func(args)


if __name__ == "__main__":
    main()
