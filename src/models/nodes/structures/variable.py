from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable


class Variable(Node):
    def __init__(self, varName: str) -> None:
        super().__init__()
        self.varName = varName

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return symbolTable.getVar(self.varName)
