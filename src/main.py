from grammar.Grammar import Grammar

if __name__=='__main__':
    V_n = ["S", "A", "B"]
    V_t = ["a", "b", "c"]
    P = {
        "S": ["aA", "bB"],
        "A": ["bS", "cA", "aB"],
        "B": ["aB", "b"],
    }

    grammar = Grammar(V_n, V_t, P)
    finite_automaton = grammar.to_finite_automaton()
    for _ in range(5):
        result = grammar.generate_string()
        print(result)
    
        if finite_automaton.is_valid_string(result):
            print(f"`{result}` is a valid string")
        else:
            print(f"`{result}` is not a valid string")
    


