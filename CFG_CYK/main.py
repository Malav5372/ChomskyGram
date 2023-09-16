from argparse import ArgumentParser
import subprocess
import cfg_input
from cyk import cyk
from output_cyk import create_output
from cnf import cnf_test, cnf_alternative, cnf
import copy


def run_pdflatex(file_name: str = "CYK_Tableau.tex", path: str = "."):
    """
    Call pdflatex on the genereated .tex file to create the PDF
    """
    return subprocess.call(['pdflatex', file_name], cwd=path)


if __name__ == '__main__':
    parser = ArgumentParser('CYK')
    parser.add_argument('-f', '--grammar-file', type=str,
                        help='specifies the path to the context-free grammar to transform.')
    parser.add_argument('-l', '--latex', action='store_true',
                        help='set to enable latex output.')
    parser.add_argument('-m', '--markdown', action='store_true',
                        help='set to enable markdown output.')
    parser.add_argument('-w', '--word', type=str,
                        help="specifies the word to calculate the CYK algorithm with.")
    parser.add_argument('-o', '--output-name', type=str,
                        help='specifies the name prefix for resulting files.')
    args = parser.parse_args()

    if not (file_input := args.grammar_file):
        specify_manual = input(
            'No file input given. Do you want to specify the grammar yourself? [Y/n]')

    grammar = cfg_input.CFG()

    if file_input:
        grammar.file_input(file_input)
    else:
        grammar.new_grammar()

    if not (word := args.word):
        word = input("No word specified.Please enter the word. \n")

    grammar_copy = copy.deepcopy(grammar.rules)
    cnf_test.print_grammar(grammar.rules)
    grammar.rules = cnf.transform_to_cnf(grammar)

    print("Transformation to context-free grammar done.")

    cnf_test.print_grammar(grammar.rules)
    table = cyk(grammar, word)

    if not (args.latex or args.markdown):
        print('No output format specified!')
        output_options = input(
            'Specify: [L]atex, [M]arkdown, or [B]oth: [L/M/B]')
        if 'B' in output_options:
            args.latex = True
            args.markdown = True
        elif 'L' in output_options:
            args.latex = True
        else:
            args.markdown = True

    if args.latex:
        tableau = create_output.to_latex(
            table, word, grammar.start, grammar.rules, grammar_copy)
        with open(file="CYK_Tableau.tex", mode="w") as file:
            file.write(tableau)
            print(f"\nWritten output to {file.name}")
            run_pdflatex()
            print("\nOutput saved to CYK_Tableau.pdf")
    if args.markdown:
        tableau = create_output.to_markdown(table, word, grammar.start)
        with open(file="CYK_Tableau.md", mode="w") as file:
            file.write(tableau)
            print(f"\nWritten output to {file.name}")
