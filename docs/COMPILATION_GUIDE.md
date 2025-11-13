# OPNscript - Sistema de Compilación & Paquetes

Guía completa de compilación y sistema de paquetes de OPNscript.

## Comandos de Compilación

### 1. Build Rápido (Recomendado)

Compila un directorio con archivos `.prisma` en un paquete autocontendido.

```bash
prisma build <source_path> [-n nombre] [-v versión]
```

**Ejemplo:**
```bash
# Compilar carpeta 'src' con nombre automático
prisma build ./src

# Compilar con nombre específico
prisma build ./src -n mi_paquete -v 2.1.0
```

**Genera:**
- `{nombre}_build/index.prisma` - Código compilado
- `{nombre}_build/functions.json` - Documentación
- `{nombre}_build/{nombre}.opn` - Metadatos

---

### 2. Compile Avanzado

Para proyectos con metadatos personalizados.

```bash
prisma compile <project_path> \
  -o <output_dir> \
  -n <name> \
  [-v version] \
  [-d description] \
  [-a author]
```

**Ejemplo:**
```bash
prisma compile ./mylib \
  -o ./dist \
  -n mylib \
  -v 3.0.0 \
  -d "Advanced graphics library" \
  -a "Jane Developer"
```

---

## Comandos de Configuración

### Inicializar Config

```bash
prisma config init
```

Crea archivos de configuración en `~/.opn/config/`:
- `packages.json` - Paquetes registrados
- `paths.json` - Rutas de búsqueda
- `settings.json` - Configuración global

### Ver Configuración

```bash
prisma config show
```

Muestra información completa de:
- Paquetes registrados
- Rutas de búsqueda
- Configuración actual

### Agregar Rutas

```bash
# Agregar ruta de búsqueda de código fuente
prisma config add-source /path/to/source

# Agregar ruta de búsqueda de paquetes
prisma config add-package /path/to/packages
```

---

## Auto-Corrección de Rutas

### Fix Paths

Escanea un proyecto y valida imports automáticamente.

```bash
prisma fix-paths <project_path>
```

**Ejemplo:**
```bash
prisma fix-paths ./my_app
```

**Salida:**
```
[FIX-PATHS] Scan complete
  Project: ./my_app
  Files scanned: 5
  Total corrections: 2
```

---

## Imports en OPNscript

### Sintaxis Básica

```prisma
import package_name;

func main() {
    package_name.function_name(args);
}
```

### Cómo Funciona

1. **Búsqueda automática** en:
   - `./opn.import/package_name/`
   - `~/.opn/packages/package_name/`
   - Rutas personalizadas

2. **Carga automática** de `index.prisma`

3. **Funciones disponibles** sin prefijo

### Ejemplo

```prisma
import render;
import math;

func main() {
    let x = math.add(10, 20);
    render.draw_circle(400, 300, x, render.color_red());
}
```

---

## Archivos Generados

### .opn (Metadatos)

```json
{
  "name": "mylib",
  "version": "1.0.0",
  "description": "My awesome library",
  "author": "John Doe",
  "main": "index.prisma",
  "functions": ["func1", "func2", ...]
}
```

### functions.json (Documentación Completa)

```json
{
  "metadata": {
    "version": "1.0.0",
    "generatedAt": "2025-11-12T20:00:00",
    "generatedBy": "OPN Compiler"
  },
  "statistics": {
    "sourceFiles": 2,
    "totalFunctions": 8,
    "categories": 3
  },
  "configuration": {
    "layers": {...},
    "autoCompletion": {...},
    "ide": {...}
  },
  "categories": {...},
  "functions": [...]
}
```

### index.prisma (Código Compilado)

Código OPN consolidado de todos los archivos fuente.

---

## Archivos de Configuración

### ~/.opn/config/packages.json

```json
{
  "version": "1.0.0",
  "packages": [
    {
      "name": "render",
      "version": "1.0.0",
      "path": "/path/to/render_build",
      "main": "index.prisma",
      "addedAt": "2025-11-12T20:00:00"
    }
  ]
}
```

