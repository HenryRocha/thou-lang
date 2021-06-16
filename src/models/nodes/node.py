import uuid
from abc import ABC, abstractmethod
from typing import List

from llvmlite.ir.builder import IRBuilder
from llvmlite.ir.module import Module
from llvmlite.ir.values import Function, GlobalVariable


class Node(ABC):
    children: List
    nid: int
    module: Module
    builder: IRBuilder
    printf: Function
    int_fmt: GlobalVariable
    str_fmt: GlobalVariable

    def __init__(self, children: List = []) -> None:
        self.children = children
        self.nid = uuid.uuid4().hex

    @abstractmethod
    def evaluate(self) -> int:
        return 0

    @abstractmethod
    def traverse(self, level: int = 0) -> str:
        return ""

    def __str__(self) -> str:
        return self.traverse(0)
