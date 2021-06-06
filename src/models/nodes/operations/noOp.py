from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType


class NoOp(Node):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, symbolTable: SymbolTable) -> int:
        pass

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"

        return outStr
