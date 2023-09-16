from string import Template
import tabulate


def to_markdown(table, word, start) -> str:
    v_indices = [str(x + 1) for x in range(len(word))]
    h_indices = [word[x - 1] for x in range(1, len(word)+1)]

    markdown_string = str(tabulate.tabulate(table,
                                            tablefmt="github",
                                            showindex=iter(v_indices),
                                            headers=list(h_indices)))

    if table[0][-1]:
        markdown_string += "\n$w \\in L$\n" if start in table[0][-1][0] else "\n$w \\notin L$\n"
    else:
        markdown_string += "\n$w \\notin L$\n"
    return markdown_string


def to_latex(table, word, start, rules, before) -> str:
    v_indices = [str(x + 1) for x in range(len(word))]
    h_indices = [word[x - 1] for x in range(1, len(word)+1)]

    template = ''.join(open("templates/latex_template.txt", "r").read().splitlines())
    latex_string = str(tabulate.tabulate(table,
                                         tablefmt="latex",
                                         showindex=iter(v_indices),
                                         headers=list(h_indices)))

    latex_string = latex_string.replace(r'\begin{tabular}'r'{r' + ("l" * len(word)),
                                        r"\begin{tabular}{|r" + "|c" * len(word) + "|")

    latex_string = latex_string.replace("['", r'\{')
    latex_string = latex_string.replace("']", r'\}')
    latex_string = latex_string.replace("', '", ", ")
    latex_string = latex_string.replace("1 & ", "\\hline\n 1 & ", 1)
    latex_string = latex_string.replace("[]", r'$\emptyset$')
    latex_string = latex_string.replace("\\end{tabular}", "$word \\end{tabular}")
    if table[0][-1]:
        is_in = '$$w \\in L$ \n' if start in table[0][-1][0] else '$$w \\notin L$ \n'
    else:
        is_in = '$$w \\notin L$ \n'
    latex_string = Template(template).safe_substitute(table=latex_string, word=is_in)
    latex_string = latex_string.replace("word", is_in)
    latex_string = Template(latex_string).safe_substitute(before=grammar_to_latex(before))
    latex_string = Template(latex_string).safe_substitute(after=grammar_to_latex(rules))
    latex_string = latex_string.replace("\\E", "epsilon")

    return latex_string

def grammar_to_latex(rules):
    table_string = ''
    for key, values in rules.items():
        table_string = table_string + str(key) +' & \\rightarrow & '+str(values) +' \\ \n'
    table_string = table_string.replace("'", "")
    table_string = table_string.replace(', ', ' \\mid ')
    table_string = table_string.replace('}', '')
    table_string = table_string.replace('{', '')
    return table_string
