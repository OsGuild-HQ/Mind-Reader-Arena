import unittest

from mindreader.game import Match, Move, beats, counter, iter_duel, outcome, run_duel


class RulesTest(unittest.TestCase):
    def test_beats(self):
        self.assertTrue(beats(Move.ROCK, Move.SCISSORS))
        self.assertTrue(beats(Move.PAPER, Move.ROCK))
        self.assertTrue(beats(Move.SCISSORS, Move.PAPER))
        self.assertFalse(beats(Move.ROCK, Move.PAPER))

    def test_counter_beats_every_move(self):
        for move in Move:
            self.assertTrue(beats(counter(move), move))

    def test_outcome(self):
        self.assertEqual(outcome(Move.ROCK, Move.SCISSORS), 1)
        self.assertEqual(outcome(Move.SCISSORS, Move.ROCK), -1)
        self.assertEqual(outcome(Move.PAPER, Move.PAPER), 0)

    def test_parse(self):
        self.assertEqual(Move.parse("r"), Move.ROCK)
        self.assertEqual(Move.parse("  Paper "), Move.PAPER)
        self.assertIsNone(Move.parse("banana"))


class MatchTest(unittest.TestCase):
    def test_scoring_and_predictability(self):
        match = Match()
        match.play_round(Move.ROCK, guess=Move.ROCK, confidence=0.9)      # bot plays paper, bot wins
        match.play_round(Move.ROCK, guess=Move.SCISSORS, confidence=0.5)  # bot plays rock, tie
        match.play_round(Move.PAPER, guess=Move.SCISSORS, confidence=0.5) # bot plays rock, player wins
        self.assertEqual((match.player_score, match.bot_score, match.ties), (1, 1, 1))
        self.assertAlmostEqual(match.predictability, 1 / 3)
        self.assertEqual(match.history[0], (Move.ROCK, Move.PAPER))

    def test_empty_match_predictability(self):
        self.assertEqual(Match().predictability, 0.0)


class DuelTest(unittest.TestCase):
    def test_duel_totals(self):
        class AlwaysGuessRock:
            def predict(self, history):
                return Move.ROCK, 1.0

        a_wins, b_wins, ties = run_duel(AlwaysGuessRock(), AlwaysGuessRock(), rounds=10)
        self.assertEqual((a_wins, b_wins, ties), (0, 0, 10))

    def test_iter_duel_yields_every_round(self):
        class AlwaysGuessRock:
            def predict(self, history):
                return Move.ROCK, 1.0

        rounds = list(iter_duel(AlwaysGuessRock(), AlwaysGuessRock(), rounds=5))
        self.assertEqual(len(rounds), 5)
        for rnd in rounds:
            self.assertEqual((rnd.a_move, rnd.b_move), (Move.PAPER, Move.PAPER))
            self.assertEqual(rnd.result, 0)

    def test_iter_duel_result_favours_the_winner(self):
        class AlwaysGuessRock:
            def predict(self, history):
                return Move.ROCK, 1.0

        class AlwaysGuessPaper:
            def predict(self, history):
                return Move.PAPER, 1.0

        rnd = next(iter_duel(AlwaysGuessRock(), AlwaysGuessPaper(), rounds=1))
        self.assertEqual((rnd.a_move, rnd.b_move), (Move.PAPER, Move.SCISSORS))
        self.assertEqual(rnd.result, -1)

    def test_run_duel_matches_iter_duel(self):
        class AlwaysGuessRock:
            def predict(self, history):
                return Move.ROCK, 1.0

        class AlwaysGuessPaper:
            def predict(self, history):
                return Move.PAPER, 1.0

        totals = run_duel(AlwaysGuessRock(), AlwaysGuessPaper(), rounds=10)
        rounds = list(iter_duel(AlwaysGuessRock(), AlwaysGuessPaper(), rounds=10))
        self.assertEqual(totals, (0, 10, 0))
        self.assertEqual(len(rounds), 10)


if __name__ == "__main__":
    unittest.main()
