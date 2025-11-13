# VS Code Editor para OPN

**Un editor profesional basado en PyQt6 optimizado para el lenguaje OPN**

## 🎯 Descripción General

VSEditor es un editor de código de escritorio similar a VS Code que proporciona:

- ✅ **Resaltado de sintaxis** avanzado para OPN, Python, JavaScript
- ✅ **Auto-indentación** inteligente con detección de brackets
- ✅ **Auto-cierre** de símbolos `{}`, `[]`, `()`, `""`, `''`
- ✅ **Detección de errores** en tiempo real con subrayado rojo
- ✅ **Autocompletado** contextual desde archivos de configuración
- ✅ **Ejecución de código** nativa (F5) con consola integrada
- ✅ **Minimapa** de navegación rápida
- ✅ **Explorador de archivos** integrado
- ✅ **Tema oscuro** de VS Code
- ✅ **Numeración de líneas** y búsqueda/reemplazo

## 🚀 Instalación y Ejecución

### Requisitos
```bash
pip install PyQt6
```

### Inicio del Editor
```bash
python vscode/VSeditor.py
```

O desde Windows PowerShell:
```powershell
python .\vscode\VSeditor.py
```

## 📁 Estructura de Archivos

```
vscode/
├── VSeditor.py              # Editor principal
├── FEATURES.md              # Guía completa de características
├── README_EDITOR.md         # Este archivo
├── test_example.opn         # Archivo de prueba
└── recursos/
    ├── colores.json         # Configuración de colores y sintaxis
    └── extensions.json      # Mapeo de extensiones a lenguajes
```

## 🎨 Interfaz

```
┌─ Activity Bar ─┬─────────────────────── Pestañas ──────────────────┐
│  🗂 Explorador │  ⦿ archivo.opn*    ⦾ otro.py                      │
│  🔎 Buscar     │┌────────────────────────────────────────────────────┤
│  🔄 Control    ││ 1   # Comentario                                   │
│  ▶ Debugger    ││ 2   func saludar(nombre) {           │ Minimapa   │
│  🧩 Extensiones││ 3       return "Hola " + nombre;     │ ▓▓▓▓▓▓▓▓   │
│                ││ 4   }                                  │ ▓▓▓▓▓▓    │
│                ││ 5                                      │ ▓▓▓▓▓▓▓▓  │
│                ││ 6   main {                             │ ▓▓▓▓▓▓    │
│                ├────────────────────────────────────────────────────┤
│  Explorador    │ [Consola/Output]                       F5 Ejecutar│
│                │ --- Ejecutando: python -m prisma.cli  │           │
│                │ Hola Usuario                           │           │
│                │ [Proceso finalizado]                   │           │
└────────────────┴────────────────────────────────────────────────────┘
```

## 🛠 Características Principales

### 1️⃣ **Auto-Indentación**
```
Antes: func foo() {↵     (presionas Enter)
Después: func foo() {
         ↵               (4 espacios automáticos)
```

### 2️⃣ **Auto-Cierre de Símbolos**
```
Escribes: {  →  Genera: {}  (cursor entre ellos)
Escribes: [  →  Genera: []
Escribes: "  →  Genera: ""
```

### 3️⃣ **Errores Detectados**
```
let numero = 42  ← Subrayado rojo (falta ;)
if x > 0 {       ← Subrayado rojo (falta })
```

### 4️⃣ **Ejecución de Código**
```
Archivo: programa.opn
Presiona: F5
Resultado: Ejecuta con `python -m prisma.cli run programa.opn`
Salida: Mostrada en la consola integrada
```

## 🎮 Controles Principales

