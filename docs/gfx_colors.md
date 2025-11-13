# Referencia de Colores GFX

Esta página documenta todos los colores disponibles en el módulo `gfx` de OPN.

## Tabla de Contenidos

- [Paleta de Colores](#paleta-de-colores)
- [Uso de Colores](#uso-de-colores)
- [Códigos Hexadecimales](#códigos-hexadecimales)
- [Ejemplos](#ejemplos)

---

## Paleta de Colores

El módulo `gfx` proporciona 8 colores predefinidos con nombres en español:

| Nombre | Código Hex | Vista Previa | Descripción |
|--------|-----------|--------------|-------------|
| `"Rojo"` | `#e74c3c` | 🔴 | Rojo vibrante |
| `"Verde"` | `#2ecc71` | 🟢 | Verde esmeralda |
| `"Azul"` | `#3498db` | 🔵 | Azul cielo |
| `"Amarillo"` | `#f1c40f` | 🟡 | Amarillo dorado |
| `"Púrpura"` | `#9b59b6` | 🟣 | Púrpura amatista |
| `"Cian"` | `#1abc9c` | 🔷 | Cian turquesa |
| `"Blanco"` | `#ecf0f1` | ⚪ | Blanco nube |
| `"Negro"` | `#2c3e50` | ⚫ | Negro medianoche |

---

## Uso de Colores

### Sintaxis

Los colores se especifican como strings con el nombre exacto (sensible a mayúsculas):

```opn
gfx.draw_circle(x, y, radio, "NombreColor");
gfx.draw_point(x, y, "NombreColor");
```

### Reglas Importantes

1. **Case-sensitive**: Debe escribirse exactamente como se muestra
   - ✅ Correcto: `"Rojo"`, `"Azul"`, `"Púrpura"`
   - ❌ Incorrecto: `"rojo"`, `"AZUL"`, `"purpura"`

2. **Acentos**: Respetar los acentos en los nombres
   - ✅ Correcto: `"Púrpura"`
   - ❌ Incorrecto: `"Purpura"`

3. **Color por defecto**: Si se proporciona un nombre inválido, se usa blanco (`#ffffff`)

---

## Códigos Hexadecimales

### Tabla de Conversión

```
Rojo      → #e74c3c  (RGB: 231, 76, 60)
Verde     → #2ecc71  (RGB: 46, 204, 113)
Azul      → #3498db  (RGB: 52, 152, 219)
Amarillo  → #f1c40f  (RGB: 241, 196, 15)
Púrpura   → #9b59b6  (RGB: 155, 89, 182)
Cian      → #1abc9c  (RGB: 26, 188, 156)
Blanco    → #ecf0f1  (RGB: 236, 240, 241)
Negro     → #2c3e50  (RGB: 44, 62, 80)
```

### Paleta Flat Design

Los colores están inspirados en la paleta **Flat UI Colors**, diseñada para interfaces modernas y atractivas.

---

## Ejemplos

### Ejemplo 1: Todos los Colores

```opn
main {
    gfx.setup_canvas(800, 400, "Paleta de Colores");
    
    gfx.draw_circle(100, 200, 40, "Rojo");
    gfx.draw_circle(200, 200, 40, "Verde");
    gfx.draw_circle(300, 200, 40, "Azul");
    gfx.draw_circle(400, 200, 40, "Amarillo");
    gfx.draw_circle(500, 200, 40, "Púrpura");
    gfx.draw_circle(600, 200, 40, "Cian");
    gfx.draw_circle(700, 200, 40, "Blanco");
    
    gfx.update_screen();
}
```

### Ejemplo 2: Gradiente de Puntos

```opn
main {
    gfx.setup_canvas(600, 400, "Puntos de Colores");
    
    let colores = ["Rojo", "Verde", "Azul", "Amarillo", "Púrpura", "Cian"];
    
    for i in 0..5 {
        for j in 0..9 {
            let x = 50 + (j * 60);
            let y = 50 + (i * 60);
            gfx.draw_point(x, y, colores[i]);
        }
    }
    
    gfx.update_screen();
}
```

### Ejemplo 3: Color Aleatorio

```opn
main {
    gfx.setup_canvas(400, 400, "Color Aleatorio");
    
    let color = gfx.get_random_color();
    py.print("Color seleccionado:", color);
    
    gfx.draw_circle(200, 200, 150, color);
    gfx.update_screen();
}
```

### Ejemplo 4: Círculos Concéntricos

```opn
main {
    gfx.setup_canvas(600, 600, "Círculos Concéntricos");
    
    gfx.draw_circle(300, 300, 200, "Rojo");
    gfx.draw_circle(300, 300, 150, "Amarillo");
    gfx.draw_circle(300, 300, 100, "Verde");
    gfx.draw_circle(300, 300, 50, "Azul");
    
    gfx.update_screen();
}
```

---

## Combinaciones Recomendadas

### Esquemas de Color

**Colores Primarios**:
```opn
"Rojo", "Azul", "Amarillo"
```

**Colores Fríos**:
```opn
"Azul", "Cian", "Púrpura"
```

**Colores Cálidos**:
```opn
"Rojo", "Amarillo", "Púrpura"
```

**Alto Contraste**:
```opn
"Negro", "Blanco"
"Rojo", "Cian"
"Azul", "Amarillo"
```

---

## Implementación Interna

El módulo `gfx` convierte los nombres de colores a códigos hexadecimales internamente:

```python
def _get_hex_color(color_name: str) -> str:
    colors = {
        "Rojo": "#e74c3c",
        "Verde": "#2ecc71",
        "Azul": "#3498db",
        "Amarillo": "#f1c40f",
        "Púrpura": "#9b59b6",
        "Cian": "#1abc9c",
        "Blanco": "#ecf0f1",
        "Negro": "#2c3e50"
    }
    return colors.get(color_name, "#ffffff")
```

---

## Próximas Características

En futuras versiones se planea agregar:

- ✨ Soporte para códigos hexadecimales directos
- 🎨 Paleta extendida con más colores
- 🌈 Funciones de mezcla de colores
- 📊 Gradientes automáticos

---

**Relacionado**:
- [← API de Gráficos](gfx_api.md)
- [Ejemplos de Gráficos →](gfx_examples.md)
- [← Volver al Índice](README.md)
