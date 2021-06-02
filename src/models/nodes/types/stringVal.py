from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType


class StringVal(Node):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def evaluate(self, symbolTable: SymbolTable) -> str:
        return Value(ValueType.STRING, self.value)
