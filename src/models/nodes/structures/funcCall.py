from typing import List

from src.models.functionTable import functionTable
from src.models.nodes.node import Node
from src.models.nodes.structures.funcDec import FuncDec
from src.models.symbolTable import SymbolTable
from src.utils.logger import logger


class FuncCall(Node):
    arguments: List[Node]

    def __init__(self, value: str, arguments: List[Node]) -> None:
        super().__init__()
        self.value = value
        self.arguments = arguments

    def evaluate(self, symbolTable: SymbolTable) -> None:
        logger.debug(f"[FuncCall] Executing function '{self.value}'")

        # Retrieve the function from the function table.
        function: FuncDec = functionTable.getFunc(func=self.value)

        # Raise an error if the function was not declared.
        if function == None:
            logger.critical("[FuncCall] Function '{self.value}' not declared")

        # Make a call to the declared functions, passing the function's pointer
        # and a list with the result for every given argument.
        return self.builder.call(function.ptr, [arg.evaluate(symbolTable=function.symbolTable) for arg in self.arguments])

    def addArg(self, node: Node) -> None:
        self.arguments.append(node)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) NV({self.value})\n"

        for child in self.arguments:
            outStr += child.traverse(int(level + 1))

        return outStr
