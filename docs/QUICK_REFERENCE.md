# Referencia Rápida - Comandos OPNscript

## Compilación (Build)

### Opción 1: Build Rápido (Recomendado)
```bash
prisma build <carpeta_fuente> [-n nombre] [-v versión]
```

**Ejemplos:**
```bash
prisma build ./src                          # Nombre automático
prisma build ./src -n milib                 # Con nombre
prisma build ./src -n milib -v 2.0.0        # Con versión
```

### Opción 2: Build Avanzado
```bash
prisma compile <ruta> -o <salida> -n <nombre> \
  [-v version] [-d descripción] [-a autor]
```

**Ejemplo:**
```bash
prisma compile ./mylib -o ./dist -n mylib -v 3.0.0 \
  -d "My Library" -a "John Doe"
```

---

## Configuración

### Inicializar
```bash
prisma config init
```

### Ver Configuración
```bash
prisma config show
```

### Agregar Rutas
```bash
prisma config add-source /ruta/fuente
prisma config add-package /ruta/paquetes
```

---

## Imports en OPNscript

### Sintaxis
```prisma
import nombre_paquete;

func main() {
    nombre_paquete.funcion(args);
}
```

### Ejemplo
```prisma
import render;
import math;

func main() {
    let x = math.add(10, 20);
    render.draw_circle(400, 300, 50, render.color_red());
}
```

---

## Auto-Corrección

### Escanear Proyecto
```bash
prisma fix-paths <carpeta_proyecto>
```

---

## Archivos Generados

Compilar crea tres archivos automáticamente:

1. **.opn** - Metadatos del paquete
2. **functions.json** - Documentación completa
3. **index.prisma** - Código compilado

---

## Configuración Global

Se guardan en: `~/.opn/config/`

1. **packages.json** - Paquetes registrados
2. **paths.json** - Rutas configuradas
3. **settings.json** - Configuración

---

## Flujo Típico

```bash
# 1. Compilar tu código
prisma build ./src -n milib -v 1.0.0

# 2. Ver configuración
prisma config show

# 3. En tu proyecto, importar
# import milib;
```

---

## Cheat Sheet

| Tarea | Comando |
|-------|---------|
| Compilar carpeta | `prisma build ./src -n nombre` |
| Compilación completa | `prisma compile ./src -o ./dist -n nombre ...` |
| Ver config | `prisma config show` |
| Agregar ruta | `prisma config add-package /ruta` |
| Corregir imports | `prisma fix-paths ./proyecto` |

---

## Estructura de Carpeta Compilada

```
nombre_build/
├── index.prisma      # Código compilado
├── functions.json    # Documentación
└── nombre.opn        # Metadatos
```

---

## Usar Paquete

```prisma
import nombre;

func main() {
    nombre.funcion();
}
```

---

**Rápida referencia para compilación y empaquetado OPN**

Para más información, ver:
- `COMPILATION_GUIDE.md` - Guía completa
- `opn.import/BUILD_SYSTEM.md` - Sistema de compilación
- `opn.import/QUICK_START.md` - Inicio rápido
