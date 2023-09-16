# Chomsky_CYK
Implementation of algorithm to Converting CFGs to CNF (Chomsky Normal Form) and  Cocke–Younger–Kasami (CYK) algorithm for CFGs

There are two modules: root and CoreMin.
Use CoreMin module for simple start of algorithms.

## Cocke-Younger-Algorithm
This is the famous CYK algorithm implemented in Java.

### CYK formal algorithm [1]

	let the input be a string S consisting of n characters: a1 ... an.
	let the grammar contain r nonterminal symbols R1 ... Rr.
	This grammar contains the subset Rs which is the set of start symbols.
	let P[n,n,r] be an array of booleans. Initialize all elements of P to false.
	for each i = 1 to n
	  for each unit production Rj -> ai
	    set P[i,1,j] = true
	for each i = 2 to n -- Length of span
	  for each j = 1 to n-i+1 -- Start of span
	    for each k = 1 to i-1 -- Partition of span
	      for each production RA -> RB RC
	        if P[j,k,B] and P[j+k,i-k,C] then set P[j,i,A] = true
	if any of P[1,n,x] is true (x is iterated over the set s, where s are all the indices for Rs) then
	  S is member of language
	else
	  S is not member of language


### Chomsky Normal Form to Context Free Grammar algorithm [2]

	1. Remove all nonterminal from the right hand side of all productions except the unit
	productions.
	2. Replace any rule that has three or more nonterminals with the equivalent rules of size
	two.
	3. Replace every rule S with S0. Add a new rule S0->S
	4. Remove all epsilon transitions by iterating their equivalent form. For each production
	that includes a terminal that is equal to epsilon, add another rule equal to the initial
	rule excluding the terminal that is equal to epsilon.
	5. Remove all the unit rules of the form A ? B


## Running the algorithm

1. Clone the project, cd into the folder and then the src folder then run javac
   to compile: `https://github.com/Malav5372/ChomskyGram.git`
   
    
2. Compile and start console applications with demonstration of algorithms.

    2.1. If you want to see whole cyk algorithm with converting grammar in CNF form
        
            `cd CYK-ChomskyNF/CoreMin/src/` 
            
            `javac cyk.java`
            
    2.2. If you want to see only CNF grammar converting
        
            `cd CYK-ChomskyNF/CoreMin/src/`
            
            `javac Grammar.java`
        
3. Run the program by giving it a grammar|input file of your choosing and supplying
   a string:
   
   3.1. CYK:

       `java Cyk grammar_hw6.txt word1_hw6.txt`

    Or simple start application to use the default input files ("grammar_hw6.txt" and "word1_hw6.txt").

       `java Cyk`
    
    3.2. CNF:

       `java Grammar grammar_hw6.txt`

    Or simple start application to use the default input files ("grammar_hw6.txt").

       `java Grammar`
    

### Requirements
  - Java 7

##References
[1] CKY Algorithm, Chomsky Normal Form. Scott Farrar. CLMA, University of Washington. January 13, 2010.

[2] Chomsky Normal Form. 
<https://www.tutorialspoint.com/automata_theory/chomsky_normal_form.htm>.
