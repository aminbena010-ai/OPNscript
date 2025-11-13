# OPNscript - Documentación Oficial

Bienvenido a la documentación oficial de **OPNscript**, un lenguaje de programación transpilado a Python con capacidades gráficas integradas.

> **Nota:** ¡La documentación completa y renderizada está disponible en nuestra página web!
>
> **[Visita la documentación en línea](https://aminbena010-ai.github.io/OPNscript/)**

## Índice de Contenidos

### 🚀 Guías de Inicio
- **[Instalación](docs/installation.md)** - Cómo instalar y configurar OPNscript
- **[Primeros Pasos](docs/getting_started.md)** - Tu primer programa en OPNscript
- **[Tipos de Archivos](docs/file_types.md)** - Diferencia entre `.prisma` y `.opn`

### 📚 Guías Principales
- **[Referencia del Lenguaje](docs/language_reference.md)** - Sintaxis completa, operadores y estructuras de control
- **[Sintaxis](docs/syntax.md)** - Guía rápida de la sintaxis de OPNscript
- **[Variables](docs/variables.md)** - Declaración y manejo de variables
- **[Librería Estándar](docs/standard_library.md)** - Funciones integradas y namespaces

### 💻 Herramientas
- **[Editor OPNscript](docs/editor.md)** - Guía completa del IDE integrado
- **[REPL](docs/repl.md)** - Uso de la consola interactiva
- **[Editor VS Code (PyQt6)](vscode/README_EDITOR.md)** - Guía del editor de escritorio avanzado

### 🏗️ Sistema de Build
- **[Guía de Compilación](docs/COMPILATION_GUIDE.md)** - Cómo compilar y empaquetar tus proyectos OPNscript

### 🎨 Módulos de Gráficos
- **[API de Gráficos (GFX)](docs/gfx_api.md)** - Motor de renderizado con Tkinter
- **[Ejemplos de Gráficos](docs/gfx_examples.md)** - Tutoriales y ejemplos prácticos
- **[Referencia de Colores](docs/gfx_colors.md)** - Paleta de colores disponibles

## ¿Qué es OPNscript?

**OPNscript** es un lenguaje de programación transpilado a Python que combina sintaxis familiar de múltiples lenguajes con capacidades de renderizado gráfico integradas. Creado por Aminá Ben, permite escribir código limpio y expresivo que se compila a Python, facilitando tanto el aprendizaje como el desarrollo profesional.

### Características Principales

- ✨ **Sintaxis Clara**: Inspirada en lenguajes populares (C, Python, JavaScript)
- 🎨 **Gráficos Integrados**: Motor de renderizado con Tkinter incluido
- 🔄 **Transpilación a Python**: Genera código Python legible
- 💻 **Editores Avanzados**: Un IDE integrado con Tkinter y un editor de escritorio tipo VS Code con PyQt6.
- 🖥️ **REPL Interactivo**: Consola para experimentación rápida
- 📦 **Sistema de Build y Paquetes**: Compila y distribuye tu código OPNscript como paquetes reutilizables.
- 📚 **Librería Estándar**: Funciones útiles organizadas por namespaces

### Ejemplo Rápido

```prisma
func main() {
    let ancho = 800;
    let alto = 600;
    
    gfx.setup_canvas(ancho, alto, "Mi Primera Ventana");
    gfx.draw_circle(400, 300, 100, "Azul");
    gfx.update_screen();
}
```

## Navegación Rápida

| Tema | Descripción |
|------|-------------|
| [Instalación](docs/installation.md) | Instalar OPNscript en tu sistema |
| [Tipos de Archivos](docs/file_types.md) | `.prisma` vs `.opn` |
| [Editor](docs/editor.md) | Usar el IDE integrado |
| [Sintaxis Básica](docs/syntax.md) | Comentarios, variables, tipos de datos |
| [Control de Flujo](docs/language_reference.md#4-control-de-flujo) | if/else, bucles for/while |
| [Funciones](docs/language_reference.md#5-funciones) | Definición y uso de funciones |
| [Gráficos](docs/gfx_api.md) | API completa del módulo gfx |
| [Ejemplos](docs/gfx_examples.md) | Proyectos de ejemplo paso a paso |

## Comandos Rápidos

```bash
# Ejecutar un programa
opn programa.prisma

# Abrir el editor
opn editor

# Iniciar REPL
opn

# Transpilar a Python
opn transpile programa.prisma
```

## Recursos Adicionales

- **Repositorio**: [GitHub - OPNscript](https://github.com/aminbena010-ai/OPNscript)
- **Documentación Web**: [aminbena010-ai.github.io/OPNscript/](https://aminbena010-ai.github.io/OPNscript/)
- **Reportar Bugs**: [Issues](https://github.com/aminbena010-ai/OPNscript/issues)
- **Licencia**: [Información de Licencia](docs/LICENSE.md)
- **Créditos**: [Créditos y Contribuidores](docs/CREDITS.md)

## Licencia

OPNscript se distribuye bajo la **Licencia MIT**, una licencia completamente libre que permite uso comercial, modificación y distribución.

Para más detalles, consulta:
- **[Licencia MIT](docs/LICENSE.md)** - Términos completos y FAQ
- **[Créditos](docs/CREDITS.md)** - Reconocimiento de tecnologías y creadores

## Características Destacadas

### 🔄 Transpilación a Python
OPNscript transpila tu código a Python puro, permitiendo:
- Ejecutar en cualquier plataforma con Python 3.8+
- Integración con librerías Python existentes
- Código generado limpio y legible

### 🎨 Gráficos Integrados
Sistema gráfico completo basado en Tkinter:
- Formas (círculos, rectángulos, líneas, etc.)
- Manejo de eventos y entrada de usuario
- Canvas escalable y responsive
- Colores predefinidos y personalizables

### 🛠️ Herramientas Profesionales
- **IDE integrado** con editor de código y consola
- **REPL interactivo** para experimentación
- **Transpilador** desde línea de comandos
- **Sistema de build** para compilar proyectos

### 📚 Librería Estándar
Funciones útiles organizadas por namespaces:
- `py.*` - Funciones de Python
- `gfx.*` - Funciones gráficas
- `math.*` - Operaciones matemáticas
- `str.*` - Manipulación de strings

## Contribuir

¿Quieres mejorar OPNscript? Consulta nuestra [guía de contribución](docs/CONTRIBUTING.md).

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0.0  
**Licencia**: [MIT](docs/LICENSE.md)  
**Creador**: [Aminá Ben](https://github.com/aminbena010-ai)  
**Repositorio**: [GitHub](https://github.com/aminbena010-ai/OPNscript)
