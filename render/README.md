# OPN Render - Paquete Gráfico para OPN

Paquete completo de renderizado 2D para el lenguaje OPN. Todas las funciones están programadas en OPN usando archivos `.prisma`.

## Estructura del Paquete

```
render/
├── shapes.prisma      # Funciones para dibujar formas geométricas
├── colors.prisma      # Gestión de colores y paletas
├── effects.prisma     # Efectos visuales y animaciones
├── utils.prisma       # Funciones utilitarias
├── examples/          # Ejemplos de uso
│   ├── ejemplo_basico.prisma      # Formas básicas
│   └── ejemplo_animacion.prisma   # Animaciones avanzadas
└── README.md          # Este archivo
```

## Módulos Disponibles

### 1. shapes.prisma - Formas Geométricas

Funciones para dibujar formas básicas:

- `draw_point_basic(x, y, color)` - Dibuja un punto
- `draw_circle_basic(x, y, radius, color)` - Dibuja un círculo
- `draw_square_filled(x, y, size, color)` - Dibuja un cuadrado lleno
- `draw_rectangle_filled(x, y, width, height, color)` - Dibuja un rectángulo lleno
- `draw_horizontal_line(x1, x2, y, color)` - Línea horizontal
- `draw_vertical_line(x, y1, y2, color)` - Línea vertical
- `draw_circle_outline(x, y, radius, color)` - Contorno de círculo
- `draw_grid_pattern(start_x, start_y, width, height, cell_size, color)` - Patrón de grilla
- `draw_concentric_circles(x, y, num_circles, spacing, color)` - Círculos concéntricos
- `draw_diamond(x, y, size, color)` - Forma de diamante

### 2. colors.prisma - Colores

Funciones para trabajar con colores:

- `get_primary_red()` - Retorna rojo
- `get_primary_green()` - Retorna verde
- `get_primary_blue()` - Retorna azul
- `get_primary_yellow()` - Retorna amarillo
- `get_primary_purple()` - Retorna púrpura
- `get_primary_cyan()` - Retorna cian
- `get_neutral_white()` - Retorna blanco
- `get_neutral_black()` - Retorna negro
- `get_color_palette_neon(index)` - Retorna color de paleta neon
- `is_dark_color(color_name)` - Verifica si es color oscuro
- `is_light_color(color_name)` - Verifica si es color claro

### 3. effects.prisma - Efectos

Funciones para efectos visuales:

- `fade_effect_circles(x, y, color, frames)` - Efecto de desvanecimiento
- `pulse_effect(x, y, color, num_pulses)` - Efecto de pulso
- `spiral_effect(center_x, center_y, color, num_points)` - Efecto espiral
- `rain_effect(color, num_drops)` - Efecto de lluvia
- `wave_effect(center_y, color, amplitude, num_waves)` - Efecto de onda
- `strobe_effect(x, y, radius, color, num_flashes)` - Efecto estroboscópico
- `trail_effect(start_x, start_y, end_x, end_y, color, num_steps)` - Efecto de estela
- `rotation_effect(center_x, center_y, radius, color, num_rotations)` - Efecto de rotación

### 4. utils.prisma - Utilidades

Funciones utilitarias:

- `init_canvas_default()` - Inicializa canvas con valores por defecto
- `init_canvas_custom(width, height, title)` - Inicializa canvas personalizado
- `clear_screen()` - Limpia la pantalla
- `draw_border_rectangle(x, y, width, height, color)` - Dibuja borde rectangular
- `draw_cross_marker(x, y, size, color)` - Dibuja marcador de cruz
- `draw_grid(grid_x, grid_y, grid_width, grid_height, cell_size, color)` - Dibuja grilla
- `fill_rect_pattern(x, y, width, height, color, pattern_size)` - Rellena patrón rectangular
- `draw_axis(x, y, size, color_x, color_y)` - Dibuja ejes X e Y
- `calculate_distance(x1, y1, x2, y2)` - Calcula distancia entre puntos
- `clamp_coordinate(value, min_val, max_val)` - Limita valor a rango
- `wrap_coordinate(value, max_val)` - Envuelve coordenada

## Cómo Usar

### Ejemplo Básico

```opn
# Importar el módulo (cuando esté disponible)
import render;

main {
    gfx.setup_canvas(800, 600, "Mi Aplicacion");
    
    gfx.draw_circle(400, 300, 50, "Rojo");
    gfx.draw_circle(400, 300, 30, "Verde");
    
    gfx.update_screen();
}
```

### Ejecución

```bash
python -m prisma run render/examples/ejemplo_basico.prisma
python -m prisma run render/examples/ejemplo_animacion.prisma
```

## Paleta de Colores Disponibles

- Rojo
- Verde
- Azul
- Amarillo
- Púrpura
- Cian
- Blanco
- Negro

## Características

✓ 100% programado en OPN
✓ Sin dependencias externas
✓ Funciones reutilizables
✓ Ejemplos incluidos
✓ Fácil de extender

## Notas

- Todos los módulos están programados en OPN (.prisma)
- Las funciones usan solo `gfx.*` (API gráfica interna)
- No utiliza librerías externas de Python
- Totalmente compatible con el transpilador OPN
