from typing import Dict, Union

from src.utils.logger import logger
from src.models.value import Value, ValueType


class SymbolTable:
    table: Dict[str, Dict[str, Union[int, bool, str]]]

    def __init__(self) -> None:
        self.table = {}

    def getVar(self, name: str) -> Union[ValueType, Union[int, bool, str]]:
        """
        Gets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] Looking up variable '{name}'")

        if name in self.table:
            return Value(self.table[name]["type"], self.table[name]["value"])
        else:
            logger.critical(f"Unknown variable '{name}'.")

    def setVar(self, name: str, varType: ValueType, value: Union[int, bool, str]) -> None:
        """
        Sets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] Setting/updating variable '{name}', as {varType}, with value '{value}'")

        self.table[name] = {"type": varType, "value": value}

    def declared(self, name: str) -> bool:
        """
        Returns 'true' if the variable has already been declared and 'false' if
        it hasn't.
        """
        if name in self.table:
            return True
        else:
            return False
