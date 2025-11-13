from __future__ import annotations

import os
import sys
from subprocess import run

# Try to import readline for command history. This will work on Linux/macOS.
# On Windows, it will fail, but we can ignore it. The REPL will still work.
try:
    import readline
except ImportError:
    pass  # readline is not available.

from colorama import Fore, Style, init

from prisma.core import TranspilerError, transpile

# Initialize colorama
init(autoreset=True)


def run_repl() -> None:
    """Starts an interactive Read-Eval-Print Loop (REPL) for OPN."""
    print(f"{Style.BRIGHT}Welcome to the OPN REPL!{Style.NORMAL}")
    print(" - Type OPN code to execute it.")
    print(" - Type `!command` to run a shell command (e.g., `!dir`).")
    print(" - Type `exit` or `exit;` or press Ctrl+D to quit.")

    # Prepare a persistent namespace and execute the standard library preamble
    namespace = {"__name__": "__main__"}
    exec(compile(transpile(""), "<opn-preamble>", "exec"), namespace)

    buffer: list[str] = []
    while True:
        try:
            # Set prompt based on whether we are in a multi-line block
            if buffer:
                prompt = f"{Fore.YELLOW}  ... {Style.RESET_ALL}"
            else:
                prompt = f"{Fore.GREEN}{Style.BRIGHT}opn> {Style.RESET_ALL}"
            line = input(prompt)

            stripped_line = line.strip()
            if not stripped_line:
                continue

            if stripped_line.lower() in ("exit", "exit;"):
                break

            # Handle shell commands
            if stripped_line.lower() in ("cls", "clear"):
                command = "cls" if os.name == "nt" else "clear"
                run(command, shell=True, check=False)
                continue
            
            if stripped_line.lower() in ("!vars", "!globals"):
                print(f"{Style.BRIGHT}--- Defined Variables & Functions ---{Style.NORMAL}")
                for name, value in sorted(namespace.items()):
                    if name.startswith("__"):
                        continue
                    try:
                        type_str = type(value).__name__
                        repr_str = repr(value)
                        if len(repr_str) > 60:
                            repr_str = repr_str[:57] + "..."
                        print(f"  {Fore.CYAN}{name}{Style.RESET_ALL} ({type_str}): {repr_str}")
                    except Exception:
                        print(f"  {Fore.CYAN}{name}{Style.RESET_ALL}: <unprintable value>")
                continue

            if stripped_line.startswith("!"):
                shell_command = stripped_line[1:].strip()
                # Intercept calls to 'opn' and run them with the current python interpreter
                if shell_command == "opn --version":
                    print(f"OPN Language Version: 0.5.0")
                    continue
                if shell_command == "opn --version -C":
                    # Asumimos que -C se refiere a la versión del Corrector/Editor
                    print(f"OPN Editor/Corrector Version: 1.2.0")
                    continue

                if shell_command.startswith("opn "):
                    args = shell_command.split()[1:]
                    # The cli.py script is smart enough to infer the 'run' command
                    # if a filename is provided. We just need to pass the arguments.
                    # We also replace the user-friendly '--run' with the internal '--execute' flag.
                    final_args = [arg.replace("--run", "--execute") for arg in args if arg != "run"]
                    run([sys.executable, "-m", "prisma.cli", *final_args], check=False)
                else:
                    run(shell_command, shell=True, check=False)
                continue

            buffer.append(line)
            source = "\n".join(buffer)

            # Attempt to transpile. If it succeeds, the code block is complete.
            try:
                python_code = transpile(source, is_repl=True)
                # If transpilation is successful, execute the code and clear the buffer
                if python_code.strip():
                    exec(compile(python_code, "<opn-repl>", "exec"), namespace)
                buffer.clear()
            except TranspilerError as e:
                # If the error is an unexpected EOF, it means the block is not yet complete.
                if "Unexpected token 'EOF'" in str(e) or "Unterminated" in str(e):
                    continue  # Wait for more input
                raise  # It's a different, real error
        except (TranspilerError, SyntaxError, NameError) as exc:
            print(f"{Fore.RED}Error: {exc}", file=sys.stderr)
            buffer.clear()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Style.BRIGHT}Exiting OPN REPL.{Style.NORMAL}")
            break