from abc import ABC, abstractmethod
from typing import List, Union

from logger import logger
from symbolTable import SymbolTable
from varTypes import Var, VarTypes


class Node(ABC):
    children: List

    def __init__(self, children: List = []) -> None:
        self.children = children

    @abstractmethod
    def evaluate(self) -> int:
        return 0

    def traverse(self, n, level=0):
        if n == None:
            return ""

        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        if hasattr(n, "varName"):
            outStr: str = f"{tabs}NT({type(n)}): VN({n.varName})\n"
        elif hasattr(n, "value"):
            outStr: str = f"{tabs}NT({type(n)}): VV({n.value})\n"
        elif hasattr(n, "operation"):
            outStr: str = f"{tabs}NT({type(n)}): VV({n.operation})\n"
        else:
            outStr: str = f"{tabs}NT({type(n)})\n"

        if hasattr(n, "condition"):
            outStr += self.traverse(n.condition, int(level + 1))

        if hasattr(n, "children"):
            for child in n.children:
                outStr += self.traverse(child, int(level + 1))
        else:
            return f"{tabs}NT({type(n)})\n"

        return outStr

    def __str__(self) -> str:
        return self.traverse(self, 0)


class BinOp(Node):
    def __init__(self, operation: str, children: List[Node]) -> None:
        super().__init__(children=children)
        self.operation = operation

    def evaluate(self, symbolTable: SymbolTable) -> int:
        var1: Var = self.children[0].evaluate(symbolTable=symbolTable)
        var2: Var = self.children[1].evaluate(symbolTable=symbolTable)

        logger.debug(f"[BinOp] {var1} {self.operation} {var2}")
        logger.debug(f"[BinOp] Multiplying {var1.value * var2.value}")

        if (var1.varType in [VarTypes.INT, VarTypes.BOOL] and var2.varType == VarTypes.STRING) or (
            var1.varType == VarTypes.STRING and var2.varType in [VarTypes.INT, VarTypes.BOOL]
        ):
            logger.critical(f"[BinOp] Variable types are different. {var1.varType} != {var2.varType}")

        if self.operation == "PLUS":
            return Var(VarTypes.INT, var1.value + var2.value)
        elif self.operation == "MINUS":
            return Var(VarTypes.INT, var1.value - var2.value)
        elif self.operation == "MULTIPLY":
            return Var(VarTypes.INT, var1.value * var2.value)
        elif self.operation == "DIVIDE":
            return Var(VarTypes.INT, var1.value // var2.value)
        else:
            logger.critical(f"[BinOp] Unknown operation: {self.operation}")


class UnOp(Node):
    def __init__(self, operation: str, children: Node) -> None:
        super().__init__(children=children)
        self.operation = operation

    def evaluate(self, symbolTable: SymbolTable) -> int:
        var: Var = self.children[0].evaluate(symbolTable=symbolTable)

        if self.operation == "PLUS":
            return Var(VarTypes.INT, +var.value)
        elif self.operation == "MINUS":
            return Var(VarTypes.INT, -var.value)
        elif self.operation == "NOT":
            return Var(VarTypes.BOOL, not bool(var.value))


class NoOp(Node):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return Var(VarTypes.INT, 0)


class IntVal(Node):
    def __init__(self, value: Union[int, bool, str]) -> None:
        super().__init__()
        self.value = value

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return Var(VarTypes.INT, int(self.value))


class Print(Node):
    def __init__(self, children: List[Node]) -> None:
        super().__init__(children=children)

    def evaluate(self, symbolTable: SymbolTable) -> None:
        print(self.children[0].evaluate(symbolTable=symbolTable).value)


class Identifier(Node):
    def __init__(self, varType: VarTypes, varName: Union[int, bool, str], children: List[Node]) -> None:
        super().__init__()
        self.varName = varName
        self.varType = varType
        self.children = children

    def evaluate(self, symbolTable: SymbolTable) -> None:
        if not symbolTable.declared(self.varName):
            if self.varType == None:
                logger.critical(f"[Identifier] Missing type on declaration for variable '{self.varName}'")

            var: Var = self.children[0].evaluate(symbolTable=symbolTable)

            logger.debug(f"[Identifier] Setting variable ({self.varType}) {self.varName} = {var.value}")
            symbolTable.setVar(name=self.varName, varType=self.varType, value=var.value)

        else:
            if self.varType != None:
                logger.critical(f"[Identifier] Variable '{self.varName}' already declared. Type: {self.varType}")

            var: Var = self.children[0].evaluate(symbolTable=symbolTable)
            existingVar: Var = symbolTable.getVar(name=self.varName)

            if (existingVar.varType in [VarTypes.INT, VarTypes.BOOL] and var.varType == VarTypes.STRING) or (
                existingVar.varType == VarTypes.STRING and var.varType in [VarTypes.INT, VarTypes.BOOL]
            ):
                logger.critical(
                    f"[Identifier] Variable reassign with mismatching types. '{self.varName}' has type {existingVar.varType} but was reassigned to {var.varType}"
                )

            logger.debug(f"[Identifier] Setting variable ({var.varType}) {self.varName} = {var.value}")

            if existingVar.varType == VarTypes.INT:
                symbolTable.setVar(name=self.varName, varType=existingVar.varType, value=int(var.value))
            elif existingVar.varType == VarTypes.BOOL:
                symbolTable.setVar(name=self.varName, varType=existingVar.varType, value=bool(var.value))
            elif existingVar.varType == VarTypes.STRING:
                symbolTable.setVar(name=self.varName, varType=existingVar.varType, value=str(var.value))


class Variable(Node):
    def __init__(self, varName: str) -> None:
        super().__init__()
        self.varName = varName

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return symbolTable.getVar(self.varName)


class Readln(Node):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, symbolTable: SymbolTable) -> int:
        inputStr: str = str(input())

        if inputStr.isnumeric():
            return Var(VarTypes.INT, int(inputStr))
        else:
            logger.critical(f"[Readln] Input must be an integer: {inputStr}")


