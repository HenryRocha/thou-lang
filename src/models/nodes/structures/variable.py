from llvmlite.ir.values import Constant
from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable


class Variable(Node):
    def __init__(self, varName: str) -> None:
        super().__init__()
        self.varName = varName

    def evaluate(self, symbolTable: SymbolTable) -> Constant:
        # Retrive the pointer to the variable.
        irAllocPtr = symbolTable.getVar(self.varName)

        # Load the value pointed by the pointer and store it in the variable with
        # the given name.
        return self.builder.load(irAllocPtr, name=self.varName)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) VN({self.varName})\n"

        return outStr
