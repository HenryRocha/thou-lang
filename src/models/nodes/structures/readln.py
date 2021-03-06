from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType
from src.utils.logger import logger


class Readln(Node):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, symbolTable: SymbolTable) -> int:
        inputStr: str = str(input())

        if inputStr.isnumeric():
            return Value(ValueType.INT, int(inputStr))
        else:
            logger.critical(f"[Readln] Input must be an integer: {inputStr}")

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"

        return outStr