class Comparison(Node):
    def __init__(self, operation: str, children: List[Node]) -> None:
        super().__init__(children=children)
        self.operation = operation

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        leftSide: Var = self.children[0].evaluate(symbolTable=symbolTable)
        rightSide: Var = self.children[1].evaluate(symbolTable=symbolTable)
        logger.debug(f"[Comparison] Comparing {leftSide} ({self.operation}) {rightSide}")

        if (leftSide.varType in [VarTypes.INT, VarTypes.BOOL] and rightSide.varType == VarTypes.STRING) or (
            leftSide.varType == VarTypes.STRING and rightSide.varType in [VarTypes.INT, VarTypes.BOOL]
        ):
            logger.critical(f"[BinOp] Variable types are different. {leftSide.varType} != {rightSide.varType}")

        result: bool = False
        if self.operation == "CMP_EQ":
            result = leftSide.value == rightSide.value
        elif self.operation == "CMP_GT":
            result = leftSide.value > rightSide.value
        elif self.operation == "CMP_LT":
            result = leftSide.value < rightSide.value
        elif self.operation == "CMP_AND":
            result = bool(leftSide.value) and bool(rightSide.value)
        elif self.operation == "CMP_OR":
            result = bool(leftSide.value) or bool(rightSide.value)
        else:
            logger.critical(f"[Comparison] Invalid comparison type: {self.operation}")

        logger.debug(f"[Comparison] Result: {result}")
        return Var(VarTypes.BOOL, result)


class Block(Node):
    children: List[Node]

    def __init__(self) -> None:
        self.children = []

    def evaluate(self, symbolTable: SymbolTable) -> None:
        for node in self.children:
            logger.debug(f"[Block] Running evaluate for {type(node)}")
            node.evaluate(symbolTable=symbolTable)

    def addNode(self, node: Node) -> None:
        self.children.append(node)


class If(Node):
    def __init__(self, condition: Node, ifTrue: Node, ifFalse: Node = None) -> None:
        super().__init__(children=[ifTrue, ifFalse])
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        conditionResult: Var = self.condition.evaluate(symbolTable=symbolTable)

        logger.debug(f"[If] Condition result: {conditionResult}")

        if conditionResult.varType == VarTypes.STRING:
            logger.critical(f"[If] Condition cannot be a STRING: {conditionResult}")

        if bool(conditionResult.value):
            return self.children[0].evaluate(symbolTable=symbolTable)
        elif self.children[1] != None:
            return self.children[1].evaluate(symbolTable=symbolTable)


class While(Node):
    def __init__(self, condition: Node, command: Node) -> None:
        super().__init__()
        self.condition = condition
        self.children = [command]

    def evaluate(self, symbolTable: SymbolTable) -> None:
        while self.condition.evaluate(symbolTable=symbolTable).value:
            self.children[0].evaluate(symbolTable=symbolTable)


class BoolVal(Node):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        if self.value:
            return Var(VarTypes.BOOL, True)
        else:
            return Var(VarTypes.BOOL, False)


class StringVal(Node):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def evaluate(self, symbolTable: SymbolTable) -> str:
        return Var(VarTypes.STRING, self.value)
