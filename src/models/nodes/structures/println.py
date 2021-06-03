from typing import List

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable


class Print(Node):
    def __init__(self, children: List[Node]) -> None:
        super().__init__(children=children)

    def evaluate(self, symbolTable: SymbolTable) -> None:
        print(self.children[0].evaluate(symbolTable=symbolTable).value)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"

        for child in self.children:
            outStr += child.traverse(level=level + 1)

        return outStr
