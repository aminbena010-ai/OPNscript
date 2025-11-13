
# OPNscript - El Lenguaje de Programación OPN

**OPN** es un lenguaje de programación moderno, fácil de aprender y con una potente API de gráficos 2D integrada. Diseñado para ser intuitivo, OPN transpila a Python, combinando la simplicidad de un lenguaje de script con el poder del ecosistema de Python.

**[Visita la Documentación Completa →](https://aminbena010-ai.github.io/OPNscript/)**

---

## Descripción

OPN es un lenguaje de programación moderno, fácil de aprender y con una potente API de gráficos 2D integrada. Diseñado para ser intuitivo, OPN transpila a Python, combinando la simplicidad de un lenguaje de script con el poder del ecosistema de Python.

## Características

-   **Sintaxis Sencilla e Intuitiva**: Inspirado en lenguajes populares, OPN es fácil de leer y escribir, ideal para principiantes y programadores experimentados.
-   **API de Gráficos 2D Integrada**: Crea visualizaciones, juegos simples y arte generativo sin necesidad de librerías externas, usando el módulo `gfx`.
-   **Basado en Python**: Se transpila a código Python, lo que garantiza un rendimiento sólido y acceso a un vasto ecosistema.
-   **Herramientas de Desarrollo**: Incluye un REPL interactivo para experimentación rápida y un Editor de Código con resaltado de sintaxis.
-   **Multi-paradigma**: Ofrece una sintaxis familiar para programadores de Python, C++, C# y JavaScript a través de su librería estándar.

---

## 🚀 Inicio Rápido

### 1. Requisitos

-   **Python 3.8+**
-   **Git**

### 2. Instalación

Clona el repositorio en tu máquina local:
```bash
git clone https://github.com/aminbena010-ai/OPNscript.git
cd OPNscript
```

### 3. ¡Hola, Mundo!

1.  Crea un archivo llamado `hola.opn` con el siguiente contenido:
    ```opn
    main {
        py.print("¡Hola, OPN!");
    }
    ```

2.  Ejecútalo desde la terminal en la carpeta raíz del proyecto:
    ```bash
    python -m src.prisma run hola.opn
    ```

---

## 🎨 Ejemplo Gráfico

Prueba el poder de la API de gráficos integrada. Crea un archivo `circulo.opn`:
```opn
main {
    gfx.setup_canvas(400, 400, "Mi Círculo OPN");
    gfx.draw_circle(200, 200, 80, "Rojo");
    gfx.update_screen();
}
```
Ejecútalo de la misma manera y verás una ventana con un círculo rojo.

---

## 📚 Documentación

Para una guía completa, referencia de la API y más ejemplos, visita la documentación oficial. La web incluye:

-   Tutoriales detallados.
-   Buscador integrado.
-   Ejemplos de código interactivos.
-   Sección de comunidad para dejar feedback.

**Leer la Documentación →**

---

## 💬 Comunidad y Contribuciones

¡Tu opinión es muy importante! Si tienes ideas, sugerencias o encuentras un error, por favor, compártelo en la sección de **Contacto y Feedback** de la documentación o abre un "Issue" en este repositorio.
