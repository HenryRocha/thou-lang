from typing import List, Union

from src.models.nodes.node import Node
from src.models.nodes.structures.s_return import Return
from src.models.symbolTable import SymbolTable
from src.models.value import Value
from src.utils.logger import logger


class Block(Node):
    children: List[Node]

    def __init__(self) -> None:
        super().__init__(children=[])

    def evaluate(self, symbolTable: SymbolTable) -> None:
        for node in self.children:
            logger.debug(f"[Block] Running evaluate for {type(node)}")
            ret: Union[None, Value] = node.evaluate(symbolTable=symbolTable)

            if type(node) == Return:
                return ret

    def setNodes(self, nodes: List[Node]) -> None:
        self.children = nodes

    def addNode(self, node: Node) -> None:
        self.children.append(node)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"

        for child in self.children:
            outStr += child.traverse(int(level + 1))

        return outStr
