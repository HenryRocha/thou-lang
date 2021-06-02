from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable


class While(Node):
    def __init__(self, condition: Node, command: Node) -> None:
        super().__init__()
        self.condition = condition
        self.children = [command]

    def evaluate(self, symbolTable: SymbolTable) -> None:
        while self.condition.evaluate(symbolTable=symbolTable).value:
            self.children[0].evaluate(symbolTable=symbolTable)
