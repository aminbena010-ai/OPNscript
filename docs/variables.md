# Resumen de Variables en OPNscript

En el lenguaje OPN, las variables se utilizan para almacenar y gestionar datos. Hay dos comandos principales para trabajar con variables: `let` y `set`.

## 1. Declaración de Variables con `let`

El comando `let` se usa para crear (declarar) una nueva variable y asignarle un valor inicial. Una vez que una variable es creada con `let`, no puedes usar `let` de nuevo para la misma variable.

### Sintaxis:
`let <nombre_variable> = <valor>;`

### Ejemplos:
```opn
# Declara una variable numérica
let edad = 25;

# Declara una variable de texto
let nombre = "Juan";
```

## 2. Reasignación de Variables con `set`

El comando `set` se usa para cambiar o actualizar el valor de una variable que **ya existe** (que fue creada previamente con `let`).

### Sintaxis:
`set <nombre_variable> = <nuevo_valor>;`

### Ejemplo:
```opn
# Primero, declaramos la variable
let puntuacion = 100;

# Luego, actualizamos su valor
set puntuacion = 150;
```