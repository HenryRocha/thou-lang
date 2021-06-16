from typing import List

from llvmlite import ir
from llvmlite.ir.types import Type
from src.models.argument import FuncArg
from src.models.functionTable import functionTable
from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.utils.logger import logger


class FuncDec(Node):
    retType = Type
    arguments: List[FuncArg]
    statements: List[Node]
    symbolTable = SymbolTable

    def __init__(self, value: str, retType: Type) -> None:
        super().__init__()
        self.value = value
        self.retType = retType
        self.arguments = []
        self.statements = None
        self.symbolTable = None
        self.ptr = None

    def evaluate(self) -> None:
        if self.value == "main":
            # Add the function to the function table.
            functionTable.setFunc(self.value, self)

        else:
            # Define all the functions types, the return type and all the
            # types for the arguments.
            funcTypes = ir.FunctionType(self.retType, [arg.varType for arg in self.arguments])

            # Create the funciton, with it's types and the given name.
            func = ir.Function(self.module, funcTypes, name=self.value)
            self.ptr = func

            # Create the entry point for this function. Works as a label is ASM.
            func_entry = func.append_basic_block(f"function_{self.value}_entry")

            # Store the current position, so we can restore after declaring the function.
            previous_position = self.builder
            Node.builder = ir.IRBuilder(func_entry)

            # Create a symbol table for this function.
            self.symbolTable = SymbolTable()

            # For every given argument, allocate a space in memory for it's
            # corresponding variable, store it's pointer in the function's
            # argument list.
            for idx, arg in enumerate(self.arguments):
                argAllocPtr = self.builder.alloca(arg.varType, name=arg.varName)
                self.builder.store(func.args[idx], argAllocPtr)
                self.symbolTable.setVar(arg.varName, argAllocPtr)
                arg.setPtr(argAllocPtr)

            # Add the function to the function table.
            functionTable.setFunc(self.value, self)

            # Evalute the statements for this function.
            logger.debug("[FuncDec] Evaluating function's block of statements.")
            self.statements.evaluate(symbolTable=self.symbolTable)
            logger.debug("[FuncDec] Done evaluating function's block of statements.")

            # Restore the builder's position.
            Node.builder = previous_position

    def setArguments(self, args: List[Type]) -> None:
        self.arguments = args

    def addArg(self, arg: Type) -> None:
        self.arguments.append(arg)

    def setStatements(self, statements: Node) -> None:
        self.statements = statements

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)}) NV({self.value})\n"
        outStr += f"{tabs}\tRT({self.retType})\n"

        for arg in self.arguments:
            outStr += f"{tabs}\tARG({arg})\n"

        outStr += f"{tabs}\tSTATEMENTS:\n"
        outStr += self.statements.traverse(level=level + 2)

        return outStr
