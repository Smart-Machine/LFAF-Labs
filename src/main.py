from automaton.Transaction import Transaction
from automaton.FiniteAutomata import FiniteAutomata
from grammar.Grammar import Grammar

if __name__ == '__main__':

    # Lab 1 grammar
    V_n = ["S", "A", "B"]
    V_t = ["a", "b", "c"]
    P = {
        "S": ["aA", "bB"],
        "A": ["bS", "cA", "aB"],
        "B": ["aB", "b"],
    }

    # Lab 2 grammar
    Q = ["q0", "q1", "q2", "q3"]
    Sigma = ["a", "b", "c"]
    F = ["q3"]
    transactions = [
        Transaction("q0", "a", "q1"),
        Transaction("q1", "b", "q1"),
        Transaction("q1", "a", "q2"),
        Transaction("q0", "a", "q0"),
        Transaction("q2", "c", "q3"),
        Transaction("q3", "c", "q3"),
    ]

    # using the first lab grammar
    # showing the functionality of
    # classifying the grammar
    grammar = Grammar(V_n, V_t, P)
    grammar_type = grammar.classify()
    print(f"Grammar type for the first lab grammar params: {grammar_type}")

    # using the second lab init
    # params, create a new automata
    finite_automaton = FiniteAutomata(
        Q=Q,
        Sigma=Sigma,
        transactions=transactions,
        F=F[0]
    )

    grammar = finite_automaton.to_grammar()
    print(f"Grammar type for the second lab: {grammar.classify()}")

    print(f"The Finite Automaton type before converting it: {finite_automaton.classify()}")
    finite_automaton.convert_to_dfa()
    print(f"The Finite Automaton type after converting it: {finite_automaton.classify()}")

    