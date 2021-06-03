import argparse
import pathlib

from src.compiler.parser import ThouParser
from src.compiler.tokenizer import ThouLexer
from src.models.nodes.structures.funcCall import FuncCall
from src.models.symbolTable import SymbolTable
from src.utils.logger import logger


def main() -> None:
    # Argparse, to enalbe the debug flag.
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="sourceFile", type=str, help="source code")
    parser.add_argument("-d", "--debug", action="store_true", help="run in debug mode", default=False)
    parser.add_argument("-v", "--verbosity", action="count", help="verbosity level", default=0, required=False)
    args = parser.parse_args()

    sourceFile = pathlib.Path(args.sourceFile)
    logger.configure(enable=bool(args.debug), verbosity=int(args.verbosity))

    if not sourceFile.exists() or not sourceFile.is_file():
        logger.critical(f"[Main] No file named '{args.sourceFile}'")
    else:
        logger.info("[Main] Reading source file...")
        with open(sourceFile.absolute(), "r") as f:
            sourceCode = f.read()
        logger.info("[Main] Done")

    lexer = ThouLexer()
    tokens = lexer.tokenize(sourceCode)
    parser = ThouParser()

    finalAST = parser.parse(tokens)
    finalAST.addNode(FuncCall(value="main", arguments=[]))
    logger.success(f"[Main] Final AST:\n{finalAST}")

    for node in finalAST.children:
        logger.info(f"[Main] Running evaluate for {type(node)}")

        if type(node) == FuncCall and node.value == "main":
            node.evaluate(symbolTable=SymbolTable())
        else:
            node.evaluate()


if __name__ == "__main__":
    main()
