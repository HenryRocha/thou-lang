from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType


class BoolVal(Node):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        if self.value:
            return Value(ValueType.BOOL, True)
        else:
            return Value(ValueType.BOOL, False)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) NV({self.value})\n"

        return outStr
