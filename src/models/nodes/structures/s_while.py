from src.models.nodes.node import Node
from src.models.symbolTable import SymbolTable


class While(Node):
    def __init__(self, condition: Node, command: Node) -> None:
        super().__init__(children=[command])
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> None:
        # Get the condition result.
        conditionResult = self.condition.evaluate(symbolTable=symbolTable)

        # Create the markers, equivalent to labels in ASM.
        while_entry = self.builder.append_basic_block(name=f"while_{self.nid}")
        while_exit = self.builder.append_basic_block(name=f"while_{self.nid}_exit")

        # Create a contidional branch, based on the condition result.
        # If the result was true, go back to while_entry, if not, go
        # to while_exit.
        self.builder.cbranch(conditionResult, while_entry, while_exit)
        self.builder.position_at_start(while_entry)

        # Run block inside while.
        self.children[0].evaluate(symbolTable=symbolTable)

        # Evaluate the condition again.
        conditionResult = self.condition.evaluate(symbolTable=symbolTable)

        # Create a contidional branch, based on the condition result.
        # If the result was true, go back to while_entry, if not, go
        # to while_exit.
        self.builder.cbranch(conditionResult, while_entry, while_exit)
        self.builder.position_at_start(while_exit)

    def traverse(self, level: int = 0) -> str:
        tabs: str = "\t" * int(level) if int(level) > 0 else ""

        outStr: str = f"{tabs}NT({type(self)})\n"
        outStr += self.condition.traverse(level=level + 1)

        for child in self.children:
            outStr += child.traverse(level=level + 1)

        return outStr
