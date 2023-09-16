from typing import List
# Defines all possible meta-symbols by which
# to separate rules
splitter = ['.', ';', '  ', ',', '|']


class CFG:

    def __init__(self):
        self.variables = []
        self.alphabet = []
        self.rules = dict(set())
        self.start = ""

    def set_variables(self, variables: List[str]):
        self.variables = variables

    def set_alphabet(self, alphabet: List[str]):
        self.alphabet = alphabet

    def set_rules(self, key, value):
        if key not in self.rules:
            self.rules.update({key: set()})
        self.rules[key].add(value)

    def set_start(self, start: str):
        self.start = start

    def new_grammar(self):
        non_terminals = input("Please enter all non-terminal symbols.\n")
        terminals = input("Please enter all terminal symbols.\n")

        for i in splitter:
            non_terminals = non_terminals.replace(i, ' ')
            terminals = terminals.replace(i, ' ')

        self.set_variables(non_terminals.split())
        self.set_alphabet(terminals.split())

        for i in self.variables:
            rule = input(
                "Please enter all rules for " + i +
                ".\nPlease enter \\E for epsilon (if needed).\n")

            for k in splitter:
                rule = rule.replace(k, ' ')
            rule = rule.split()

            check_syntax(self.variables, self.alphabet, rule)
            for k in rule:
                self.set_rules(i, k)

        start = input("Please enter the starting symbol.\n")
        if not start in self.variables:
            print(
                f"The starting symbol {start} has to be part of the non-terminals!\n")
            raise SystemExit
        else:
            self.set_start(start)

    def file_input(self, path=None):

        path = path or (input(
            "Enter path to the file that includes the grammar.\
                (Default: /templates/input_template.txt)") or "/templates/input_template.txt")

        file = open(path, "r").readlines()
        file = list(filter(lambda x: x not in ['\n', ''], file))

        # set non-terminals and terminals by looking at the first two
        # lines of the file and replacing separators
        for i in splitter:
            file[0] = file[0].replace(i, ' ')
            file[1] = file[1].replace(i, ' ')
        self.set_variables(file[0].split())
        self.set_alphabet(file[1].split())

        if (start := file[2][0]) not in self.variables:
            print(f"The starting symbol {start} must be part of the non-terminals!")
            exit(1)
        else:
            self.set_start(start)

        # set rules from line 4 onwards
        for rules in file[3:]:
            # split left and right hand side of rules
            lhs, rhs = rules.split('->')

            map(lambda split: rhs.replace(split, ' '), splitter)

            rules_split = rhs.split()

            check_syntax(self.variables, self.alphabet, rules_split)

            for r in rules_split:
                self.set_rules(lhs, r.strip())


def check_syntax(variables: List[str], alphabet: List[str], rules: List[str]):
    """
    Checks if terminals and non-terminals that were entered at the rule stage
    are actually present in the list of terminals and non-terminals.

    Terminates if this is not the case.
    """
    for rule in rules:
        if rule == r'\E':
            continue
        for item in rule:
            if item.islower() and item not in alphabet:
                print("Inappropriate terminal symbols have been entered.\n")
                raise SystemExit
            if item.isupper() and item not in variables:
                print("Inappropriate symbols have been entered. \n")
                raise SystemExit
