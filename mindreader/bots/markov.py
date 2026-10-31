import random
from collections import Counter

from mindreader.bots import Bot
from mindreader.game import Move


class MindReader(Bot):
    name = "Mind Reader"
    emoji = "🔮"
    description = "Learns your patterns: 'after rock, rock they usually throw...'"
    win_taunts = ["I see your future... and it's losing.", "Your patterns betray you.", "Such a simpleton"]
    lose_taunts = ["The crystal ball is cloudy...", "You're harder to read than I thought.", "Your mind is too strong to mess with."]

    def predict(self, history):
        moves = [opponent for opponent, _ in history]
        # Look at the last 2 moves first, then fall back to just the last 1.
        for depth in (2, 1):
            if len(moves) <= depth:
                continue
            recent = moves[-depth:]
            followers = Counter(
                moves[i + depth]
                for i in range(len(moves) - depth)
                if moves[i:i + depth] == recent
            )
            if followers:
                guess, times = followers.most_common(1)[0]
                return guess, times / sum(followers.values())
        return random.choice(list(Move)), 1 / 3
