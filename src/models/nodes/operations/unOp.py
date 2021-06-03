from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType


class UnOp(Node):
    def __init__(self, operation: str, children: Node) -> None:
        super().__init__(children=children)
        self.operation = operation

    def evaluate(self, symbolTable: SymbolTable) -> int:
        var: Value = self.children[0].evaluate(symbolTable=symbolTable)

        if self.operation == "PLUS":
            return Value(ValueType.INT, +var.value)
        elif self.operation == "MINUS":
            return Value(ValueType.INT, -var.value)
        elif self.operation == "NOT":
            return Value(ValueType.BOOL, not bool(var.value))

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}): VV({self.operation})\n"

        for child in self.children:
            outStr += child.traverse(int(level + 1))

        return outStr
