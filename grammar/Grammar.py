import random 
from automaton.FiniteAutomaton import FiniteAutomaton


class Grammar:

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
            next_transition = random.choice(self.get_filtered_production(next_production))
            generated_string = generated_string.replace(next_production, "")
            generated_string += next_transition 
            print(f"Compiling... {generated_string}")
        return generated_string

    def to_finite_automaton(self) -> FiniteAutomaton:
        return FiniteAutomaton(self.V_n, self.V_t, self.P)