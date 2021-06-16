from llvmlite import ir
from llvmlite.ir.values import Constant
from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable


class BoolVal(Node):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def evaluate(self, symbolTable: SymbolTable) -> Constant:
        return ir.Constant(ir.IntType(1), int(self.value))

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) NV({self.value})\n"

        return outStr
