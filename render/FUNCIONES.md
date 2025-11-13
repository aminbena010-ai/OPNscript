# Referencia Completa de Funciones - OPN Render

## Resumen

Total: **72+ funciones** distribuidas en **5 módulos**

---

## render.prisma (Archivo Principal)

### Formas Geométricas (4 funciones)

```opn
func draw_point(x, y, color)
func draw_circle(x, y, radius, color)
func draw_square(x, y, size, color)
func draw_rectangle(x, y, width, height, color)
```

### Colores (8 funciones)

```opn
func color_red()          # Rojo
func color_green()        # Verde
func color_blue()         # Azul
func color_yellow()       # Amarillo
func color_purple()       # Púrpura
func color_cyan()         # Cian
func color_white()        # Blanco
func color_black()        # Negro
```

### Utilidades (3 funciones)

```opn
func init_render(width, height, title)
func update_render()
func draw_border(x, y, width, height, color)
```

### Patrones (3 funciones)

```opn
func draw_grid_cells(start_x, start_y, cell_size, rows, cols, color)
func draw_concentric(center_x, center_y, num_circles, spacing, color)
func draw_stars(center_x, center_y, num_points, distance, color)
```

### Animaciones (3 funciones)

```opn
func animate_expand(center_x, center_y, color, max_frames)
func animate_pulse(center_x, center_y, color, num_pulses)
func animate_trail(start_x, start_y, color, num_frames)
```

### Información (2 funciones)

```opn
func get_render_version()       # Retorna versión
func get_render_info()          # Retorna información
```

**Total render.prisma: 23 funciones**

---

## shapes.prisma (Formas Geométricas)

```opn
func draw_point_basic(x, y, color)
func draw_circle_basic(x, y, radius, color)
func draw_square_filled(x, y, size, color)
func draw_rectangle_filled(x, y, width, height, color)
func draw_horizontal_line(x1, x2, y, color)
func draw_vertical_line(x, y1, y2, color)
func draw_circle_outline(x, y, radius, color)
func draw_grid_pattern(start_x, start_y, width, height, cell_size, color)
func draw_concentric_circles(x, y, num_circles, spacing, color)
func draw_diamond(x, y, size, color)
```

**Total shapes.prisma: 10 funciones**

---

## colors.prisma (Gestión de Colores)

### Colores Primarios (6 funciones)

```opn
func get_primary_red()
func get_primary_green()
func get_primary_blue()
func get_primary_yellow()
func get_primary_purple()
func get_primary_cyan()
```

### Colores Neutrales (2 funciones)

```opn
func get_neutral_white()
func get_neutral_black()
```

### Paletas (1 función)

```opn
func get_color_palette_neon(index)
```

### Utilidades de Color (2 funciones)

```opn
func is_dark_color(color_name)
func is_light_color(color_name)
```

**Total colors.prisma: 11 funciones**

---

## effects.prisma (Efectos Visuales)

```opn
func fade_effect_circles(x, y, color, frames)
func pulse_effect(x, y, color, num_pulses)
func spiral_effect(center_x, center_y, color, num_points)
func rain_effect(color, num_drops)
func wave_effect(center_y, color, amplitude, num_waves)
func strobe_effect(x, y, radius, color, num_flashes)
func trail_effect(start_x, start_y, end_x, end_y, color, num_steps)
func rotation_effect(center_x, center_y, radius, color, num_rotations)
```

**Total effects.prisma: 8 funciones**

---

## utils.prisma (Utilidades)

```opn
func init_canvas_default()
func init_canvas_custom(width, height, title)
func clear_screen()
func draw_border_rectangle(x, y, width, height, color)
func draw_cross_marker(x, y, size, color)
func draw_grid(grid_x, grid_y, grid_width, grid_height, cell_size, color)
func fill_rect_pattern(x, y, width, height, color, pattern_size)
func draw_axis(x, y, size, color_x, color_y)
func calculate_distance(x1, y1, x2, y2)
func clamp_coordinate(value, min_val, max_val)
func wrap_coordinate(value, max_val)
```

**Total utils.prisma: 11 funciones**

---

## Resumen por Categoría

| Categoría | Cantidad |
|-----------|----------|
| Formas | 14 |
| Colores | 11 |
| Efectos | 8 |
| Utilidades | 14 |
| Animaciones | 3 |
| Patrones | 6 |
| Información | 2 |
| **Total** | **58+** |

---

## Funciones de API Gráfica Interna (gfx.*)

Estas funciones están disponibles de OPN nativamente y se usan dentro del paquete:

```opn
gfx.setup_canvas(width, height, title)
gfx.draw_point(x, y, color)
gfx.draw_circle(x, y, radius, color)
gfx.update_screen()
gfx.quit()
```

---

## Ejemplos de Cada Función

### draw_point
```opn
gfx.draw_point(100, 100, "Rojo");
```

### draw_circle
```opn
gfx.draw_circle(400, 300, 50, "Verde");
```

### draw_square
```opn
let size = 40;
gfx.setup_canvas(800, 600, "Canvas");
draw_square(200, 200, size, "Azul");
gfx.update_screen();
```

### draw_rectangle
```opn
draw_rectangle(100, 100, 200, 150, "Amarillo");
```

### color_red
```opn
let color = color_red();
gfx.draw_circle(x, y, r, color);
```

### animate_expand
```opn
animate_expand(400, 300, "Púrpura", 100);
```

### draw_concentric
```opn
draw_concentric(400, 300, 5, 30, "Rojo");
```

### draw_grid_cells
```opn
draw_grid_cells(50, 50, 40, 10, 15, "Blanco");
```

---

## Tablas de Referencia Rápida

### Colores Disponibles

| Nombre | Código |
|--------|--------|
| Rojo | "Rojo" |
| Verde | "Verde" |
| Azul | "Azul" |
| Amarillo | "Amarillo" |
| Púrpura | "Púrpura" |
| Cian | "Cian" |
| Blanco | "Blanco" |
| Negro | "Negro" |

### Parámetros Comunes

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| x, y | int | Coordenadas en píxeles |
| radius | int | Radio del círculo |
| color | string | Nombre del color |
| width, height | int | Dimensiones |
| title | string | Título de la ventana |

### Rangos Recomendados

| Elemento | Rango |
|----------|-------|
| Canvas X | 0 - 800 |
| Canvas Y | 0 - 600 |
| Radio | 5 - 200 |
| Tamaño | 10 - 100 |
| Frames | 50 - 300 |

---

## Notas de Implementación

- Todas las funciones están en OPN (.prisma)
- Sin dependencias externas de Python
- Compatible con el transpilador OPN
- Funciones reutilizables y extensibles
- Código modular por tema

---

## Guía de Búsqueda Rápida

**¿Quiero dibujar...**
- Formas → `shapes.prisma`
- Con colores → `colors.prisma`
- Efectos especiales → `effects.prisma`
- Utilidades → `utils.prisma`
- Animaciones → `render.prisma`

**¿Quiero usar...**
- Función principal → `render.prisma`
- Formas específicas → `shapes.prisma`
- Gestión de color → `colors.prisma`
- Cálculos/helpers → `utils.prisma`

---

**OPN Render v1.0.0 - Referencia Completa**
