# Ejemplos de Gráficos con GFX

Esta guía presenta ejemplos prácticos y tutoriales paso a paso para crear gráficos con el módulo `gfx`.

## Tabla de Contenidos

- [Nivel Básico](#nivel-básico)
- [Nivel Intermedio](#nivel-intermedio)
- [Nivel Avanzado](#nivel-avanzado)
- [Proyectos Completos](#proyectos-completos)

---

## Nivel Básico

### 1. Hola Mundo Gráfico

El programa más simple con gráficos:

```opn
main {
    gfx.setup_canvas(400, 400, "Hola Mundo");
    gfx.draw_circle(200, 200, 50, "Rojo");
    gfx.update_screen();
}
```

**Qué hace**:
1. Crea una ventana de 400x400 píxeles
2. Dibuja un círculo rojo en el centro
3. Muestra la ventana

---

### 2. Tres Círculos

Dibujando múltiples formas:

```opn
main {
    gfx.setup_canvas(800, 300, "Tres Círculos");
    
    # Círculo izquierdo
    gfx.draw_circle(150, 150, 80, "Rojo");
    
    # Círculo central
    gfx.draw_circle(400, 150, 80, "Verde");
    
    # Círculo derecho
    gfx.draw_circle(650, 150, 80, "Azul");
    
    gfx.update_screen();
}
```

---

### 3. Puntos en Línea

Usando bucles para crear patrones:

```opn
main {
    gfx.setup_canvas(600, 200, "Línea de Puntos");
    
    for i in 1..10 {
        let x = i * 60;
        gfx.draw_point(x, 100, "Azul");
    }
    
    gfx.update_screen();
}
```

---

## Nivel Intermedio

### 4. Círculos Concéntricos

Creando un patrón de anillos:

```opn
main {
    gfx.setup_canvas(600, 600, "Círculos Concéntricos");
    
    let centro_x = 300;
    let centro_y = 300;
    let colores = ["Rojo", "Amarillo", "Verde", "Cian", "Azul", "Púrpura"];
    
    for i in 1..6 {
        let radio = 250 - (i * 40);
        let indice = i - 1;
        gfx.draw_circle(centro_x, centro_y, radio, colores[indice]);
    }
    
    gfx.update_screen();
}
```

**Conceptos**:
- Variables para coordenadas
- Listas de colores
- Cálculo de radios decrecientes

---

### 5. Cuadrícula de Puntos

Patrón bidimensional con bucles anidados:

```opn
main {
    gfx.setup_canvas(500, 500, "Cuadrícula");
    
    for fila in 1..10 {
        for columna in 1..10 {
            let x = columna * 50;
            let y = fila * 50;
            gfx.draw_point(x, y, "Verde");
        }
    }
    
    gfx.update_screen();
}
```

---

### 6. Círculos Aleatorios

Usando colores y posiciones aleatorias:

```opn
main {
    gfx.setup_canvas(800, 600, "Círculos Aleatorios");
    
    for i in 1..20 {
        let x = py.random.randint(50, 750);
        let y = py.random.randint(50, 550);
        let radio = py.random.randint(10, 50);
        let color = gfx.get_random_color();
        
        gfx.draw_circle(x, y, radio, color);
    }
    
    gfx.update_screen();
}
```

**Conceptos**:
- Números aleatorios con `py.random.randint()`
- Colores aleatorios con `gfx.get_random_color()`
- Bucles para repetición

---

## Nivel Avanzado

### 7. Espiral de Círculos

Creando una espiral matemática:

```opn
main {
    gfx.setup_canvas(800, 800, "Espiral");
    
    let centro_x = 400;
    let centro_y = 400;
    let colores = ["Rojo", "Amarillo", "Verde", "Cian", "Azul", "Púrpura"];
    
    for i in 1..50 {
        let angulo = i * 0.5;
        let distancia = i * 8;
        
        # Aproximación simple de coordenadas polares
        let x = centro_x + (distancia * (i % 2));
        let y = centro_y + (distancia * ((i + 1) % 2));
        
        let color_idx = (i - 1) % 6;
        gfx.draw_circle(x, y, 15, colores[color_idx]);
    }
    
    gfx.update_screen();
}
```

---

### 8. Patrón de Onda

Simulando una onda con círculos:

```opn
main {
    gfx.setup_canvas(800, 400, "Onda");
    
    for i in 1..40 {
        let x = i * 20;
        let amplitud = 100;
        let frecuencia = 0.2;
        
        # Simulación simple de onda sinusoidal
        let offset = (i % 4) * 25;
        let y = 200 + offset - 50;
        
        let color = "Azul";
        if i % 2 == 0 {
            set color = "Cian";
        }
        
        gfx.draw_circle(x, y, 10, color);
    }
    
    gfx.update_screen();
}
```

---

### 9. Degradado de Tamaños

Círculos con tamaños progresivos:

```opn
main {
    gfx.setup_canvas(900, 300, "Degradado de Tamaños");
    
    for i in 1..15 {
        let x = i * 60;
        let y = 150;
        let radio = i * 3;
        
        let color = "Púrpura";
        if i > 10 {
            set color = "Rojo";
        } else {
            if i > 5 {
                set color = "Azul";
            }
        }
        
        gfx.draw_circle(x, y, radio, color);
    }
    
    gfx.update_screen();
}
```

---

## Proyectos Completos

### 10. Semáforo

Simulación de un semáforo:

```opn
func dibujar_semaforo(x, y, luz_activa) {
    # Caja del semáforo (simulada con círculos negros)
    gfx.draw_circle(x, y - 80, 35, "Negro");
    gfx.draw_circle(x, y, 35, "Negro");
    gfx.draw_circle(x, y + 80, 35, "Negro");
    
    # Luz roja
    if luz_activa == 1 {
        gfx.draw_circle(x, y - 80, 30, "Rojo");
    }
    
    # Luz amarilla
    if luz_activa == 2 {
        gfx.draw_circle(x, y, 30, "Amarillo");
    }
    
    # Luz verde
    if luz_activa == 3 {
        gfx.draw_circle(x, y + 80, 30, "Verde");
    }
}

main {
    gfx.setup_canvas(400, 600, "Semáforo");
    
    # Dibujar semáforo con luz verde activa
    dibujar_semaforo(200, 300, 3);
    
    gfx.update_screen();
}
```

---

### 11. Cara Sonriente

Dibujando una cara simple:

```opn
main {
    gfx.setup_canvas(500, 500, "Cara Sonriente");
    
    # Cara
    gfx.draw_circle(250, 250, 150, "Amarillo");
    
    # Ojo izquierdo
    gfx.draw_circle(200, 220, 15, "Negro");
    
    # Ojo derecho
    gfx.draw_circle(300, 220, 15, "Negro");
    
    # Sonrisa (simulada con puntos)
    for i in 1..10 {
        let x = 150 + (i * 20);
        let y = 300 + ((i - 5) * (i - 5) / 5);
        gfx.draw_point(x, y, "Negro");
    }
    
    gfx.update_screen();
}
```

---

### 12. Sistema Solar Simplificado

Representación básica del sistema solar:

```opn
main {
    gfx.setup_canvas(1000, 600, "Sistema Solar");
    
    # Sol
    gfx.draw_circle(500, 300, 60, "Amarillo");
    
    # Mercurio
    gfx.draw_circle(580, 300, 8, "Negro");
    
    # Venus
    gfx.draw_circle(630, 300, 15, "Amarillo");
    
    # Tierra
    gfx.draw_circle(700, 300, 18, "Azul");
    
    # Marte
    gfx.draw_circle(780, 300, 12, "Rojo");
    
    # Júpiter
    gfx.draw_circle(880, 300, 40, "Púrpura");
    
    gfx.update_screen();
}
```

---

### 13. Tablero de Ajedrez

Patrón de tablero usando círculos:

```opn
main {
    gfx.setup_canvas(640, 640, "Tablero");
    
    for fila in 0..7 {
        for columna in 0..7 {
            let x = 40 + (columna * 80);
            let y = 40 + (fila * 80);
            
            let color = "Blanco";
            if (fila + columna) % 2 == 0 {
                set color = "Negro";
            }
            
            gfx.draw_circle(x, y, 35, color);
        }
    }
    
    gfx.update_screen();
}
```

---

## Consejos y Trucos

### Optimización

1. **Agrupa las operaciones de dibujo**: Dibuja todo antes de llamar a `update_screen()`
2. **Usa variables para valores repetidos**: Facilita ajustes posteriores
3. **Comenta tu código**: Especialmente en patrones complejos

### Debugging

```opn
main {
    gfx.setup_canvas(400, 400, "Debug");
    
    let x = 200;
    let y = 200;
    
    py.print("Dibujando en:", x, y);  # Debug
    gfx.draw_circle(x, y, 50, "Rojo");
    
    gfx.update_screen();
}
```

### Experimentación

- Cambia valores gradualmente para ver el efecto
- Combina diferentes patrones
- Usa `py.random.randint()` para variación

---

## Desafíos

Intenta crear estos proyectos por tu cuenta:

1. **Bandera**: Dibuja la bandera de tu país
2. **Reloj**: Crea un reloj analógico simple
3. **Árbol**: Dibuja un árbol usando círculos
4. **Galaxia**: Simula una galaxia espiral
5. **Fuegos Artificiales**: Explosión de círculos de colores

---

**Relacionado**:
- [← API de Gráficos](gfx_api.md)
- [Referencia de Colores](gfx_colors.md)
- [← Volver al Índice](README.md)
