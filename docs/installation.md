# Instalación de OPN

Guía completa para instalar y configurar el lenguaje de programación OPN en tu sistema.

## Tabla de Contenidos

- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Verificación](#verificación)
- [Configuración del Editor](#configuración-del-editor)
- [Solución de Problemas](#solución-de-problemas)

---

## Requisitos del Sistema

### Software Necesario

- **Python 3.8 o superior**
- **Tkinter** (incluido con Python en la mayoría de instalaciones)
- **Sistema Operativo**: Windows, macOS, o Linux

### Verificar Python

```bash
python --version
```

Debe mostrar Python 3.8 o superior.

### Verificar Tkinter

```bash
python -c "import tkinter; print('Tkinter OK')"
```

Si muestra "Tkinter OK", está instalado correctamente.

---

## Instalación

### Opción 1: Desde el Código Fuente

1. **Clonar o descargar el repositorio**:

```bash
git clone https://github.com/aminbena010-ai/OPNscript.git
cd OPNscript
```

2. **Navegar al directorio del proyecto**:

```bash
cd prisma-lang/src
```

3. **Ejecutar OPN**:

```bash
python -m prisma
```

### Opción 2: Instalación con pip (Próximamente)

```bash
pip install opn-lang
```

---

## Verificación

### Probar la Instalación

1. **Iniciar el REPL**:

```bash
cd prisma-lang/src
python -m prisma
```

Deberías ver:

```
OPN Interactive Shell
Type 'exit' to quit, 'cls' to clear screen
opn>
```

2. **Ejecutar un comando simple**:

```opn
opn> py.print("Hola, OPN!");
Hola, OPN!
```

3. **Probar gráficos**:

```opn
opn> gfx.setup_canvas(400, 400, "Test");
opn> gfx.draw_circle(200, 200, 50, "Rojo");
opn> gfx.update_screen();
```

Debe aparecer una ventana con un círculo rojo.

---

## Configuración del Editor

### Visual Studio Code

1. **Instalar extensión de sintaxis** (si está disponible)

2. **Configurar asociación de archivos**:

Agregar a `settings.json`:

```json
{
  "files.associations": {
    "*.opn": "opn",
    "*.prisma": "opn"
  }
}
```

3. **Configurar tarea de ejecución**:

Crear `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run OPN",
      "type": "shell",
      "command": "python",
      "args": [
        "-m",
        "prisma",
        "run",
        "${file}"
      ],
      "options": {
        "cwd": "${workspaceFolder}/OPN4/prisma-lang/src"
      },
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}
```

### Sublime Text

1. **Crear Build System**:

`Tools > Build System > New Build System`

```json
{
  "cmd": ["python", "-m", "prisma", "run", "$file"],
  "working_dir": "C:/ruta/a/OPN4/prisma-lang/src",
  "selector": "source.opn"
}
```

### Atom

1. **Instalar package** `script`

2. **Configurar comando**:

```coffee
'source.opn':
  'command': 'python'
  'args': ['-m', 'prisma', 'run', '{FILE_ACTIVE}']
```

---

## Estructura de Directorios

Después de la instalación, tu estructura debería verse así:

```
OPNscript/
├── docs/                    # Documentación
│   ├── README.md
│   ├── gfx_api.md
│   └── ...
├── prisma-lang/
│   └── src/
│       └── prisma/
│           ├── __main__.py
│           ├── cli.py
│           ├── transpiler.py
│           ├── pygfx_api.py
│           └── ...
└── tests/
    ├── main.opn
    └── main.prisma
```

---

## Ejecutar Programas

### Desde la Línea de Comandos

```bash
# Navegar al directorio src
cd prisma-lang/src

# Ejecutar un archivo
python -m prisma run ruta/al/archivo.opn

# O simplemente
python -m prisma ruta/al/archivo.opn
```

### Desde el REPL

```bash
python -m prisma
```

Luego dentro del REPL:

```opn
opn> !opn run tests/main.opn
```

---

## Solución de Problemas

### Error: "No module named 'prisma'"

**Solución**: Asegúrate de estar en el directorio correcto:

```bash
cd OPN4/prisma-lang/src
python -m prisma
```

### Error: "No module named 'tkinter'"

**Windows**:
- Reinstalar Python desde python.org asegurándote de marcar "tcl/tk and IDLE"

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install python3-tk
```

**macOS**:
```bash
brew install python-tk
```

### La ventana gráfica no aparece

1. Verifica que Tkinter esté instalado:
```bash
python -c "import tkinter; tkinter.Tk()"
```

2. Asegúrate de llamar a `gfx.update_screen()`:
```opn
gfx.setup_canvas(400, 400, "Test");
gfx.draw_circle(200, 200, 50, "Rojo");
gfx.update_screen();  # ¡Importante!
```

### Error: "Canvas no inicializado"

Llama a `gfx.setup_canvas()` antes de dibujar:

```opn
# ✅ Correcto
gfx.setup_canvas(800, 600, "Mi App");
gfx.draw_circle(400, 300, 50, "Azul");

# ❌ Incorrecto
gfx.draw_circle(400, 300, 50, "Azul");  # Error!
```

---

## Actualización

Para actualizar a la última versión:

```bash
cd OPNscript
git pull origin main
```

O descarga la última versión desde el repositorio.

---

## Desinstalación

Para desinstalar OPN:

1. Elimina el directorio del proyecto:
```bash
rm -rf OPNscript
```

2. Si instalaste con pip (futuro):
```bash
pip uninstall opn-lang
```

---

## Próximos Pasos

Ahora que tienes OPN instalado:

1. Lee la [Guía de Inicio Rápido](getting_started.md)
2. Explora los [Ejemplos de Gráficos](gfx_examples.md)
3. Consulta la [Referencia del Lenguaje](language_reference.md)

---

**Relacionado**:
- [Primeros Pasos →](getting_started.md)
- [API de Gráficos →](gfx_api.md)
- [← Volver al Índice](README.md)
