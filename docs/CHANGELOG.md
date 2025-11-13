# Changelog - OPNscript

## [1.0.0] - 2025-11-11

### 🎉 Major Release - Production Ready

#### ✨ New Features

**Editor Integrado**
- Editor GUI completo con Tkinter
- Autocompletado inteligente (Ctrl+Space)
- Detección de errores en tiempo real
- Panel de documentación integrado
- Consola funcional con comandos reales
- Resaltado de sintaxis
- Números de línea automáticos
- Tema oscuro optimizado

**Sistema de Configuración Modular**
- Carpeta `config/` con archivos organizados:
  - `aliases.py` - Aliases de funciones (30+ aliases)
  - `keywords.py` - Palabras clave y builtins (19+ funciones documentadas)
  - `colors.py` - Colores de sintaxis y temas
- Fácil extensión y personalización

**Tipos de Archivos**
- `.prisma` - Archivos de código ejecutable
- `.opn` - Archivos de datos y configuración
- Documentación completa de la diferencia

**CLI Mejorado**
- `opn run <archivo>` - Ejecutar programas
- `opn transpile <archivo>` - Transpilar a Python
- `opn editor` - Lanzar el IDE
- `opn` - Iniciar REPL
- Soporte implícito de comando `run`

#### 🔧 Improvements

**Transpiler**
- Soporte para distinguir archivos `.prisma` y `.opn`
- Integración con sistema de aliases
- Mejor manejo de imports
- Detección automática de módulo `gfx`

**Documentación**
- 10+ archivos de documentación completa
- Guía del editor (`editor.md`)
- Guía de tipos de archivos (`file_types.md`)
- README actualizado con ejemplos
- CONTRIBUTING.md para colaboradores
- Todas las guías actualizadas y enlazadas

**Distribución**
- `setup.py` completo y funcional
- `pyproject.toml` actualizado
- `.gitignore` configurado
- `MANIFEST.in` para incluir archivos necesarios
- Listo para publicar en PyPI

#### 📚 Documentation

**Nuevos Documentos**
- `docs/editor.md` - Guía completa del editor (400+ líneas)
- `docs/file_types.md` - Explicación de `.prisma` vs `.opn`
- `CONTRIBUTING.md` - Guía para contribuidores
- `CHANGELOG.md` - Este archivo

**Documentos Actualizados**
- `docs/README.md` - Índice reorganizado
- `prisma-lang/README.md` - README principal del proyecto
- Todos los enlaces actualizados

#### 🐛 Bug Fixes

- Corregido error de orden en `visitor.py` (Expression/Statement)
- Mejorado manejo de aliases en transpiler
- Corregidos imports en módulos

#### 🎨 Editor Features

**Consola Integrada**
- Comandos: `help`, `clear`, `version`, `run`, `transpile`, `check`, `ls`, `pwd`, `cd`, `python`
- Historial de comandos (↑/↓)
- Ejecución real de código Python
- Salida con colores (info, error, success, warning)

**Autocompletado**
- Keywords del lenguaje
- Funciones builtin
- API de gráficos (gfx)
- Colores predefinidos
- Aliases de funciones

**Detector de Errores**
- Falta de `:` en declaraciones
- Paréntesis desbalanceados
- Corchetes desbalanceados
- Llaves desbalanceadas
- Actualización en tiempo real

**Panel de Documentación**
- Búsqueda por texto
- Filtrado por categorías
- Información completa de funciones
- Ejemplos de código

#### 📦 Project Structure

```
OPNscript/
├── prisma-lang/
│   ├── src/
│   │   └── prisma/
│   │       ├── config/          # ✨ NEW
│   │       │   ├── __init__.py
│   │       │   ├── aliases.py
│   │       │   ├── keywords.py
│   │       │   └── colors.py
│   │       ├── editor.py        # ✨ NEW (800+ lines)
│   │       ├── transpiler.py    # 🔧 Updated
│   │       ├── cli.py           # 🔧 Updated
│   │       ├── pygfx_api.py
│   │       ├── repl.py
│   │       └── visitor.py       # 🐛 Fixed
│   ├── setup.py                 # 🔧 Updated
│   └── pyproject.toml           # 🔧 Updated
├── docs/
│   ├── README.md                # 🔧 Updated
│   ├── editor.md                # ✨ NEW
│   ├── file_types.md            # ✨ NEW
│   ├── getting_started.md
│   ├── gfx_api.md
│   ├── gfx_colors.md
│   ├── gfx_examples.md
│   ├── installation.md
│   ├── language_reference.md
│   ├── repl.md
│   ├── standard_library.md
│   ├── syntax.md
│   └── variables.md
├── tests/
│   ├── main.prisma
│   └── main.opn
├── .gitignore                   # ✨ NEW
├── MANIFEST.in                  # ✨ NEW
├── CONTRIBUTING.md              # ✨ NEW
├── CHANGELOG.md                 # ✨ NEW (this file)
└── README.md                    # 🔧 Updated
```

#### 🚀 Installation

```bash
# Clone repository
git clone https://github.com/aminbena010-ai/OPNscript.git
cd OPNscript/prisma-lang

# Install
pip install -e .

# Or from PyPI (when published)
pip install opnscript
```

#### 📖 Quick Start

```bash
# Launch editor
opn editor

# Run a program
opn hello.prisma

# Start REPL
opn

# Transpile to Python
opn transpile program.prisma
```

#### 🎯 Next Steps

- [ ] Publish to PyPI
- [ ] Create GitHub repository
- [ ] Add CI/CD pipeline
- [ ] Create video tutorials
- [ ] Build VSCode extension
- [ ] Implement debugger
- [ ] Expand standard library

---

## Previous Versions

### [0.1.0] - Initial Development
- Basic transpiler
- Graphics API (Tkinter)
- REPL
- Basic CLI
- Initial documentation

---

**Creador**: Aminá Ben  
**Contribuidores**: Comunidad OPNscript  
**Licencia**: [MIT](LICENSE.md)  
**Python**: >=3.8
