from bot.pace_bot import PaceBot


def main() -> None:
    """
    Entry point of the trading bot.

    Initializes the PaceBot instance and starts its execution loop.
    """
    pacebot: PaceBot = PaceBot()
    pacebot.run()


if __name__ == "__main__":
    main()
