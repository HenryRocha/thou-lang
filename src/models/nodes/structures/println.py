from typing import List

from llvmlite import ir
from llvmlite.ir.types import IntType
from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.utils.logger import logger


class Print(Node):
    def __init__(self, children: List[Node]) -> None:
        super().__init__(children=children)

    def evaluate(self, symbolTable: SymbolTable) -> None:
        value = self.children[0].evaluate(symbolTable=symbolTable)

        if value.type == IntType(1) or value.type == IntType(64):
            fmt_arg = self.builder.bitcast(self.int_fmt, ir.IntType(8).as_pointer())

        elif "x i8" in str(value.type):
            fmt_arg = self.builder.bitcast(self.str_fmt, ir.IntType(8).as_pointer())

        else:
            logger.critical(f"[Print] Type of value is unexpected {value.type}")

        # Call Print Function
        self.builder.call(self.printf, [fmt_arg, value])

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"

        for child in self.children:
            outStr += child.traverse(level=level + 1)

        return outStr
