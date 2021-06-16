from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable


class UnOp(Node):
    def __init__(self, operation: str, children: Node) -> None:
        super().__init__(children=children)
        self.operation = operation

    def evaluate(self, symbolTable: SymbolTable) -> int:
        var = self.children[0].evaluate(symbolTable=symbolTable)

        if self.operation == "PLUS":
            return var
        elif self.operation == "MINUS":
            return self.builder.neg(var)
        elif self.operation == "NOT":
            return self.builder.not_(var)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}): VV({self.operation})\n"

        for child in self.children:
            outStr += child.traverse(int(level + 1))

        return outStr
