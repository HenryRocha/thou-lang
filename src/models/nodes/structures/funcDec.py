from typing import List

from src.models.argument import FuncArg
from src.models.functionTable import functionTable
from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import ValueType


class FuncDec(Node):
    retType = ValueType
    arguments: List[FuncArg]
    statements: List[Node]
    symbolTable = SymbolTable

    def __init__(self, value: str, retType: ValueType) -> None:
        super().__init__()
        self.value = value
        self.retType = retType
        self.arguments = []
        self.statements = []
        self.symbolTable = None

    def evaluate(self) -> None:
        functionTable.setFunc(self.value, self)

    def setArguments(self, args: List[ValueType]) -> None:
        self.arguments = args

    def addArg(self, arg: ValueType) -> None:
        self.arguments.append(arg)

    def setStatements(self, statements: List[Node]) -> None:
        self.statements = statements

    def addStatement(self, statement: Node) -> None:
        self.statements.append(statement)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) NV({self.value})\n"
        outStr += f"{tabs}\tRT({self.retType})\n"

        for arg in self.arguments:
            outStr += f"{tabs}\tARG({arg})\n"

        outStr += f"{tabs}\tSTATEMENTS:\n"
        for statement in self.statements:
            outStr += statement.traverse(level=level + 2)

        return outStr
