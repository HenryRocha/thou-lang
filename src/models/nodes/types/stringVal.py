from llvmlite import ir
from llvmlite.ir.values import Constant
from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.utils.logger import logger


class StringVal(Node):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = str(value)

        if len(self.value) > 128:
            logger.critical(f"[StringVal] Invalid string size {len(self.value)}. All strings must be of size <=128.")
        else:
            self.value = self.value.ljust(128)

    def evaluate(self, symbolTable: SymbolTable) -> Constant:
        return ir.Constant(ir.ArrayType(ir.IntType(8), 128), bytearray(self.value.encode("UTF-8")))

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) NV({self.value})\n"

        return outStr
