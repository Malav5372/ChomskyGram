/*
 * Chomsky Normal Form algorithm for Context Free Grammar
 * Author: Alexander Vasiliev <alexandrvasilievby@gmail.com>
 * https://github.com/belrbeZ
 */

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

public class Grammar {

    private static String pathToGrammar = "grammar_hw6.txt";


    ArrayList<String[]> rules;

    /**
     * Constructor, the Grammar File is saved in an ArrayList of type String[].
     * So that rules can be accessed as a list and each part of the rule can be
     * accessed inidividually in the String array.
     *
     * @param grammarFile
     */
    public Grammar(String grammarFile) {
        this.rules = convertrules(readrules(grammarFile));
    }

    /**
     * Converts the rules according to the steps
     * http://www.cs.nyu.edu/courses/fall07/V22.0453-001/cnf.pdf returns the
     * rules in CNF format
     *
     * @param rules
     * @return
     */
    public static ArrayList<String[]> convertrules(ArrayList<String[]> rules) {
        if (rules == null) {
            return null;
        }

        stepOne(rules);
        stepTwo(rules);
        stepThree(rules);
        stepFour(rules);
        stepFive(rules);
        return rules;
    }

    /**
     * ############## STEP FIVE ##################
     *
     * @param rules
     */
    public static void stepFive(ArrayList<String[]> rules) {
        List<String[]> unitProductions = findUnitProductions(rules);

        // find strong graph components.

        for (int i = 0; i < unitProductions.size(); i++) {
            String[] production = unitProductions.get(i);
            for (int j = 0; j < unitProductions.size(); j++) {
                String[] tempProduction = unitProductions.get(j);
                if (production[0] == tempProduction[1]
                        && production[1] == tempProduction[0]) {
                    // it is strong graph component since they nodes point to
                    // each other
                    // replace all rules that have the second symbol with the
                    // first symbol
                    // S'->X => S'->S'
                    for (int k = 0; k < rules.size(); k++) {
                        String[] rule = rules.get(k);
                        for (int l = 0; l < rule.length; l++) {
                            if (rule[l].equals(production[1])) {
                                rule[l] = production[0];
                            }
                        }
                        rules.set(k, rule);
                    }
                }
            }
        }

        // remove rules of the form X->X
        for (int i = 0; i < rules.size(); i++) {
            String[] rule = rules.get(i);
            if (rule[0].equals(rule[1]) && rule.length == 2) {
                rules.remove(i);
                i--;
            }
        }

        unitProductions = findUnitProductions(rules);
        // we now have a reduced graph
        // we traverse through the graph
        for (int i = 0; i < unitProductions.size(); i++) {
            String[] production = unitProductions.get(i);
            step5Recursion(rules, production, getIndexInRules(rules, production));
        }
        // remove duplicate rules
        for (int i = 0; i < rules.size(); i++) {
            String[] rule = rules.get(i);
            for (int j = 0; j < rules.size(); j++) {
                if (rules.get(j).length == rules.get(i).length) {
                    boolean isEqual = true;

                    for (int k = 0; k < rule.length; k++) {
                        if (!rules.get(j)[k].equals(rule[k])) {
                            isEqual = false;
                        }
                    }
                    if (i != j && isEqual) {
                        rules.remove(j);
                        j--;
                    }
                }
            }
        }
        System.out.println("STEP 5");
        for (int i = 0; i < rules.size(); i++) {
            String[] rule = rules.get(i);
            for (int j = 0; j < rule.length; j++) {
                System.out.print(rule[j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    private static int getIndexInRules(ArrayList<String[]> rules, String[] production) {
        for (int i = 0; i < rules.size(); i++) {
            if (rules.get(i)[0].equals(production[0]) &&
                    rules.get(i)[1].equals(production[1])) {
                return i;
            }
        }
        return -1;
    }

    public static void step5Recursion(ArrayList<String[]> rules,
                                      String[] production, int oldProductionIndex) {
        for (int j = 0; j < rules.size(); j++) {
            // System.out.println(rules.get (j)[0]+" "); // debugging

            if (rules.get(j)[0].equals(production[1])) {
                if (rules.get(j).length == 2
                        && Character.isLowerCase(rules.get(j)[1].charAt(0))) {
                    // case where letter is lowercase
                    // S -> a
                    String[] rule = {production[0], rules.get(j)[1]};
                    rules.add(rule);
                    int ruleCount = 0;
                    int meetedInRight = 0;
                    for (int k = 0; k < rules.size(); k++) {
                        String[] curRule = rules.get(k);
                        if (curRule[0].equals(production[1])) {
                            ruleCount++;
                        }
                        for (int i = 1; i < curRule.length; i++) {
                            if (curRule[i].equals(production[1])) {
                                meetedInRight++;
                            }
                        }
                    }


                    if (ruleCount > 0 && meetedInRight <= 1) {
                        //check if is somewhere in right part
                        rules.remove(j);
                        j--;
                    }


                } else if (rules.get(j).length == 2
                        && Character.isUpperCase(rules.get(j)[1].charAt(0))) {

                    String[] newProduction = {production[0], rules.get(j)[1]};
                    // check conditions before removing
                    rules.remove(oldProductionIndex);
                    if (oldProductionIndex < j) {
                        j--;
                    }
                    rules.add(newProduction);
                    int tempIndexOfAddedRule = rules.size() - 1;
                    step5Recursion(rules, newProduction, tempIndexOfAddedRule);
                    if (rules.get(tempIndexOfAddedRule)[0].equals(newProduction[0]) &&
                            rules.get(tempIndexOfAddedRule)[1].equals(newProduction[1])) {
                        rules.remove(tempIndexOfAddedRule);
                    }
                    // re-avaluate it for | transitions
                } else if (rules.get(j).length == 3) {

                    String[] rule = {production[0], rules.get(j)[1],
                            rules.get(j)[2]};
                    rules.add(rule);

                }

            }
        }
        if (rules.get(oldProductionIndex)[0].equals(production[0]) &&
                rules.get(oldProductionIndex)[1].equals(production[1])) {
            rules.remove(oldProductionIndex);
        }
    }

    public static ArrayList<String[]> findUnitProductions(
            ArrayList<String[]> rules) {
        ArrayList<String[]> unitProductions = new ArrayList();
        // create graph of unit productions
        for (int i = 0; i < rules.size(); i++) {
            if (rules.get(i).length == 2
                    && Character.isUpperCase(rules.get(i)[1].charAt(0))) {
                // it is a unit production
                // create a graph
                unitProductions.add(rules.get(i));
            }
        }
        return unitProductions;
    }

    /**
     * ############## STEP FOUR ##################
     * Remove epsilon symbol 'o'
     *
     * @param rules
     */
    public static void stepFour(ArrayList<String[]> rules) {
        for (int i = 0; i < rules.size(); i++) {
            if (rules.get(i)[1].equals("o")) {
                // made into a function
                String nullNonTerminal = rules.get(i)[0];
                rules.remove(i);

                removeEpsilon(rules, nullNonTerminal);
            }
            //
        }
        System.out.println("STEP 4");
        for (int i = 0; i < rules.size(); i++) {
            String[] rule = rules.get(i);
            for (int j = 0; j < rule.length; j++) {
                System.out.print(rule[j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    public static void removeEpsilon(ArrayList<String[]> rules,
                                     String nullNonTerminal) {

        for (int j = 0; j < rules.size(); j++) {

            if (rules.get(j)[1].equals(nullNonTerminal)) {
                if (rules.get(j).length == 3) {
                    if (rules.get(j)[2].equals(nullNonTerminal)) {
                        // case1
                        String newNullNonTerminal = rules.get(j)[0];
                        // reecursion on newNull

                        if (!isDoubleNonTerminal(rules, nullNonTerminal)) {
                            rules.remove(j);

                            removeEpsilon(rules, newNullNonTerminal);
                        }
                    } else {
                        // case 3
                        String[] newRule = {rules.get(j)[0], rules.get(j)[2]};
                        if (isDoubleNonTerminal(rules, nullNonTerminal)) {
                            rules.add(j, newRule);
                            j++;
                        } else
                            rules.set(j, newRule);
                    }
                } else {
                    // case 2
                    String newNullNonTerminal = rules.get(j)[0];
                    // recursion
                    if (!isDoubleNonTerminal(rules, nullNonTerminal)) {

                        rules.remove(j);

                        removeEpsilon(rules, newNullNonTerminal);
                    }
                }
                // String[] newRule={rules.get(j)[0])
            } else if (rules.get(j).length == 3) {

                if (rules.get(j)[2].equals(nullNonTerminal)) {

                    // case 4
                    // S-> B A
                    // A-> e
                    // = S -> B
                    String[] newRule = {rules.get(j)[0], rules.get(j)[1]};
                    if (isDoubleNonTerminal(rules, nullNonTerminal)) {
                        rules.add(j, newRule);
                        // interesting problem because when u add u keep adding
                        // and the loop never ends.
                        // System.out.println(newRule[1]);
                        // break;
                        j++;
                    } else
                        rules.set(j, newRule);
                }
            }
        }
    }

    public static boolean isDoubleNonTerminal(ArrayList<String[]> rules,
                                              String NonTerminal) {
        // we removed the 1st one
        int count = 1;
        for (int i = 0; i < rules.size(); i++) {
            if (rules.get(i)[0].equals(NonTerminal))
                count++;
        }
        // System.out.println(count);
        if (count > 1)
            return true;
        return false;
    }

    /**
     * ############## STEP THREE ##################
     * Create S' for S
     *
     * @param rules
     */
    public static void stepThree(ArrayList<String[]> rules) {
        boolean thereIsS = false;
        for (int i = 0; i < rules.size(); i++) {
            String[] rule = rules.get(i);
            for (int j = 1; j < rule.length; j++) {
                if (rule[j].equals("S")) {
                    thereIsS = true;
                    break;
                }
            }
        }
        if (thereIsS) {
            for (int i = 0; i < rules.size(); i++) {
                String[] rule = rules.get(i);
                for (int j = 0; j < rule.length; j++) {
                    if (rule[j].equals("S")) {
                        rule[j] = "S_0";
                    }
                }
            }
            String[] SigmaRule = {"S", "S_0"};
            rules.add(SigmaRule);
        }
        System.out.println("STEP 3");
        for (int i = 0; i < rules.size(); i++) {
            String[] rule = rules.get(i);
            for (int j = 0; j < rule.length; j++) {
                System.out.print(rule[j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    /**
     * ############## STEP TWO ##################
     * Remove and replace all unit productions with size > 2
     *
     * @param rules
     */
    public static void stepTwo(ArrayList<String[]> rules) {
        int count = 0;

        for (int i = 0; i < rules.size(); i++) {
            while (rules.get(i).length > 3) {

                int n = rules.get(i).length;

                String[] g = new String[3];

                g[0] = "P" + count;
                g[1] = rules.get(i)[n - 2];
                g[2] = rules.get(i)[n - 1];

                rules.add(g);

                String[] h = new String[n - 1];

                for (int j = 0; j < n - 2; j++) {
                    h[j] = rules.get(i)[j];
                }

                h[n - 2] = "P" + count;
                count++;

                rules.remove(i);
                rules.add(h);

            }

        }
        System.out.println("STEP 2");
        for (int i = 0; i < rules.size(); i++) {
            String[] rule = rules.get(i);
            for (int j = 0; j < rule.length; j++) {
                System.out.print(rule[j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    /**
     * ############## STEP ONE ##################
     *
     * @param rules
     */
    public static void stepOne(ArrayList<String[]> rules) {
        int s = rules.size();

        for (int i = 0; i < s; i++) {
            if (rules.get(i).length > 2) {
                for (int j = 0; j < rules.get(i).length; j++) {

                    char n = rules.get(i)[j].charAt(0);

                    if (Character.isLowerCase(n)) {
                        String[] g = new String[2];

                        g[0] = rules.get(i)[j].toUpperCase() + "_0";// add one
                        // more

                        g[1] = rules.get(i)[j];
                        boolean isAlreadyDefined = false;
                        for (int k = 0; k < rules.size(); k++) {
                            if (g[0].equals(rules.get(k)[0]))
                                isAlreadyDefined = true;
                        }
                        if (!isAlreadyDefined)
                            rules.add(g);

                        rules.get(i)[j] = rules.get(i)[j].toUpperCase()
                                + "_0"; // change the grammar
                    }

                }

            }

        }
        System.out.println("STEP 1");
        for (int i = 0; i < rules.size(); i++) {
            String[] rule = rules.get(i);
            for (int j = 0; j < rule.length; j++) {
                System.out.print(rule[j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    /**
     * Size of the array list
     *
     * @return
     */
    public int size() {
        return this.rules.size();
    }

    /**
     * returns the ith element of the array list
     *
     * @param i
     * @return
     */
    public String[] get(int i) {
        return this.rules.get(i);
    }

    /**
     * returns the list of rules in grammar
     *
     * @return list of rules
     */
    public ArrayList<String[]> getRules() {
        return rules;
    }

    /**
     * are the rules read or just null?
     *
     * @return
     */
    public boolean isRead() {
        if (this.rules != null)
            return true;
        return false;
    }

    /**
     * Reads the rules
     *
     * @param grammarFile
     * @return
     */
    public ArrayList<String[]> readrules(String grammarFile) {
        ArrayList<String[]> rules = new ArrayList<String[]>();
        try {
            FileReader fr = new FileReader(grammarFile);
            BufferedReader br = new BufferedReader(fr);
            String line = br.readLine();
            while (line != null) {
                String[] rule = line.toString().split(" ");
                rules.add(rule);
                line = br.readLine();
            }

        } catch (Exception e) {
            System.err.println("Can't find file " + grammarFile + " for parse grammar!");
            return null;
        }
        return rules;
    }

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
