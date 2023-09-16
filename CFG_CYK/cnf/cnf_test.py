import unittest
from cnf import cnf, cnf_alternative
import cfg_input
from cyk import check_rule

ERRMSG_ELIM = r'something went wrong: unexpected occurrence of \E.'
ERRMSG_NON_ISO = "something went wrong: unexpected occurrence of terminal symbol."
ERRMSG_LONG_RIGHT = "something went wrong: expected length was < 3."
ERRMSG_CHAIN = "something went wrong: unexpected single non-terminal symbol."


class TestCasesA(unittest.TestCase):

    def setUp(self) -> None:
        self.grammar = cfg_input.CFG()
        self.grammar.rules = {
            'S': {'ASA', 'aB'},
            'A': {'B', 'S'},
            'B': {'b', r'\E'}
        }
        self.grammar.alphabet = ['a', 'b']
        self.grammar.variables = list(set(key for key in self.grammar.rules))
        self.grammar.start = 'S'
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        for key, val in self.grammar.rules.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("Eliminated all occurrences of epsilon:")
        print_grammar(self.grammar.rules)

    def test_elim_chains(self):
        eliminated_a = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_a.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("Eliminated all occurrences of chained rules:")
        print_grammar(eliminated_a)

    def test_elim_nonisoterm(self):
        self.grammar.rules, _ = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        if isinstance(self.grammar.rules, tuple):
            for value in self.grammar.rules[0].values():
                for strings in value:
                    if len(strings) > 1:
                        for term in self.grammar.alphabet:
                            self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        self.grammar.rules = cnf.transform_to_cnf(self.grammar)
        print_grammar(self.grammar.rules)
        for value in self.grammar.rules.values():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_A: ")
        print_grammar(self.grammar.rules)


class TestCasesB(unittest.TestCase):

    def setUp(self):
        self.grammar = cfg_input.CFG()
        self.grammar.rules = {
            'S': {'TU'},
            'T': {'aTb', r'\E'},
            'U': {'R'},
            'R': {'Ucc', r'\E'}
        }
        self.grammar.alphabet = ['a', 'b', 'c']
        self.grammar.variables = list(set(key for key in self.grammar.rules))
        self.grammar.start = 'S'
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):

        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        eps_keys = check_rule(self.grammar.rules, r'\E')
        self.assertLessEqual(len(eps_keys), 1)
        if len(eps_keys) == 1:
            self.assertIn(self.grammar.start, eps_keys)
        print("eliminated_ all occurrences of epsilon:")
        print_grammar(self.grammar.rules)

    def test_elim_chains(self):
        eliminated_b = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_b.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated_ all occurrences of chained rules:")
        print_grammar(eliminated_b)

    def test_elim_nonisoterm(self):
        eliminated_b = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        print_grammar(self.grammar.rules)
        if isinstance(eliminated_b, tuple):
            for value in eliminated_b[0].values():
                for strings in value:
                 if len(strings) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        else:
            for value in eliminated_b.values():
                for strings in value:
                 if len(strings) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        shorted_b = cnf.transform_to_cnf(self.grammar)
        for value in shorted_b.values():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_A: ")
        print_grammar(shorted_b)


class TestCasesC(unittest.TestCase):

    def setUp(self):
        self.grammar = cfg_input.CFG()
        self.grammar.rules = {
            'S': {'ASA', 'BSB', r'\E'},
            'A': {'a'},
            'B': {'b'}
        }
        self.grammar.alphabet = ['a', 'b']
        self.grammar.variables = list(set(key for key in self.grammar.rules))
        self.grammar.start = 'S'
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):

        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        eliminated_c = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        for key, val in eliminated_c.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated_ all occurrences of epsilon:")
        print_grammar(eliminated_c)

    def test_elim_chains(self):
        eliminated_c = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_c.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated_ all occurrences of chained rules:")
        print_grammar(eliminated_c)

    def test_elim_nonisoterm(self):
        eliminated_c = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        print_grammar(self.grammar.rules)
        if isinstance(eliminated_c, tuple):
            for value in eliminated_c[0].values():
                for strings in value:
                    if len(strings) > 1:
                        for term in self.grammar.alphabet:
                            self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        else:
            for value in eliminated_c.values():
                for strings in value:
                    if len(strings) > 1:
                        for term in self.grammar.alphabet:
                            self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        shorted_c = cnf.long_right_elim(self.grammar.rules, self.grammar.alphabet)
        for value in shorted_c.values():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_A: ")
        print_grammar(shorted_c)


