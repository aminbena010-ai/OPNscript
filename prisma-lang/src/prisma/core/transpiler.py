from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Any
from pathlib import Path

import textwrap

from .package_loader import PackageLoader
from .visitor import (
    Program,
    Class,
    This,
    Function,
    Parameter,
    Block,
    Statement,
    LetStatement,
    SetStatement,
    ImportStatement,
    ReturnStatement,
    ExpressionStatement,
    IfStatement,
    TryStatement,
    ForStatement,
    WhileStatement,
    Expression,
    Identifier,
    Attribute,
    Literal,
    UnaryOperation,
    BinaryOperation,
    LambdaExpression,
    CallExpression,
    RangeExpression,
    ListExpression,
    IndexExpression,
)
from prisma.config import CALL_ALIASES


@dataclass
class ForStatement(Statement):
    target: str
    iterable: Expression
    body: Block


@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: Block


class TranspilerError(Exception):
    def __init__(self, message: str, token: Token | None = None):
        if token:
            super().__init__(f"{message} at line {token.line}, column {token.column}")
        else:
            super().__init__(message)


@dataclass(slots=True)
class Token:
    kind: str
    value: str
    line: int
    column: int


KEYWORDS = {
    "func": "FUNC",
    "main": "MAIN",
    "let": "LET",
    "return": "RETURN",
    "if": "IF",
    "else": "ELSE",
    "for": "FOR",
    "try": "TRY",
    "catch": "CATCH",
    "import": "IMPORT",
    "while": "WHILE",
    "in": "IN",
    "true": "TRUE",
    "false": "FALSE",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "class": "CLASS",
    "this": "THIS",
    "extends": "EXTENDS",
}


SYMBOLS = {
    "{": "LBRACE",
    "}": "RBRACE",
    "(": "LPAREN",
    ")": "RPAREN",
    "[": "LBRACKET",
    "]": "RBRACKET",
    ";": "SEMICOLON",
    ",": "COMMA",
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "<": "LT",
    ">": "GT",
    "=": "EQUAL",
    "!": "BANG",
    ".": "DOT",
}


