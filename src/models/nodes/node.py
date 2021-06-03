from abc import ABC, abstractmethod
from typing import List


class Node(ABC):
    children: List

    def __init__(self, children: List = []) -> None:
        self.children = children

    @abstractmethod
    def evaluate(self) -> int:
        return 0

    @abstractmethod
    def traverse(self, level: int = 0) -> str:
        return ""

    def __str__(self) -> str:
        return self.traverse(0)
