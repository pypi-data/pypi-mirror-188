from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class PrintChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "print-checker"
    priority = -1
    msgs = {
        "W0001": (
            "'print' statement in project code.",
            "no-print-statement",
            "Do not use print statement in project code.",
        )
    }
    options = ()

    def visit_call(self, node: nodes.Call) -> None:
        if isinstance(node.func, nodes.Name) and node.func.name == "print":
            self.add_message("no-print-statement", node=node)


def register(linter):
    print("Registering PrintChecker...")
    checker = PrintChecker(linter)
    linter.register_checker(checker)
    print("...PrintChecker registered")