MULTI_SYMBOLS = {
    "==": "EQ",
    "!=": "NEQ",
    "<=": "LTE",
    ">=": "GTE",
    "..": "RANGE",
}


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.length = len(source)
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while not self._is_at_end():
            char = self._peek()
            if char in " \t\r\n":
                self._consume_whitespace()
                continue
            if char == "#" or (char == "/" and self._peek_next() == "/"):
                self._consume_comment()
                continue
            token = self._read_token()
            tokens.append(token)
        tokens.append(Token("EOF", "", self.line, self.column))
        return tokens

    def _read_token(self) -> Token:
        # Manejo de comentarios de bloque /* ... */
        if self._peek() == '/' and self._peek_next() == '*':
            self._consume_block_comment()
            return self._read_token() # Vuelve a leer después del comentario
        line, column = self.line, self.column
        char = self._advance()
        pair = char + (self._peek() if not self._is_at_end() else "")
        if pair in MULTI_SYMBOLS:
            self._advance()
            return Token(MULTI_SYMBOLS[pair], pair, line, column)
        if char in SYMBOLS:
            return Token(SYMBOLS[char], char, line, column)
        if char.isalpha() or char == "_":
            return self._identifier(char, line, column)
        if char.isdigit():
            return self._number(char, line, column)
        if char == '"':
            return self._string(line, column)
        raise TranspilerError(f"Unexpected character '{char}' at line {line}, column {column}")

    def _consume_whitespace(self) -> None:
        while not self._is_at_end() and self._peek() in " \t\r\n":
            char = self._advance()
            if char == "\n":
                self.line += 1
                self.column = 1

    def _consume_comment(self) -> None:
        while not self._is_at_end() and self._peek() != "\n":
            self._advance()
        if not self._is_at_end():
            self._advance()
            self.line += 1
            self.column = 1

    def _consume_block_comment(self) -> None:
        self._advance()  # Consume /
        self._advance()  # Consume *
        while not self._is_at_end() and not (self._peek() == '*' and self._peek_next() == '/'):
            if self._peek() == '\n':
                self.line += 1
                self.column = 1
            self._advance()
        self._advance()  # Consume *
        self._advance()  # Consume /

    def _identifier(self, initial: str, line: int, column: int) -> Token:
        value = [initial]
        while not self._is_at_end() and (self._peek().isalnum() or self._peek() in {"_"}):
            value.append(self._advance())
        text = "".join(value)
        kind = KEYWORDS.get(text, "IDENT")
        return Token(kind, text, line, column)

    def _number(self, initial: str, line: int, column: int) -> Token:
        value = [initial]
        has_decimal = False
        while not self._is_at_end():
            char = self._peek()
            if char == "." and not has_decimal and self._peek_next() != ".":
                has_decimal = True
                value.append(self._advance())
                continue
            if char.isdigit():
                value.append(self._advance())
                continue
            break
        return Token("NUMBER", "".join(value), line, column)

    def _string(self, line: int, column: int) -> Token:
        value: List[str] = []
        while not self._is_at_end():
            char = self._advance()
            if char == '"':
                return Token("STRING", "".join(value), line, column)
            if char == "\\":
                escaped = self._advance()
                value.append(self._escape(escaped))
            else:
                value.append(char)
        raise TranspilerError(f"Unterminated string at line {line}, column {column}")

    def _escape(self, char: str) -> str:
        escapes = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
        if char not in escapes:
            raise TranspilerError(f"Unsupported escape sequence '\\{char}' at line {self.line}, column {self.column}")
        return escapes[char]

    def _peek(self) -> str:
        return self.source[self.index]

    def _peek_next(self) -> str:
        if self.index + 1 >= self.length:
            return "\0"
        return self.source[self.index + 1]

    def _advance(self) -> str:
        char = self.source[self.index]
        self.index += 1
        self.column += 1
        return char

    def _is_at_end(self) -> bool:
        return self.index >= self.length


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        # In OPN, top-level statements are only allowed inside func/main blocks.
        # We can relax this for a REPL, but for now, we'll parse functions.
        # A future improvement could be to parse loose statements for the REPL.
        functions: List[Function] = []
        statements: List = []  # For REPL mode in the future
        classes: List[Class] = []

        while not self._match("EOF"):
            if self._check("IMPORT"):
                statements.append(self._import_statement())
            elif self._check("FUNC"):
                self._advance() # Consume 'FUNC'
                functions.append(self._function_declaration())
            elif self._check("MAIN"):
                self._advance() # Consume 'MAIN'
                functions.append(self._main_block())
            elif self._check("CLASS"):
                classes.append(self._class_declaration())
            else:
                # For REPL mode, parse other statements at the top level
                try:
                    # Attempt to parse as a statement for REPL-like behavior
                    statements.append(self._statement())
                except TranspilerError:
                    token = self._peek()
                    # If we are not at EOF, it's a real error.
                    if token.kind != "EOF":
                        raise TranspilerError(f"Unexpected token '{token.value}'. Only 'func', 'main', 'class', or 'import' are allowed at the top level.", token)
        return Program(functions=functions, statements=statements, classes=classes, tokens=self.tokens)

    def _class_declaration(self) -> Class:
        self._consume("CLASS", "Expected 'class' keyword.")
        name = self._consume("IDENT", "Expected class name.").value
        superclass = None
        if self._match("EXTENDS"):
            superclass_name = self._consume("IDENT", "Expected superclass name.")
            superclass = Identifier(superclass_name.value)
        
        body = self._block()
        return Class(name, superclass, body)

    def _import_statement(self) -> ImportStatement:
        name = self._consume("IDENT", "Expected module name after 'import'")
        self._consume("SEMICOLON", "Expected ';' after module name")
        return ImportStatement(name.value)

    def _function_declaration(self) -> Function:
        name = self._consume("IDENT", "Expected function name")
        self._consume("LPAREN", "Expected '(' after function name")
        parameters = self._parameters()
        self._consume("RPAREN", "Expected ')' after parameters")
        body = self._block()
        return Function(name.value, parameters, body)

    def _main_block(self) -> Function:
        body = self._block()
        return Function("main", [], body)

    def _parameters(self) -> List[Parameter]:
        params: List[Parameter] = []
        if self._check("RPAREN"):
            return params
        while True:
            name = self._consume("IDENT", "Expected parameter name")
            params.append(Parameter(name.value))
            if not self._match("COMMA"):
                break
        return params

    def _block(self) -> Block:
        self._consume("LBRACE", "Expected '{' to start block")
        statements: List = []
        while not self._check("RBRACE"):
            statements.append(self._statement())
        self._consume("RBRACE", "Expected '}' to close block")
        return Block(statements)

    def _statement(self):
        if self._match("LET"):
            name = self._consume("IDENT", "Expected identifier after let")
            self._consume("EQUAL", "Expected '=' in let statement")
            value = self._expression()
            self._consume("SEMICOLON", "Expected ';' after let statement")
            return LetStatement(name.value, value)
        
        # Manejo de reasignación (sin 'set')
        if self._check("IDENT") and self._peek_next().kind == "EQUAL":
            name = self._consume("IDENT", "Expected identifier after set")
            self._consume("EQUAL", "Expected '=' in set statement")
            value = self._expression()
            self._consume("SEMICOLON", "Expected ';' after set statement")
            return SetStatement(name.value, value)

        if self._match("RETURN"):
            if self._check("SEMICOLON"):
                self._advance()
                return ReturnStatement(None)
            value = self._expression()
            self._consume("SEMICOLON", "Expected ';' after return value")
            return ReturnStatement(value)
        if self._match("IF"):
            condition = self._expression()
            consequence = self._block()
            alternative = None
            if self._match("ELSE"):
                if self._match("IF"):
                    alternative = self._statement()
                else:
                    alternative = self._block()
            return IfStatement(condition, consequence, alternative)
        if self._match("FOR"):
            target = self._consume("IDENT", "Expected loop variable")
            self._consume("IN", "Expected 'in' after loop variable")
            iterable = self._expression()
            if self._match("RANGE"):
                end_expr = self._expression()
                iterable = RangeExpression(iterable, end_expr)
            body = self._block()
            return ForStatement(target.value, iterable, body)
        if self._match("WHILE"):
            condition = self._expression()
            body = self._block()
            return WhileStatement(condition, body)
        if self._match("TRY"):
            try_block = self._block()
            self._consume("CATCH", "Expected 'catch' after try block")
            error_variable = None
            if self._check("IDENT"):
                error_variable = self._consume("IDENT", "Expected error variable name").value
            catch_block = self._block()
            return TryStatement(try_block, error_variable, catch_block)
        
        # Si ninguna de las palabras clave de declaración coincide,
        # se asume que es una declaración de expresión (ej. una llamada a función).
        expr = self._expression()
        self._consume("SEMICOLON", "Expected ';' after expression")
        return ExpressionStatement(expr)

    def _expression(self) -> Expression:
        return self._or()

    def _or(self) -> Expression:
        expr = self._and()
        while self._match("OR"):
            operator = "or"
            right = self._and()
            expr = BinaryOperation(expr, operator, right)
        return expr

    def _and(self) -> Expression:
        expr = self._equality()
        while self._match("AND"):
            operator = "and"
            right = self._equality()
            expr = BinaryOperation(expr, operator, right)
        return expr

    def _equality(self) -> Expression:
        expr = self._comparison()
        while True:
            if self._match("EQ"):
                right = self._comparison()
                expr = BinaryOperation(expr, "==", right)
            elif self._match("NEQ"):
                right = self._comparison()
                expr = BinaryOperation(expr, "!=", right)
            else:
                break
        return expr

    def _comparison(self) -> Expression:
        expr = self._term()
        while True:
            if self._match("LT"):
                right = self._term()
                expr = BinaryOperation(expr, "<", right)
            elif self._match("LTE"):
                right = self._term()
                expr = BinaryOperation(expr, "<=", right)
            elif self._match("GT"):
                right = self._term()
                expr = BinaryOperation(expr, ">", right)
            elif self._match("GTE"):
                right = self._term()
                expr = BinaryOperation(expr, ">=", right)
            else:
                break
        return expr

    def _term(self) -> Expression:
        expr = self._factor()
        while True:
            if self._match("PLUS"):
                right = self._factor()
                expr = BinaryOperation(expr, "+", right)
            elif self._match("MINUS"):
                right = self._factor()
                expr = BinaryOperation(expr, "-", right)
            else:
                break
        return expr

    def _factor(self) -> Expression:
        expr = self._unary()
        while True:
            if self._match("STAR"):
                right = self._unary()
                expr = BinaryOperation(expr, "*", right)
            elif self._match("SLASH"):
                right = self._unary()
                expr = BinaryOperation(expr, "/", right)
            else:
                break
        return expr

    def _unary(self) -> Expression:
        if self._match("NOT"):
            operand = self._unary()
            return UnaryOperation("not", operand)
        if self._match("MINUS"):
            operand = self._unary()
            return UnaryOperation("-", operand)
        return self._call()

    def _call(self) -> Expression:
        expr = self._primary()
        while True:
            if self._match("LPAREN"):
                arguments = self._arguments()
                expr = CallExpression(expr, arguments)
            elif self._match("DOT"):
                name = self._consume("IDENT", "Expected attribute name")
                expr = Attribute(expr, name.value)
            elif self._match("LBRACKET"):
                index = self._expression()
                self._consume("RBRACKET", "Expected ']' after index")
                expr = IndexExpression(expr, index)
            else:
                break
        return expr

    def _arguments(self) -> List[Expression]:
        args: List[Expression] = []
        if self._check("RPAREN"):
            self._consume("RPAREN", "Expected ')' after arguments")
            return args
        while True:
            args.append(self._expression())
            if self._match("COMMA"):
                continue
            break
        self._consume("RPAREN", "Expected ')' after arguments")
        return args

    def _primary(self) -> Expression:
        if self._match("NUMBER"):
            token = self._previous()
            if "." in token.value:
                return Literal(float(token.value))
            return Literal(int(token.value))
        if self._match("STRING"):
            return Literal(self._previous().value)
        if self._match("TRUE"):
            return Literal(True)
        if self._match("FALSE"):
            return Literal(False)
        if self._match("IDENT"):
            return Identifier(self._previous().value)
        if self._match("THIS"):
            return This()
        if self._match("LPAREN"):
            expr = self._expression()
            self._consume("RPAREN", "Expected ')' after expression")
            return expr
        if self._match("LBRACKET"):
            elements = self._list_elements()
            self._consume("RBRACKET", "Expected ']' to close list")
            return ListExpression(elements)
        token = self._peek() # Obtener el token ofensivo
        raise TranspilerError(f"Unexpected token '{token.value}'", token)

    def _match(self, kind: str) -> bool:
        if self._check(kind):
            self._advance()
            return True
        return False

    def _list_elements(self) -> List[Expression]:
        elements: List[Expression] = []
        if self._check("RBRACKET"):
            return elements
        while True:
            elements.append(self._expression())
            if not self._match("COMMA"):
                break
        return elements

    def _check(self, kind: str) -> bool:
        if self.current >= len(self.tokens):
            return kind == "EOF"
        return self.tokens[self.current].kind == kind

    def _consume(self, kind: str, message: str) -> Token:
        if self._check(kind):
            return self._advance()
        token = self._peek() # Obtener el token ofensivo
        raise TranspilerError(message, token) # Lanzar error con el token

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def _is_at_end(self) -> bool:
        return self._peek().kind == "EOF"

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _peek_next(self) -> Token:
        if self.current + 1 >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.current + 1]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]


