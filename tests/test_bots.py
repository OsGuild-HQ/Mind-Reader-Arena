"""These tests run against EVERY bot automatically, including the one you just added."""

import random
import unittest

from mindreader.bots import Bot, all_bots
from mindreader.game import Move


def random_history(length):
    return [(random.choice(list(Move)), random.choice(list(Move))) for _ in range(length)]


class EveryBotTest(unittest.TestCase):
    def test_bots_are_discovered(self):
        self.assertIn("markov", all_bots())

    def test_every_bot_follows_the_rules(self):
        for bot_id, cls in all_bots().items():
            with self.subTest(bot=bot_id):
                bot = cls()
                self.assertTrue(issubclass(cls, Bot))
                self.assertNotEqual(cls.name, Bot.name, "give your bot a name")
                for length in (0, 1, 5, 50):
                    guess, confidence = bot.predict(random_history(length))
                    self.assertIsInstance(guess, Move)
                    self.assertGreaterEqual(confidence, 0.0)
                    self.assertLessEqual(confidence, 1.0)
                self.assertIsInstance(bot.taunt(won=True), str)
                self.assertIsInstance(bot.taunt(won=False), str)


class SmartBotsTest(unittest.TestCase):
    def test_accountant_spots_favourite_move(self):
        history = [(Move.ROCK, Move.PAPER)] * 5 + [(Move.PAPER, Move.PAPER)]
        guess, _ = all_bots()["frequency"]().predict(history)
        self.assertEqual(guess, Move.ROCK)

    def test_mind_reader_learns_a_cycle(self):
        cycle = [Move.ROCK, Move.PAPER, Move.SCISSORS] * 4  # ends on scissors, next is rock
        history = [(move, Move.ROCK) for move in cycle]
        guess, confidence = all_bots()["markov"]().predict(history)
        self.assertEqual(guess, Move.ROCK)
        self.assertEqual(confidence, 1.0)

    def test_pattern_breaker_learns_a_cycle(self):
        cycle = [Move.ROCK, Move.ROCK, Move.PAPER] * 2
        history = [(move, Move.ROCK) for move in cycle]
        guess, _ = all_bots()["pattern_breaker"]().predict(history)
        self.assertEqual(guess, Move.ROCK)


if __name__ == "__main__":
    unittest.main()
