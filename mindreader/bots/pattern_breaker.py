from pattern_breaker import get_move

def test_bot():
    test_cases = [
        [],
        ["rock"],
        ["rock", "paper", "scissors"],
        ["rock", "rock", "paper", "rock", "rock", "paper"],
        ["scissors", "scissors", "rock", "scissors", "scissors", "rock"]
    ]

    for history in test_cases:
        move = get_move(history)

        print(f"Opponent history: {history}")
        print(f"Bot chooses: {move}")
        print("-" * 40)

        assert move in ["rock", "paper", "scissors"]

    print("All tests passed!")


if __name__ == "__main__":
    test_bot()
