from typing import Dict

from llvmlite.ir.values import Constant
from src.utils.logger import logger


class SymbolTable:
    table: Dict[str, Constant]

    def __init__(self) -> None:
        self.table = {}

    def getVar(self, name: str) -> Constant:
        """
        Gets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] Looking up variable '{name}'")

        if self.declared(name):
            return self.table[name]
        else:
            logger.critical(f"Unknown variable '{name}'.")

    def setVar(self, name: str, value: Constant) -> None:
        """
        Sets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] Setting/updating variable '{name}', as {value.type}, with value '{value}'")

        self.table[name] = value

    def declared(self, name: str) -> bool:
        """
        Returns 'true' if the variable has already been declared and 'false' if
        it hasn't.
        """
        if name in self.table:
            return True
        else:
            return False
