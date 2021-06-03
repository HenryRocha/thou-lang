from typing import List, Union

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType
from src.utils.logger import logger


class Identifier(Node):
    def __init__(self, varType: ValueType, varName: Union[int, bool, str], children: List[Node]) -> None:
        super().__init__(children=children)
        self.varName = varName
        self.varType = varType

    def evaluate(self, symbolTable: SymbolTable) -> None:
        if not symbolTable.declared(self.varName):
            if self.varType == None:
                logger.critical(f"[Identifier] Missing type on declaration for variable '{self.varName}'")

            var: Value = self.children[0].evaluate(symbolTable=symbolTable)

            logger.debug(f"[Identifier] Setting variable ({self.varType}) {self.varName} = {var.value}")
            symbolTable.setVar(name=self.varName, varType=self.varType, value=var.value)

        else:
            if self.varType != None:
                logger.critical(f"[Identifier] Variable '{self.varName}' already declared. Type: {self.varType}")

            var: Value = self.children[0].evaluate(symbolTable=symbolTable)
            existingVar: Value = symbolTable.getVar(name=self.varName)

            if (existingVar.varType in [ValueType.INT, ValueType.BOOL] and var.varType == ValueType.STRING) or (
                existingVar.varType == ValueType.STRING and var.varType in [ValueType.INT, ValueType.BOOL]
            ):
                logger.critical(
                    f"[Identifier] Variable reassign with mismatching types. '{self.varName}' has type {existingVar.varType} but was reassigned to {var.varType}"
                )

            logger.debug(f"[Identifier] Setting variable ({var.varType}) {self.varName} = {var.value}")

            if existingVar.varType == ValueType.INT:
                symbolTable.setVar(name=self.varName, varType=existingVar.varType, value=int(var.value))
            elif existingVar.varType == ValueType.BOOL:
                symbolTable.setVar(name=self.varName, varType=existingVar.varType, value=bool(var.value))
            elif existingVar.varType == ValueType.STRING:
                symbolTable.setVar(name=self.varName, varType=existingVar.varType, value=str(var.value))

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) VT({self.varType}) VV({self.varName})\n"

        for child in self.children:
            outStr += child.traverse(level=level + 1)

        return outStr
