import pandas as pd
import copy
import random
import string


class State:
    """
    Consists of the grid and words left to be placed in the grid. This class also keeps track of the size of the grid.
    """

    def __init__(self, m=13, n=13, words=False):
        """
        Initializes the grid

        :param m: number of rows of grid
        :type m: int
        :param n: number of columns of grid
        :type n: int
        :param words: words to be put in list
        :type words: bool or list

        :rtype: None
        """
        self.num_rows = m
        self.num_cols = n

        # Initialize grid
        initial_rows = [None] * m
        initial_grid = [initial_rows] * n
        self.grid = pd.DataFrame(initial_grid)

        # Checks if words were passed
        if not words:
            self.words = ["Admissible", "Agent", "Backtrack", "Cannibal", "Deadend", "Global", "Graphsearch",
                          "Heuristic", "Hill", "LISP", "Local", "Missionary", "Optimum", "Search", "Symmetry"]
        else:
            self.words = words

        self.words = [x.upper() for x in self.words]


class Puzzle:
    """
    Class containing all grid methods and flailing wildly method
    """

    @staticmethod
    def rule(word, row, col, dh, dv):
        """
        :param word: word for rule
        :type word: int or string
        :param row: starting row
        :type row: int
        :param col: starting column
        :type col: int
        :param dh: horizontal direction
        :type dh: int
        :param dv: vertical direction
        :type dv: int

        :return: Returns a dictionary representing the a rule for the input parameters
        :rtype: dict
        """
        return {'word': word, 'row': row, 'col': col, 'dh': dh, 'dv': dv}

    @staticmethod
    def goal(state):
        """
        :param state: state to check
        :type state: State

        :return: Returns True if input state is the goal, else returns False
        :rtype: bool
        """
        if not state.words:
            return True
        else:
            return False

    @staticmethod
    def apply_rule(rule, state):
        """
        :param rule: Rule to be applied
        :type rule: Puzzle.rule
        :param state: state to apply rule to
        :type state: State

        :return: Returns the value of applying a rule to a given state. This does not change the value of state.
        :rtype: State.grid, State.words
        """

        state = copy.deepcopy(state)
        grid = state.grid

        for character in state.words[rule['word']]:
            grid.iloc[rule['row'], rule['col']] = character
            rule['row'] += rule['dh']
            rule['col'] += rule['dv']

        state.words.remove(state.words[rule['word']])
        return grid, state.words

    @staticmethod
    def precondition(rule, state):
        """
        Checks the passed rule on the passed state, and checks if it is applicable

        :param rule: Rule to check
        :type rule: Puzzle.rule
        :param state: state to check
        :type state: State

        :return: Returns True if the given rule may be applied to state, else returns False.
        :rtype: bool
        """

        rule = copy.deepcopy(rule)
        grid = state.grid
        for character in state.words[rule['word']]:
            if 0 <= rule['row'] < state.num_rows and 0 <= rule['col'] < state.num_cols:
                val = grid.iloc[rule['row'], rule['col']]
            else:
                return 0

            if not val or val == character:
                pass
            else:
                return 0

            rule['row'] += rule['dh']
            rule['col'] += rule['dv']

        return 1

    def generate_rules(self, state):
        """
        Generates all applicable rules of input state

        :param state: state to extract applicable rules from
        :type state: State

        :return:  A list of all possible rules that may be applied to the current state
        :rtype: list

        """
        words_index = [i for i in range(len(state.words))]
        possible_x_starting_points = [i for i in range(state.num_rows)]
        possible_y_starting_points = [i for i in range(state.num_cols)]
        possible_dh = [0, 1, -1]
        possible_dv = [0, 1, -1]

        rules_res = []
        res = [self.rule(i, j, k, o, m) for i in words_index for j in possible_x_starting_points
               for k in possible_y_starting_points for o in possible_dh for m in possible_dv if (abs(o) + abs(m)) > 0]

        for r in res:
            var = self.precondition(copy.deepcopy(r), state)
            if var == 1:
                rules_res.append(r)

        return rules_res

    @staticmethod
    def describe_state(state):
        """
        Describes the input state.
        """
        print("The current grid:")
        print(state.grid.to_string(index=False, header=False))
        print("Words still remaining:")
        print(state.words)

    @staticmethod
    def describe_rule(rule):
        """
        Describes the input rule.
        """
        strng = 'Place the word "{}" in the grid starting at position ({},{}) and proceeding in ' \
                'the direction [{},{}].'.format(rule['word'], rule['row'], rule['col'], rule['dh'], rule['dv'])
        return strng

    def flailing_wildly(self, state):
        """
        Implements the flailing wildly search strategy. Prints progress at every iteration.

        :param state: Initial state
        :type state: State
        """
        error = False
        while not self.goal(state):
            self.describe_state(state)
            applicable_rules = self.generate_rules(state)

            rule_descriptions = []
            for r in copy.deepcopy(applicable_rules):
                r['word'] = state.words[r['word']]
                rule_descriptions.append(self.describe_rule(r))

            if not applicable_rules:
                print("Ran out of options!")
                error = True
                break
            else:
                print("Following rules were applicable:")
                print(rule_descriptions)

                choice = random.choice(applicable_rules)
                choice_copy = copy.deepcopy(choice)
                choice_copy['word'] = state.words[choice_copy['word']]
                print("The folowing rule was chosen:")
                print(self.describe_rule(choice_copy))
                state.grid, state.words = self.apply_rule(choice, state)

                print("\n")

        if not error:
            print("Goal Reached!")
            print("The final grid:")
            print(state.grid.to_string(index=False, header=False))

            state.grid = state.grid.applymap(self.random_fill_none)
            print("\n")
            print("The final grid with Nones filled in with random words:")
            print(state.grid.to_string(index=False, header=False))

    @staticmethod
    def random_fill_none(val):
        """Function to replace None value with a random english letter"""
        if not val:
            return random.choice(string.ascii_letters)
        else:
            return val


if __name__ == '__main__':
    statee = State()  # Initialize state
    p = Puzzle()  # Initialize Puzzle
    p.flailing_wildly(statee)  # Apply flail wildly
