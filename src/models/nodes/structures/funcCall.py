from typing import List

from src.models.argument import FuncArg
from src.models.functionTable import FunctionTable
from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import ValueType
from src.utils.logger import logger


class FuncCall(Node):
    arguments: List[Node]

    def __init__(self, value: str, arguments: List[Node]) -> None:
        super().__init__()
        self.value = value
        self.arguments = arguments

    def evaluate(self, symbolTable: SymbolTable) -> None:
        logger.debug(f"[FuncCall] Running evaluate for function '{self.value.value}'")

    def addArg(self, node: Node) -> None:
        self.arguments.append(node)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) NV({self.value})\n"

        for child in self.arguments:
            outStr += child.traverse(int(level + 1))

        return outStr
