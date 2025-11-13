# Librería Estándar de OPNscript

## Overview
OPN ships with a pragmatic standard library exposed through six namespaces. Each namespace mirrors a familiar ecosystem, letting you reuse habits from other languages while keeping OPN's syntax clear.

## C namespace
- **c.printf(format, values...)**: Uses `printf`-style placeholders. Transpiles to Python's `%` string formatting and prints the result.

## C++ namespace
- **cpp.cout(value)**: Streams a value to standard output with a trailing newline.

## C# namespace
- **cs.write_line(value)**: Mirrors `Console.WriteLine`, printing a value followed by a newline.

## Python namespace
- **py.print(*values)**: Wraps Python's built-in `print`, forwarding any arguments.
- **py.input(prompt)**: Displays a prompt and reads a line from standard input.
- **py.random.randint(a, b)**: Returns a random integer between a and b (inclusive).

## CSS namespace
- **css.set(selector, property, value)**: Records a style rule and prints a human-friendly confirmation when executed. You can call it multiple times to build up a stylesheet.

## JavaScript namespace
- **js.log(value)**: Equivalent to `console.log`, printing a diagnostic line prefixed with `js:`.

## Utility helpers
- **range(start, end)**: Returns a Python `range` object. Commonly used with `for` loops.
- **to_string(value)**: Converts any value to a string using Python's `str`.
- **to_number(value)**: Attempts to convert a string to an integer or float.

All helpers are implemented in the transpiler preamble, so transpiled programs run without extra imports.
