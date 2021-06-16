from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable
from src.utils.logger import logger


class If(Node):
    def __init__(self, condition: Node, ifTrue: Node, ifFalse: Node = None) -> None:
        super().__init__(children=[ifTrue, ifFalse])
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        conditionResult = self.condition.evaluate(symbolTable=symbolTable)
        logger.debug(f"[If] Condition result: {conditionResult}")

        ret = None
        with self.builder.if_else(conditionResult) as (then, otherwise):
            with then:
                ret = self.children[0].evaluate(symbolTable=symbolTable)

            with otherwise:
                if self.children[1] != None:
                    ret = self.children[1].evaluate(symbolTable=symbolTable)

        return ret

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"
        outStr += f"{self.condition.traverse(level=level+1)}"

        for child in self.children:
            outStr += child.traverse(level=level + 1)

        return outStr