class TestCasesD(unittest.TestCase):

    def setUp(self):
        self.grammar = cfg_input.CFG()
        self.grammar.rules = {
            'S': {'LR', r'\E'},
            'L': {'ALLA', 'BLLB', r'\E'},
            'R': {'ARA', 'BRB', r'\E'},
            'A': {'a'},
            'B': {'b'}
        }
        self.grammar.alphabet = ['a', 'b']
        self.grammar.variables = list(set(key for key in self.grammar.rules))
        self.grammar.start = 'S'
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):

        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        print_grammar(self.grammar.rules)
        for key, val in self.grammar.rules.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated_ all occurrences of epsilon:")

    def test_elim_chains(self):
        eliminated_d = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_d.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated_ all occurrences of chained rules:")
        print_grammar(eliminated_d)

    def test_elim_nonisoterm(self):
        eliminated_d = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet)

        if isinstance(eliminated_d, tuple):
            for value in eliminated_d[0].values():
                for strings in value:
                    if len(strings) > 1:
                        for term in self.grammar.alphabet:
                            self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        else:
            for value in eliminated_d.values():
                for strings in value:
                    if len(strings) > 1:
                        for term in self.grammar.alphabet:
                            self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        print_grammar(self.grammar.rules)
        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        print_grammar(self.grammar.rules)
        self.grammar.rules, _ = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        if isinstance(self.grammar.rules, tuple):
            print_grammar(self.grammar.rules[0])
            shorted_d = cnf.long_right_elim(self.grammar.rules[0], self.grammar.alphabet)
            for value in shorted_d.values():
                for val in value:
                    self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        else:
            print_grammar(self.grammar.rules)
            shorted_d = cnf.long_right_elim(self.grammar.rules, self.grammar.alphabet)
            for value in shorted_d.values():
                for val in value:
                    self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_A: ")
        print_grammar(shorted_d)


class TestCasesE(unittest.TestCase):

    def setUp(self):
        self.grammar = cfg_input.CFG()
        self.grammar.rules = {
            'S': {'aaA'},
            'A': {'BAB', 'B', r'\E'},
            'B': {'bb'}
        }
        self.grammar.alphabet = ['a', 'b']
        self.grammar.variables = list(set(key for key in self.grammar.rules))
        self.grammar.start = 'S'
        print("grammar:")
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):

        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        eliminated_e = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        for key, val in eliminated_e.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated_ all occurrences of epsilon:")
        print_grammar(eliminated_e)

    def test_elim_chains(self):
        eliminated_e = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_e.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated_ all occurrences of chained rules:")
        print_grammar(eliminated_e)

    def test_elim_nonisoterm(self):
        eliminated_e = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        if isinstance(eliminated_e, tuple):
            for value in eliminated_e[0].values():
                for strings in value:
                    if len(strings) > 1:
                        for term in self.grammar.alphabet:
                            self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        else:
            for value in eliminated_e.values():
                for strings in value:
                    if len(strings) > 1:
                        for term in self.grammar.alphabet:
                            self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        self.grammar.rules, _ = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        if isinstance(self.grammar.rules, tuple):
            print_grammar(self.grammar.rules[0])
            shorted_e = cnf.long_right_elim(self.grammar.rules[0], self.grammar.alphabet)
            print_grammar(shorted_e)
            for value in shorted_e.values():
                for val in value:
                    self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        else:
            print_grammar(self.grammar.rules)
            shorted_e = cnf.long_right_elim(self.grammar.rules, self.grammar.alphabet)
            print_grammar(shorted_e)
            for value in shorted_e.values():
                for val in value:
                    self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_E: ")


