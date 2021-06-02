from typing import List

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.utils.logger import logger


class Block(Node):
    children: List[Node]

    def __init__(self) -> None:
        self.children = []

    def evaluate(self, symbolTable: SymbolTable) -> None:
        for node in self.children:
            logger.debug(f"[Block] Running evaluate for {type(node)}")
            node.evaluate(symbolTable=symbolTable)

    def addNode(self, node: Node) -> None:
        self.children.append(node)
