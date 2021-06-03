from typing import List

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType
from src.utils.logger import logger


class CompOp(Node):
    def __init__(self, operation: str, children: List[Node]) -> None:
        super().__init__(children=children)
        self.operation = operation

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        leftSide: Value = self.children[0].evaluate(symbolTable=symbolTable)
        rightSide: Value = self.children[1].evaluate(symbolTable=symbolTable)
        logger.debug(f"[CompOp] Comparing {leftSide} ({self.operation}) {rightSide}")

        if (leftSide.varType in [ValueType.INT, ValueType.BOOL] and rightSide.varType == ValueType.STRING) or (
            leftSide.varType == ValueType.STRING and rightSide.varType in [ValueType.INT, ValueType.BOOL]
        ):
            logger.critical(f"[Consumed] Variable types are different. {leftSide.varType} != {rightSide.varType}")

        result: bool = False
        if self.operation == "CMP_EQ":
            result = leftSide.value == rightSide.value
        elif self.operation == "CMP_GT":
            result = leftSide.value > rightSide.value
        elif self.operation == "CMP_LT":
            result = leftSide.value < rightSide.value
        elif self.operation == "CMP_AND":
            result = bool(leftSide.value) and bool(rightSide.value)
        elif self.operation == "CMP_OR":
            result = bool(leftSide.value) or bool(rightSide.value)
        else:
            logger.critical(f"[CompOp] Invalid comparison type: {self.operation}")

        logger.debug(f"[CompOp] Result: {result}")
        return Value(ValueType.BOOL, result)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}): VV({self.operation})\n"

        for child in self.children:
            outStr += child.traverse(int(level + 1))

        return outStr
