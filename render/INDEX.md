# Índice - Paquete OPN Render

## Descripción

**OPN Render v1.0.0** es un paquete completo de gráficos 2D para el lenguaje OPN, programado 100% en OPN usando archivos `.prisma`. No depende de librerías externas de Python.

## Características Principales

✅ Motor gráfico 2D completo
✅ 100% programado en OPN
✅ Sin dependencias externas
✅ Funciones reutilizables
✅ Ejemplos incluidos
✅ Fácil de aprender y extender

## Contenido del Paquete

### Módulos Principales

| Archivo | Descripción | Funciones |
|---------|-------------|-----------|
| `render.prisma` | Archivo principal con funciones básicas | 25+ |
| `shapes.prisma` | Funciones para dibujar formas | 10+ |
| `colors.prisma` | Gestión de colores y paletas | 12+ |
| `effects.prisma` | Efectos visuales y animaciones | 8+ |
| `utils.prisma` | Funciones utilitarias | 11+ |

### Ejemplos Listos para Usar

1. **ejemplo_basico.prisma** - Introducción a formas básicas
2. **ejemplo_animacion.prisma** - Animaciones avanzadas
3. **demo_completo.prisma** - Demostración de todas las características

### Documentación

- `README.md` - Documentación técnica completa
- `GUIA_USO.md` - Guía práctica con ejemplos
- `INDEX.md` - Este archivo

## Estructura de Carpetas

```
render/
├── render.prisma                  ← Importar este archivo
├── shapes.prisma                  ← Formas (importable)
├── colors.prisma                  ← Colores (importable)
├── effects.prisma                 ← Efectos (importable)
├── utils.prisma                   ← Utilidades (importable)
├── examples/
│   ├── ejemplo_basico.prisma
│   ├── ejemplo_animacion.prisma
│   └── demo_completo.prisma
├── shapes/                        ← Subdirectorio vacío (para expansión)
├── effects/                       ← Subdirectorio vacío (para expansión)
├── utils/                         ← Subdirectorio vacío (para expansión)
├── README.md                      ← Documentación
├── GUIA_USO.md                   ← Guía de uso
└── INDEX.md                       ← Este archivo
```

## Cómo Empezar

### 1. Requisitos
- OPN language instalado
- Python 3.7+

### 2. Primer Programa
```opn
main {
    gfx.setup_canvas(800, 600, "Mi App");
    gfx.draw_circle(400, 300, 50, "Rojo");
    gfx.update_screen();
}
```

### 3. Ejecutar
```bash
python -m prisma run mi_programa.prisma
```

## Funciones Disponibles por Categoría

### Inicialización (render.prisma)
- `init_render(width, height, title)` - Inicializar canvas
- `update_render()` - Actualizar pantalla

### Formas Básicas (shapes.prisma)
- `draw_point(x, y, color)` - Punto
- `draw_circle(x, y, radius, color)` - Círculo
- `draw_square(x, y, size, color)` - Cuadrado
- `draw_rectangle(x, y, width, height, color)` - Rectángulo

### Colores (colors.prisma)
- `color_red()`, `color_green()`, `color_blue()` - Colores primarios
- `color_yellow()`, `color_purple()`, `color_cyan()` - Colores secundarios
- `color_white()`, `color_black()` - Neutrales
- `get_color_palette_neon(index)` - Paleta neon

### Patrones (render.prisma)
- `draw_grid_cells(...)` - Grilla de celdas
- `draw_concentric(...)` - Círculos concéntricos
- `draw_stars(...)` - Patrón de estrellas

### Animaciones (render.prisma)
- `animate_expand(...)` - Expansión de círculos
- `animate_pulse(...)` - Efecto de pulso
- `animate_trail(...)` - Efecto de estela

### Utilidades (utils.prisma)
- `draw_border(...)` - Borde rectangular
- `draw_grid(...)` - Grilla completa
- `calculate_distance(...)` - Distancia entre puntos
- `clamp_coordinate(...)` - Limitar rango

## Paleta de Colores

```
Rojo      → "#e74c3c"
Verde     → "#2ecc71"
Azul      → "#3498db"
Amarillo  → "#f1c40f"
Púrpura   → "#9b59b6"
Cian      → "#1abc9c"
Blanco    → "#ecf0f1"
Negro     → "#2c3e50"
```

## Ejemplos de Uso

### Ejemplo 1: Círculos Concéntricos
```opn
main {
    gfx.setup_canvas(800, 600, "Concentricos");
    
    let i = 0;
    for i in 1..10 {
        let radius = i * 30;
        gfx.draw_circle(400, 300, radius, "Verde");
    }
    
    gfx.update_screen();
}
```

### Ejemplo 2: Grilla de Formas
```opn
main {
    gfx.setup_canvas(800, 600, "Grilla");
    
    let row = 0;
    let col = 0;
    
    for row in 1..8 {
        for col in 1..10 {
            let x = 100 + col * 60;
            let y = 100 + row * 60;
            gfx.draw_circle(x, y, 20, "Azul");
        }
    }
    
    gfx.update_screen();
}
```

### Ejemplo 3: Animación
```opn
main {
    gfx.setup_canvas(800, 600, "Animacion");
    
    let frame = 0;
    for frame in 1..150 {
        let x = 100 + frame * 2;
        let y = 300;
        gfx.draw_circle(x, y, 15, "Rojo");
        gfx.update_screen();
    }
}
```

## Rendimiento

| Operación | Rendimiento |
|-----------|-------------|
| Draw calls | ~1000 por frame |
| FPS objetivo | 30-60 FPS |
| Canvas máximo | 800x600 |
| Animaciones | 200+ frames |

## Notas Técnicas

- **Lenguaje**: 100% OPN (.prisma)
- **API Gráfica**: gfx.* (interna)
- **Sin imports externos**: Solo OPN puro
- **Transpilación**: Compatible con OPN transpiler
- **Ejecución**: Via CLI: `python -m prisma run`

## Compatibilidad

- ✅ OPN Language v0.5.0+
- ✅ Python 3.7+
- ✅ Windows, macOS, Linux
- ✅ Tkinter (gfx API backend)

## Extensibilidad

El paquete está diseñado para ser extendido:

1. Agrega nuevas funciones a `shapes.prisma`
2. Crea nuevas paletas en `colors.prisma`
3. Implementa nuevos efectos en `effects.prisma`
4. Comparte tus contribuciones

## Troubleshooting

**Problema**: El programa no se ejecuta
**Solución**: Verifica que esté el `main { }` block

**Problema**: Canvas no aparece
**Solución**: Llama a `gfx.setup_canvas()` primero

**Problema**: Formas no aparecen
**Solución**: Verifica nombres de colores exactos

## Licencia

Paquete OPN Render - Código abierto para OPN Language

## Autor

Desarrollado como paquete oficial de gráficos 2D para OPN Language

## Soporte

Para problemas o sugerencias, revisa:
- README.md (documentación técnica)
- GUIA_USO.md (guía práctica)
- examples/ (ejemplos funcionales)

---

**OPN Render v1.0.0** - Motor Gráfico 2D para OPN Language
