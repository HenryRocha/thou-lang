from typing import List

from llvmlite.ir.values import Constant
from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.utils.logger import logger


class CompOp(Node):
    def __init__(self, operation: str, children: List[Node]) -> None:
        super().__init__(children=children)
        self.operation = operation

    def evaluate(self, symbolTable: SymbolTable) -> Constant:
        leftSide = self.children[0].evaluate(symbolTable=symbolTable)
        rightSide = self.children[1].evaluate(symbolTable=symbolTable)
        logger.debug(f"[CompOp] Comparing {leftSide} ({self.operation}) {rightSide}")

        result: bool = False
        if self.operation == "CMP_EQ":
            result = self.builder.icmp_signed("==", leftSide, rightSide)
        elif self.operation == "CMP_NEQ":
            result = self.builder.icmp_signed("!=", leftSide, rightSide)
        elif self.operation == "CMP_GT":
            result = self.builder.icmp_signed(">", leftSide, rightSide)
        elif self.operation == "CMP_GEQ":
            result = self.builder.icmp_signed(">=", leftSide, rightSide)
        elif self.operation == "CMP_LT":
            result = self.builder.icmp_signed("<", leftSide, rightSide)
        elif self.operation == "CMP_LEQ":
            result = self.builder.icmp_signed("<=", leftSide, rightSide)
        elif self.operation == "CMP_AND":
            result = self.builder.and_(leftSide, rightSide)
        elif self.operation == "CMP_OR":
            result = self.builder.or_(leftSide, rightSide)
        else:
            logger.critical(f"[CompOp] Invalid comparison type: {self.operation}")

        logger.debug(f"[CompOp] Result: {result}")
        return result

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}): VV({self.operation})\n"

        for child in self.children:
            outStr += child.traverse(int(level + 1))

        return outStr