CALL_ALIASES = {
    "c.printf": "c_printf",
    "cpp.cout": "cpp_cout",
    "cs.write_line": "cs_write_line",
    "py.print": "py_print",
    "py.breakpoint": "py_breakpoint",
    "py.input": "py_input",
    "py.random.randint": "py_random_randint",
    "css.set": "css_set",
    "str.length": "len",
    "str.charAt": "lambda s, i: s[i]",
    "js.log": "js_log",
}


RUNTIME_PREAMBLE = textwrap.dedent(
    """
import time
import random

_PROFILING_DATA = {}

def profiler(func):
    \"\"\"A simple decorator to profile function execution time.\"\"\"
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = (end_time - start_time) * 1000  # in ms
        
        # Store cumulative time
        _PROFILING_DATA[func.__name__] = _PROFILING_DATA.get(func.__name__, 0) + duration
        
        print(f"[PROFILE] {func.__name__} executed in {duration:.4f} ms")
        return result
    return wrapper

def c_printf(format_string, *values):
    print(format_string % values)


def cpp_cout(value):
    print(value)


def cs_write_line(value):
    print(value)


def py_print(*values):
    print(*values)


def py_breakpoint():
    breakpoint()


def py_input(prompt=""):
    return input(prompt)


def py_random_randint(a, b):
    return random.randint(a, b)


def css_set(selector, prop, value):
    rule = f"{selector} {{ {prop}: {value}; }}"
    _styles.append(rule)
    print(f"css: {rule}")


def js_log(value):
    print(f"js: {value}")


def to_string(value):
    return str(value)


def to_number(value):
    try:
        return int(value)
    except ValueError:
        return float(value)
    except TypeError:
        raise ValueError("Cannot convert value to number")
    except Exception as exc:
        raise ValueError("Cannot convert value to number") from exc
    """
)


