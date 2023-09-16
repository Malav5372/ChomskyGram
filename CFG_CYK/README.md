# CFG-Chomsky(CNF)-CYK 

This package takes a CF grammar $G$ and a word $w$ as an input, transforms $G$ into Chomsky normal form and performs the Cocke-Younger-Kasami-algorithm (CYK) to evaluate whether the word can be created by the grammar or not.

## Table of Contents
* **Requirements**
* **Usage**
* **Example**

## Usage

1. **Requirements**
   
   - Windows user (my condolences) need to download and install [miktex](https://miktex.org/download).
    
2. **Execute Program** 

    - Execute from command line using `python3 main.py` or execute `main.py` using your favourite IDE or text editor.

3. **Enter Grammar**

    - Enter the members of the grammar in order with following syntax:
        
| Member                    | Syntax/Input | Output                                               |
|---------------------------|--------------|------------------------------------------------------|
| Symbols                   | $S, B, C...$ | $\{S, B, C\}$                                        |
| Terminal Symbols          | $a, b, c...$ | $\{a, b, c\}$                                        |
| Rules per Symbol (e.g. $S$) | $B, a$, \E   | $\{S \to B \ \| \ a \ \| \ \varepsilon \ \| \ ...\}$ |
| Starting Symbol           | $S$          | $S$                                                  |

   - The grammar may also be entered through an external file with following regulations:
    
    Empty lines in the file will be ignored.

| Order of lines | Grammar member | Rules | Example |
|--------|------------------|--------------------------------------------|-------------|
| 1      | Symbols          | upper case letters                         | S, A, B     |
| 2      | Terminal Symbols | lower case letters                         | a, b        |
| 3      | Starting Symbol  | part of symbols                            | S           |
| 4 to x | Rules per Symbol | first character of the line is the symbol  | S -> AB, AA |
| 4 to x | Rules per Symbol | '->' may be inserted for better clarity    | A -> BA; a  |
| 4 to x | Rules per Symbol | applying rules are stated after the symbol | B -> b      |
    
    Notice that the notation for epsilon is \E. 
    Also note that the LaTeX table will go out of bound for long words. 
4. **Enter Word**

    → Enter the word, nothing fancy to it.

5. **Open PDF**

    → Open the .pdf file using `evince` or your favourite pdf viewer.

Example
---
- **Input:** 

![](https://i.imgur.com/E7otsnk.png)

- **Grammar in CNF:**

![](https://i.imgur.com/nMcuVZ0.png)

- **Finished CYK-Table of $w = aaccca$:**

![](https://i.imgur.com/nIM9x1X.png)

Next Steps:
---

- implement elimination of starting symbol from right sides. :heavy_check_mark:
- implement a desktop UI (because why not)
- maybe implement picture/screenshot input support? 
- create PD automata from new rules and visualize it
