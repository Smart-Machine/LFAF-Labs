# Topic: Introduction to formal languages. Regular grammars. Finite Automata. 

### Course: Formal Languages & Finite Automata
### Author: Radu Calin 

----

## Theory
The set G, with the following parameters, is called a `Grammar`:
* Vn -> set of nonterminal symbols
* Vt -> set of terminal symbols
* S -> starting symbol 
* P -> set of productions

Example:
```
Vn = {S, A, B},
Vt = {a, b, c}, 
P = { 
    S → aA     
    A → bS    
    S → bB   
    A → cA    
    A → aB  
    B → aB   
    B → b
}
```

From the language, denoted `L(G)`, we can generate words, as follows:
```
S -> bB -> baB -> bab
```

The `Finite Automaton` is an abstract model of digital computer. It has the following 5 parameters:
* Q -> set of states
* Σ -> input alphabet
* δ -> set of transitions
* q0 -> initial state
* F -> final state 

## Objectives:

* Understand what a language is and what it needs to have in order to be considered a formal one. 
* Provide the initial setup for the evolving project that you will work on during this semester. I said project because usually at lab works, I encourage/impose students to treat all the labs like stages of development of a whole project. Basically you need to do the following:
    * Create a local && remote repository of a VCS hosting service (let us all use Github to avoid unnecessary headaches);
    * Choose a programming language, and my suggestion would be to choose one that supports all the main paradigms;
    * Create a separate folder where you will be keeping the report. This semester I wish I won't see reports alongside source code files, fingers crossed;
* According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:
    * Implement a type/class for your grammar;
    * Add one function that would generate 5 valid strings from the language expressed by your given grammar;
    * Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;
    * For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;



## Implementation description

The following piece of code, represents the implementation of the Grammar class. It has as the attributes of the class all the needed parameters. The logic of the class is contained in the function `generate_string()`. Also, the class has the functionality of converting itself to a FiniteAutomata.

```python
import random 
from automata.FiniteAutomata import FiniteAutomata


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

    def to_finite_automaton(self) -> FiniteAutomata:
        return FiniteAutomata(self.V_n, self.V_t, self.P)
```

The implementation of the `Transaction` class, shown below, is used in the `FiniteAutomata`. 

```python
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
```

And the implementation for the `FiniteAutomata` is provided below:

```python
from typing import Callable, Union
from .Transaction import Transaction


class FiniteAutomata:

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

```

The most important function is the `is_valid_string()` one, as it provides a way to check for whenever a string was generated by obeying the rules of the `Grammar` or not.

## Conclusions / Screenshots / Results

The program is compiling a string by the use of a `Grammar`, and then checking its validation by the use of the `FiniteAutomata`, as follows:

```bash
Compiling... aA
Compiling... acA
Compiling... acaB
Compiling... acaaB
Compiling... acaaaB
Compiling... acaaab
acaaab
`acaaab` is a valid string
Compiling... aA
Compiling... aaB
Compiling... aaaB
Compiling... aaaaB
Compiling... aaaaaB
Compiling... aaaaab
aaaaab
`aaaaab` is a valid string
Compiling... bB
Compiling... baB
Compiling... bab
bab
`bab` is a valid string
Compiling... bB
Compiling... bb
bb
`bb` is a valid string
Compiling... bB
Compiling... bb
bb
`bb` is a valid string
``` 

## References

* [FLFA-Labs](https://github.com/DrVasile/FLFA-Labs)
* [FLFA-Labs-Examples](https://github.com/DrVasile/FLFA-Labs-Examples)
* [LFPC_Guide](https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf)