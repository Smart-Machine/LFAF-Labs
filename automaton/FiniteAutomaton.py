from typing import Callable, Union
from .Transaction import Transaction


class FiniteAutomaton:

    Q: list 
    Sigma: list 
    Delta: Callable[[str, str], str] 
    Q0: str 
    F: Union[list, str] 
    transactions: list

    def __init__(
            self, 
            Q: list, 
            Sigma: list, 
            productions: dict, 
            Q0: str = "S", 
            F: Union[list, str] = "X"
        ) -> None:

        self.Q = Q + [F] 
        self.Sigma = Sigma
        self.Q0 = Q0
        self.F = F
        self.Delta = self.delta
        self.transactions = []
        
        for state in self.Q[:-1]:
            for symbol in self.Sigma:
                final_state = self.delta(state, symbol, productions)
                if final_state is None: 
                    continue
                if final_state == "":
                    final_state = self.F
                self.transactions.append(Transaction(state, symbol, final_state))

    # implemented only for left-sided regular grammar
    def delta(self, state: str, symbol: str, productions: dict) -> str:
        for key, value in productions.items():
            if key == state:
                for transaction in value:
                    if transaction[0] == symbol:
                        if len(transaction) > 1:
                            return transaction[1] 
                        else: 
                            return ""
    
    def get_initial_state(self, symbol: str, final_state: str) -> list:
        initial_states = []
        for transaction in self.transactions:
            if transaction.symbol == symbol and transaction.final_state == final_state:
                initial_states.append(transaction.initial_state)
        return initial_states

    def is_valid_string(self, generated_string: str) -> bool:
        initial_state = self.Q0 
        symbol = generated_string[0]

        while len(generated_string) > 1:
            state = ""
            for transaction in self.transactions:
                if transaction.initial_state == initial_state and transaction.symbol == symbol:
                    state = transaction.final_state
                    break
            if not state:
                return False
            else: 
                initial_state = state
            generated_string = generated_string[1:]
            symbol = generated_string[0] if len(generated_string) > 1 else None 

        for transaction in self.transactions:
            if transaction.initial_state == initial_state and transaction.final_state == self.F:
                return True

        return False
