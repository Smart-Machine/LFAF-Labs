import random


class GrammarType:
    type_0 = "Unrestricted grammar"
    type_1 = "Context-sensitive grammar"
    type_2 = "Context-free grammar"
    type_3 = "Regular grammar"


class Grammar():

    V_n: list
    V_t: list
    P: dict
    S: str

    def __init__(self, V_n: list, V_t: list, P: dict, S: str = "S") -> None:
        self.V_n = V_n
        self.V_t = V_t
        self.P = P
        self.S = S

    def find_next_production(self, searched_string: str) -> str:
        for s in searched_string:
            if s.isupper():
                return s

    def get_filtered_production(self, next_production: str) -> list:
        filtered_dict = {}
        for key, value in self.P.items():
            if key == next_production:
                filtered_dict[key] = value
        return filtered_dict[next_production]

    def generate_string(self) -> str:
        generated_string = self.S
        while not generated_string.islower():
            next_production = self.find_next_production(generated_string)
            next_transition = random.choice(
                self.get_filtered_production(next_production))
            generated_string = generated_string.replace(next_production, "")
            generated_string += next_transition
            print(f"Compiling... {generated_string}")
        return generated_string

    def to_finite_automaton(self):
        from automaton.FiniteAutomata import FiniteAutomata
        return FiniteAutomata(self.V_n, self.V_t, self.P)

    def classify(self) -> str:
        type = None

        # checking type_3
        for key, value in self.P.items():
            for p in value:
                if (len(p) == 1 and p in self.V_t or
                    len(p) == 2 and p[0] in self.V_t and p[1] in self.V_n and
                        len(key) == 1 and key.isupper()):
                    type = GrammarType.type_3
                    break

        # checking type_2
        for key, value in self.P.items():
            for p in value:
                if (len(key) == 1 and key.isupper() and
                    any(e.islower() for e in p) and
                    any(e.isupper() for e in p) and
                        len(p) > 2 or p[0].isupper()):
                    type = GrammarType.type_2
                    break

        # checking type_0 and type_1
        has_comp_states = False
        has_empty_trans = False
        for key, value in self.P.items():
            for p in value:
                if len(key) > 1 and any(e.isupper() for e in key):
                    has_comp_states = True
                if p == "ε":
                    has_empty_trans = True

        if has_empty_trans and has_comp_states:
            type = GrammarType.type_0
        elif has_comp_states:
            type = GrammarType.type_1

        return type