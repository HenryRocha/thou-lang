# thou-lang

Custom programming language based on the classic english grammar. Created for Insper's 2021.1 Computer Logic class.

## EBNF

```
MAIN = FUNCTION ;

FUNCTION = TYPE, IDENTIFIER, "(", [{PARAM}], ")", BLOCK ;
PARAM = TYPE, IDENTIFIER ;
RETURN = "return_to_the_one_whom_bid_thou", (EXPRESSION | COMPARISON), ";" ;

FUNCTION_CALL = IDENTIFIER, "(", (EXPRESSION | COMPARISON), {",", (EXPRESSION | COMPARISON)}, ")", ";" ;

BLOCK = "{", STATEMENT, { STATEMENT }, "}" ;
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | WHILE | RETURN | FUNCTION_CALL) ;

PRINT = "thou_shalt_utter", "(", (EXPRESSION | COMPARISON), ")", ";" ;

IF = "shouldst_this_be_true", "(", COMPARISSON, ")", BLOCK, { ELSE };
ELSE = "if_naught", BLOCK ;

WHILE = "thou_shall_repeat_if", "(", COMPARISSON, ")", BLOCK ;

TYPE = "maths" | "is_it_true" | "kayne_west_phrase" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

ASSIGNMENT = TYPE, IDENTIFIER, "=", (COMPARISON | EXPRESSION | NUMBER | STRING | BOOLEAN), ";" ;
ASSIGNMENT = TYPE, IDENTIFIER, ";" ;
COMPARISON = EXPRESSION, (">", "<", "==", ">=", "<=", "!="), EXPRESSION ;

EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;

BOOLEAN = "it_is_sooth" | "it_is_false" ;

NUMBER = DIGIT, { DIGIT } ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;

STRING = '"', LETTER, { LETTER }, '"' ;
LETTER = ( a | ... | z | A | ... | Z ) ;
```
