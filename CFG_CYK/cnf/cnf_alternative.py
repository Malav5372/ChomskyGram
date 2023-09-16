import string

# what in the jesus buttermilk fuck is this
def non_iso_term_elim_alternative(rules, variables, alphabet):
    alph = set(string.ascii_uppercase) - set(variables)
    length_difference = len(alphabet) - len(alph)

    alternate_alph = set(string.ascii_uppercase)
    needed_symbols = [alternate_alph.pop() for _ in range(int(length_difference / 10) + 1)]
    new_dict = {}

    for symbol in needed_symbols:
        for diff in range(length_difference):
            alph.add(symbol + str(diff))

    map_term_not_term = [(char, symbol) for char, symbol in zip(alphabet, alph)]
    for keys, set_of_strings in rules.items():
        new_dict[keys] = set()
        set_copy = set_of_strings.copy()
        for strings in set_copy:
            string_copy = strings
            for term_symbol in map_term_not_term:
                if term_symbol[0] in string_copy and len(string_copy) > 1:
                    string_copy = string_copy.replace(term_symbol[0], term_symbol[1])
                    new_dict[term_symbol[1]] = set(term_symbol[0])
            set_copy.remove(strings)
            set_copy.add(string_copy)

        new_dict[keys].update(set_copy)

    for set_of_strings in new_dict.values():  # make sure it worked, reiterate if needed
        for strings in set_of_strings:
            if len(strings) > 1 and (set(strings) & set(alphabet)):
                        return non_iso_term_elim_alternative(new_dict,
                                             (key for key in new_dict.keys()),
                                             alphabet)
    return new_dict, True


def long_right_alternative(rules):
    alternate_keys = [list(key)[0] for key in rules.keys() if len(key) > 1]
    alph = set(string.ascii_uppercase) - set(alternate_keys)

    new_dict = {}
    am_new_keys = 0

    new_key = alph.pop() + str(am_new_keys)
    for key, set_of_strings in rules.items():
        new_dict[key] = set_of_strings.copy()
        for strings in set_of_strings:
            amount_integers = len([num for num in [char for char in strings] if num not in string.ascii_uppercase])
            if len(strings) - amount_integers > 2:
                string_copy = strings
                length = 0
                new_val = ""
                for char in reversed(string_copy):
                    if length == 2:
                        break
                    if char not in string.ascii_uppercase:
                        new_val = char + new_val
                        continue
                    new_val = char + new_val
                    length += 1

                am_new_keys += 1
                if am_new_keys > 9:
                    new_key = alph.pop()
                    am_new_keys = 0
                if len(new_key) > 1:
                    new_key = ''.join(list(new_key)[:-1]) + str(am_new_keys)
                    
                string_copy = string_copy[:-len(new_val)] + new_key
                new_dict[key].remove(strings)
                new_dict[key].add(string_copy)
                new_dict[new_key] = set()
                new_dict[new_key].add(new_val)
    
    for key, set_of_strings in new_dict.items():
        for strings in set_of_strings:
            amount_integers = len([num for num in
                                   [char for char in strings]
                                   if num not in string.ascii_uppercase])
            if len(strings) - amount_integers > 2:
                return long_right_alternative(new_dict)

    return new_dict
