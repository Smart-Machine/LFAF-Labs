class Transaction:

    initial_state: str
    final_state: str
    symbol: str

    def __init__(
        self,
        initial_state: str,
        symbol: str,
        final_state: str
    ) -> None:

        self.initial_state = initial_state
        self.final_state = final_state
        self.symbol = symbol
