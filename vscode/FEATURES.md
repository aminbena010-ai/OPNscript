# VSCode Editor OPN - Guía de Características

## 🚀 Características Avanzadas Implementadas

### 1. **Auto-Indentación Automática**
Cuando presionas **Enter**, el editor mantiene automáticamente el nivel de indentación y suma espacios adicionales si hay brackets abiertos.

**Ejemplo:**
```opn
func saludar() {    ← Presiona Enter aquí
    let x = 1;      ← Auto-indentado 4 espacios
    if x > 0 {      ← Presiona Enter aquí
        py.print(x) ← Auto-indentado 8 espacios (4 + 4 extra por {)
```

---

### 2. **Auto-Cierre de Símbolos Inteligente**

#### Brackets
- Escribe `{` → Se cierra automáticamente: `{}`
- Escribe `[` → Se cierra automáticamente: `[]`
- Escribe `(` → Se cierra automáticamente: `()`

#### Comillas
- Escribe `"` → Se cierra automáticamente: `""`
- Escribe `'` → Se cierra automáticamente: `''`

**Características Inteligentes:**
- Si el siguiente carácter es el cierre, salta al siguiente sin duplicar
- No duplica si el cierre ya existe
- Respeta caracteres escapados (`\"`)

---

### 3. **Detección de Errores en Tiempo Real**

El editor detecta y marca errores de sintaxis con **subrayado ondulado rojo** (estilo VS Code):

#### Errores Detectados:
✗ Instrucciones sin `;` 
```opn
let numero = 42  ← ERROR: Falta punto y coma
```

✗ Brackets sin cerrar
```opn
if true {        ← ERROR: No hay cierre }
```

✗ Strings sin cerrar
```opn
let msg = "Hola  ← ERROR: String abierto
```

---

### 4. **Tipografía Profesional de VS Code**

Soporta las mejores fuentes monoespaciadas:
1. **Fira Code** (recomendada - con ligaduras)
2. Monaco
3. Consolas
4. DejaVu Sans Mono

El editor selecciona automáticamente la mejor disponible en tu sistema.

---

### 5. **Ejecución Completa de Lenguajes**

Presiona **F5** o ve a **Ejecutar → Ejecutar Archivo** para ejecutar:

#### Archivos OPN/Prisma
```
# Tu código OPN se ejecuta con:
# python -m prisma.cli run archivo.opn
```

#### Archivos Python
```python
# Tu código Python se ejecuta con:
# python archivo.py
```

#### Archivos JavaScript
```javascript
// Tu código JavaScript se ejecuta con:
// node archivo.js
```

**Salida en Consola:**
- Presiona **Ctrl+`** para mostrar/ocultar la consola
- Ver salida estándar y errores en tiempo real

---

## 📋 Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| **F5** | Ejecutar archivo actual |
| **Ctrl+`** | Mostrar/Ocultar consola |
| **Ctrl+N** | Nuevo archivo |
| **Ctrl+O** | Abrir archivo |
| **Ctrl+S** | Guardar |
| **Ctrl+Shift+S** | Guardar como |
| **Ctrl+F** | Buscar/Reemplazar |
| **Ctrl+Shift+E** | Mostrar/Ocultar explorador |
| **Ctrl+Shift+M** | Mostrar/Ocultar minimapa |
| **Ctrl+L** | Mostrar/Ocultar numeración |

---

## 🎨 Tema y Colores

### Colores Configurados para OPN:

| Elemento | Color | Uso |
|----------|-------|-----|
| Palabras clave | Azul (#569CD6) | `func`, `main`, `let`, `set`, `if`, `for`, etc. |
| Strings | Naranja (#CE9178) | `"texto"`, `'caracteres'` |
| Números | Verde (#B5CEA8) | `42`, `3.14`, `100` |
| Funciones | Amarillo (#DCDCAA) | `py.print()`, `gfx.draw_circle()` |
| Variables | Celeste (#9CDCFE) | Identificadores de usuario |
| Comentarios | Verde oscuro (#6A9955) | `# Esto es un comentario` |
| Errores | Rojo (#F44747) | Subrayado ondulado en errores |

---

## 💡 Consejos Útiles

### Auto-Completado
Mientras escribes, el editor sugiere:
- Palabras clave OPN
- Funciones de la API (`gfx.*`, `py.*`, `js.*`, etc.)
- Variables definidas

Navega con **↑↓** y presiona **Tab** o **Enter** para aceptar.

### Múltiples Archivos
- Abre varios archivos en pestañas
- Auto-guardado cada 60 segundos
- Notificación con `*` si tiene cambios sin guardar

### Explorador de Archivos
- Presiona **Ctrl+Shift+E** para abrir explorador
- Haz doble clic en archivos para abrirlos
- Los archivos `.opn` se reconocen automáticamente

---

## 🔧 Configuración de Archivos

### `recursos/extensions.json`
Define qué extensión usa qué lenguaje:
```json
{
  "opn": "opn",
  "py": "python",
  "js": "javascript"
}
```

### `recursos/colores.json`
Define colores y reglas de sintaxis para cada lenguaje:
```json
{
  "palette": {
    "keyword": "#569CD6",
    ...
  },
  "languages": {
    "opn": {
      "rules": [...],
      "completions": [...],
      "execution_command": "..."
    }
  }
}
```

---

## 📝 Archivos de Ejemplo

Prueba con `test_example.opn`:
```opn
# Ejemplo completo de OPN
func saludar(nombre) {
    return "Hola, " + nombre;
}

main {
    let numero = 42;
    if numero > 10 {
        py.print(saludar("Usuario"));
    }
    for i in 1..5 {
        py.print(i);
    }
}
```

---

## 🐛 Resolución de Problemas

**P: El editor no se abre**
- Asegúrate de tener PyQt6 instalado: `pip install PyQt6`

**P: OPN no ejecuta**
- Verifica que el módulo `prisma` esté instalado
- Intenta: `python -m prisma.cli run archivo.opn`

**P: No hay colores en el editor**
- Verifica que `recursos/colores.json` esté en la carpeta `vscode/`
- Comprueba que los archivos JSON sean válidos

**P: Auto-indentación no funciona**
- Presiona Enter para nuevas líneas
- El editor calcula automáticamente la indentación

---

## 📚 Recursos Adicionales

- Documentación OPN: `docs/language_reference.md`
- Sintaxis OPN: `docs/syntax.md`
- Variables: `docs/variables.md`
- Ejemplos de prueba: `tests/main.opn`

---

**¡El editor está listo para desarrollo profesional en OPN!** 🎉
