from typing import Callable, Union
from .Transaction import Transaction


class FiniteAutomata():

    Q: list
    Sigma: list
    Delta: Callable[[str, str], str]
    Q0: str
    F: Union[list, str]
    transactions: list
    type: str
    table: dict

    def __init__(
        self,
        Q: list,
        Sigma: list,
        productions: dict = {},
        transactions: list = [],
        Q0: str = "S",
        F: Union[list, str] = "X"
    ) -> None:

        self.Q = Q + [F]
        self.Sigma = Sigma
        self.Q0 = Q0
        self.F = F
        self.Delta = self.delta
        self.transactions = transactions
        self.type = ""
        self.table = {}

        for state in self.Q[:-1]:
            for symbol in self.Sigma:
                final_state = self.delta(state, symbol, productions)
                if final_state is None:
                    continue
                if final_state == "":
                    final_state = self.F
                self.transactions.append(
                    Transaction(state, symbol, final_state))

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

    def classify(self) -> str:
        if self.is_nfa():
            self.type = "NFA"
        else:
            self.type = "DFA"
        return self.type

    def is_nfa(self) -> bool:
        for i in self.transactions:
            for j in self.transactions:
                if (i.initial_state == j.initial_state and
                    i.symbol == j.symbol and
                        i.final_state != j.final_state):
                    return True
        return False

    def convert_to_dfa(self) -> None:
        nfa = {}
        for transaction in self.transactions:
            if not nfa.get(transaction.initial_state):
                nfa[transaction.initial_state] = {
                    transaction.symbol: [transaction.final_state]
                }
            elif not nfa[transaction.initial_state].get(transaction.symbol):
                nfa[transaction.initial_state][transaction.symbol] = [
                    transaction.final_state
                ]
            else:
                nfa[transaction.initial_state][transaction.symbol].append(
                    transaction.final_state
                )

        for state in nfa.keys():
            for symbol in self.Sigma:
                if not nfa[state].get(symbol):
                    nfa[state][symbol] = []

        dfa = {}
        new_states = []
        states = [list(nfa.keys())[0]]
        symbols = self.Sigma

        # first row
        dfa[states[0]] = {}
        for symbol in symbols:
            value = "".join(nfa[states[0]][symbol])
            dfa[states[0]][symbol] = value
            if value not in states:
                new_states.append(value)
                states.append(value)

        # rest rows
        while len(new_states) != 0:
            state = new_states.pop(0)
            dfa[state] = {}
            fragmented_states = [state[i:i+2] for i in range(0, len(state), 2)]
            for _ in range(len(fragmented_states)):
                for i in range(len(symbols)):
                    temp = []
                    for j in range(len(fragmented_states)):
                        temp += nfa[fragmented_states[j]][symbols[i]]
                    s = "".join(temp)
                    if s not in states:
                        new_states.append(s)
                        states.append(s)
                    dfa[state][symbols[i]] = s
            if dfa[state] == {}:
                dfa.pop(state)

        self.table = dfa

        transaction = []
        for initial_state in dfa.keys():
            for symbol in dfa[initial_state].keys():
                final_state = dfa[initial_state][symbol]
                if final_state:
                    transaction.append(Transaction(
                        initial_state,
                        symbol,
                        final_state
                    ))
        self.transactions = transaction
        self.classify()

    def convert_to_non_terminal_symbols(self, Q: list) -> list:
        V_n = []
        for state in Q:
            V_n.append(chr(ord("A")+int(state[1])))
        return V_n

    def convert_transactions_to_productions(self) -> dict:
        P = {}
        for transaction in self.transactions:
            initial_state = chr(ord("A") + int(transaction.initial_state[1]))
            symbol = transaction.symbol
            final_state = chr(ord("A") + int(transaction.final_state[1]))

            if P.get(initial_state):
                P[initial_state].append(symbol+final_state)
            else:
                P[initial_state] = [symbol+final_state]

        return P

    def to_grammar(self):
        from grammar.Grammar import Grammar
        V_n = list(set(self.convert_to_non_terminal_symbols(self.Q)))
        P = self.convert_transactions_to_productions()
        return Grammar(V_n=V_n, V_t=self.Sigma, S=self.Q0, P=P)