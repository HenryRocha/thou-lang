from typing import List

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable


class Print(Node):
    def __init__(self, children: List[Node]) -> None:
        super().__init__(children=children)

    def evaluate(self, symbolTable: SymbolTable) -> None:
        print(self.children[0].evaluate(symbolTable=symbolTable).value)
