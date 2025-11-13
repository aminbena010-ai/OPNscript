# Guía de Uso - Paquete OPN Render

## Introducción

OPN Render es un paquete completo de gráficos 2D diseñado específicamente para el lenguaje OPN. Todo está programado en OPN usando archivos `.prisma`, sin dependencias externas de Python.

## Inicio Rápido

### 1. Estructura del Paquete

```
render/
├── render.prisma              # Archivo principal (importar este)
├── shapes.prisma              # Funciones de formas
├── colors.prisma              # Gestión de colores
├── effects.prisma             # Efectos visuales
├── utils.prisma               # Utilidades
├── examples/                  # Ejemplos listos para usar
│   ├── ejemplo_basico.prisma
│   ├── ejemplo_animacion.prisma
│   └── demo_completo.prisma
└── README.md                  # Documentación
```

### 2. Crear tu Primer Programa

Crea un archivo `mi_programa.prisma`:

```opn
# Mi primer programa con OPN Render

func mi_escena() {
    gfx.setup_canvas(800, 600, "Mi Primera Escena");
    
    gfx.draw_circle(400, 300, 50, "Rojo");
    gfx.draw_circle(400, 300, 30, "Verde");
    gfx.draw_circle(400, 300, 10, "Azul");
    
    gfx.update_screen();
}

main {
    mi_escena();
}
```

### 3. Ejecutar tu Programa

```bash
python -m prisma run mi_programa.prisma
```

## Ejemplos Disponibles

### Ejemplo Básico
Formas geométricas simples:
```bash
python -m prisma run render/examples/ejemplo_basico.prisma
```

### Ejemplo Animación
Animaciones dinámicas:
```bash
python -m prisma run render/examples/ejemplo_animacion.prisma
```

### Demo Completo
Demostración de todas las características:
```bash
python -m prisma run render/examples/demo_completo.prisma
```

## Funciones Principales

### Inicialización

```opn
gfx.setup_canvas(ancho, alto, "Título");
```

### Dibujar Formas

```opn
gfx.draw_point(x, y, color);         # Punto
gfx.draw_circle(x, y, radio, color); # Círculo
```

### Actualizar Pantalla

```opn
gfx.update_screen();
```

## Colores Disponibles

```
"Rojo"
"Verde"
"Azul"
"Amarillo"
"Púrpura"
"Cian"
"Blanco"
"Negro"
```

## Patrones Comunes

### Grilla de Círculos

```opn
func grilla_circulos() {
    let row = 0;
    let col = 0;
    
    for row in 1..10 {
        for col in 1..10 {
            let x = 100 + col * 50;
            let y = 100 + row * 50;
            gfx.draw_circle(x, y, 15, "Azul");
        }
    }
}

main {
    gfx.setup_canvas(800, 600, "Grilla");
    grilla_circulos();
    gfx.update_screen();
}
```

### Círculos Concéntricos

```opn
func concentricos() {
    let i = 0;
    
    for i in 1..8 {
        let radius = i * 30;
        gfx.draw_circle(400, 300, radius, "Verde");
    }
}

main {
    gfx.setup_canvas(800, 600, "Concentricos");
    concentricos();
    gfx.update_screen();
}
```

### Animación Simple

```opn
func animacion() {
    let frame = 0;
    
    for frame in 1..100 {
        let radius = 10 + frame;
        gfx.draw_circle(400, 300, radius, "Rojo");
        gfx.update_screen();
    }
}

main {
    gfx.setup_canvas(800, 600, "Animacion");
    animacion();
}
```

## Consejos y Trucos

### 1. Usar Variables para Colores

```opn
let color_fondo = "Negro";
let color_forma = "Rojo";

gfx.draw_circle(x, y, r, color_forma);
```

### 2. Reutilizar Funciones

```opn
func dibujar_forma(x, y, color) {
    gfx.draw_circle(x, y, 30, color);
}

main {
    dibujar_forma(100, 100, "Rojo");
    dibujar_forma(200, 200, "Verde");
}
```

### 3. Loops Anidados para Patrones

```opn
for row in 1..5 {
    for col in 1..5 {
        let x = 100 + col * 60;
        let y = 100 + row * 60;
        gfx.draw_circle(x, y, 20, "Amarillo");
    }
}
```

### 4. Condicionales en Animaciones

```opn
for frame in 1..200 {
    let x = 100 + frame;
    
    if x >= 700 {
        x = 100;
    }
    
    gfx.draw_circle(x, 300, 15, "Azul");
    gfx.update_screen();
}
```

## Límites y Consideraciones

- Canvas: 800x600 píxeles (personalizable)
- Colores: 8 colores predefinidos
- Rendimiento: Óptimo para ~1000 draw calls/frame
- Animaciones: Máximo ~200 frames recomendado

## Solución de Problemas

### El programa no se ejecuta
- Verifica que el archivo tenga extensión `.prisma`
- Asegúrate de que `main { }` existe en tu código

### El canvas no aparece
- Llama a `gfx.setup_canvas()` al inicio
- Llama a `gfx.update_screen()` al final

### Las formas no aparecen
- Verifica los colores: usa nombres exactos (ej: "Rojo", no "rojo")
- Asegúrate de que las coordenadas estén dentro del canvas

## Extender el Paquete

Para agregar nuevas funciones, edita el archivo correspondiente:

```opn
# En shapes.prisma
func mi_nueva_forma(x, y, color) {
    gfx.draw_circle(x, y, 20, color);
}
```

## Recursos Adicionales

- Documentación completa: `render/README.md`
- Ejemplos: `render/examples/`
- API gráfica interna: `gfx.*`

¡Que disfrutes creando con OPN Render!
