# Tipos de Archivos en OPNscript

OPNscript utiliza dos extensiones de archivo diferentes, cada una con un propósito específico:

## 📄 Archivos `.prisma` - Código Ejecutable

Los archivos con extensión `.prisma` contienen **código fuente ejecutable** del lenguaje OPN.

### Características:
- Contienen lógica de programa, funciones, clases y estructuras de control
- Se transpilan a Python y se ejecutan
- Soportan todas las características del lenguaje OPN
- Pueden importar módulos y usar la API de gráficos

### Ejemplo de archivo `.prisma`:

```prisma
func main() {
    py.print("Hola desde OPN!");
    
    let x = 10;
    let y = 20;
    let suma = x + y;
    
    py.print("La suma es:", suma);
}
```

### Uso:
```bash
# Ejecutar un archivo .prisma
python -m prisma run programa.prisma

# O simplemente
python -m prisma programa.prisma

# Transpilar sin ejecutar
python -m prisma transpile programa.prisma -o salida.py
```

---

## 📦 Archivos `.opn` - Datos y Configuración

Los archivos con extensión `.opn` están diseñados para **almacenamiento de datos** y configuración avanzada.

### Características:
- Almacenan datos estructurados, configuraciones y recursos
- Pueden contener definiciones de datos, constantes y estructuras
- Útiles para separar datos de la lógica del programa
- Pueden ser importados por archivos `.prisma`

### Casos de uso:
1. **Configuración de aplicaciones**
2. **Datos de juegos** (niveles, personajes, items)
3. **Recursos estáticos** (colores, constantes, mensajes)
4. **Definiciones de estructuras de datos**

### Ejemplo de archivo `.opn`:

```opn
let COLORES = {
    "rojo": "#FF0000",
    "verde": "#00FF00",
    "azul": "#0000FF"
};

let CONFIGURACION = {
    "ancho_ventana": 800,
    "alto_ventana": 600,
    "titulo": "Mi Juego OPN"
};

let NIVELES = [
    {"nombre": "Nivel 1", "dificultad": 1},
    {"nombre": "Nivel 2", "dificultad": 2},
    {"nombre": "Nivel 3", "dificultad": 3}
];
```

### Importar datos desde `.opn`:

```prisma
import config from "configuracion.opn";

func main() {
    py.print("Título:", config.CONFIGURACION["titulo"]);
    py.print("Dimensiones:", config.CONFIGURACION["ancho_ventana"], "x", config.CONFIGURACION["alto_ventana"]);
}
```

---

## 🔄 Comparación

| Característica | `.prisma` | `.opn` |
|----------------|-----------|--------|
| **Propósito** | Código ejecutable | Datos y configuración |
| **Contiene** | Funciones, clases, lógica | Constantes, estructuras de datos |
| **Ejecución** | Se ejecuta directamente | Se importa como módulo |
| **Uso típico** | Programas principales | Archivos de recursos |
| **Transpilación** | Genera código Python ejecutable | Genera módulos de datos |

---

## 📋 Convenciones de Nombres

### Para archivos `.prisma`:
- `main.prisma` - Punto de entrada principal
- `utils.prisma` - Utilidades y funciones auxiliares
- `game.prisma` - Lógica del juego
- `graphics.prisma` - Funciones de gráficos

### Para archivos `.opn`:
- `config.opn` - Configuración de la aplicación
- `data.opn` - Datos generales
- `levels.opn` - Datos de niveles
- `constants.opn` - Constantes del programa
- `resources.opn` - Recursos y assets

---

## 🎯 Mejores Prácticas

### 1. **Separación de Responsabilidades**
```
proyecto/
├── src/
│   ├── main.prisma          # Código principal
│   ├── game_logic.prisma    # Lógica del juego
│   └── renderer.prisma      # Renderizado
└── data/
    ├── config.opn           # Configuración
    ├── levels.opn           # Datos de niveles
    └── assets.opn           # Recursos
```

### 2. **Organización Modular**
- Mantén el código ejecutable en archivos `.prisma`
- Almacena datos y configuraciones en archivos `.opn`
- Usa imports para conectar código y datos

### 3. **Nomenclatura Clara**
- Usa nombres descriptivos que indiquen el contenido
- Prefiere minúsculas con guiones bajos: `game_config.opn`
- Agrupa archivos relacionados en carpetas

---

## 🚀 Ejemplo Completo

### `config.opn` (Datos):
```opn
let GAME_CONFIG = {
    "width": 800,
    "height": 600,
    "title": "Space Shooter",
    "fps": 60
};

let COLORS = {
    "background": gfx.Negro,
    "player": gfx.Azul,
    "enemy": gfx.Rojo
};
```

### `main.prisma` (Código):
```prisma
import config from "config.opn";

func main() {
    let cfg = config.GAME_CONFIG;
    
    gfx.setup_canvas(cfg["width"], cfg["height"], cfg["title"]);
    
    gfx.draw_circle(400, 300, 20, config.COLORS["player"]);
    
    gfx.update_screen();
    gfx.init();
}
```

### Ejecutar:
```bash
python -m prisma main.prisma
```

---

## 📚 Recursos Adicionales

- [Guía de Inicio](getting_started.md)
- [API de Gráficos](gfx_api.md)
- [Ejemplos](gfx_examples.md)
- [REPL](repl.md)

---

**Nota**: Ambos tipos de archivos se transpilan a Python, pero `.prisma` está optimizado para código ejecutable mientras que `.opn` está diseñado para datos estructurados y configuración.
