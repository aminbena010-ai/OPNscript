# Primeros Pasos con OPN

Guía rápida para comenzar a programar en OPN.

## Tabla de Contenidos

- [Tu Primer Programa](#tu-primer-programa)
- [Conceptos Básicos](#conceptos-básicos)
- [Primer Programa Gráfico](#primer-programa-gráfico)
- [Usando el REPL](#usando-el-repl)
- [Próximos Pasos](#próximos-pasos)

---

## Tu Primer Programa

### Hola Mundo

Crea un archivo llamado `hola.opn`:

```opn
main {
    py.print("¡Hola, Mundo!");
}
```

**Ejecutar**:

```bash
cd prisma-lang/src
python -m prisma run hola.opn
```

**Salida**:
```
¡Hola, Mundo!
```

### Explicación

- `main { }`: Bloque principal del programa (punto de entrada)
- `py.print()`: Función para imprimir en consola
- `;`: Cada instrucción termina con punto y coma

---

## Conceptos Básicos

### Variables

```opn
main {
    # Declarar variable
    let nombre = "Ana";
    let edad = 25;
    
    # Imprimir
    py.print("Nombre:", nombre);
    py.print("Edad:", edad);
    
    # Modificar variable
    set edad = 26;
    py.print("Nueva edad:", edad);
}
```

**Reglas**:
- `let` para declarar
- `set` para modificar
- Los nombres son case-sensitive

### Operaciones Matemáticas

```opn
main {
    let a = 10;
    let b = 5;
    
    py.print("Suma:", a + b);
    py.print("Resta:", a - b);
    py.print("Multiplicación:", a * b);
    py.print("División:", a / b);
}
```

### Condicionales

```opn
main {
    let edad = 18;
    
    if edad >= 18 {
        py.print("Eres mayor de edad");
    } else {
        py.print("Eres menor de edad");
    }
}
```

### Bucles

```opn
main {
    # Contar del 1 al 5
    for i in 1..5 {
        py.print("Número:", i);
    }
}
```

### Funciones

```opn
func saludar(nombre) {
    py.print("¡Hola,", nombre, "!");
}

main {
    saludar("Carlos");
    saludar("María");
}
```

---

## Primer Programa Gráfico

### Círculo Simple

Crea `circulo.opn`:

```opn
main {
    # Configurar ventana
    gfx.setup_canvas(400, 400, "Mi Primer Círculo");
    
    # Dibujar círculo rojo en el centro
    gfx.draw_circle(200, 200, 80, "Rojo");
    
    # Mostrar ventana
    gfx.update_screen();
}
```

**Ejecutar**:
```bash
python -m prisma run circulo.opn
```

### Múltiples Formas

```opn
main {
    gfx.setup_canvas(600, 400, "Formas");
    
    # Tres círculos de diferentes colores
    gfx.draw_circle(150, 200, 60, "Rojo");
    gfx.draw_circle(300, 200, 60, "Verde");
    gfx.draw_circle(450, 200, 60, "Azul");
    
    # Puntos decorativos
    gfx.draw_point(150, 100, "Amarillo");
    gfx.draw_point(300, 100, "Amarillo");
    gfx.draw_point(450, 100, "Amarillo");
    
    gfx.update_screen();
}
```

### Patrón con Bucle

```opn
main {
    gfx.setup_canvas(800, 200, "Patrón");
    
    # Dibujar 10 círculos en línea
    for i in 1..10 {
        let x = i * 80;
        gfx.draw_circle(x, 100, 30, "Púrpura");
    }
    
    gfx.update_screen();
}
```

---

## Usando el REPL

### Iniciar el REPL

```bash
cd prisma-lang/src
python -m prisma
```

Verás:
```
OPN Interactive Shell
Type 'exit' to quit, 'cls' to clear screen
opn>
```

### Comandos Básicos

**Imprimir**:
```opn
opn> py.print("Hola desde REPL");
Hola desde REPL
```

**Variables**:
```opn
opn> let x = 10;
opn> let y = 20;
opn> py.print(x + y);
30
```

**Gráficos**:
```opn
opn> gfx.setup_canvas(300, 300, "REPL Test");
opn> gfx.draw_circle(150, 150, 50, "Verde");
opn> gfx.update_screen();
```

### Comandos Especiales

- `exit` o `exit;` - Salir del REPL
- `cls` o `clear` - Limpiar pantalla
- `!comando` - Ejecutar comando del sistema

**Ejemplos**:
```opn
opn> cls
# Limpia la pantalla

opn> !dir
# Lista archivos (Windows)

opn> !ls
# Lista archivos (Linux/Mac)

opn> exit
# Sale del REPL
```

---

## Programa Completo de Ejemplo

### Calculadora Simple

```opn
func sumar(a, b) {
    return a + b;
}

func restar(a, b) {
    return a - b;
}

func multiplicar(a, b) {
    return a * b;
}

func dividir(a, b) {
    if b == 0 {
        py.print("Error: División por cero");
        return 0;
    }
    return a / b;
}

main {
    let num1 = 10;
    let num2 = 5;
    
    py.print("Números:", num1, "y", num2);
    py.print("Suma:", sumar(num1, num2));
    py.print("Resta:", restar(num1, num2));
    py.print("Multiplicación:", multiplicar(num1, num2));
    py.print("División:", dividir(num1, num2));
}
```

### Dibujo Interactivo

```opn
func dibujar_fila(y, color) {
    for i in 1..10 {
        let x = i * 60;
        gfx.draw_circle(x, y, 20, color);
    }
}

main {
    gfx.setup_canvas(600, 400, "Filas de Colores");
    
    dibujar_fila(80, "Rojo");
    dibujar_fila(160, "Verde");
    dibujar_fila(240, "Azul");
    dibujar_fila(320, "Amarillo");
    
    gfx.update_screen();
}
```

---

## Errores Comunes

### 1. Olvidar el punto y coma

❌ **Incorrecto**:
```opn
let x = 10
py.print(x)
```

✅ **Correcto**:
```opn
let x = 10;
py.print(x);
```

### 2. Usar `set` en lugar de `let`

❌ **Incorrecto**:
```opn
set nombre = "Juan";  # Error: variable no declarada
```

✅ **Correcto**:
```opn
let nombre = "Juan";  # Primero declarar
set nombre = "Pedro"; # Luego modificar
```

### 3. Olvidar `gfx.setup_canvas()`

❌ **Incorrecto**:
```opn
main {
    gfx.draw_circle(200, 200, 50, "Rojo");  # Error!
    gfx.update_screen();
}
```

✅ **Correcto**:
```opn
main {
    gfx.setup_canvas(400, 400, "Ventana");
    gfx.draw_circle(200, 200, 50, "Rojo");
    gfx.update_screen();
}
```

### 4. Olvidar `gfx.update_screen()`

❌ **Incorrecto**:
```opn
main {
    gfx.setup_canvas(400, 400, "Ventana");
    gfx.draw_circle(200, 200, 50, "Rojo");
    # No se ve nada porque falta update_screen()
}
```

✅ **Correcto**:
```opn
main {
    gfx.setup_canvas(400, 400, "Ventana");
    gfx.draw_circle(200, 200, 50, "Rojo");
    gfx.update_screen();  # ¡Importante!
}
```

---

## Consejos para Principiantes

1. **Empieza simple**: Comienza con programas pequeños y ve agregando complejidad
2. **Usa el REPL**: Experimenta con comandos antes de escribir programas completos
3. **Comenta tu código**: Usa `#` para explicar qué hace cada parte
4. **Prueba frecuentemente**: Ejecuta tu código después de cada cambio
5. **Lee los errores**: Los mensajes de error te indican qué está mal

---

## Ejercicios Prácticos

### Ejercicio 1: Variables y Operaciones

Crea un programa que:
1. Declare dos variables numéricas
2. Calcule suma, resta, multiplicación y división
3. Imprima los resultados

### Ejercicio 2: Bucle Simple

Crea un programa que imprima los números del 1 al 10.

### Ejercicio 3: Función de Saludo

Crea una función que reciba un nombre y edad, y salude personalizadamente.

### Ejercicio 4: Tres Círculos

Dibuja tres círculos de diferentes tamaños y colores.

### Ejercicio 5: Patrón de Puntos

Usa un bucle para dibujar 20 puntos en línea horizontal.

---

## Próximos Pasos

Ahora que conoces lo básico:

1. **Explora la [Referencia del Lenguaje](language_reference.md)** para aprender más sintaxis
2. **Prueba los [Ejemplos de Gráficos](gfx_examples.md)** para proyectos más complejos
3. **Consulta la [API de Gráficos](gfx_api.md)** para todas las funciones disponibles
4. **Lee sobre el [REPL](repl.md)** para uso avanzado de la consola

---

**Relacionado**:
- [← Instalación](installation.md)
- [Referencia del Lenguaje →](language_reference.md)
- [Ejemplos de Gráficos →](gfx_examples.md)
- [← Volver al Índice](README.md)
