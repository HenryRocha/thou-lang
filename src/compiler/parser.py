from sly import Parser
from sly.lex import Token

from src.models.nodes import *
from src.utils.logger import logger
from src.compiler.tokenizer import ThouLexer
from src.models.value import ValueType


class ThouParser(Parser):
    tokens = ThouLexer.tokens

    precedence = (
        ("left", PLUS, MINUS),
        ("left", MULTIPLY, DIVIDE),
        ("right", UMINUS, UPLUS, UNOT),
    )

    def __init__(self):
        self.symbolTable = {}

    @_("LBRACKET { command } RBRACKET")
    def block(self, p):
        logger.info(f"[ParseBlock] Start...")

        ret: Node = Block()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        logger.debug(f"[ParseBlock] Block commands: {commands}")
        if commands == ["LBRACKET", "_1_repeat", "RBRACKET"]:
            for n in p.command:
                ret.addNode(n)

        logger.info(f"[ParseBlock] End")
        return ret

    @_(
        "SEPARATOR",
        "TYPE_INT IDENTIFIER SEPARATOR",
        "TYPE_INT IDENTIFIER ASSIGN or_expr SEPARATOR",
        "TYPE_STRING IDENTIFIER SEPARATOR",
        "TYPE_STRING IDENTIFIER ASSIGN or_expr SEPARATOR",
        "TYPE_BOOL IDENTIFIER SEPARATOR",
        "TYPE_BOOL IDENTIFIER ASSIGN or_expr SEPARATOR",
        "IDENTIFIER ASSIGN or_expr SEPARATOR",
        "PRINT LPAREN or_expr RPAREN SEPARATOR",
        "WHILE LPAREN or_expr RPAREN command",
        "IF LPAREN or_expr RPAREN command ELSE command",
        "IF LPAREN or_expr RPAREN command",
        "block",
    )
    def command(self, p):
        logger.info(f"[ParseCommand] Start...")

        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]

        if commands == ["TYPE_INT", "IDENTIFIER", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] IDENTIFIER is assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.INT, children=[NoOp()])

        elif commands == ["TYPE_INT", "IDENTIFIER", "ASSIGN", "or_expr", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] IDENTIFIER is not assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.INT, children=[p.or_expr])

        elif commands == ["TYPE_STRING", "IDENTIFIER", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] IDENTIFIER is assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.STRING, children=[NoOp()])

        elif commands == ["TYPE_STRING", "IDENTIFIER", "ASSIGN", "or_expr", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] IDENTIFIER is not assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.STRING, children=[p.or_expr])

        elif commands == ["TYPE_BOOL", "IDENTIFIER", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] IDENTIFIER is assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.BOOL, children=[NoOp()])

        elif commands == ["TYPE_BOOL", "IDENTIFIER", "ASSIGN", "or_expr", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] IDENTIFIER is not assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.BOOL, children=[p.or_expr])

        elif commands == ["IDENTIFIER", "ASSIGN", "or_expr", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] IDENTIFIER reassign")
            ret = Identifier(varName=p._slice[0].value, varType=None, children=[p.or_expr])

        elif commands == ["PRINT", "LPAREN", "or_expr", "RPAREN", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed PRINT")
            ret = Print(children=[p.or_expr])

        elif commands == ["IF", "LPAREN", "or_expr", "RPAREN", "command"]:
            logger.debug(f"[ParseCommand] Consumed IF without ELSE")
            ret = If(condition=p.or_expr, ifTrue=p.command)

        elif commands == ["IF", "LPAREN", "or_expr", "RPAREN", "command", "ELSE", "command"]:
            logger.debug(f"[ParseCommand] Consumed IF with ELSEeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            ret = If(condition=p.or_expr, ifTrue=p.command0, ifFalse=p.command1)

        elif commands == ["WHILE", "LPAREN", "or_expr", "RPAREN", "command"]:
            logger.debug(f"[ParseCommand] Consumed IF without ELSE")
            ret = While(condition=p.or_expr, command=p.command)

        elif commands == ["SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed SEPARATOR")
            ret = NoOp()

        elif commands == ["block"]:
            logger.debug(f"[ParseCommand] Consumed BLOCK")
            ret = p.block

        logger.info(f"[ParseCommand] End. Result:\n{ret}")
        return ret

    @_("and_expr", "and_expr CMP_OR or_expr")
    def or_expr(self, p):
        logger.info(f"[ParseOrExpr] Start...")

        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["and_expr"]:
            ret = p.and_expr

        elif commands == ["and_expr", "CMP_OR", "or_expr"]:
            logger.trace(f"[ParseOrExpr] Consumed CMP_AND")
            ret = CompOp(operation=p._slice[1].type, children=[p.and_expr, p.or_expr])

        return ret

    @_("eq_expr", "eq_expr CMP_AND and_expr")
    def and_expr(self, p):
        logger.info(f"[ParseAndExpr] Start...")

        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["eq_expr"]:
            ret = p.eq_expr

        elif commands == ["eq_expr", "CMP_AND", "and_expr"]:
            logger.trace(f"[ParseAndExpr] Consumed CMP_AND")
            ret = CompOp(operation=p._slice[1].type, children=[p.eq_expr, p.and_expr])

        return ret

    @_("rel_expr", "rel_expr CMP_EQ eq_expr")
    def eq_expr(self, p):
        logger.info(f"[ParseEqExpr] Start...")

        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["rel_expr"]:
            ret = p.rel_expr

        elif commands == ["rel_expr", "CMP_EQ", "eq_expr"]:
            logger.trace(f"[ParseEqExpr] Consumed CMP_GT")
            ret = CompOp(operation=p._slice[1].type, children=[p.rel_expr, p.eq_expr])

        return ret

    @_("expr", "expr CMP_GT rel_expr", "expr CMP_LT rel_expr")
    def rel_expr(self, p):
        logger.info(f"[ParseRelExpr] Start...")

        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["expr"]:
            ret = p.expr

        elif commands == ["expr", "CMP_GT", "rel_expr"]:
            logger.trace(f"[ParseRelExpr] Consumed CMP_GT")
            ret = CompOp(operation=p._slice[1].type, children=[p.expr, p.rel_expr])

        elif commands == ["expr", "CMP_LT", "rel_expr"]:
            logger.trace(f"[ParseRelExpr] Consumed CMP_LT")
            ret = CompOp(operation=p._slice[1].type, children=[p.expr, p.rel_expr])

        return ret

    @_("term", "term PLUS expr", "term MINUS expr")
    def expr(self, p):
        logger.info(f"[ParseExpression] Start...")

        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["term"]:
            ret = p.term

        elif commands == ["term", "PLUS", "expr"]:
            logger.trace(f"[ParseExpression] Consumed PLUS")
            ret = BinOp(operation=p._slice[1].type, children=[p.term, p.expr])

        elif commands == ["term", "MINUS", "expr"]:
            logger.trace(f"[ParseExpression] Consumed MINUS")
            ret = BinOp(operation=p._slice[1].type, children=[p.term, p.expr])

        logger.info(f"[ParseExpression] End")
        return ret

    @_("factor", "factor MULTIPLY term", "factor DIVIDE term")
    def term(self, p):
        logger.info("[ParseTerm] Start...")

        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["factor"]:
            ret = p.factor

        elif commands == ["factor", "MULTIPLY", "term"]:
            logger.trace(f"[ParseTerm] Consumed MULTIPLY")
            ret = BinOp(operation=p._slice[1].type, children=[p.factor, p.term])

        elif commands == ["factor", "DIVIDE", "term"]:
            logger.trace(f"[ParseTerm] Consumed DIVIDE")
            ret = BinOp(operation=p._slice[1].type, children=[p.factor, p.term])

        logger.info("[ParseTerm] End")
        return ret

    @_(
        "VAL_NUMBER",
        "VAL_STRING",
        "VAL_BOOL",
        "IDENTIFIER",
        "PLUS factor %prec UPLUS",
        "MINUS factor %prec UMINUS",
        "NOT factor %prec UNOT",
        "READLN LPAREN RPAREN",
        "LPAREN or_expr RPAREN",
    )
    def factor(self, p):
        logger.debug("[ParseFactor] Start...")

        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["VAL_NUMBER"]:
            logger.debug(f"[ParseFactor] Consumed NUMBER: {p._slice[0]}")
            ret = IntVal(value=int(p._slice[0].value))

        elif commands == ["VAL_BOOL"]:
            logger.debug(f"[ParseFactor] Consumed BOOL_VALUE: {p._slice[0]}")
            ret = BoolVal(value=bool(p._slice[0].value))

        elif commands == ["VAL_STRING"]:
            logger.debug(f"[ParseFactor] Consumed STRING_VALUE: {p._slice[0]}")
            ret = StringVal(value=str(p._slice[0].value[1:-1]))

        elif commands == ["MINUS", "factor"]:
            logger.debug(f"[ParseFactor] Consumed PLUS: {p._slice[0]}")
            logger.trace("[ParseFactor] Started ParseFactor RECURSION...")
            ret = UnOp(operation=p._slice[0].type, children=[p.factor])
            logger.trace("[ParseFactor] Ended ParseFactor RECURSION...")

        elif commands == ["PLUS", "factor"]:
            logger.debug(f"[ParseFactor] Consumed MINUS: {p._slice[0]}")
            logger.trace("[ParseFactor] Started ParseFactor RECURSION...")
            ret = UnOp(operation=p._slice[0].type, children=[p.factor])
            logger.trace("[ParseFactor] Ended ParseFactor RECURSION...")

        elif commands == ["NOT", "factor"]:
            logger.debug(f"[ParseFactor] Consumed NOT: {p._slice[0]}")
            logger.trace("[ParseFactor] Started ParseFactor RECURSION...")
            ret = UnOp(operation=p._slice[0].type, children=[p.factor])
            logger.trace("[ParseFactor] Ended ParseFactor RECURSION...")

        elif commands == ["LPAREN", "or_expr", "RPAREN"]:
            logger.debug(f"[ParseFactor] Consumed LEFT_PARENTHESIS: {p._slice[0]}")
            logger.trace("[ParseFactor] Started ParseOrExpr RECURSION...")
            ret = p.or_expr
            logger.trace("[ParseFactor] Ended ParseOrExpr RECURSION...")

        elif commands == ["IDENTIFIER"]:
            logger.debug(f"[ParseFactor] Consumed VARIABLE: {p._slice[0]}")
            ret = Variable(varName=p._slice[0].value)

        elif commands == ["READLN", "LPAREN", "RPAREN"]:
            logger.debug(f"[ParseFactor] Consumed READLN: {p._slice[0]}")
            ret = Readln()

        else:
            logger.critical(f"[ParseFactor] Unexpected token: {p._slice[0]}")

        logger.debug("[ParseFactor] End")
        return ret
