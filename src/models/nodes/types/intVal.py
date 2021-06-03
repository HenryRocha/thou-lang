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

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) NV({self.value})\n"

        return outStr