class PythonEmitter:
    def __init__(self, tokens: List[Token]) -> None:
        self.lines: List[str] = []
        self.indent = 0
        self.is_repl = False
        self.imported_modules = set()
        self.tokens = tokens
        self.package_loader = PackageLoader()

    def emit(self, program: Program, is_repl: bool = False, source_file: str = None) -> str:
        self.is_repl = is_repl
        self.lines = []
        
        is_data_file = False
        if source_file:
            file_ext = Path(source_file).suffix.lower()
            is_data_file = file_ext == '.opn'

        source_text = " ".join(t.value for t in self.tokens)
        needs_gfx = "gfx" in source_text

        for statement in program.statements:
            self._visit_statement(statement)

        # Procesar declaraciones de clase
        for class_def in program.classes:
            self._visit_class(class_def)

        # In REPL mode, we process statements directly. Otherwise, we define functions.
        if is_repl and not program.functions:
            self._emit_statements(program.statements)
        else:
            for function in program.functions:
                self._visit_function(function)
                self.lines.append("")

        body = "\n".join(line for line in self.lines if line is not None).rstrip()
        if is_repl:
            return body

        preamble = RUNTIME_PREAMBLE.rstrip()
        
        if needs_gfx:
            preamble += "\n\nfrom prisma import pygfx_api as gfx"

        main_guard = ""
        # Only add the main guard if a 'main' function actually exists.
        if any(f.name == "main" for f in program.functions):
            main_guard = 'if __name__ == "__main__":\n    main()'

        segments = [preamble, body, main_guard]
        return "\n\n".join(filter(None, segments)).rstrip() + "\n"

    def _emit_line(self, text: str) -> None:
        self.lines.append("    " * self.indent + text)

    def _visit_function(self, function: Function) -> None:
        params = ", ".join(param.name for param in function.parameters)
        self._emit_line("@profiler")
        self._emit_line(f"def {function.name}({params}):")
        self.indent += 1
        self._emit_statements(function.body.statements)
        self.indent -= 1

    def _visit_class(self, class_def: Class) -> None:
        if class_def.superclass:
            self._emit_line(f"class {class_def.name}({class_def.superclass.value}):")
        else:
            self._emit_line(f"class {class_def.name}:")
        
        self.indent += 1
        # Extraer funciones y sentencias 'let' del cuerpo de la clase
        methods = [stmt for stmt in class_def.body.statements if isinstance(stmt, Function)]
        fields = [stmt for stmt in class_def.body.statements if isinstance(stmt, LetStatement)]

        # Por ahora, solo manejamos métodos. Los campos se manejarían en el constructor.
        self._emit_statements(methods)
        self.indent -= 1

    def _emit_statements(self, statements: Iterable) -> None:
        stmts = list(statements)
        if not stmts:
            self._emit_line("pass")
            return
        for statement in stmts:
            self._visit_statement(statement)

    def _visit_statement(self, statement: Statement) -> None:
        if isinstance(statement, LetStatement):
            self._emit_line(f"{statement.name} = {self._render_expression(statement.value)}")
        elif isinstance(statement, ImportStatement):
            import_type, import_value = self.package_loader.resolve_import(statement.module)
            if import_type == 'opn':
                self._emit_line(f"# OPN Package: {statement.module}")
                self._emit_line(import_value)
            else:
                self._emit_line(f"import {import_value}")
        elif isinstance(statement, Function):
            # Manejar funciones anidadas o métodos de clase
            func_name = statement.name
            if func_name == "constructor":
                func_name = "__init__"
            params = ", ".join(['self'] + [p.name for p in statement.parameters])
            self._emit_line(f"def {func_name}({params}):")
            self.indent += 1
            self._emit_statements(statement.body.statements)
            self.indent -= 1
        elif isinstance(statement, SetStatement):
            self._emit_line(f"{statement.name} = {self._render_expression(statement.value)}")
        elif isinstance(statement, ReturnStatement):
            if statement.value is None:
                self._emit_line("return")
            else:
                self._emit_line(f"return {self._render_expression(statement.value)}")
        elif isinstance(statement, ExpressionStatement):
            self._emit_line(self._render_expression(statement.expression))
        elif isinstance(statement, IfStatement):
            self._emit_line(f"if {self._render_expression(statement.condition)}:")
            self.indent += 1
            self._emit_statements(statement.consequence.statements)
            self.indent -= 1
            if statement.alternative is not None:
                self._emit_line("else:")
                self.indent += 1
                self._emit_statements(statement.alternative.statements)
                self.indent -= 1
        elif isinstance(statement, ForStatement):
            self._emit_line(f"for {statement.target} in {self._render_expression(statement.iterable)}:")
            self.indent += 1
            self._emit_statements(statement.body.statements)
            self.indent -= 1
        elif isinstance(statement, WhileStatement):
            self._emit_line(f"while {self._render_expression(statement.condition)}:")
            self.indent += 1
            self._emit_statements(statement.body.statements)
            self.indent -= 1
        elif isinstance(statement, TryStatement):
            self._emit_line("try:")
            self.indent += 1
            self._emit_statements(statement.try_block.statements)
            self.indent -= 1
            if statement.error_variable:
                self._emit_line(f"except Exception as {statement.error_variable}:")
            else:
                self._emit_line("except Exception:")
            self.indent += 1
            self._emit_statements(statement.catch_block.statements)
            self.indent -= 1
        else:
            raise TranspilerError("Unsupported statement")

    def _render_expression(self, expression: Expression) -> str:
        if isinstance(expression, Literal):
            if isinstance(expression.value, str):
                return repr(expression.value)
            return str(expression.value)
        if isinstance(expression, Identifier):
            return expression.value
        if isinstance(expression, This):
            return "self"
        if isinstance(expression, Attribute):
            return f"{self._render_expression(expression.value)}.{expression.attribute}"
        if isinstance(expression, UnaryOperation):
            operand = self._render_expression(expression.operand)
            if expression.operator == "-":
                return f"-{operand}"
            return f"not {operand}"
        if isinstance(expression, BinaryOperation):
            left = self._render_expression(expression.left)
            right = self._render_expression(expression.right)
            return f"({left} {expression.operator} {right})"
        if isinstance(expression, RangeExpression):
            start = self._render_expression(expression.start)
            end = self._render_expression(expression.end)
            return f"range({start}, {end} + 1)"
        if isinstance(expression, ListExpression):
            elements = ", ".join(self._render_expression(e) for e in expression.elements)
            return f"[{elements}]"
        if isinstance(expression, IndexExpression):
            target = self._render_expression(expression.target)
            index = self._render_expression(expression.index)
            return f"{target}[{index}]"
        if isinstance(expression, CallExpression):
            # --- Modificación para Inyección de Línea ---
            # Si la llamada es a 'py.print', inyectamos el número de línea como primer argumento.
            callee_token = self._get_token_for_expression(expression.callee)
            is_py_print = self._resolve_name(expression.callee) == "py.print"

            if is_py_print and callee_token:
                line_number = callee_token.line
                args = f"{line_number}, " + ", ".join(self._render_expression(arg) for arg in expression.arguments)
            else:
                args = ", ".join(self._render_expression(arg) for arg in expression.arguments)

            callee_name = self._resolve_name(expression.callee)
            if callee_name in CALL_ALIASES:
                callee = CALL_ALIASES[callee_name]
            else:
                callee = self._render_expression(expression.callee)
            return f"{callee}({args})"
        raise TranspilerError("Unsupported expression")

    def _resolve_name(self, expression: Expression) -> Optional[str]:
        if isinstance(expression, Identifier):
            return expression.value
        if isinstance(expression, Attribute):
            base = self._resolve_name(expression.value)
            if base is None:
                return None
            return f"{base}.{expression.attribute}"
        return None

    def _get_token_for_expression(self, expression: Expression) -> Optional[Token]:
        """Intenta encontrar el token inicial para una expresión para obtener su línea."""
        if hasattr(expression, 'value') and isinstance(expression.value, str):
            # Heurística para Identifier y otros nodos simples
            for token in self.tokens:
                if token.value == expression.value:
                    return token
        return None


class OPNTranspiler:
    def __init__(self, source: str) -> None:
        self.source = source

    def parse(self) -> Program:
        lexer = Lexer(self.source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def transpile(self, is_repl: bool = False, source_file: str = None) -> str:
        program = self.parse()
        emitter = PythonEmitter(program.tokens)
        return emitter.emit(program, is_repl=is_repl, source_file=source_file)


def transpile(source: str, is_repl: bool = False, source_file: str = None) -> str:
    return OPNTranspiler(source).transpile(is_repl=is_repl, source_file=source_file)


def transpile_path(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return transpile(handle.read(), source_file=path)
