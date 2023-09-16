/*
 * CYK algorithm for Context Free Language
 * Author: Alexander Vasiliev <alexandrvasilievby@gmail.com>
 * https://github.com/belrbeZ
 */

import cnf.Grammar;
import cyk.CykCore;
import cyk.ICykAlgorithm;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class CykAlgorithmImpl implements ICykAlgorithm {

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
            System.err.println("You didn't set paths to grammar and word files. Default files will be used: " + pathToGrammar + ", " + pathToWord + ".");
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
                if (CykCore.cyk(parsedLine, grammar))
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
                if (CykCore.cyk(parsedLine, grammar))
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
