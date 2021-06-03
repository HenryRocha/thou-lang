from typing import Union

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value


class Return(Node):
    def __init__(self, value: str, child: Node) -> None:
        super().__init__(children=[child])
        self.value = value

    def evaluate(self, symbolTable: SymbolTable) -> Value:
        result: Value = self.children[0].evaluate(symbolTable=symbolTable)
        return result

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"
        outStr += self.children[0].traverse(level=level + 1)

        return outStr
