from typing import Union

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value
from src.utils.logger import logger


class While(Node):
    def __init__(self, condition: Node, command: Node) -> None:
        super().__init__(children=[command])
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> None:
        while self.condition.evaluate(symbolTable=symbolTable).value:
            ret: Union[None, Value] = self.children[0].evaluate(symbolTable=symbolTable)
            if ret != None:
                return ret

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"
        outStr += self.condition.traverse(level=level + 1)

        for child in self.children:
            outStr += child.traverse(level=level + 1)

        return outStr