| Tecla | Función |
|-------|---------|
| `F5` | Ejecutar archivo actual |
| `Ctrl+N` | Nuevo archivo |
| `Ctrl+O` | Abrir archivo |
| `Ctrl+S` | Guardar |
| `Ctrl+Shift+S` | Guardar como |
| `Ctrl+F` | Buscar/Reemplazar |
| `Ctrl+Shift+E` | Explorador |
| `Ctrl+` ` | Consola |
| `Ctrl+Z` | Deshacer |
| `Ctrl+Y` | Rehacer |

## 📚 Configuración

### Agregar Nuevos Lenguajes

**1. Edita `recursos/extensions.json`:**
```json
{
  "mappings": {
    "rs": "rust",
    "go": "golang"
  }
}
```

**2. Edita `recursos/colores.json`:**
```json
{
  "languages": {
    "rust": {
      "rules": [
        ["\\bfn\\b", "keyword", "bold"],
        ["\\\"[^\\\"]*\\\"", "string", ""]
      ],
      "completions": ["fn", "let", "mut"],
      "execution_command": "rustc {file} && {file}.exe"
    }
  }
}
```

## 🐍 Ejemplos de Uso

### Ejecutar Código OPN
```opn
# archivo.opn
main {
    let numero = 42;
    py.print("Respuesta: " + numero);
}
```
Presiona F5 → Salida: `Respuesta: 42`

### Ejecutar Python
```python
# script.py
print("Hola desde Python")
for i in range(5):
    print(i)
```
Presiona F5 → Salida mostrada en consola

### Ejecutar JavaScript
```javascript
// programa.js
console.log("Hola desde JS");
```
Presiona F5 → Requiere Node.js instalado

## 🔍 Sistema de Autocompletado

El editor sugiere automáticamente:

```
Digitas: py.pr[TAB] → Completa a: py.print(
Digitas: let[TAB]   → Completa a: let
Digitas: gfx.dr[TAB] → Completa a: gfx.draw_circle(
```

Palabras disponibles para OPN:
- Keywords: `func`, `main`, `let`, `set`, `return`, `if`, `for`, `and`, `or`
- APIs: `py.print`, `py.input`, `js.log`, `gfx.draw_circle`, `gfx.draw_rect`
- Utilidades: `to_string`, `to_number`

## 📊 Monitoreo de Cambios

- **Auto-guardado** cada 60 segundos (solo archivos con ruta)
- **Indicador de cambios** con `*` en la pestaña
- **Confirmación** al cerrar archivos sin guardar

## 🎨 Paleta de Colores

| Elemento | Color | Uso |
|----------|-------|-----|
| Fondo | #1E1E1E | Fondo principal |
| Texto | #D4D4D4 | Texto normal |
| Keywords | #569CD6 | `func`, `let`, `main` |
| Strings | #CE9178 | `"texto"` |
| Números | #B5CEA8 | `42`, `3.14` |
| Funciones | #DCDCAA | `print()`, `draw_circle()` |
| Errores | #F44747 | Subrayado ondulado rojo |

## 🐛 Requisitos del Sistema

- **Python** 3.8+
- **PyQt6** (instalar con `pip install PyQt6`)
- **Sistema Operativo**: Windows, macOS, Linux
- **Pantalla**: Resolución mínima 800x600

## 🔗 Dependencias Opcionales

Para ejecutar código OPN:
```bash
pip install opn-language
# O instala desde el directorio prisma-lang:
pip install ./prisma-lang
```

Para ejecutar JavaScript:
```bash
# Instala Node.js desde https://nodejs.org
```

## 📝 Notas

- El editor se enfoca en **OPN** pero soporta múltiples lenguajes
- La configuración se carga automáticamente desde JSON
- Los cambios de configuración requieren reiniciar el editor
- El minimapa proporciona navegación rápida en archivos grandes

## 🤝 Contribuciones

Para mejorar el editor:
1. Modifica `recursos/colores.json` para añadir lenguajes
2. Edita `VSeditor.py` para nuevas características
3. Prueba con diferentes tipos de archivos

## 📄 Licencia

Este editor es parte del proyecto OPN Language.

---

**¡Disfruta desarrollando en OPN!** 🚀
