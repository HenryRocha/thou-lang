from typing import List, Union

from src.models.argument import FuncArg
from src.models.functionTable import functionTable
from src.models.nodes.node import Node
from src.models.nodes.operations.noOp import NoOp
from src.models.nodes.structures.funcDec import FuncDec
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType
from src.utils.logger import logger


class FuncCall(Node):
    arguments: List[Node]

    def __init__(self, value: str, arguments: List[Node]) -> None:
        super().__init__()
        self.value = value
        self.arguments = arguments

    def evaluate(self, symbolTable: SymbolTable) -> None:
        logger.debug(f"[FuncCall] Executing function '{self.value}'")

        # Retrieve the function from the function table.
        function: FuncDec = functionTable.getFunc(func=self.value)

        # Create the function's symbol table, so it has it's own variables.
        function.symbolTable = SymbolTable()

        # Check if the number of arguments is correct.
        if len(self.arguments) == len(function.arguments):
            # Go through every given argument, check if the type matches with the one declared by the function
            # and then add it's evaluate result to the function's symbol table.
            for i in range(len(self.arguments)):
                funcArg: FuncArg = function.arguments[i]
                givenArg: Value = self.arguments[i].evaluate(symbolTable=symbolTable)

                if givenArg.varType == funcArg.varType:
                    function.symbolTable.setVar(name=funcArg.varName, varType=funcArg.varType, value=givenArg.value)
                else:
                    logger.critical(f"[FuncCall] Parameter type mismatch, expected {funcArg} got {givenArg}")
        else:
            logger.critical(f"[FuncCall] Number of parameters mismatch, function has {len(function.arguments)} parameters but {len(self.arguments)} were given")

        # For every statement in the function, run evaluate for it.
        for statement in function.statements:
            logger.debug(f"[FuncCall] Running statement for function '{self.value}': {type(statement)}")
            ret: Union[None, Value] = statement.evaluate(symbolTable=function.symbolTable)
            logger.success(f"[FuncCall] Statement {type(statement)} for function '{self.value}' returned {ret}")

            if ret != None:
                # Check if the returned type matches the one declared in the function.
                if ret.varType == function.retType:
                    return ret
                else:
                    logger.critical(f"[FuncCall] Function return type mismatch, declared as {function.retType} but returned {ret.varType}")

    def addArg(self, node: Node) -> None:
        self.arguments.append(node)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) NV({self.value})\n"

        for child in self.arguments:
            outStr += child.traverse(int(level + 1))

        return outStr
