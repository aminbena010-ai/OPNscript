KEYWORDS = [
    "if", "else", "elif", "while", "for", "in", "break", "continue",
    "def", "return", "class", "import", "from", "as", "try", "except",
    "finally", "with", "lambda", "yield", "pass", "raise", "assert",
    "global", "nonlocal", "del", "and", "or", "not", "is", "None",
    "True", "False", "var", "let", "const", "function", "async", "await"
]

OPERATORS = [
    "+", "-", "*", "/", "//", "%", "**",
    "==", "!=", "<", ">", "<=", ">=",
    "=", "+=", "-=", "*=", "/=", "//=", "%=", "**=",
    "&", "|", "^", "~", "<<", ">>",
    "and", "or", "not",
    "(", ")", "[", "]", "{", "}",
    ",", ":", ";", ".", "->", "=>"
]

BUILTINS = {
    "print": {
        "signature": "print(*args, sep=' ', end='\\n')",
        "description": "Imprime valores en la consola",
        "example": "print('Hola', 'Mundo')"
    },
    "input": {
        "signature": "input(prompt='')",
        "description": "Lee entrada del usuario",
        "example": "nombre = input('Tu nombre: ')"
    },
    "len": {
        "signature": "len(obj)",
        "description": "Retorna la longitud de un objeto",
        "example": "len([1, 2, 3])  # 3"
    },
    "range": {
        "signature": "range(start, stop, step=1)",
        "description": "Genera una secuencia de números",
        "example": "for i in range(10): print(i)"
    },
    "int": {
        "signature": "int(x, base=10)",
        "description": "Convierte a entero",
        "example": "int('42')  # 42"
    },
    "float": {
        "signature": "float(x)",
        "description": "Convierte a flotante",
        "example": "float('3.14')  # 3.14"
    },
    "str": {
        "signature": "str(obj)",
        "description": "Convierte a cadena",
        "example": "str(42)  # '42'"
    },
    "list": {
        "signature": "list(iterable)",
        "description": "Crea una lista",
        "example": "list(range(5))  # [0,1,2,3,4]"
    },
    "dict": {
        "signature": "dict(**kwargs)",
        "description": "Crea un diccionario",
        "example": "dict(a=1, b=2)"
    },
    "open": {
        "signature": "open(file, mode='r')",
        "description": "Abre un archivo",
        "example": "with open('file.txt') as f: data = f.read()"
    },
    "abs": {
        "signature": "abs(x)",
        "description": "Valor absoluto",
        "example": "abs(-5)  # 5"
    },
    "min": {
        "signature": "min(*args)",
        "description": "Retorna el mínimo",
        "example": "min(1, 2, 3)  # 1"
    },
    "max": {
        "signature": "max(*args)",
        "description": "Retorna el máximo",
        "example": "max(1, 2, 3)  # 3"
    },
    "sum": {
        "signature": "sum(iterable, start=0)",
        "description": "Suma elementos",
        "example": "sum([1, 2, 3])  # 6"
    },
    "sorted": {
        "signature": "sorted(iterable, reverse=False)",
        "description": "Retorna lista ordenada",
        "example": "sorted([3, 1, 2])  # [1,2,3]"
    },
    "enumerate": {
        "signature": "enumerate(iterable, start=0)",
        "description": "Enumera elementos",
        "example": "for i, v in enumerate(['a','b']): print(i, v)"
    },
    "zip": {
        "signature": "zip(*iterables)",
        "description": "Combina iterables",
        "example": "list(zip([1,2], ['a','b']))  # [(1,'a'),(2,'b')]"
    },
    "map": {
        "signature": "map(function, iterable)",
        "description": "Aplica función a elementos",
        "example": "list(map(str, [1,2,3]))  # ['1','2','3']"
    },
    "filter": {
        "signature": "filter(function, iterable)",
        "description": "Filtra elementos",
        "example": "list(filter(lambda x: x>0, [-1,0,1]))  # [1]"
    },
}

GFX_FUNCTIONS = {
    "gfx.setup_canvas": {
        "signature": "gfx.setup_canvas(width, height, title='OPN Graphics')",
        "description": "Configura el canvas de gráficos",
        "example": "gfx.setup_canvas(800, 600, 'Mi Juego')"
    },
    "gfx.draw_point": {
        "signature": "gfx.draw_point(x, y, color, size=1)",
        "description": "Dibuja un punto en el canvas",
        "example": "gfx.draw_point(100, 100, gfx.Rojo, 5)"
    },
    "gfx.draw_circle": {
        "signature": "gfx.draw_circle(x, y, radius, color, filled=True)",
        "description": "Dibuja un círculo",
        "example": "gfx.draw_circle(200, 200, 50, gfx.Azul)"
    },
    "gfx.update_screen": {
        "signature": "gfx.update_screen()",
        "description": "Actualiza la pantalla",
        "example": "gfx.update_screen()"
    },
    "gfx.init": {
        "signature": "gfx.init()",
        "description": "Inicia el loop de gráficos",
        "example": "gfx.init()"
    },
    "gfx.quit": {
        "signature": "gfx.quit()",
        "description": "Cierra la ventana de gráficos",
        "example": "gfx.quit()"
    },
}

GFX_COLORS = [
    "gfx.Rojo", "gfx.Verde", "gfx.Azul", "gfx.Amarillo",
    "gfx.Púrpura", "gfx.Cian", "gfx.Blanco", "gfx.Negro"
]
