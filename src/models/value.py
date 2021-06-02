from enum import Enum


class ValueType(Enum):
    INT = 1
    BOOL = 2
    STRING = 3


class Value:
    varType: ValueType
    value: str

    def __init__(self, varType: ValueType, value: str) -> None:
        self.varType = varType
        self.value = value

    def __str__(self) -> str:
        return f"VT({self.varType}): VV({self.value})"
