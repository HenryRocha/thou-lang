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

    debugfile = "./parser.out"

    def __init__(self):
        self.symbolTable = {}

    @_("{ parseFuncDef }")
    def parseFunctions(self, p):
        ret: Block = Block()
        for node in p.parseFuncDef:
            ret.addNode(node)
        return ret

    @_(
        "TYPE_INT IDENTIFIER LPAREN { parseFuncDefArgs } RPAREN parseCommand",
        "TYPE_BOOL IDENTIFIER LPAREN { parseFuncDefArgs } RPAREN parseCommand",
        "TYPE_STRING IDENTIFIER LPAREN { parseFuncDefArgs } RPAREN parseCommand",
    )
    def parseFuncDef(self, p):
        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        logger.trace(f"[ParseFuncDef] Commands {commands}")
        if commands == ["TYPE_INT", "IDENTIFIER", "LPAREN", "_4_repeat", "RPAREN", "parseCommand"]:
            logger.debug(f"[ParseFuncDef] Consumed function declaration '{p._slice[1].value}'")

            ret = FuncDec(value=p._slice[1].value, retType=p._slice[0].value)
            logger.trace(f"[ParseFunctionDef] Arguments for '{p._slice[1].value}' {type(p._4_repeat)} {p._4_repeat}")
            ret.setArguments(p._4_repeat[0][0] if len(p._4_repeat) > 0 else [])
            ret.setStatements(p.parseCommand.children)
        else:
            logger.critical(f"[ParseFuncDef] Unexpected commands {commands}")

        return ret

    @_("parseFuncArgDef { ARG_SEPARATOR parseFuncArgDef }")
    def parseFuncDefArgs(self, p):
        ret: List[Value] = [p.parseFuncArgDef0] + [arg[1] for arg in p._5_repeat]
        logger.debug(f"[ParseFuncDefArgs] Consumed {len(ret)} arguments: {ret}")
        return ret

    @_(
        "TYPE_INT IDENTIFIER",
        "TYPE_BOOL IDENTIFIER",
        "TYPE_STRING IDENTIFIER",
    )
    def parseFuncArgDef(self, p):
        logger.trace(f"[ParseFuncDefArg] Consumed argument {p._slice}")

        if p._slice[0].type == "TYPE_INT":
            return Value(ValueType.INT, p._slice[1].value)
        elif p._slice[0].type == "TYPE_BOOL":
            return Value(ValueType.BOOL, p._slice[1].value)
        elif p._slice[0].type == "TYPE_STRING":
            return Value(ValueType.STRING, p._slice[1].value)

    @_("LBRACKET { parseCommand } RBRACKET")
    def parseBlock(self, p):
        ret: Node = Block()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["LBRACKET", "_6_repeat", "RBRACKET"]:
            logger.debug(f"[ParseBlock] Consumed block")
            ret.setNodes(nodes=[node[0] for node in p._6_repeat])
        else:
            logger.critical(f"[ParseBlock] Unexpected commands {commands}")

        return ret

    @_(
        "SEPARATOR",
        "TYPE_INT IDENTIFIER SEPARATOR",
        "TYPE_INT IDENTIFIER ASSIGN parseOrExpr SEPARATOR",
        "TYPE_STRING IDENTIFIER SEPARATOR",
        "TYPE_STRING IDENTIFIER ASSIGN parseOrExpr SEPARATOR",
        "TYPE_BOOL IDENTIFIER SEPARATOR",
        "TYPE_BOOL IDENTIFIER ASSIGN parseOrExpr SEPARATOR",
        "IDENTIFIER ASSIGN parseOrExpr SEPARATOR",
        "IDENTIFIER LPAREN { parseFuncCallArgs } RPAREN SEPARATOR",
        "PRINT LPAREN parseOrExpr RPAREN SEPARATOR",
        "WHILE LPAREN parseOrExpr RPAREN parseCommand",
        "IF LPAREN parseOrExpr RPAREN parseCommand ELSE parseCommand",
        "IF LPAREN parseOrExpr RPAREN parseCommand",
        "RETURN parseOrExpr SEPARATOR",
        "parseBlock",
    )
    def parseCommand(self, p):
        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        logger.trace(f"[ParseCommand] Commands: {commands}")

        if commands == ["TYPE_INT", "IDENTIFIER", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed IDENTIFIER, not assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.INT, children=[NoOp()])

        elif commands == ["TYPE_INT", "IDENTIFIER", "ASSIGN", "parseOrExpr", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed IDENTIFIER, assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.INT, children=[p.parseOrExpr])

        elif commands == ["TYPE_STRING", "IDENTIFIER", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed IDENTIFIER, not assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.STRING, children=[NoOp()])

        elif commands == ["TYPE_STRING", "IDENTIFIER", "ASSIGN", "parseOrExpr", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed IDENTIFIER, assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.STRING, children=[p.parseOrExpr])

        elif commands == ["TYPE_BOOL", "IDENTIFIER", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed IDENTIFIER, not assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.BOOL, children=[NoOp()])

        elif commands == ["TYPE_BOOL", "IDENTIFIER", "ASSIGN", "parseOrExpr", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed IDENTIFIER, assigned on declaration")
            ret = Identifier(varName=p._slice[1].value, varType=ValueType.BOOL, children=[p.parseOrExpr])

        elif commands == ["IDENTIFIER", "ASSIGN", "parseOrExpr", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed IDENTIFIER reassign")
            ret = Identifier(varName=p._slice[0].value, varType=None, children=[p.parseOrExpr])

        elif commands == ["IDENTIFIER", "LPAREN", "_7_repeat", "RPAREN", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed function call '{p._slice[0].value}'")
            logger.trace(f"[ParseCommand] Arguments for '{p._slice[0].value}' {type(p._7_repeat)} {p._7_repeat}")
            ret = FuncCall(value=p._slice[0].value, arguments=p._7_repeat[0][0] if len(p._7_repeat) > 0 else [])

        elif commands == ["PRINT", "LPAREN", "parseOrExpr", "RPAREN", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed PRINT")
            ret = Print(children=[p.parseOrExpr])

        elif commands == ["IF", "LPAREN", "parseOrExpr", "RPAREN", "parseCommand"]:
            logger.debug(f"[ParseCommand] Consumed IF without ELSE")
            ret = If(condition=p.parseOrExpr, ifTrue=p.parseCommand)

        elif commands == ["IF", "LPAREN", "parseOrExpr", "RPAREN", "parseCommand", "ELSE", "parseCommand"]:
            logger.debug(f"[ParseCommand] Consumed IF with ELSE")
            ret = If(condition=p.parseOrExpr, ifTrue=p.parseCommand0, ifFalse=p.parseCommand1)

        elif commands == ["WHILE", "LPAREN", "parseOrExpr", "RPAREN", "parseCommand"]:
            logger.debug(f"[ParseCommand] Consumed IF without ELSE")
            ret = While(condition=p.parseOrExpr, command=p.parseCommand)

        elif commands == ["SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed SEPARATOR")
            ret = NoOp()

        elif commands == ["RETURN", "parseOrExpr", "SEPARATOR"]:
            logger.debug(f"[ParseCommand] Consumed RETURN")
            ret = Return(value=p._slice[0].value, child=p.parseOrExpr)

        elif commands == ["parseBlock"]:
            logger.debug(f"[ParseCommand] Consumed BLOCK")
            ret = p.parseBlock

        else:
            logger.critical(f"[ParseCommand] Unexpected commands {commands}")

        return ret

    @_("parseOrExpr { ARG_SEPARATOR parseOrExpr }")
    def parseFuncCallArgs(self, p):
        ret: List[FuncArg] = [p.parseOrExpr0] + [arg[1] for arg in p._8_repeat]
        logger.debug(f"[ParseFunctionCallArgs] Consumed {len(ret)} arguments: {ret}")
        return ret

    @_("parseAndExpr", "parseAndExpr CMP_OR parseOrExpr")
    def parseOrExpr(self, p):
        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["parseAndExpr"]:
            ret = p.parseAndExpr

        elif commands == ["parseAndExpr", "CMP_OR", "parseOrExpr"]:
            logger.trace(f"[ParseOrExpr] Consumed CMP_AND")
            ret = CompOp(operation=p._slice[1].type, children=[p.parseAndExpr, p.parseOrExpr])

        return ret

    @_("parseEqExpr", "parseEqExpr CMP_AND parseAndExpr")
    def parseAndExpr(self, p):
        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["parseEqExpr"]:
            ret = p.parseEqExpr

        elif commands == ["parseEqExpr", "CMP_AND", "parseAndExpr"]:
            logger.trace(f"[ParseAndExpr] Consumed CMP_AND")
            ret = CompOp(operation=p._slice[1].type, children=[p.parseEqExpr, p.parseAndExpr])

        return ret

    @_("parseRelExpr", "parseRelExpr CMP_EQ parseEqExpr")
    def parseEqExpr(self, p):
        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["parseRelExpr"]:
            ret = p.parseRelExpr

        elif commands == ["parseRelExpr", "CMP_EQ", "parseEqExpr"]:
            logger.trace(f"[ParseEqExpr] Consumed CMP_GT")
            ret = CompOp(operation=p._slice[1].type, children=[p.parseRelExpr, p.parseEqExpr])

        return ret

    @_("parseExpression", "parseExpression CMP_GT parseRelExpr", "parseExpression CMP_LT parseRelExpr")
    def parseRelExpr(self, p):
        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["parseExpression"]:
            ret = p.parseExpression

        elif commands == ["parseExpression", "CMP_GT", "parseRelExpr"]:
            logger.trace(f"[ParseRelExpr] Consumed CMP_GT")
            ret = CompOp(operation=p._slice[1].type, children=[p.parseExpression, p.parseRelExpr])

        elif commands == ["parseExpression", "CMP_LT", "parseRelExpr"]:
            logger.trace(f"[ParseRelExpr] Consumed CMP_LT")
            ret = CompOp(operation=p._slice[1].type, children=[p.parseExpression, p.parseRelExpr])

        return ret

    @_("parseTerm", "parseTerm PLUS parseExpression", "parseTerm MINUS parseExpression")
    def parseExpression(self, p):
        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["parseTerm"]:
            ret = p.parseTerm

        elif commands == ["parseTerm", "PLUS", "parseExpression"]:
            logger.trace(f"[ParseExpression] Consumed PLUS")
            ret = BinOp(operation=p._slice[1].type, children=[p.parseTerm, p.parseExpression])

        elif commands == ["parseTerm", "MINUS", "parseExpression"]:
            logger.trace(f"[ParseExpression] Consumed MINUS")
            ret = BinOp(operation=p._slice[1].type, children=[p.parseTerm, p.parseExpression])

        return ret

    @_("parseFactor", "parseFactor MULTIPLY parseTerm", "parseFactor DIVIDE parseTerm")
    def parseTerm(self, p):
        ret: Node = NoOp()

        commands = [str(t.type) if type(t) == Token else str(t) for t in p._slice]
        if commands == ["parseFactor"]:
            ret = p.parseFactor

        elif commands == ["parseFactor", "MULTIPLY", "parseTerm"]:
            logger.trace(f"[ParseTerm] Consumed MULTIPLY")
            ret = BinOp(operation=p._slice[1].type, children=[p.parseFactor, p.parseTerm])

        elif commands == ["parseFactor", "DIVIDE", "parseTerm"]:
            logger.trace(f"[ParseTerm] Consumed DIVIDE")
            ret = BinOp(operation=p._slice[1].type, children=[p.parseFactor, p.parseTerm])

        return ret

    @_(
        "VAL_NUMBER",
        "VAL_STRING",
        "VAL_BOOL",
        "IDENTIFIER",
        "IDENTIFIER LPAREN { parseFuncCallArgs } RPAREN",
        "PLUS parseFactor %prec UPLUS",
        "MINUS parseFactor %prec UMINUS",
        "NOT parseFactor %prec UNOT",
        "READLN LPAREN RPAREN",
        "LPAREN parseOrExpr RPAREN",
    )
    def parseFactor(self, p):
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

        elif commands == ["MINUS", "parseFactor"]:
            logger.debug(f"[ParseFactor] Consumed PLUS: {p._slice[0]}")
            logger.trace("[ParseFactor] Started ParseFactor RECURSION...")
            ret = UnOp(operation=p._slice[0].type, children=[p.parseFactor])
            logger.trace("[ParseFactor] Ended ParseFactor RECURSION...")

        elif commands == ["PLUS", "parseFactor"]:
            logger.debug(f"[ParseFactor] Consumed MINUS: {p._slice[0]}")
            logger.trace("[ParseFactor] Started ParseFactor RECURSION...")
            ret = UnOp(operation=p._slice[0].type, children=[p.parseFactor])
            logger.trace("[ParseFactor] Ended ParseFactor RECURSION...")

        elif commands == ["NOT", "parseFactor"]:
            logger.debug(f"[ParseFactor] Consumed NOT: {p._slice[0]}")
            logger.trace("[ParseFactor] Started ParseFactor RECURSION...")
            ret = UnOp(operation=p._slice[0].type, children=[p.parseFactor])
            logger.trace("[ParseFactor] Ended ParseFactor RECURSION...")

        elif commands == ["LPAREN", "parseOrExpr", "RPAREN"]:
            logger.debug(f"[ParseFactor] Consumed LEFT_PARENTHESIS: {p._slice[0]}")
            logger.trace("[ParseFactor] Started ParseOrExpr RECURSION...")
            ret = p.parseOrExpr
            logger.trace("[ParseFactor] Ended ParseOrExpr RECURSION...")

        elif commands == ["IDENTIFIER"]:
            logger.debug(f"[ParseFactor] Consumed VARIABLE: {p._slice[0]}")
            ret = Variable(varName=p._slice[0].value)

        elif commands == ["IDENTIFIER", "LPAREN", "_9_repeat", "RPAREN"]:
            logger.debug(f"[ParseFactor] Consumed function call '{p._slice[0].value}'")
            logger.trace(f"[ParseFactor] Arguments for '{p._slice[0].value}' {type(p._9_repeat)} {p._9_repeat}")
            ret = FuncCall(value=p._slice[0].value, arguments=p._9_repeat[0][0] if len(p._9_repeat) > 0 else [])

        elif commands == ["READLN", "LPAREN", "RPAREN"]:
            logger.debug(f"[ParseFactor] Consumed READLN: {p._slice[0]}")
            ret = Readln()

        else:
            logger.critical(f"[ParseFactor] Unexpected commands: {commands}")

        return ret
