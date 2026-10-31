import random
from collections import Counter

from mindreader.bots import Bot
from mindreader.game import Move


class Accountant(Bot):
    name = "The Accountant"
    emoji = "🧮"
    description = "Counts every move you've made and bets on your favourite."
    win_taunts = ["The numbers never lie.", "Exactly as my spreadsheet predicted.", "Statistically speaking, you are going down."]
    lose_taunts = ["A statistical outlier.", "I'll need to re-audit that.", "Your lucky star saved you. But it won't always."]

    def predict(self, history):
        if not history:
            return random.choice(list(Move)), 1 / 3
        counts = Counter(opponent for opponent, _ in history)
        favourite, times = counts.most_common(1)[0]
        return favourite, times / len(history)
