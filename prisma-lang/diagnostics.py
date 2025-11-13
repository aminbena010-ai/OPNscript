# ----------------------------------------------------
# Módulo de Diagnóstico y Reporte de Errores para OPN
# ----------------------------------------------------
# v1.1: Añade colores, estructura mejorada y sugerencias de solución.

class Colors:
    """Clase para almacenar códigos de color ANSI para la terminal."""
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

class OPNError(Exception):
    """Clase base para todos los errores personalizados del lenguaje OPN."""
    def __init__(self, message, line=None, column=None, hint=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.hint = hint  # Nueva propiedad para sugerencias

def report_error(source_path, source_code, error: OPNError):
    """
    Muestra un error de forma clara, señalando la línea y columna.
    """
    error_type = "Error de Sintaxis" if error.line is not None else "Error de Ejecución"
    header = f"{Colors.RED}--- {error_type} en OPN ---{Colors.RESET}"
    print(f"\n{header}")

    if error.line is not None and error.column is not None:
        lines = source_code.split('\n')
        # Asegurarse de que la línea existe para evitar errores de índice
        line_str = lines[error.line - 1] if error.line <= len(lines) else ""

        # Imprime la ubicación del error
        print(f"{Colors.WHITE}en {source_path}:{error.line}:{error.column}{Colors.RESET}")
        print(f"\n{Colors.CYAN}Problema:{Colors.RESET} {Colors.WHITE}{error.message}{Colors.RESET}")

        # Imprime el fragmento de código
        print(f"\n  {Colors.PURPLE}{error.line} |{Colors.RESET} {line_str}")
        print(f"    {Colors.PURPLE}|{Colors.RESET} {' ' * (error.column - 1)}{Colors.RED}^{Colors.RESET}")

        # Imprime la sugerencia si existe
        if error.hint:
            print(f"\n{Colors.YELLOW}Sugerencia:{Colors.RESET} {Colors.WHITE}{error.hint}{Colors.RESET}")
    else:
        print(f"{Colors.WHITE}{error.message}{Colors.RESET}")

    # La longitud del separador se calcula sin los códigos de color
    separator_len = len(header) - (len(Colors.RED) + len(Colors.RESET))
    print(f"\n{'-' * separator_len}\n")