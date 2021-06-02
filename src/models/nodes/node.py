from abc import ABC, abstractmethod
from typing import List


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
