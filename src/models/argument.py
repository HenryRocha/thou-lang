from llvmlite.ir.types import Type


class FuncArg:
    varType: Type
    varName: str

    def __init__(self, varType: Type, varName: str) -> None:
        self.varType = varType
        self.varName = varName

    def setPtr(self, ptr) -> None:
        self.allocPtr = ptr

    def __str__(self) -> str:
        return f"FAT({self.varType}): FAV({self.varName})"
