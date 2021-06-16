from typing import List, Union

from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import ValueType
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

            # Evaluate the variable.
            var = self.children[0].evaluate(symbolTable=symbolTable)

            # Allocate a space in memory for this variable, according to it's type.
            irAllocPtr = self.builder.alloca(var.type, name=self.varName)

        else:
            if self.varType != None:
                logger.critical(f"[Identifier] Variable '{self.varName}' already declared. Type: {self.varType}")

            # Evaluate the new value for the variable.
            var = self.children[0].evaluate(symbolTable=symbolTable)

            # Retrieve the pointer to this variable.
            irAllocPtr = symbolTable.getVar(name=self.varName)

        # Store the variable in memory, with the new value.
        self.builder.store(var, irAllocPtr)
        logger.debug(f"[Identifier] Setting variable ({var.type}) {self.varName} = {var}")

        # Set the variable on the symbol table.
        symbolTable.setVar(name=self.varName, value=irAllocPtr)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) VT({self.varType}) VV({self.varName})\n"

        for child in self.children:
            outStr += child.traverse(level=level + 1)

        return outStr
