# Editor OPNscript - Guía Completa

El **Editor OPNscript** es un IDE integrado para el lenguaje OPNscript con características avanzadas de desarrollo.

## 🚀 Iniciar el Editor

### Desde la línea de comandos:
```bash
python -m prisma editor
```

### Desde Python:
```python
from prisma.editor import main
main()
```

---

## 🎨 Interfaz del Editor

El editor está dividido en varias secciones:

### 1. **Barra de Menú**
- **Archivo**: Nuevo, Abrir, Guardar, Guardar como, Salir
- **Editar**: Deshacer, Rehacer, Cortar, Copiar, Pegar, Buscar
- **Ejecutar**: Ejecutar (F5), Transpilar (F6), Verificar errores (F7)
- **Ver**: Consola, Documentación, Errores
- **Ayuda**: Documentación, Acerca de

### 2. **Barra de Herramientas**
Acceso rápido a las funciones más usadas:
- 📄 Nuevo archivo
- 📂 Abrir archivo
- 💾 Guardar
- ▶️ Ejecutar
- 🔧 Transpilar
- 🔍 Verificar errores

### 3. **Editor de Código**
- Números de línea automáticos
- Resaltado de sintaxis
- Deshacer/Rehacer ilimitado
- Tema oscuro optimizado para programación

### 4. **Panel de Consola**
Consola interactiva con comandos integrados (ver sección de Consola)

### 5. **Panel de Documentación**
Documentación integrada con búsqueda y filtrado

### 6. **Panel de Errores**
Muestra errores y advertencias en tiempo real

---

## ⌨️ Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl+N` | Nuevo archivo |
| `Ctrl+O` | Abrir archivo |
| `Ctrl+S` | Guardar |
| `Ctrl+Shift+S` | Guardar como |
| `Ctrl+Z` | Deshacer |
| `Ctrl+Y` | Rehacer |
| `Ctrl+X` | Cortar |
| `Ctrl+C` | Copiar |
| `Ctrl+V` | Pegar |
| `Ctrl+F` | Buscar |
| `Ctrl+Space` | Autocompletado |
| `F5` | Ejecutar código |
| `F6` | Transpilar código |
| `F7` | Verificar errores |

---

## 🤖 Autocompletado Inteligente

El editor incluye autocompletado basado en el contexto:

### Activar autocompletado:
- Presiona `Ctrl+Space` mientras escribes
- El editor sugerirá automáticamente:
  - Palabras clave del lenguaje
  - Funciones builtin
  - Funciones de la API gfx
  - Colores predefinidos
  - Aliases de funciones

### Ejemplo:
```
Escribes: gfx.dr
Presionas: Ctrl+Space
Sugerencias: gfx.draw_point, gfx.draw_circle
```

---

## 🔍 Detector de Errores en Tiempo Real

El editor detecta errores mientras escribes:

### Errores detectados:
- ❌ Falta de `:` en declaraciones `if`, `for`, `while`, `def`
- ⚠️ Paréntesis desbalanceados `()`
- ⚠️ Corchetes desbalanceados `[]`
- ⚠️ Llaves desbalanceadas `{}`

### Verificación manual:
- Presiona `F7` o usa el menú **Ejecutar → Verificar errores**
- Los errores aparecen en el panel inferior con número de línea

---

## 💻 Consola Integrada

La consola del editor es **funcional y real**, no una simulación.

### Comandos disponibles:

#### **help**
Muestra la lista de comandos disponibles
```
> help
```

#### **clear**
Limpia la consola
```
> clear
```

#### **version**
Muestra la versión de OPN
```
> version
OPN Language v1.0.0
```

#### **run <archivo>**
Ejecuta un archivo .prisma
```
> run main.prisma
```

#### **transpile <archivo>**
Transpila un archivo a Python
```
> transpile game.prisma
```

#### **check <archivo>**
Verifica errores en un archivo
```
> check utils.prisma
```

#### **ls [directorio]**
Lista archivos en el directorio
```
> ls
> ls src/
```

#### **pwd**
Muestra el directorio actual
```
> pwd
C:\Users\ADMIN\Desktop\OPN\OPN4
```

#### **cd <directorio>**
Cambia el directorio actual
```
> cd src
> cd ..
```

#### **python <código>**
Ejecuta código Python directamente
```
> python 2 + 2
4
> python print("Hola")
Hola
```

### Historial de comandos:
- Usa `↑` (flecha arriba) para comandos anteriores
- Usa `↓` (flecha abajo) para comandos siguientes

---

## 📚 Panel de Documentación

El panel de documentación incluye:

### Búsqueda:
- Escribe en el campo de búsqueda para filtrar
- Busca por nombre de función o descripción