class TestCasesAlternative(unittest.TestCase):

    def setUp(self):
        self.grammar = cfg_input.CFG()
        self.grammar.rules = {
            "A": {"aBcD", "a"},
            "B": {"aBcD", "a"},
            "C": {"aBcD", "a"},
            "D": {"aBcD", "a"},
            "E": {"aBcD", "a"},
            "F": {"aBcD", "a"},
            "G": {"aBcD", "a"},
            "H": {"aBcD", "a"},
            "I": {"aBcD", "a"},
            "J": {"aBcD", "a"},
            "K": {"aBcD", "a"},
            "L": {"aBcD", "a"},
            "M": {"aBcD", "a"},
            "N": {"aBcD", "a"},
            "O": {"aBcD", "a"},
            "P": {"aBcD", "a"},
            "Q": {"aBcD", "a"},
            "R": {"aBcD", "a"},
            "S": {"aBcD", "a"},
            "T": {"aBcD", "a"},
            "U": {"aBcD", "a"},
            "V": {"aBcD", "a"},
            "W": {"aBcD", "a"},
            "X": {"aBcD", "a"},
            "Y": {"aBcD", "a"},
            "Z": {"aBcD", "a"}
        }
        self.grammar.alphabet = ['a', 'c']
        self.grammar.variables = list(set(key for key in self.grammar.rules))
        self.grammar.start = 'S'
        print("grammar:")
        print_grammar(self.grammar.rules)

    def test_non_iso_alternative(self):
        eliminated_e = cnf_alternative.non_iso_term_elim_alternative(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        print_grammar(eliminated_e[0])

        for value in eliminated_e[0].values():
            for strings in value:
                if len(strings) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, strings, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_long_right_alternative(self):
        self.grammar.rules = cnf_alternative.non_iso_term_elim_alternative(self.grammar.rules,
                                                                           self.grammar.variables,
                                                                           self.grammar.alphabet)[0]

        print_grammar(self.grammar.rules)
        shorted_e = cnf_alternative.long_right_alternative(self.grammar.rules)
        for value in shorted_e.values():
            for val in value:
                amount_integers = len([key for key in shorted_e if len(key) > 1])
                accepted_length = amount_integers + 2
                self.assertLessEqual(len(val), accepted_length, ERRMSG_LONG_RIGHT)
        print_grammar(shorted_e)
        print("successfully eliminated_ long right sides for TEST_E: ")


# class TestRandom(unittest.TestCase):
#     """class to a random generated CFG"""
#     def setUp(self):
#         self.grammar = eingabe.CFG()
#         self.grammar.rules, self.grammar.alphabet = random_grammar(8, 3)
#         self.grammar.variables = []
#         for key in self.grammar.rules:
#             self.grammar.variables.append(key)
#         self.grammar.start = list(self.grammar.variables)[0]
#         print("grammar:")
#         print_grammar(self.grammar.rules)
# 
#     def test_all(self):
#         """test for full functionality"""
#         print("amount of keys [input]: ", len(self.grammar.variables))
#         self.grammar.rules = cnf.cnf(self.grammar)
#         for key, val in self.grammar.rules.items():
#             if key is not self.grammar.start:
#                 self.assertNotIn(r'\E', val, ERRMSG_ELIM)
#         print("eliminated all occurrences of epsilon:")
#         print_grammar(self.grammar.rules)
#         for values in self.grammar.rules.values():
#             for val in values:
#                 self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
#         print("eliminated all occurrences of chained rules:")
#         print_grammar(self.grammar.rules)
#         for value in self.grammar.rules.values():
#             for strings in value:
#                 if len(strings) > 1:
#                     for term in self.grammar.alphabet:
#                         self.assertNotIn(term, strings, ERRMSG_NON_ISO)
#         print("Successfully eliminated all occurrences of non-isolated terminal symbols.")
#         print_grammar(self.grammar.rules)
#         for value in self.grammar.rules.values():
#             for val in value:
#                 amount_integers = len([key for key in self.grammar.rules if len(key) > 1])
#                 accepted_length = amount_integers + 2
#                 self.assertLessEqual(len(val), accepted_length, ERRMSG_LONG_RIGHT)
#         print("successfully eliminated long right sides.")
#         print("amount of keys [output]: ", len(self.grammar.rules.keys()))
#         print_grammar(self.grammar.rules)
#         word = eingabe.new_word()
#         table = cyk.cyk(self.grammar, word)
#         tableau = tabular.to_latex(table, len(word), self.grammar.start)
#         file = open(file="CYK_Tableau.tex", mode="w")
#         file.write(tableau)
#         print("\nwritten in CYK_Tableau.tex")


# def random_grammar(amount_keys, max_values):
#     """generate random grammar"""
#     grammar = dict()
#     uppercases = list(string.ascii_uppercase)
#     lowercases = list(string.ascii_lowercase)
#     random_keys = set(random.sample(uppercases, amount_keys))
#     for key in random_keys:
#         val = set()
#         for _ in range(random.randint(1, max_values)):
#             val.add(''.join(random.sample(random.sample(uppercases + lowercases,
#                                                         random.randint(5, 7)), 5)))
#         grammar.update({key: val})
#     terminals = set()
#     for values in grammar.values():
#         for strings in values:
#             for chars in strings:
#                 if chars in lowercases:
#                     terminals.add(chars)
#     return grammar, terminals


def print_grammar(rules):
    for key, value in rules.items():
        print( str(key) +' --> ' + str(value))
    print("\n")


if __name__ == '__main__':
    unittest.main()
