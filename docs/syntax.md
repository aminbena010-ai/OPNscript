# Sintaxis de OPNscript

## Program layout
1. Define reusable routines with the `func` keyword.
2. Provide a `main { ... }` entry block. The statements inside `main` run when the transpiled program starts.
3. Separate statements with semicolons. Blocks are delimited by curly braces.

## Comments
- Start a comment with `#`. Everything following the `#` on the same line is ignored.

## Declarations and statements
- Introduce variables with `let name = expression;`.
- Reassign an existing variable with `set name = expression;`.
- Return from a function with `return expression;`.
- Use `cls` or `clear` to clear the console screen.
- Any bare expression followed by `;` is evaluated for its side effects.

## Functions
```
func add(lhs, rhs) {
    return lhs + rhs;
}
```
- Parameters are dynamically typed.
- `main` behaves like an anonymous function with no parameters.

## Expressions
1. Literals: integers (`42`), floating numbers (`3.14`), strings (`"text"`), booleans (`true`, `false`).
2. Arithmetic: `+`, `-`, `*`, `/` with standard precedence.
3. Comparisons: `==`, `!=`, `<`, `<=`, `>`, `>=` (evaluate to booleans).
4. Logical: `and`, `or`, `not`.
5. Grouping with parentheses.
6. Function calls: `identifier(arg1, arg2)` or `namespace.identifier(args)`.

## Control flow
```
if condition {
    # positive branch
} else {
    # fallback branch
}
```
- `if` expressions require braces for both branches. The `else` branch is optional.
- Looping uses `for name in start..end { ... }`, where `end` is exclusive.

## Example
```
func greet(name) {
    py.print("Hello, " + name);
}

main {
    let audience = "OPN";
    greet(audience);
    js.log("Program finished");
}
```
