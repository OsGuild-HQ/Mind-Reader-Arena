# 🔮 Mind Reader Arena

**Rock-Paper-Scissors against AI bots that try to read your mind.**

Every bot looks at your past moves and tries to *predict* what you'll throw next. Can you stay unpredictable, or are you an open book? 📖

This is a beginner-friendly open source project for the **OSGuild workshop**. It is pure Python with no dependencies and no API keys. You can play in 30 seconds and open your first PR in 30 minutes.

## Quick start

```bash
git clone https://github.com/sadeeqrabiu/Mind-Reader-Arena.git
cd Mind-Reader-Arena
python3 -m mindreader            # play vs the Mind Reader (10 rounds)
```

Requires Python 3.9+. Nothing to install.

## Commands

| Command | What it does |
|---|---|
| `python3 -m mindreader play --bot frequency --rounds 5` | Play against a specific bot |
| `python3 -m mindreader bots` | List every bot in the arena |
| `python3 -m mindreader duel random_bot markov --rounds 5` | Watch two bots fight round-by-round 🍿 |
| `python3 -m mindreader tournament` | Every bot fights every other bot and you get a leaderboard 🏆 |

## Example

```
Round 3/10, your move: r
  Round 3: you ✊  vs  ✋ Mind Reader  →  Bot wins!
  🔮 "I was 100% sure you'd throw rock." I see your future... and it's losing.
...
  You 3  ·  Mind Reader 5  ·  Ties 2
  Predictability: 60%  You're an open book! 📖
```

## The bots

| Id | Bot | Strategy |
|---|---|---|
| `random_bot` | 🐒 Chaos Monkey | Pure random |
| `frequency` | 🧮 The Accountant | Bets on your most-used move |
| `markov` | 🔮 Mind Reader | Learns "after X, they usually throw Y" patterns |

**Your bot could be next.** See [CONTRIBUTING.md](CONTRIBUTING.md).

## Project layout

```
mindreader/
├── cli.py        # commands: play, bots, tournament
├── game.py       # rules + scoring (pure logic, no printing)
├── display.py    # colors, emoji, scoreboards
└── bots/         # 👈 one file = one bot, auto-discovered
tests/            # run with: python3 -m unittest
```

## Want to contribute?

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Pick something from [GOOD_FIRST_ISSUES.md](GOOD_FIRST_ISSUES.md).
3. Open a PR. 🎉

## License

MIT, see [LICENSE](LICENSE).
