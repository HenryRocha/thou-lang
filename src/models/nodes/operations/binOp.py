from typing import List

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType
from src.utils.logger import logger


class BinOp(Node):
    def __init__(self, operation: str, children: List[Node]) -> None:
        super().__init__(children=children)
        self.operation = operation

    def evaluate(self, symbolTable: SymbolTable) -> int:
        var1: Value = self.children[0].evaluate(symbolTable=symbolTable)
        var2: Value = self.children[1].evaluate(symbolTable=symbolTable)

        logger.debug(f"[BinOp] {var1} {self.operation} {var2}")
        logger.debug(f"[BinOp] Multiplying {var1.value * var2.value}")

        if (var1.varType in [ValueType.INT, ValueType.BOOL] and var2.varType == ValueType.STRING) or (
            var1.varType == ValueType.STRING and var2.varType in [ValueType.INT, ValueType.BOOL]
        ):
            logger.critical(f"[BinOp] Variable types are different. {var1.varType} != {var2.varType}")

        if self.operation == "PLUS":
            return Value(ValueType.INT, var1.value + var2.value)
        elif self.operation == "MINUS":
            return Value(ValueType.INT, var1.value - var2.value)
        elif self.operation == "MULTIPLY":
            return Value(ValueType.INT, var1.value * var2.value)
        elif self.operation == "DIVIDE":
            return Value(ValueType.INT, var1.value // var2.value)
        else:
            logger.critical(f"[BinOp] Unknown operation: {self.operation}")
