/*
 * CYK algorithm for Context Free Language
 * Author: Alexander Vasiliev <alexandrvasilievby@gmail.com>
 * https://github.com/belrbeZ
 */

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class cyk {

    private static final Map<Character, Character> parseSymbols;
    private static String pathToGrammar = "grammar_hw6.txt";
    private static String pathToWord = "word1_hw6.txt";

    static {
        Map<Character, Character> aMap = new HashMap<>();
        aMap.put('0', 'a');
        aMap.put('1', 'b');
        aMap.put('2', 'c');
        aMap.put('3', 'd');
        aMap.put('4', 'e');
        aMap.put('5', 'f');
        aMap.put('6', 'g');
        aMap.put('7', 'h');
        aMap.put('8', 'i');
        aMap.put('9', 'j');
        aMap.put('-', 'q');
        aMap.put('*', 'w');
        aMap.put('(', 'r');
        aMap.put(')', 't');
        parseSymbols = Collections.unmodifiableMap(aMap);
    }

    /**
     * Finds the index of the symbol The purpose of this is to use each symbol
     * as a unique id with a specific index and truth value on the P table.
     *
     * @param Grammar
     * @param symbol
     * @return
     */
    public static int findIndex(Grammar Grammar, String symbol) {
        for (int i = 0; i < Grammar.size(); i++) {
            String[] rule = Grammar.get(i);
            if (rule.length == 2) {
                if (symbol.equals(Grammar.get(i)[0]))
                    return i;
            }
        }
        for (int i = 0; i < Grammar.size(); i++) {
            if (symbol.equals(Grammar.get(i)[0]))
                return i;
        }
        return -1;

    }

    /**
     * Finds the starting symbol which is S or the first symbol of the grammar
     *
     * @param Grammar
     * @return
     */
    public static Integer[] findStartingSymbols(Grammar Grammar) {
        /*
         * for (int i = 0; i < Grammar.size (); i++) { String[] rule =
         * Grammar.get (i); if (rule[0].equals ("S_0")) return i; }
         */
        ArrayList<Integer> startSymbols = new ArrayList<Integer>();
        for (int i = 0; i < Grammar.size(); i++) {
            String[] rule = Grammar.get(i);
            if (rule[0].equals("S")) {
                startSymbols.add(i);
                if (rule.length == 2) {
                    startSymbols.add(findIndex(Grammar, rule[1]));
                }
            }
        }

        Integer[] output = new Integer[startSymbols.size()];
        output = startSymbols.toArray(output);
        return output;
    }

    /**
     * Returns whether or not the string S belongs to grammar
     *
     * @param S
     * @param grammar
     * @return
     */
    public static boolean cyk(String S, Grammar grammar) {
        int n = S.length();
        int r = grammar.size();
        Integer[] startSymbols = findStartingSymbols(grammar);
        boolean P[][][] = new boolean[n][n][r];
        // let P[n,n,r] be an array of booleans. Initialize all elements of P to
        // false.
        initializeP(P, n, r);
        // for each i = 1 to n, we do -1 because it is java and arrays start
        // from 0
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < r; j++) {
                // for each unit production Rj -> ai
                String[] rule = (String[]) grammar.get(j);
                if (rule.length == 2) {
                    if (rule[1].equals(String.valueOf(S.charAt(i)))) {

                        int A = findIndex(grammar, rule[0]);
                        // set P[i,1,j] = true
                        P[i][0][A] = true;

                    }
                }
            }
        }

        // for each i = 2 to n -- Length of span
        for (int i = 1; i < n; i++) {
            // for each j = 1 to n-i+1 -- Start of span
            for (int j = 0; j < n - i; j++) {
                // for each k = 1 to i-1 -- Partition of span
                for (int k = 0; k < i; k++) {
                    // for each production RA -> RB RC
                    for (int m = 0; m < r; m++) {
                        String[] rule = grammar.get(m);
                        if (rule.length > 2) {

                            int A = findIndex(grammar, rule[0]);
                            int B = findIndex(grammar, rule[1]);
                            int C = findIndex(grammar, rule[2]);
                            // System.out.println(rule[2]+" "+C);
                            // if P[j,k,B] and P[j+k,i-k,C] then set P[j,i,A] =
                            // true
                            if (P[j][k][B] && P[j + k + 1][i - k - 1][C])
                                P[j][i][A] = true;

                        }
                    }
                }
            }
        }

        printP3DMatrix(P, grammar, S);

        System.out.println("###Parse Tree###");
        for (int i = 0; i < S.length(); i++) {
            System.out.print(S.charAt(i) + " ");
        }

        System.out.println();
        printP(P, n, r, grammar);
        // if any of P[1,n,x] is true (x is iterated over the set s, where s are
        // all the indices for Rs) then
        for (int i = 0; i < startSymbols.length; i++) {
            int x = startSymbols[i];
            if (x >= 0)
                if (P[0][n - 1][x])
                    return true; // S is member of language
        }

        // else
        return false; // S is not member of language
    }

    private static void printP3DMatrix(boolean[][][] p, Grammar grammar, String input) {
        ArrayList<ArrayList<String>> content = new ArrayList<>(p.length);

        StringBuilder curStateIndex = new StringBuilder();
        for (int i = 0; i < p.length; i++) {
            ArrayList<String> contentRow = new ArrayList<>(p[i].length);

            for (int j = 0; j < p[i].length; j++) {

                for (int k = 0; k < p[i][j].length; k++) {
                    String[] curState = grammar.get(k);

                    if (p[i][j][k]) {
                        for (int l = 0; l < curState.length; l++) {
                            curStateIndex.append(curState[l]);
                            if (l == 0) {
                                curStateIndex.append("->");
                            } else if (l < curState.length - 1) {
                                curStateIndex.append(" ");
                            } else if (l == curState.length - 1) {
                                curStateIndex.append(";");
                            }
                        }
                    }
                }
                if (curStateIndex.length() == 0) {
                    curStateIndex.append(" ");
                }
                contentRow.add(j, curStateIndex.toString());
                curStateIndex.setLength(0);
            }

            content.add(i, contentRow);
        }


        ArrayList<String> headers = new ArrayList<>();
        for (int i = 0; i < input.length(); i++) {
            headers.add(String.valueOf(input.charAt(i)));
            curStateIndex.setLength(0);
        }

        ConsoleTable consoleTable = new ConsoleTable(headers, content);
        consoleTable.printTable();

    }

    /**
     * Prints the parse table.
     *
     * @param P
     * @param n
     * @param r
     * @param grammar
     */
    public static void printP(boolean P[][][], int n, int r, Grammar grammar) {
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n - i; k++) {
                System.out.print("{");
                for (int m = 0; m < r; m++) {
                    if (P[k][i][m]) {
                        System.out.print(grammar.get(m)[0] + " ");
                    }

                }

                System.out.print("} ");
            }
            System.out.println();
        }
    }

    /**
     * Initializes the P array
     *
     * @param P
     * @param n
     * @param r
     */
    public static void initializeP(boolean P[][][], int n, int r) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < r; k++) {
                    P[i][j][k] = false;
                }
            }
        }
    }

    /**
     * Main
     *
     * @param args
     */
    public static void main(String args[]) {

        if (args.length == 2) {
            pathToGrammar = args[0];
            pathToWord = args[1];
            System.out.println("You set paths to grammar and word files: " + pathToGrammar + ", " + pathToWord + ".");
        } else {
            System.err.println("You didn't set path to grammar and word files. Default files will be used: " + pathToGrammar + ", " + pathToWord + ".");
        }

        Grammar grammar = new Grammar(pathToGrammar);
        if (!grammar.isRead()) {
            System.out.println("Grammar could not be read.");
            return;
        }

        processCYK(grammar);

        System.out.println("end");
        return;
    }

    private static void processCYK(Grammar grammar) {
        String input;
        String parsedLine;

        try {
            FileReader fr = new FileReader(pathToWord);
            BufferedReader br = new BufferedReader(fr);
            input = br.readLine();
            while (input != null) {
                if ("quit".equals(input) || "exit".equals(input)) {
                    break;
                }
                parsedLine = replaceNumbersWithSymbols(input);
                if (cyk(parsedLine, grammar))
                    System.out.println("String is part of the language");
                else
                    System.out.println("String is NOT part of the language");
                input = br.readLine();
            }
        } catch (IOException ex) {
            System.err.println("Can't read file with word " + pathToWord + " for analyze!");
            Scanner in = new Scanner(System.in);
            while (in.hasNext()) {
                input = in.next();
                if ("quit".equals(input) || "exit".equals(input)) {
                    break;
                }
                parsedLine = replaceNumbersWithSymbols(input);
                if (cyk(parsedLine, grammar))
                    System.out.println("String is part of the language");
                else
                    System.out.println("String is NOT part of the language");
            }
        }

    }

    private static String replaceNumbersWithSymbols(String line) {
        StringBuilder newString = new StringBuilder();
        for (char ch :
                line.toCharArray()) {
            if (parseSymbols.containsKey(ch)) {
                newString.append(parseSymbols.get(ch));
            } else {
                newString.append(ch);
            }
        }
        return newString.toString();
    }
}
