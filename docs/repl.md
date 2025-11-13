# REPL - Consola Interactiva de OPN

Guía completa del REPL (Read-Eval-Print Loop) de OPN.

## Tabla de Contenidos

- [Introducción](#introducción)
- [Iniciar el REPL](#iniciar-el-repl)
- [Comandos Básicos](#comandos-básicos)
- [Comandos Especiales](#comandos-especiales)
- [Uso Avanzado](#uso-avanzado)
- [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Introducción

El REPL de OPN es una consola interactiva que permite:

- ✨ Ejecutar código OPN línea por línea
- 🧪 Experimentar con sintaxis y funciones
- 🎨 Probar gráficos rápidamente
- 🔧 Depurar código
- 📝 Aprender el lenguaje de forma interactiva

---

## Iniciar el REPL

### Desde la Línea de Comandos

```bash
cd prisma-lang/src
python -m prisma
```

### Salida Esperada

```
OPN Interactive Shell
Type 'exit' to quit, 'cls' to clear screen
opn>
```

El prompt `opn>` indica que el REPL está listo para recibir comandos.

---

## Comandos Básicos

### Imprimir Texto

```opn
opn> py.print("Hola, REPL");
Hola, REPL
```

### Variables

**Declarar**:
```opn
opn> let x = 10;
opn> let nombre = "Ana";
opn> let activo = true;
```

**Usar**:
```opn
opn> py.print(x);
10
opn> py.print(nombre);
Ana
```

**Modificar**:
```opn
opn> set x = 20;
opn> py.print(x);
20
```

### Operaciones Matemáticas

```opn
opn> py.print(5 + 3);
8
opn> py.print(10 * 2);
20
opn> py.print(15 / 3);
5.0
```

### Expresiones

```opn
opn> let a = 5;
opn> let b = 3;
opn> py.print(a + b);
8
opn> py.print(a > b);
True
```

---

## Comandos Especiales

### `exit` - Salir del REPL

```opn
opn> exit
```

O con punto y coma:
```opn
opn> exit;
```

### `cls` / `clear` - Limpiar Pantalla

**Windows**:
```opn
opn> cls
```

**Linux/Mac**:
```opn
opn> clear
```

### `!comando` - Ejecutar Comandos del Sistema

**Listar archivos (Windows)**:
```opn
opn> !dir
```

**Listar archivos (Linux/Mac)**:
```opn
opn> !ls
```

**Ver directorio actual**:
```opn
opn> !cd
```

**Ejecutar script OPN**:
```opn
opn> !opn run tests/main.opn
```

---

## Uso Avanzado

### Funciones en el REPL

```opn
opn> func saludar(nombre) {
...>     py.print("Hola,", nombre);
...> }
opn> saludar("Carlos");
Hola, Carlos
```

**Nota**: El REPL muestra `...>` para líneas de continuación.

### Condicionales

```opn
opn> let edad = 18;
opn> if edad >= 18 {
...>     py.print("Mayor de edad");
...> } else {
...>     py.print("Menor de edad");
...> }
Mayor de edad
```

### Bucles

```opn
opn> for i in 1..5 {
...>     py.print("Número:", i);
...> }
Número: 1
Número: 2
Número: 3
Número: 4
Número: 5
```

### Gráficos Interactivos

```opn
opn> gfx.setup_canvas(400, 400, "REPL Graphics");
[GFX TK] Tkinter Initialized.
[GFX TK] Canvas inicializado: REPL Graphics (400x400)

opn> gfx.draw_circle(200, 200, 80, "Azul");
opn> gfx.update_screen();
[GFX TK] Pantalla actualizada.
```

---

## Ejemplos Prácticos

### Ejemplo 1: Calculadora Interactiva

```opn
opn> let num1 = 15;
opn> let num2 = 7;
opn> py.print("Suma:", num1 + num2);
Suma: 22
opn> py.print("Resta:", num1 - num2);
Resta: 8
opn> py.print("Multiplicación:", num1 * num2);
Multiplicación: 105
opn> py.print("División:", num1 / num2);
División: 2.142857142857143
```

### Ejemplo 2: Prueba de Colores

```opn
opn> gfx.setup_canvas(600, 200, "Colores");
opn> gfx.draw_circle(100, 100, 40, "Rojo");
opn> gfx.draw_circle(200, 100, 40, "Verde");
opn> gfx.draw_circle(300, 100, 40, "Azul");
opn> gfx.draw_circle(400, 100, 40, "Amarillo");
opn> gfx.draw_circle(500, 100, 40, "Púrpura");
opn> gfx.update_screen();
```

### Ejemplo 3: Generador de Números Aleatorios

```opn
opn> for i in 1..5 {
...>     let num = py.random.randint(1, 100);
...>     py.print("Número aleatorio:", num);
...> }
Número aleatorio: 42
Número aleatorio: 87
Número aleatorio: 15
Número aleatorio: 63
Número aleatorio: 91
```

### Ejemplo 4: Patrón Dinámico

```opn
opn> gfx.setup_canvas(800, 200, "Patrón");
opn> for i in 1..10 {
...>     let x = i * 80;
...>     let color = gfx.get_random_color();
...>     gfx.draw_circle(x, 100, 30, color);
...> }
opn> gfx.update_screen();
```

---

## Características del REPL

### Historial de Comandos

- **Flecha Arriba** (↑): Comando anterior
- **Flecha Abajo** (↓): Comando siguiente

### Autocompletado

El REPL no tiene autocompletado nativo, pero puedes:
- Copiar y pegar código
- Usar un editor externo y copiar al REPL

### Manejo de Errores

El REPL muestra errores sin cerrar la sesión:

```opn
opn> let x = 10;
opn> py.print(y);
Error: name 'y' is not defined
opn> # El REPL sigue funcionando
```

---

## Flujo de Trabajo Recomendado

### 1. Experimentación Rápida

Usa el REPL para probar ideas:

```opn
opn> let radio = 50;
opn> py.print("Área:", 3.14 * radio * radio);
Área: 7850.0
```

### 2. Desarrollo Iterativo

1. Escribe código en el REPL
2. Prueba que funcione
3. Copia al archivo `.opn`
4. Ejecuta el archivo completo

### 3. Debugging

```opn
opn> let x = 10;
opn> let y = 20;
opn> py.print("x:", x, "y:", y);
x: 10 y: 20
opn> py.print("Suma:", x + y);
Suma: 30
```

---

## Limitaciones del REPL

### No Soportado

1. **Múltiples líneas complejas**: Funciones muy largas pueden ser difíciles de escribir
2. **Edición de código**: No puedes editar líneas anteriores (usa ↑ para repetir)
3. **Importaciones**: No hay sistema de módulos en el REPL

### Soluciones

- Para código complejo, usa archivos `.opn`
- Para edición, usa un editor de texto y copia al REPL
- Para proyectos grandes, ejecuta archivos con `python -m prisma run`

---

## Atajos y Trucos

### Repetir Último Comando

```opn
opn> py.print("Hola");
Hola
opn> # Presiona ↑ y Enter
py.print("Hola");
Hola
```

### Ejecutar Múltiples Comandos

Escribe cada comando en una línea separada:

```opn
opn> let x = 5;
opn> let y = 10;
opn> py.print(x + y);
15
```

### Limpiar y Reiniciar

```opn
opn> cls
# Pantalla limpia, pero variables siguen existiendo
opn> py.print(x);  # Si x fue declarado antes
5
```

Para reiniciar completamente, sal y vuelve a entrar:
```opn
opn> exit
$ python -m prisma
opn>
```

---

## Ejemplos de Sesiones Completas

### Sesión 1: Matemáticas Básicas

```opn
OPN Interactive Shell
Type 'exit' to quit, 'cls' to clear screen
opn> let a = 25;
opn> let b = 5;
opn> py.print("Suma:", a + b);
Suma: 30
opn> py.print("Resta:", a - b);
Resta: 20
opn> py.print("Multiplicación:", a * b);
Multiplicación: 125
opn> py.print("División:", a / b);
División: 5.0
opn> exit
```

### Sesión 2: Gráficos Simples

```opn
OPN Interactive Shell
Type 'exit' to quit, 'cls' to clear screen
opn> gfx.setup_canvas(400, 400, "Test");
[GFX TK] Canvas inicializado: Test (400x400)
opn> gfx.draw_circle(200, 200, 100, "Rojo");
opn> gfx.draw_circle(200, 200, 70, "Amarillo");
opn> gfx.draw_circle(200, 200, 40, "Verde");
opn> gfx.update_screen();
[GFX TK] Pantalla actualizada.
opn> exit
```

---

## Solución de Problemas

### El REPL no inicia

**Problema**: `No module named 'prisma'`

**Solución**:
```bash
cd OPN4/prisma-lang/src
python -m prisma
```

### Los comandos no funcionan

**Problema**: Olvidaste el punto y coma

**Solución**: Agrega `;` al final:
```opn
opn> let x = 10;  # ✅ Correcto
```

### La ventana gráfica no aparece

**Problema**: Olvidaste `update_screen()`

**Solución**:
```opn
opn> gfx.setup_canvas(400, 400, "Test");
opn> gfx.draw_circle(200, 200, 50, "Azul");
opn> gfx.update_screen();  # ¡Importante!
```

---

## Próximos Pasos

- Practica con los [Ejemplos de Gráficos](gfx_examples.md)
- Consulta la [Referencia del Lenguaje](language_reference.md)
- Lee sobre la [API de Gráficos](gfx_api.md)

---

**Relacionado**:
- [← Primeros Pasos](getting_started.md)
- [Referencia del Lenguaje →](language_reference.md)
- [← Volver al Índice](README.md)
