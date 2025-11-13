import json
import sys

files_to_check = [
    ('recursos/snippets.json', 'Snippets'),
    ('recursos/colores.json', 'Colores'),
    ('recursos/extensions.json', 'Extensiones')
]

all_ok = True
for filepath, label in files_to_check:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"[OK] {label}: {filepath}")
    except Exception as e:
        print(f"[ERROR] {label}: {str(e)}")
        all_ok = False

if all_ok:
    print("\n[SUCCESS] Todos los archivos JSON son validos")
else:
    print("\n[FAILED] Algunos archivos JSON tienen errores")
    sys.exit(1)
