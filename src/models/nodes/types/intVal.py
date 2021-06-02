from typing import Union

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType


class IntVal(Node):
    def __init__(self, value: Union[int, bool, str]) -> None:
        super().__init__()
        self.value = value

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return Value(ValueType.INT, int(self.value))
