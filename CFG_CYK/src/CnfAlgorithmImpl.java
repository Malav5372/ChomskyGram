
/*
 * Chomsky Normal Form algorithm for Context Free Grammar
 * Author: Alexander Vasiliev <alexandrvasilievby@gmail.com>
 * https://github.com/belrbeZ
 */

import cnf.Grammar;
import cnf.ICnfAlgorithm;

public class CnfAlgorithmImpl implements ICnfAlgorithm {

    private static String pathToGrammar = "grammar_hw6.txt";

    /**
     * Prints the CNF rules
     *
     * @param args
     */
    public static void main(String[] args) {
        if (args.length == 1) {
            pathToGrammar = args[0];
            System.out.println("You set path to grammar file: " + pathToGrammar + ".");
        } else {
            System.err.println("You didn't set path to grammar and word files. Default files will be used: " + pathToGrammar + ".");
        }

        Grammar grammar = new Grammar(pathToGrammar);
        if (!grammar.isRead()) {
            System.out.println("Grammar could not be read.");
            return;
        }

        for (int i = 0; i < grammar.size(); i++) {
            String[] rule = grammar.get(i);
            for (int j = 0; j < rule.length; j++) {
                System.out.print(rule[j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }
}
