from sly import Lexer


class ThouLexer(Lexer):
    # Set of token names. This is always required
    tokens = {
        IDENTIFIER,
        PLUS,
        MINUS,
        MULTIPLY,
        DIVIDE,
        NOT,
        LPAREN,
        RPAREN,
        LBRACKET,
        RBRACKET,
        PRINT,
        READLN,
        IF,
        ELSE,
        WHILE,
        CMP_LT,
        CMP_LEQ,
        CMP_GT,
        CMP_GEQ,
        CMP_EQ,
        CMP_NEQ,
        CMP_AND,
        CMP_OR,
        ASSIGN,
        SEPARATOR,
        ARG_SEPARATOR,
        TYPE_INT,
        TYPE_BOOL,
        TYPE_STRING,
        VAL_BOOL,
        VAL_NUMBER,
        VAL_STRING,
        RETURN,
    }

    # String containing ignored characters between tokens.
    ignore = " \t"
    ignore_comment = r"/\*(.*?)\*/"

    # Regular expression rules for tokens.
    IDENTIFIER = r"[a-zA-Z_][a-zA-Z0-9_]*"
    IDENTIFIER["thou_shalt_utter"] = PRINT
    IDENTIFIER["thou_shalt_read"] = READLN
    IDENTIFIER["shouldst_this_be_true"] = IF
    IDENTIFIER["if_naught"] = ELSE
    IDENTIFIER["thou_shall_repeat_if"] = WHILE
    IDENTIFIER["maths"] = TYPE_INT
    IDENTIFIER["is_it_true"] = TYPE_BOOL
    IDENTIFIER["kayne_west_phrase"] = TYPE_STRING
    IDENTIFIER["it_is_sooth"] = VAL_BOOL
    IDENTIFIER["it_is_false"] = VAL_BOOL
    IDENTIFIER["return_to_the_one_whom_bid_thou"] = RETURN

    VAL_NUMBER = r"\d+"
    VAL_STRING = r"""("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')"""

    CMP_LEQ = r"<="
    CMP_LT = r"<"
    CMP_GEQ = r">="
    CMP_GT = r">"
    CMP_NEQ = r"!="
    CMP_EQ = r"=="

    CMP_AND = r"&&"
    CMP_OR = r"\|\|"

    PLUS = r"\+"
    MINUS = r"-"
    MULTIPLY = r"\*"
    DIVIDE = r"/"
    NOT = r"!"

    ASSIGN = r"="
    SEPARATOR = r";"
    ARG_SEPARATOR = r","

    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACKET = r"\{"
    RBRACKET = r"\}"

    @_(r"\n+")
    def ignore_newline(self, t):
        # Define a rule so we can track line numbers
        self.lineno += len(t.value)
