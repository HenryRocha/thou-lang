from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType


class NoOp(Node):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return Value(ValueType.INT, 0)
