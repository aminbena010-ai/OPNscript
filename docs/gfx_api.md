# API de Gráficos (GFX)

El módulo `gfx` proporciona capacidades de renderizado 2D utilizando **Tkinter** como motor de renderizado.

## Tabla de Contenidos

- [Introducción](#introducción)
- [Configuración Inicial](#configuración-inicial)
- [Funciones de Dibujo](#funciones-de-dibujo)
- [Gestión de Ventana](#gestión-de-ventana)
- [Utilidades](#utilidades)
- [Ejemplos](#ejemplos)

---

## Introducción

El módulo `gfx` está disponible automáticamente en todos los programas OPN. No requiere importación explícita.

### Motor de Renderizado

**Versión actual**: Tkinter  
**Características**:
- Canvas 2D con coordenadas cartesianas
- Sistema de colores predefinidos
- Renderizado en tiempo real
- Gestión automática de ventanas

---

## Configuración Inicial

### `gfx.setup_canvas(width, height, title)`

Inicializa el canvas de dibujo y crea la ventana principal.

**Parámetros**:
- `width` (int): Ancho del canvas en píxeles
- `height` (int): Alto del canvas en píxeles  
- `title` (string): Título de la ventana

**Ejemplo**:
```opn
main {
    gfx.setup_canvas(800, 600, "Mi Aplicación");
}
```

**Notas**:
- Debe llamarse antes de cualquier función de dibujo
- Solo se puede llamar una vez por programa
- El color de fondo por defecto es `#2c3e50` (azul oscuro)

---

## Funciones de Dibujo

### `gfx.draw_point(x, y, color)`

Dibuja un punto (círculo pequeño de 2px de radio) en las coordenadas especificadas.

**Parámetros**:
- `x` (int): Coordenada X del punto
- `y` (int): Coordenada Y del punto
- `color` (string): Nombre del color (ver [Referencia de Colores](gfx_colors.md))

**Ejemplo**:
```opn
gfx.draw_point(100, 100, "Rojo");
gfx.draw_point(200, 150, "Verde");
```

---

### `gfx.draw_circle(x, y, radius, color)`

Dibuja un círculo relleno centrado en las coordenadas especificadas.

**Parámetros**:
- `x` (int): Coordenada X del centro
- `y` (int): Coordenada Y del centro
- `radius` (int): Radio del círculo en píxeles
- `color` (string): Nombre del color

**Ejemplo**:
```opn
gfx.draw_circle(400, 300, 50, "Azul");
gfx.draw_circle(500, 300, 75, "Púrpura");
```

**Notas**:
- El círculo se dibuja desde el centro
- El borde y el relleno usan el mismo color

---

## Gestión de Ventana

### `gfx.update_screen()`

Actualiza el canvas para mostrar todos los cambios realizados.

**Ejemplo**:
```opn
main {
    gfx.setup_canvas(800, 600, "Demo");
    gfx.draw_circle(400, 300, 100, "Rojo");
    gfx.update_screen();  # Muestra los cambios
}
```

**Notas**:
- Debe llamarse después de dibujar para ver los resultados
- Refresca toda la ventana
- Mantiene la ventana abierta hasta que el usuario la cierre

---

### `gfx.init()`

Inicializa el sistema de ventanas Tkinter manualmente.

**Uso**:
```opn
gfx.init();
```

**Notas**:
- Generalmente no es necesario llamarla directamente
- `setup_canvas()` la llama automáticamente
- Útil para configuraciones avanzadas

---

### `gfx.quit()`

Cierra la ventana y libera recursos.

**Uso**:
```opn
gfx.quit();
```

**Notas**:
- Se llama automáticamente al finalizar el programa
- Destruye la ventana de Tkinter
- No es necesario llamarla manualmente en la mayoría de casos

---

## Utilidades

### `gfx.get_random_color()`

Devuelve un nombre de color aleatorio de la paleta disponible.

**Retorna**: String con el nombre del color

**Ejemplo**:
```opn
main {
    let color = gfx.get_random_color();
    gfx.setup_canvas(400, 400, "Color Aleatorio");
    gfx.draw_circle(200, 200, 100, color);
    gfx.update_screen();
}
```

**Colores posibles**:
- "Rojo", "Verde", "Azul"
- "Amarillo", "Púrpura", "Cian"

---

## Ejemplos

### Ejemplo 1: Punto Simple

```opn
main {
    gfx.setup_canvas(400, 400, "Punto");
    gfx.draw_point(200, 200, "Rojo");
    gfx.update_screen();
}
```

### Ejemplo 2: Múltiples Círculos

```opn
main {
    gfx.setup_canvas(800, 600, "Círculos");
    
    gfx.draw_circle(200, 300, 80, "Rojo");
    gfx.draw_circle(400, 300, 80, "Verde");
    gfx.draw_circle(600, 300, 80, "Azul");
    
    gfx.update_screen();
}
```

### Ejemplo 3: Patrón con Bucle

```opn
main {
    gfx.setup_canvas(800, 600, "Patrón");
    
    for i in 1..10 {
        let x = i * 80;
        let radio = i * 5;
        gfx.draw_circle(x, 300, radio, "Púrpura");
    }
    
    gfx.update_screen();
}
```

---

## Sistema de Coordenadas

El canvas usa un sistema de coordenadas estándar:

```
(0,0) ────────────────► X
  │
  │
  │
  │
  ▼
  Y
```

- **Origen**: Esquina superior izquierda (0, 0)
- **Eje X**: Aumenta hacia la derecha
- **Eje Y**: Aumenta hacia abajo

---

## Próximos Pasos

- Ver [Ejemplos de Gráficos](gfx_examples.md) para proyectos completos
- Consultar [Referencia de Colores](gfx_colors.md) para la paleta completa
- Explorar [Tutoriales Avanzados](gfx_advanced.md) para técnicas avanzadas

---

**Relacionado**:
- [← Volver al Índice](README.md)
- [Ejemplos de Gráficos →](gfx_examples.md)
- [Referencia de Colores →](gfx_colors.md)
