import random
from collections import Counter

from mindreader.bots import Bot
from mindreader.game import Move


class PatternBreaker(Bot):
    name = "Pattern Breaker"
    emoji = "🧩"
    description = "Spots repeating cycles in your moves and jumps to the next one."
    win_taunts = ["Your pattern is broken.", "Predictable rhythm, really."]
    lose_taunts = ["A chaotic choice... clever.", "I'll find the new pattern."]

    def predict(self, history):
        moves = [opponent for opponent, _ in history]
        period = self._find_period(moves)
        if period:
            return moves[-period], 0.6
        if not moves:
            return random.choice(list(Move)), 1 / 3
        counts = Counter(moves)
        favourite, times = counts.most_common(1)[0]
        return favourite, times / len(moves)

    @staticmethod
    def _find_period(moves):
        for period in range(1, len(moves) // 2 + 1):
            if moves[-period:] == moves[-2 * period:-period]:
                return period
        return None
