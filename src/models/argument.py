from src.models.value import ValueType


class FuncArg:
    varType: ValueType
    varName: str

    def __init__(self, varType: ValueType, varName: str) -> None:
        self.varType = varType
        self.varName = varName

    def __str__(self) -> str:
        return f"FAT({self.varType}): FAV({self.varName})"
