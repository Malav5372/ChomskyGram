import string
from cyk import check_rule
from cnf import cnf_alternative, cnf_test


def transform_to_cnf(grammar):
    grammar.rules = start_elim(grammar.start, grammar.rules, grammar.variables)
    print('Occurrences of starting symbol on right sides eliminated')
    cnf_test.print_grammar(grammar.rules)

    grammar.rules = epsilon_elim(grammar.start, grammar.rules)
    print("Occurrences of epsilon eliminated.")
    cnf_test.print_grammar(grammar.rules)

    grammar.rules = chain_elim(grammar.rules)
    print("Occurrences of chained rules eliminated.")
    cnf_test.print_grammar(grammar.rules)

    grammar_alternative = non_iso_term_elim(grammar.rules, grammar.variables, grammar.alphabet)
    print("Occurrences of non isolated terminal symbols eliminated.")
    cnf_test.print_grammar(grammar_alternative[0])

    if grammar_alternative[1]:
        grammar_alternative = cnf_alternative.long_right_alternative(grammar_alternative[0])
        print("Occurrences of long right sides eliminated.")
        return grammar_alternative

    grammar.rules = long_right_elim(grammar_alternative[0], grammar.alphabet)
    print("Occurrences of long right sides eliminated.")
    cnf_test.print_grammar(grammar.rules)

    return grammar.rules


def start_elim(start: str, rules, variables):
    """
    Since we would like to keep the original starting symbol, 
    insert a new nonterminal between S and further rules.

    S -> new_key

    new_key -> [S_rules]
    
    Also replace all occurrences of S in right hand sides with new_key
    """
    new_key = set(set(string.ascii_uppercase) - set(variables)).pop()
    print(f'Creating new rule {new_key} -> [{start}]')

    rules[new_key] = {f'{start}'}
    for values in rules.values():
        for value in values:
            if start in value:
                value.replace(start, new_key)
    return rules


def epsilon_elim(start: str, rules):
    eps = r'\E'
    eps_keys = check_rule(rules, eps)  # find occurrences of epsilon in rules

    if not eps_keys:
        return rules

    for key, value in rules.items():
        tmp_key = set()
        tmp_rule = set()

        for val in value:
            # get keys to remove from tmp_key
            tmp_key.update(char for char in eps_keys if char in val)
            tmp_rule.update(val.replace(char, "") for char in tmp_key for val in value if
                            char in val)  # create rules by removing characters
        value.update(tmp_rule)

    for key, values in rules.items():  # replace empty sets with epsilon
        tmpval = values.copy()
        for word in values:
            if not word:
                tmpval.add(eps)
                tmpval.remove('')
        rules[key] = tmpval

    for key in eps_keys:
        rules[key].remove(r'\E')

    eps_keys = check_rule(rules, eps)
    if len(eps_keys) > 1 or not (len(eps_keys) == 1 and start in eps_keys):
        return epsilon_elim(start, rules)

    return rules


def chain_elim(rules):
    keys = rules.keys()
    new_dict = {}

    for key in list(keys):
        new_dict.update({key: rules[key]})
        new_keys = check_rule(rules, key)  # get vars that point to singular variables
        for k in new_keys:  # substitute rules of V on rhs with V itself
            rules[k].update(rules[key])
            rules[k].remove(key)

    return new_dict


# search rules for non-isolated terminal symbols (e.g. in the form of 'aa' or 'aA'...)
def non_iso_term_elim(rules, variables, alphabet):
    alph = set(string.ascii_uppercase) - set(variables)
    new_dict = dict()

    if len(alphabet) > len(alph):
        return cnf_alternative.non_iso_term_elim_alternative(rules, variables, alphabet)

    map_term_not_term = [(char, symbol) for char, symbol in zip(alphabet, alph)]
    for keys, values in rules.items():
        new_dict[keys] = set()
        tmp_val = values.copy()  # save temporary copy of values
        for val in tmp_val:  # iterate over set of strings
            tmp_str = val
            # substitute new variable with every occurrence of terminal symbol..
            for term in map_term_not_term:
                # if the terminal symbol is not isolated
                if term[0] in tmp_str and len(tmp_str) > 1:
                    tmp_str = tmp_str.replace(term[0], term[1])
                    new_dict[term[1]] = set(term[0])
            tmp_val.remove(val)
            tmp_val.add(tmp_str)

        new_dict[keys].update(tmp_val)

    for value in new_dict.values():  # make sure it worked, reiterate if needed
        for strings in value:
            if len(strings) > 1:
                for term in alphabet:
                    if term in strings:
                        non_iso_term_elim(new_dict,
                                          (key for key, values in new_dict.items()),
                                          alphabet)
    return new_dict, False


def long_right_elim(rules, alphabet):
    alph = set(string.ascii_uppercase) - set(key for key in rules)
    if len(alphabet) > len(alph):
        return cnf_alternative.long_right_alternative(rules)

    new_dict = dict()
    for key, values in rules.items():
        tmp_val = values.copy()
        new_dict[key] = tmp_val

        for strings in values:
            if len(strings) > 2:
                tmp_str = strings
                new_val = tmp_str[-2:]  # ABC -> A BC (split last two vars)
                new_key = alph.pop()  # new variable X
                tmp_str = tmp_str[:-2] + new_key  # updated rule AX

                new_dict[key].remove(strings)
                new_dict[key].add(tmp_str)
                new_dict[new_key] = set()
                new_dict[new_key].add(new_val)  # new rule: X -> BC

    repeat = False
    for key, values in new_dict.items():  # not pretty i know. if needed, reiterate
        for strings in values:
            if len(strings) > 2:
                repeat = True
    if repeat:
        return long_right_elim(new_dict, alphabet)
    return new_dict
