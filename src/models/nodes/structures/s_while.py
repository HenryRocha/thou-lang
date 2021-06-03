from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable


class While(Node):
    def __init__(self, condition: Node, command: Node) -> None:
        super().__init__(children=[command])
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> None:
        while self.condition.evaluate(symbolTable=symbolTable).value:
            self.children[0].evaluate(symbolTable=symbolTable)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"
        outStr += f"{tabs}Condition: {self.condition.traverse(level=level+1)}"

        for child in self.children:
            outStr += child.traverse(level=level + 1)

        return outStr
