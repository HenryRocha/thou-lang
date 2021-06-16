from typing import List

from llvmlite.ir.values import Constant
from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.utils.logger import logger


class BinOp(Node):
    def __init__(self, operation: str, children: List[Node]) -> None:
        super().__init__(children=children)
        self.operation = operation

    def evaluate(self, symbolTable: SymbolTable) -> Constant:
        var1 = self.children[0].evaluate(symbolTable=symbolTable)
        var2 = self.children[1].evaluate(symbolTable=symbolTable)

        logger.trace(f"[BinOp] {var1} {self.operation} {var2}")

        if self.operation == "PLUS":
            return self.builder.add(var1, var2)
        elif self.operation == "MINUS":
            return self.builder.sub(var1, var2)
        elif self.operation == "MULTIPLY":
            return self.builder.mul(var1, var2)
        elif self.operation == "DIVIDE":
            return self.builder.sdiv(var1, var2)
        else:
            logger.critical(f"[BinOp] Unknown operation: {self.operation}")

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}): VV({self.operation})\n"

        for child in self.children:
            outStr += child.traverse(int(level + 1))

        return outStr
