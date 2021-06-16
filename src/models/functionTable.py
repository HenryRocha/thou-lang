from typing import Dict

from src.models.nodes.node import Node
from src.utils.logger import logger


class FunctionTable:
    table: Dict[str, Node]

    def __init__(self) -> None:
        self.table = {}

    def getFunc(self, func: str) -> Node:
        """
        Gets the Node for the given function name.
        """
        logger.debug(f"[FuncTable] Looking up function '{func}'")

        if self.declared(func):
            return self.table[func]
        else:
            logger.critical(f"[FuncTable] Unknown function '{func}'.")

    def setFunc(self, func: str, node: Node) -> None:
        """
        Sets the value for the given variable name.
        """
        logger.debug(f"[FuncTable] Setting function '{func}'")

        if not self.declared(func):
            self.table[func] = node
        else:
            logger.critical(f"[FuncTable] Function '{func}' already declared")

    def delFunc(self, func: str) -> None:
        """
        Deletes the given function from the table.
        """
        logger.debug(f"[FuncTable] Deleting function '{func}'")

        if self.declared(func):
            del self.table[func]
        else:
            logger.critical(f"[FuncTable] Cannot delete function '{func}', it was not declared")

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
