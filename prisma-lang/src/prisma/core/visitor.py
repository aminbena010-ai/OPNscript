from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, List, Optional, TypeVar


class Node:
    pass


class Statement(Node):
    pass


class Expression(Node):
    pass


@dataclass(slots=True)
class Program(Node):
    functions: List['Function']
    statements: List[Statement]
    classes: List['Class']
    tokens: List
 

@dataclass(slots=True)
class Class(Node):
    name: str
    superclass: Optional['Identifier']
    body: 'Block'


@dataclass(slots=True)
class This(Expression):
    pass


@dataclass(slots=True)
class Parameter(Node):
    name: str


@dataclass(slots=True)
class Block(Node):
    statements: List[Statement]


@dataclass(slots=True)
class Function(Node):
    name: str
    parameters: List[Parameter]
    body: Block


@dataclass(slots=True)
class LetStatement(Statement):
    name: str
    value: Expression


@dataclass(slots=True)
class SetStatement(Statement):
    name: str
    value: Expression


@dataclass(slots=True)
class ImportStatement(Statement):
    module: str


@dataclass(slots=True)
class ReturnStatement(Statement):
    value: Optional[Expression]


@dataclass(slots=True)
class ExpressionStatement(Statement):
    expression: Expression


@dataclass(slots=True)
class IfStatement(Statement):
    condition: Expression
    consequence: Block
    alternative: Optional[Block]


@dataclass(slots=True)
class TryStatement(Statement):
    try_block: Block
    error_variable: Optional[str]
    catch_block: Block


@dataclass(slots=True)
class ForStatement(Statement):
    target: str
    iterable: Expression
    body: Block


@dataclass(slots=True)
class WhileStatement(Statement):
    condition: Expression
    body: Block


@dataclass(slots=True)
class Identifier(Expression):
    value: str


@dataclass(slots=True)
class Attribute(Expression):
    value: Expression
    attribute: str


@dataclass(slots=True)
class Literal(Expression):
    value: object


@dataclass(slots=True)
class UnaryOperation(Expression):
    operator: str
    operand: Expression


@dataclass(slots=True)
class BinaryOperation(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass(slots=True)
class LambdaExpression(Expression):
    parameters: List[Parameter]
    body: Expression


@dataclass(slots=True)
class CallExpression(Expression):
    callee: Expression
    arguments: List[Expression]


@dataclass(slots=True)
class RangeExpression(Expression):
    start: Expression
    end: Expression


@dataclass(slots=True)
class ListExpression(Expression):
    elements: List[Expression]


@dataclass(slots=True)
class IndexExpression(Expression):
    target: Expression
    index: Expression


T = TypeVar("T")


class Visitor(Generic[T]):
    def visit(self, node: Node) -> T:
        method = getattr(self, f"visit_{node.__class__.__name__}", self.generic_visit)
        return method(node)

    def visit_each(self, nodes: Iterable[Node]) -> List[T]:
        return [self.visit(node) for node in nodes]

    def generic_visit(self, node: Node) -> T:
        raise NotImplementedError(f"No visit_{node.__class__.__name__} method")


class Transformer(Visitor[Node]):
    def visit(self, node: Node) -> Node:
        return super().visit(node)

    def generic_visit(self, node: Node) -> Node:
        return node
