import tkinter as tk
import random

# --- Variables de estado global para la API de Tkinter ---
_ROOT = None
_SCREEN = None
_RUNNING = False
_TITLE = ""
_DRAW_CALL_COUNT = 0
_UPDATE_COUNT = 0

def init():
    """Inicializa la ventana raíz de Tkinter si no existe."""
    global _ROOT, _RUNNING
    if _ROOT is None:
        _ROOT = tk.Tk()
        _ROOT.withdraw()  # Ocultar la ventana hasta que se configure el canvas
        _RUNNING = True
        print("[GFX TK] Tkinter Initialized.")

def quit():
    """Destruye la ventana de Tkinter si existe."""
    global _ROOT, _RUNNING, _DRAW_CALL_COUNT, _UPDATE_COUNT
    if _ROOT:
        # Report GFX stats before quitting
        print("\n--- GFX Stats ---")
        print(f"Total Draw Calls: {_DRAW_CALL_COUNT}")
        print(f"Total Screen Updates: {_UPDATE_COUNT}")
        print("-----------------\n")

        try:
            _ROOT.destroy()
        except tk.TclError:
            pass  # La ventana ya fue destruida
        _ROOT = None
        _RUNNING = False

def setup_canvas(width: int, height: int, title: str):
    """Configura y muestra el canvas principal."""
    global _ROOT, _SCREEN, _TITLE
    if not _ROOT:
        init()
    _ROOT.deiconify()  # Mostrar la ventana
    _TITLE = title
    _ROOT.title(title)
    if _SCREEN is None:
        _SCREEN = tk.Canvas(_ROOT, width=width, height=height, bg="#2c3e50")
        _SCREEN.pack()
    else:
        _SCREEN.config(width=width, height=height)
    print(f"[GFX TK] Canvas inicializado: {title} ({width}x{height})")

# Función auxiliar para convertir nombres de color a tuplas RGB
def _get_hex_color(color_name: str) -> str:
    """Convierte nombres de color a códigos hexadecimales para Tkinter."""
    colors = {
        "Rojo": "#e74c3c", "Verde": "#2ecc71", "Azul": "#3498db",
        "Amarillo": "#f1c40f", "Púrpura": "#9b59b6", "Cian": "#1abc9c",
        "Blanco": "#ecf0f1", "Negro": "#2c3e50"
    }
    return colors.get(color_name, "#ffffff") # Blanco por defecto

def draw_point(x: int, y: int, color: str):
    """Dibuja un pequeño círculo para simular un punto."""
    global _DRAW_CALL_COUNT
    if _SCREEN:
        _DRAW_CALL_COUNT += 1
        hex_color = _get_hex_color(color)
        _SCREEN.create_oval(x-1, y-1, x+1, y+1, fill=hex_color, outline=hex_color)
        
def draw_circle(x: int, y: int, radius: int, color: str):
    """Dibuja un círculo relleno."""
    global _DRAW_CALL_COUNT
    if _SCREEN:
        _DRAW_CALL_COUNT += 1
        hex_color = _get_hex_color(color)
        _SCREEN.create_oval(x-radius, y-radius, x+radius, y+radius, fill=hex_color, outline=hex_color)
        
def update_screen():
    """Refresca el canvas para mostrar los cambios."""
    global _UPDATE_COUNT
    if _ROOT:
        _UPDATE_COUNT += 1
        _ROOT.update()
        print("[GFX TK] Pantalla actualizada.")

# Función de utilidad para OPN
def get_random_color() -> str:
    """Devuelve un color aleatorio simple para el ejemplo."""
    return random.choice(["Rojo", "Verde", "Azul", "Amarillo", "Púrpura", "Cian"])