### Categorías:
- **Todos**: Muestra toda la documentación
- **Builtins**: Funciones integradas de Python/OPN
- **GFX**: API de gráficos
- **Keywords**: Palabras clave del lenguaje
- **Aliases**: Aliases de funciones

### Información mostrada:
- **Firma de función**: Parámetros y tipos
- **Descripción**: Qué hace la función
- **Ejemplo**: Código de ejemplo

---

## 🎯 Flujo de Trabajo Típico

### 1. Crear un nuevo proyecto:
```
1. Archivo → Nuevo (Ctrl+N)
2. Escribe tu código
3. Archivo → Guardar como (Ctrl+Shift+S)
4. Guarda como "mi_programa.prisma"
```

### 2. Escribir código con autocompletado:
```
1. Escribe: gfx.
2. Presiona Ctrl+Space
3. Selecciona la función deseada
4. El editor muestra la documentación
```

### 3. Verificar errores:
```
1. Presiona F7
2. Revisa el panel de errores
3. Haz clic en un error para ir a la línea
4. Corrige el error
```

### 4. Ejecutar el programa:
```
1. Presiona F5
2. La consola muestra la salida
3. Si hay errores, aparecen en rojo
```

### 5. Transpilar a Python:
```
1. Presiona F6
2. El código Python aparece en la consola
3. Opcional: Guardar con -o salida.py
```

---

## 🎨 Personalización

### Tema de colores:
El editor usa un tema oscuro optimizado:
- **Fondo**: `#1E1E1E`
- **Texto**: `#D4D4D4`
- **Palabras clave**: `#569CD6`
- **Cadenas**: `#CE9178`
- **Comentarios**: `#6A9955`
- **Números**: `#B5CEA8`
- **Funciones**: `#DCDCAA`
- **Errores**: `#F44747`
- **Advertencias**: `#CCA700`

---

## 🔧 Configuración Avanzada

### Archivos de configuración:
El editor usa archivos en `prisma/config/`:
- `aliases.py` - Aliases de funciones
- `keywords.py` - Palabras clave y builtins
- `colors.py` - Colores de sintaxis

### Modificar aliases:
```python
# En prisma/config/aliases.py
CALL_ALIASES = {
    "mi.funcion": "mi_funcion_python",
    # Agrega tus propios aliases
}
```

---

## 🐛 Solución de Problemas

### El editor no inicia:
```bash
# Verifica que tkinter esté instalado
python -m tkinter

# Si no está instalado:
# Windows: Reinstala Python con tkinter
# Linux: sudo apt-get install python3-tk
# macOS: Viene incluido con Python
```

### Los comandos de consola no funcionan:
- Verifica que estés en el directorio correcto con `pwd`
- Usa rutas absolutas si es necesario
- Revisa los permisos de archivo

### El autocompletado no aparece:
- Presiona `Ctrl+Space` explícitamente
- Asegúrate de estar escribiendo una palabra válida
- Verifica que los archivos de config estén presentes

---

## 📖 Ejemplos de Uso

### Ejemplo 1: Crear un programa simple
```prisma
func main() {
    py.print("Hola desde el editor OPN!");
    
    let numeros = [1, 2, 3, 4, 5];
    let suma = 0;
    
    for num in numeros {
        suma = suma + num;
    }
    
    py.print("La suma es:", suma);
}
```

### Ejemplo 2: Usar gráficos
```prisma
func main() {
    gfx.setup_canvas(800, 600, "Mi Ventana");
    
    gfx.draw_circle(400, 300, 50, gfx.Azul);
    gfx.draw_point(400, 300, gfx.Rojo, 5);
    
    gfx.update_screen();
    gfx.init();
}
```

### Ejemplo 3: Usar la consola
```
> run ejemplo1.prisma
Hola desde el editor OPN!
La suma es: 15
Ejecución completada exitosamente

> transpile ejemplo2.prisma
[Código Python generado...]

> check ejemplo1.prisma
✓ No se encontraron problemas en ejemplo1.prisma
```

---

## 🚀 Características Futuras

Próximamente en el editor:
- [ ] Resaltado de sintaxis avanzado
- [ ] Depurador integrado
- [ ] Gestión de proyectos
- [ ] Integración con Git
- [ ] Snippets personalizables
- [ ] Temas de color personalizables
- [ ] Extensiones y plugins

---

## 📚 Recursos Adicionales

- [Tipos de Archivos (.prisma vs .opn)](file_types.md)
- [API de Gráficos](gfx_api.md)
- [Guía de Inicio](getting_started.md)
- [Ejemplos](gfx_examples.md)

---

**¡Disfruta programando en OPN con el editor integrado!** 🎉