### ~/.opn/config/paths.json

```json
{
  "version": "1.0.0",
  "sourcePaths": ["/path/to/src"],
  "packagePaths": [
    "./opn.import",
    "~/.opn/packages"
  ],
  "outputPath": "./opn_build"
}
```

### ~/.opn/config/settings.json

```json
{
  "version": "1.0.0",
  "autoCorrectPaths": true,
  "autoCompile": false,
  "targetLanguage": "python",
  "debugMode": false,
  "encoding": "utf-8"
}
```

---

## Casos de Uso

### Caso 1: Compilar Proyecto Simple

```bash
# 1. Estructura de carpetas
# src/
#   math.prisma
#   string.prisma

# 2. Compilar
prisma build src -n utils -v 1.0.0

# 3. Usar en otro proyecto
# import utils;
```

### Caso 2: Crear Librería Compleja

```bash
# 1. Compilación avanzada
prisma compile ./mylib \
  -o ./release \
  -n mylib \
  -v 3.0.0 \
  -d "Advanced library" \
  -a "Jane Developer"

# 2. Registrar paquete
prisma config add-package ./release

# 3. Verificar
prisma config show
```

### Caso 3: Gestionar Múltiples Paquetes

```bash
# 1. Compilar varios
prisma build ./math -n math
prisma build ./graphics -n graphics
prisma build ./utils -n utils

# 2. Verificar
prisma config show

# 3. Usar en código
# import math;
# import graphics;
# import utils;
```

### Caso 4: Auto-Corrección

```bash
# 1. Tengo proyecto con imports
# import oldname;

# 2. Renombro paquete
prisma build ./src -n newname

# 3. Corro fix-paths
prisma fix-paths ./my_project

# 4. Reviso cambios
# import newname;  ✓
```

---

## Características Principales

### Compilación Automática
- ✓ Consolidación de múltiples archivos
- ✓ Extracción automática de funciones
- ✓ Generación de metadatos
- ✓ Documentación automática

### Gestión de Configuración
- ✓ Configuración centralizada en `~/.opn/`
- ✓ Gestión de rutas de búsqueda
- ✓ Registro automático de paquetes
- ✓ Validación de imports

### Imports Inteligentes
- ✓ Búsqueda automática en múltiples rutas
- ✓ Carga automática de índices
- ✓ Soporte para paquetes personalizados
- ✓ Auto-corrección de imports

### IDE Integration
- ✓ Autocompletado en VSEditor.py
- ✓ Documentación en tiempo real
- ✓ Validación de funciones
- ✓ Información de parámetros

---

## Troubleshooting

### Paquete no encontrado

```
Error: Package 'mylib' not found
```

**Soluciones:**
1. Verificar que existe `./opn.import/mylib/index.prisma`
2. Ejecutar: `prisma config add-package /path/to/packages`
3. Ejecutar: `prisma fix-paths ./my_project`

### Funciones no aparecen

```
Error: 'undefined' is not a function
```

**Soluciones:**
1. Verificar que la función existe en `functions.json`
2. Verificar que la función está en `.opn` (lista de funciones)
3. Recompilar: `prisma build ./src -n package_name`

### Rutas incorrectas

**Solución:**
```bash
# Auto-corregir todas las rutas
prisma fix-paths ./my_project
```

---

## Próximos Pasos

1. Lee [opn.import/BUILD_SYSTEM.md](opn.import/BUILD_SYSTEM.md) para más detalles
2. Lee [opn.import/QUICK_START.md](opn.import/QUICK_START.md) para ejemplos
3. Lee [opn.import/TEMPLATE.md](opn.import/TEMPLATE.md) para crear paquetes
4. Consulta [opn.import/INTEGRATION.md](opn.import/INTEGRATION.md) para VSEditor

---

**Versión**: 1.0.0
**Última actualización**: 2025-11-12
**Sistema**: OPN Compilation & Package System
