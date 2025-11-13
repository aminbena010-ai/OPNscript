# Contribuyendo a OPNscript

¡Gracias por tu interés en contribuir a OPNscript! Este documento proporciona pautas e instrucciones para contribuir.

## 🚀 Getting Started

### Requisitos
- Python 3.8 o superior
- Git
- Conocimiento básico de Python y transpiladores

### Configurar el Entorno de Desarrollo

1. **Fork y clona el repositorio**
```bash
git clone https://github.com/aminbena010-ai/OPNscript.git
cd OPNscript
```

2. **Crea un entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala en modo desarrollo**
```bash
cd prisma-lang
pip install -e ".[dev]"
```

4. **Ejecuta pruebas para verificar la configuración**
```bash
pytest
```

## 📋 Cómo Contribuir

### Reportar Bugs

Antes de crear un reporte de bug:
1. Verifica el [rastreador de problemas](https://github.com/aminbena010-ai/OPNscript/issues) para reportes existentes
2. Verifica que el bug existe en la versión más reciente
3. Recopila información relevante (SO, versión de Python, mensajes de error)

Crea un reporte de bug con:
- Título claro y descriptivo
- Pasos para reproducir
- Comportamiento esperado vs real
- Ejemplos de código (si aplica)
- Mensajes de error y stack traces

### Sugerir Características

¡Las solicitudes de características son bienvenidas! Por favor:
1. Verifica las solicitudes de características existentes
2. Explica el caso de uso
3. Proporciona ejemplos de cómo funcionaría
4. Considera la complejidad de la implementación

### Pull Requests

1. **Crea una rama de característica**
```bash
git checkout -b feature/tu-nombre-caracteristica
```

2. **Realiza tus cambios**
- Sigue las pautas de estilo de código
- Agrega pruebas para nueva funcionalidad
- Actualiza la documentación según sea necesario

3. **Prueba tus cambios**
```bash
pytest
python -m prisma run tests/main.prisma
```

4. **Commit con mensajes claros**
```bash
git commit -m "Add feature: descripción de lo que agregaste"
```

5. **Push y crear PR**
```bash
git push origin feature/tu-nombre-caracteristica
```

## 🎨 Pautas de Estilo de Código

### Código Python
- Sigue PEP 8
- Usa type hints donde sea apropiado
- Longitud máxima de línea: 100 caracteres
- Usa nombres de variables significativos

Example:
```python
def transpile_expression(expr: Expression) -> str:
    """Transpile an expression to Python code.
    
    Args:
        expr: The expression to transpile
        
    Returns:
        Python code as a string
    """
    if isinstance(expr, Literal):
        return str(expr.value)
    # ...
```

### Código OPNscript
- Usa 4 espacios para indentación
- Nombres claros de funciones y variables
- Agrega comentarios para lógica compleja

Example:
```prisma
func calculate_fibonacci(n) {
    if n <= 1 {
        return n;
    }
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2);
}
```

## 🧪 Pruebas

### Ejecutar Pruebas
```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar archivo de prueba específico
pytest tests/test_transpiler.py

# Ejecutar con cobertura
pytest --cov=prisma
```

### Escribir Pruebas
```python
def test_transpile_function():
    source = """
    func add(a, b) {
        return a + b;
    }
    """
    result = transpile(source)
    assert "def add(a, b):" in result
    assert "return a + b" in result
```

## 📚 Documentación

### Actualizar Documentación
- La documentación está en la carpeta `docs/`
- Usa formato Markdown
- Incluye ejemplos de código
- Mantente amigable para principiantes

### Estructura de Documentación
```
docs/
├── README.md           # Índice de documentación
├── getting_started.md  # Guía para principiantes
├── file_types.md       # .prisma vs .opn
├── gfx_api.md         # Referencia de API gráfica
├── editor.md          # Guía del editor
├── LICENSE.md         # Información de licencia
├── CREDITS.md         # Créditos y contribuidores
└── ...
```

## 🏗️ Estructura del Proyecto

```
OPNscript/
├── prisma-lang/
│   ├── src/
│   │   └── prisma/
│   │       ├── config/          # Archivos de configuración
│   │       │   ├── __init__.py
│   │       │   ├── aliases.py   # Aliases de funciones
│   │       │   ├── keywords.py  # Palabras clave del lenguaje
│   │       │   └── colors.py    # Colores de sintaxis
│   │       ├── transpiler.py    # Transpilador principal
│   │       ├── cli.py           # Interfaz CLI
│   │       ├── editor.py        # IDE integrado
│   │       ├── pygfx_api.py     # API gráfica
│   │       ├── repl.py          # REPL interactivo
│   │       └── visitor.py       # Visitante AST
│   ├── tests/                   # Archivos de prueba
│   ├── setup.py                 # Script de configuración
│   └── pyproject.toml           # Configuración del proyecto
├── docs/                        # Documentación
└── CONTRIBUTING.md              # Este archivo
```

## 🔍 Áreas para Contribuir

### Alta Prioridad
- [ ] Mejorar mensajes de error
- [ ] Agregar más funciones integradas
- [ ] Expandir la librería estándar
- [ ] Optimizaciones de rendimiento
- [ ] Más cobertura de pruebas

### Prioridad Media
- [ ] Extensión de VS Code
- [ ] Mejoras de resaltado de sintaxis
- [ ] Integración de depurador
- [ ] Administrador de paquetes
- [ ] Playground web

### Documentación
- [ ] Más ejemplos
- [ ] Tutoriales en video
- [ ] Expansión de referencia API
- [ ] Traducción a otros idiomas

## 🎯 Ideas de Contribución

### Para Principiantes
- Corregir errores tipográficos en documentación
- Agregar ejemplos de código
- Mejorar mensajes de error
- Escribir pruebas para características existentes

### Para Nivel Intermedio
- Agregar nuevas funciones integradas
- Mejorar la interfaz del editor
- Optimizar el rendimiento del transpilador
- Agregar nuevas funciones gráficas

### Para Avanzado
- Implementar depurador
- Crear administrador de paquetes
- Construir extensión de VS Code
- Agregar nuevas características del lenguaje

## 📝 Pautas de Mensajes de Commit

Usa mensajes de commit claros y descriptivos:

```
Add feature: Descripción breve

Explicación detallada de qué se agregó y por qué.
Incluye cualquier cambio importante o notas de migración.

Fixes #123
```

Tipos de commits:
- `Add feature:` - Nueva funcionalidad
- `Fix:` - Correcciones de errores
- `Update:` - Actualizaciones de características existentes
- `Refactor:` - Refactorización de código
- `Docs:` - Cambios de documentación
- `Test:` - Adiciones o cambios de pruebas

## 🤝 Proceso de Revisión de Código

1. Todos los PRs requieren revisión antes de fusionarse
2. Aborda los comentarios de revisión rápidamente
3. Mantén los PRs enfocados y de tamaño razonable
4. Actualiza tu PR según los comentarios

## 📜 Licencia

Al contribuir, aceptas que tus contribuciones se licenciarán bajo la Licencia MIT.

## 💬 Obtener Ayuda

- Abre un issue para preguntas
- Únete a discusiones en GitHub Discussions
- Consulta la documentación existente

## 🙏 Reconocimiento

Los contribuidores serán reconocidos en:
- Sección de contribuidores de README.md
- Notas de lanzamiento
- Documentación del proyecto

¡Gracias por contribuir a OPNscript! 🎉
