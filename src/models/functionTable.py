from typing import Dict

from src.utils.logger import logger
from src.models.nodes.node import Node


class FunctionTable:
    table: Dict[str, Node]

    def __init__(self) -> None:
        self.table = {}

    def getFunc(self, func: str) -> Node:
        """
        Gets the Node for the given function name.
        """
        logger.debug(f"[FuncTable] Looking up function '{func}'")

        if func in self.table:
            return self.table[func]
        else:
            logger.critical(f"Unknown function '{func}'.")

    def setFunc(self, func: str, node: Node) -> None:
        """
        Sets the value for the given variable name.
        """
        logger.debug(f"[FuncTable] Setting function '{func}'")

        if not self.declared(func):
            self.table[func] = node
        else:
            logger.critical(f"[FuncTable] Function '{func}' already declared")

    def declared(self, func: str) -> bool:
        """
        Returns 'true' if the variable has already been declared and 'false' if
        it hasn't.
        """
        if func in self.table:
            return True
        else:
            return False


functionTable = FunctionTable()
