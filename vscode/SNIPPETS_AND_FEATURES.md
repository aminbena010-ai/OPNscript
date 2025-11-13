# Nuevas Características - Editor OPN v2.0

## Características Principales Agregadas

### 1. **Sistema de Snippets/Atajos Automáticos** ⚡

Cuando escribes palabras clave seguidas de espacio, se expanden automáticamente con la estructura correcta.

#### Snippets OPN:
- `main` → `main { }`
- `func` → `func name() { }`
- `if` → `if condition { }`
- `ifelse` → `if condition { } else { }`
- `for` → `for item in collection { }`
- `let` → `let variable = value;`
- `set` → `set variable = value;`
- `return` → `return value;`
- `print` → `py.print(value);`
- `input` → `py.input(prompt);`

#### Snippets Python:
- `def` → `def function_name(): pass`
- `class` → `class ClassName: def __init__(self): pass`
- `if` → `if condition: pass`
- `for` → `for item in collection: pass`
- `while` → `while condition: pass`
- `try` → `try: except Exception as e: pass`
- `import` → `import module`
- `from` → `from module import name`

#### Snippets JavaScript:
- `function` → `function name() { }`
- `const` → `const variable = value;`
- `let` → `let variable = value;`
- `if` → `if (condition) { }`
- `for` → `for (let i = 0; i < max; i++) { }`
- `arrow` → `const name = () => { };`
- `class` → `class Name { constructor() { } }`
- `async` → `async function name() { }`

**Cómo Funciona:**
1. Escribe una palabra clave (ej: `main`)
2. Presiona **Espacio**
3. El editor automáticamente:
   - Reemplaza la palabra con la estructura completa
   - Agrega la indentación correcta
   - Posiciona el cursor para que comiences a escribir

### 2. **Autocompletado Mejorado con Descripciones** 📚

El sistema de autocompletado ahora muestra descripciones útiles para cada sugerencia.

**Ejemplo:**
```
py.print - Imprimir en consola
py.input - Leer entrada del usuario
gfx.draw_circle - Dibujar un círculo
```

**Cómo Acceder:**
- Presiona **Ctrl+Espacio** en cualquier momento
- Comienza a escribir una palabra clave
- Ve las sugerencias con sus descripciones
- Selecciona con flecha arriba/abajo
- Presiona **Enter** o **Tab** para insertar

**Características:**
- Las descripciones se muestran en el popup de autocompletado
- Si seleccionas un snippet, se expande automáticamente
- Compatible con OPN, Python y JavaScript
- 39+ palabras clave con descripciones

### 3. **Reconocimiento Mejorado de Comentarios** 💬

El editor ahora reconoce correctamente comentarios con:
- `#` para OPN y Python
- `//` para JavaScript y comentarios simples
- `/* */` para comentarios de bloque en JavaScript

Los comentarios:
- Se colorean con color verde (#6A9955)
- No interfieren con el resto del código
- Se reconocen sin romper la sintaxis

### 4. **Configuración Centralizada de Snippets** ⚙️

Archivo: `recursos/snippets.json`

Estructura de un snippet:
```json
{
  "main": {
    "body": "main {\n    $0\n}",
    "description": "Bloque principal del programa",
    "scope": "global"
  }
}
```

- `body`: Contenido del snippet con variables (`$0`, `$1`, `$2`)
- `description`: Texto que se muestra en el autocompletado
- `scope`: Dónde se puede usar (global, any, function)

**Ampliable:**
Puedes agregar nuevos snippets editando `recursos/snippets.json` directamente.

---

## Casos de Uso

### Caso 1: Escribir un Programa OPN Rápidamente
```
1. Escribir: main
2. Presionar: Espacio
3. Resultado automático:
   main {
       |  <- Cursor aquí
   }
4. Escribe el código dentro del bloque
```

### Caso 2: Crear una Función Python
```
1. Escribir: def
2. Presionar: Espacio
3. Resultado:
   def function_name():
       |  <- Cursor aquí
```

### Caso 3: Usar Autocompletado con Descripción
```
1. Presionar: Ctrl+Espacio
2. Escribir: py
3. Ver sugerencias:
   - py.print - Imprimir en consola
   - py.input - Leer entrada del usuario
   - py.random.randint - Número aleatorio
4. Seleccionar: py.print
5. Resultado: py.print(|) <- Cursor dentro de paréntesis
```

---

## Archivos Modificados/Creados

- ✅ `VSeditor.py` - Lógica de snippets, autocompletado mejorado
- ✅ `recursos/snippets.json` - **NUEVO** - Configuración de snippets
- ✅ `recursos/colores.json` - Sin cambios (compatible)
- ✅ `recursos/extensions.json` - Sin cambios (compatible)

---

## Cómo Personalizar

### Agregar un Nuevo Snippet OPN

Edita `recursos/snippets.json` y agrega:
```json
"tu_snippet": {
  "body": "contenido con $0 para cursor final",
  "description": "Descripción que verás en autocompletado",
  "scope": "any"
}
```

### Agregar una Palabra Clave al Autocompletado

Edita `recursos/colores.json`:
```json
"completions": [
  "main",
  "func",
  "tu_palabra_nueva"
]
```

---

## Funcionalidades Técnicas

### Sistema de Snippets
- Detecta palabras clave al escribir espacio
- Valida que sea una línea independiente (sin código antes)
- Expande con indentación automática correcta
- Soporta variables en snippets (`$0`, `$1`, `$2`)

### Modelo de Autocompletado
- Clase personalizada `CompletionModel` que extiende `QStringListModel`
- Muestra nombre + descripción en el popup
- Recupera automáticamente solo el nombre al insertar

### Gestión de Configuración
- Carga automática de `snippets.json` al iniciar
- Almacenado en variable global `SNIPPETS_CONFIG`
- Por lenguaje: OPN, Python, JavaScript

---

## Atajos de Teclado

| Atajo | Función |
|-------|---------|
| **Espacio** (después de palabra clave) | Expande snippet |
| **Ctrl+Espacio** | Abre autocompletado |
| **Enter/Tab** | Selecciona opción de autocompletado |
| **Flecha arriba/abajo** | Navega autocompletado |
| **Esc** | Cierra autocompletado |

---

## Ejemplos Completos

### Ejemplo 1: Programa OPN Completo
```
// Escribir:
main
[Espacio]
let x = 10
[Enter]
if x > 5
[Espacio]

// Resultado automático:
main {
    let x = 10;
    if x > 5 {
        |
    }
}
```

### Ejemplo 2: Función con Print
```
// Escribir:
func
[Espacio]
[Autocompletado aparece]
[Seleccionar "py.print"]

// Resultado:
func function_name() {
    py.print(|);
}
```

---

## Compatibilidad

- ✅ Windows 10/11
- ✅ Python 3.8+
- ✅ PyQt6
- ✅ OPN (v1+)
- ✅ Python 3.x
- ✅ JavaScript (Node.js)

---

## Versión

**v2.0** - Noviembre 2025  
**Estado**: Producción ✅

---

## Próximas Mejoras Planeadas

- [ ] Snippets con saltos de cursor (Tab para siguiente variable)
- [ ] Modo "zen" (distracción mínima)
- [ ] Temas adicionales
- [ ] Depurador integrado
- [ ] Extensiones de plugins
- [ ] Soporte para más lenguajes
