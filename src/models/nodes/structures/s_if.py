from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.models.value import Value, ValueType
from src.utils.logger import logger


class If(Node):
    def __init__(self, condition: Node, ifTrue: Node, ifFalse: Node = None) -> None:
        super().__init__(children=[ifTrue, ifFalse])
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        conditionResult: Value = self.condition.evaluate(symbolTable=symbolTable)

        logger.debug(f"[If] Condition result: {conditionResult}")

        if conditionResult.varType == ValueType.STRING:
            logger.critical(f"[If] Condition cannot be a STRING: {conditionResult}")

        if bool(conditionResult.value):
            return self.children[0].evaluate(symbolTable=symbolTable)
        elif self.children[1] != None:
            return self.children[1].evaluate(symbolTable=symbolTable)
