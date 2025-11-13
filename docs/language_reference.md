# Guía de Referencia del Lenguaje OPNscript

Bienvenido a la documentación completa de OPN. Esta guía cubre toda la sintaxis, características y funciones disponibles en el lenguaje.

## 1. Estructura del Programa

Un programa en OPN se compone de funciones y un bloque principal `main` que sirve como punto de entrada.

```opn
# Define una función reutilizable
func mi_funcion() {
    py.print("Desde una función");
}

# El punto de entrada del programa
main {
    py.print("Hola, OPN!");
    mi_funcion();
}
```

## 2. Sintaxis Básica

### Comentarios
Los comentarios empiezan con `#` y se extienden hasta el final de la línea.
```opn
# Esto es un comentario.
let x = 10; # Esto también es un comentario.
```

### Variables
Las variables se declaran con `let` y se reasignan con `set`.

```opn
let mensaje = "Hola";  # Declaración
set mensaje = "Hola, Mundo"; # Reasignación
```

### Tipos de Datos y Literales
- **Números**: Enteros (`10`) y de punto flotante (`3.14`).
- **Cadenas de texto (Strings)**: Delimitadas por comillas dobles (`"hola"`).
- **Booleanos**: `true` y `false`.

## 3. Operadores

### Aritméticos
`+` (suma), `-` (resta), `*` (multiplicación), `/` (división).

### Comparación
`==` (igual), `!=` (diferente), `<` (menor que), `<=` (menor o igual que), `>` (mayor que), `>=` (mayor o igual que).

### Lógicos
`and` (Y lógico), `or` (O lógico), `not` (negación).

## 4. Control de Flujo

### Condicionales `if/else`
```opn
if x > 10 {
    py.print("x es mayor que 10");
} else {
    py.print("x no es mayor que 10");
}
```
El bloque `else` es opcional.

### Bucles `for`
Los bucles `for` iteran sobre un rango. El operador `..` crea un rango inclusivo.

```opn
# Imprime los números del 1 al 5
for i in 1..5 {
    py.print(i);
}
```

## 5. Funciones

### Definición y Llamada
Las funciones se definen con la palabra clave `func`.

```opn
func sumar(a, b) {
    return a + b;
}

main {
    let resultado = sumar(5, 3); # resultado es 8
    py.print(resultado);
}
```

### Retorno de Valores
Usa `return` para devolver un valor desde una función. Si se omite, la función no devuelve nada.

## 6. Librería Estándar

OPN incluye una librería estándar accesible a través de varios espacios de nombres.

### `c` (Estilo C)
- **c.printf(formato, ...valores)**: Imprime texto con formato.

### `cpp` (Estilo C++)
- **cpp.cout(valor)**: Imprime un valor seguido de una nueva línea.

### `cs` (Estilo C#)
- **cs.write_line(valor)**: Imprime un valor seguido de una nueva línea.

### `py` (Estilo Python)
- **py.print(...valores)**: Imprime uno o más valores.
- **py.input(prompt)**: Lee una línea de texto desde la consola.
- **py.random.randint(a, b)**: Devuelve un número entero aleatorio entre `a` y `b` (ambos incluidos).

### `css` (Estilo CSS)
- **css.set(selector, propiedad, valor)**: Define una regla de estilo CSS.

### `js` (Estilo JavaScript)
- **js.log(valor)**: Imprime un mensaje de diagnóstico, similar a `console.log`.

### Funciones de Utilidad
- **to_string(valor)**: Convierte cualquier valor a una cadena de texto.
- **to_number(valor)**: Intenta convertir una cadena de texto a un número (entero o flotante).

## 7. Consola Interactiva (REPL)

Ejecuta `opn` o `python -m prisma.cli` en tu terminal para iniciar la consola interactiva.

### Comandos Especiales
- **`exit`** o **`exit;`**: Sale de la consola.
- **`cls`** / **`clear`**: Limpia la pantalla de la consola.
- **`!comando`**: Ejecuta un comando del sistema (ej: `!dir`, `!ls`).
- **`!opn <archivo.prisma> --run`**: Ejecuta un script de OPN desde dentro de la consola.