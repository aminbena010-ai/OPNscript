import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import sys
import os
import re
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from prisma.config import CALL_ALIASES, KEYWORDS, OPERATORS, BUILTINS, GFX_FUNCTIONS, GFX_COLORS, SYNTAX_COLORS, THEME_COLORS

class ErrorDetector:
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def check_syntax(self, code: str) -> List[Dict]:
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('if ') and not stripped.endswith(':'):
                issues.append({
                    'line': i,
                    'type': 'error',
                    'message': 'Falta ":" al final de la declaración if'
                })
            
            if stripped.startswith('def ') and not stripped.endswith(':'):
                issues.append({
                    'line': i,
                    'type': 'error',
                    'message': 'Falta ":" al final de la declaración de función'
                })
            
            if stripped.startswith('for ') and not stripped.endswith(':'):
                issues.append({
                    'line': i,
                    'type': 'error',
                    'message': 'Falta ":" al final del bucle for'
                })
            
            if stripped.startswith('while ') and not stripped.endswith(':'):
                issues.append({
                    'line': i,
                    'type': 'error',
                    'message': 'Falta ":" al final del bucle while'
                })
            
            open_parens = line.count('(')
            close_parens = line.count(')')
            if open_parens != close_parens:
                issues.append({
                    'line': i,
                    'type': 'warning',
                    'message': f'Paréntesis desbalanceados: {open_parens} abiertos, {close_parens} cerrados'
                })
            
            open_brackets = line.count('[')
            close_brackets = line.count(']')
            if open_brackets != close_brackets:
                issues.append({
                    'line': i,
                    'type': 'warning',
                    'message': f'Corchetes desbalanceados: {open_brackets} abiertos, {close_brackets} cerrados'
                })
            
            open_braces = line.count('{')
            close_braces = line.count('}')
            if open_braces != close_braces:
                issues.append({
                    'line': i,
                    'type': 'warning',
                    'message': f'Llaves desbalanceadas: {open_braces} abiertas, {close_braces} cerradas'
                })
        
        return issues

class AutoCompleter:
    def __init__(self):
        self.suggestions = []
        self.current_word = ""
        self.position = None
        
    def get_suggestions(self, text: str, cursor_pos: str) -> List[str]:
        try:
            line_start = text.rfind('\n', 0, text.index(cursor_pos)) + 1
            line_text = text[line_start:text.index(cursor_pos)]
            
            words = re.findall(r'\b\w+\b', line_text)
            if not words:
                return []
            
            current_word = words[-1]
            self.current_word = current_word
            
            suggestions = []
            
            for keyword in KEYWORDS:
                if keyword.startswith(current_word):
                    suggestions.append(keyword)
            
            for builtin in BUILTINS.keys():
                if builtin.startswith(current_word):
                    suggestions.append(builtin)
            
            for gfx_func in GFX_FUNCTIONS.keys():
                if gfx_func.startswith(current_word):
                    suggestions.append(gfx_func)
            
            for color in GFX_COLORS:
                if color.startswith(current_word):
                    suggestions.append(color)
            
            for alias in CALL_ALIASES.keys():
                if alias.startswith(current_word):
                    suggestions.append(alias)
            
            return sorted(set(suggestions))[:10]
        except:
            return []

class ConsoleWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg='#1E1E1E')
        
        self.output = scrolledtext.ScrolledText(
            self,
            height=10,
            bg='#1E1E1E',
            fg='#D4D4D4',
            insertbackground='#AEAFAD',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        input_frame = tk.Frame(self, bg='#1E1E1E')
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(input_frame, text='>', bg='#1E1E1E', fg='#4EC9B0', font=('Consolas', 10, 'bold')).pack(side=tk.LEFT)
        
        self.input = tk.Entry(
            input_frame,
            bg='#2D2D2D',
            fg='#D4D4D4',
            insertbackground='#AEAFAD',
            font=('Consolas', 10),
            relief=tk.FLAT
        )
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input.bind('<Return>', self.execute_command)
        
        self.command_history = []
        self.history_index = -1
        self.input.bind('<Up>', self.history_up)
        self.input.bind('<Down>', self.history_down)
        
        self.write("OPN Console v1.0 - Escribe 'help' para ver comandos disponibles\n", 'info')
    
    def write(self, text: str, tag: str = 'normal'):
        self.output.insert(tk.END, text + '\n', tag)
        self.output.tag_config('normal', foreground='#D4D4D4')
        self.output.tag_config('info', foreground='#4FC1FF')
        self.output.tag_config('error', foreground='#F44747')
        self.output.tag_config('success', foreground='#4EC9B0')
        self.output.tag_config('warning', foreground='#CCA700')
        self.output.see(tk.END)
    
    def clear(self):
        self.output.delete('1.0', tk.END)
    
    def execute_command(self, event=None):
        command = self.input.get().strip()
        if not command:
            return
        
        self.write(f'> {command}', 'info')
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        self.input.delete(0, tk.END)
        
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd == 'help':
            self.show_help()
        elif cmd == 'clear':
            self.clear()
        elif cmd == 'version':
            self.write('OPN Language v1.0.0', 'success')
        elif cmd == 'run':
            if args:
                self.run_file(args[0])
            else:
                self.write('Error: Especifica un archivo para ejecutar', 'error')
        elif cmd == 'transpile':
            if args:
                self.transpile_file(args[0])
            else:
                self.write('Error: Especifica un archivo para transpilar', 'error')
        elif cmd == 'check':
            if args:
                self.check_file(args[0])
            else:
                self.write('Error: Especifica un archivo para verificar', 'error')
        elif cmd == 'ls':
            self.list_files(args[0] if args else '.')
        elif cmd == 'pwd':
            self.write(os.getcwd(), 'normal')
        elif cmd == 'cd':
            if args:
                try:
                    os.chdir(args[0])
                    self.write(f'Directorio cambiado a: {os.getcwd()}', 'success')
                except Exception as e:
                    self.write(f'Error: {str(e)}', 'error')
            else:
                self.write('Error: Especifica un directorio', 'error')
        elif cmd == 'python':
            self.execute_python(' '.join(args))
        elif cmd == 'exit':
            self.write('Usa el botón de cerrar para salir del editor', 'warning')
        else:
            self.write(f'Comando desconocido: {cmd}. Escribe "help" para ver comandos disponibles', 'error')
    
    def show_help(self):
        help_text = """
Comandos disponibles:
  help              - Muestra esta ayuda
  clear             - Limpia la consola
  version           - Muestra la versión de OPN
  run <archivo>     - Ejecuta un archivo .prisma
  transpile <arch>  - Transpila un archivo .prisma a Python
  check <archivo>   - Verifica errores en un archivo
  ls [directorio]   - Lista archivos en el directorio
  pwd               - Muestra el directorio actual
  cd <directorio>   - Cambia el directorio actual
  python <código>   - Ejecuta código Python directamente
  exit              - Cierra el editor
"""
        self.write(help_text, 'info')
    
    def run_file(self, filepath: str):
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'prisma', 'run', filepath],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.stdout:
                self.write(result.stdout, 'normal')
            if result.stderr:
                self.write(result.stderr, 'error')
            if result.returncode == 0:
                self.write(f'Ejecución completada exitosamente', 'success')
            else:
                self.write(f'Ejecución terminó con código {result.returncode}', 'error')
        except subprocess.TimeoutExpired:
            self.write('Error: Tiempo de ejecución excedido (30s)', 'error')
        except Exception as e:
            self.write(f'Error: {str(e)}', 'error')
    
    def transpile_file(self, filepath: str):
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'prisma', 'transpile', filepath],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.stdout:
                self.write(result.stdout, 'normal')
            if result.stderr:
                self.write(result.stderr, 'error')
            if result.returncode == 0:
                self.write(f'Transpilación completada', 'success')
        except Exception as e:
            self.write(f'Error: {str(e)}', 'error')
    
    def check_file(self, filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            detector = ErrorDetector()
            issues = detector.check_syntax(code)
            
            if not issues:
                self.write(f'✓ No se encontraron problemas en {filepath}', 'success')
            else:
                self.write(f'Se encontraron {len(issues)} problema(s):', 'warning')
                for issue in issues:
                    tag = 'error' if issue['type'] == 'error' else 'warning'
                    self.write(f"  Línea {issue['line']}: {issue['message']}", tag)
        except Exception as e:
            self.write(f'Error: {str(e)}', 'error')
    
    def list_files(self, directory: str):
        try:
            files = os.listdir(directory)
            self.write(f'Archivos en {os.path.abspath(directory)}:', 'info')
            for f in sorted(files):
                path = os.path.join(directory, f)
                if os.path.isdir(path):
                    self.write(f'  📁 {f}/', 'normal')
                else:
                    ext = os.path.splitext(f)[1]
                    icon = '📄' if ext in ['.prisma', '.opn', '.py'] else '📋'
                    self.write(f'  {icon} {f}', 'normal')
        except Exception as e:
            self.write(f'Error: {str(e)}', 'error')
    
    def execute_python(self, code: str):
        try:
            result = eval(code)
            if result is not None:
                self.write(str(result), 'success')
        except Exception as e:
            try:
                exec(code)
                self.write('Código ejecutado', 'success')
            except Exception as e2:
                self.write(f'Error: {str(e2)}', 'error')
    
    def history_up(self, event):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.input.delete(0, tk.END)
            self.input.insert(0, self.command_history[self.history_index])
    
    def history_down(self, event):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input.delete(0, tk.END)
            self.input.insert(0, self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.input.delete(0, tk.END)

class DocumentationPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg='#1E1E1E')
        
        search_frame = tk.Frame(self, bg='#1E1E1E')
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(search_frame, text='Buscar:', bg='#1E1E1E', fg='#D4D4D4', font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_docs)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            bg='#2D2D2D',
            fg='#D4D4D4',
            insertbackground='#AEAFAD',
            font=('Consolas', 9),
            relief=tk.FLAT
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.category_var = tk.StringVar(value='Todos')
        categories = ['Todos', 'Builtins', 'GFX', 'Keywords', 'Aliases']
        category_menu = ttk.Combobox(
            search_frame,
            textvariable=self.category_var,
            values=categories,
            state='readonly',
            width=12
        )
        category_menu.pack(side=tk.LEFT, padx=5)
        category_menu.bind('<<ComboboxSelected>>', lambda e: self.filter_docs())
        
        self.doc_text = scrolledtext.ScrolledText(
            self,
            bg='#1E1E1E',
            fg='#D4D4D4',
            insertbackground='#AEAFAD',
            font=('Consolas', 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.doc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.doc_text.tag_config('title', foreground='#4EC9B0', font=('Consolas', 11, 'bold'))
        self.doc_text.tag_config('signature', foreground='#DCDCAA', font=('Consolas', 9, 'bold'))
        self.doc_text.tag_config('description', foreground='#D4D4D4')
        self.doc_text.tag_config('example', foreground='#CE9178', font=('Consolas', 9, 'italic'))
        self.doc_text.tag_config('category', foreground='#569CD6', font=('Consolas', 9, 'bold'))
        
        self.load_documentation()
    
    def load_documentation(self):
        self.doc_text.config(state=tk.NORMAL)
        self.doc_text.delete('1.0', tk.END)
        
        self.doc_text.insert(tk.END, '═' * 60 + '\n')
        self.doc_text.insert(tk.END, 'DOCUMENTACIÓN OPN LANGUAGE\n', 'title')
        self.doc_text.insert(tk.END, '═' * 60 + '\n\n')
        
        self.add_category_docs('FUNCIONES BUILTIN', BUILTINS)
        self.add_category_docs('FUNCIONES GFX', GFX_FUNCTIONS)
        self.add_keywords_docs()
        self.add_aliases_docs()
        
        self.doc_text.config(state=tk.DISABLED)
    
    def add_category_docs(self, title: str, functions: Dict):
        self.doc_text.insert(tk.END, f'\n{title}\n', 'category')
        self.doc_text.insert(tk.END, '─' * 60 + '\n')
        
        for name, info in functions.items():
            self.doc_text.insert(tk.END, f'\n• {name}\n', 'title')
            self.doc_text.insert(tk.END, f'  {info["signature"]}\n', 'signature')
            self.doc_text.insert(tk.END, f'  {info["description"]}\n', 'description')
            self.doc_text.insert(tk.END, f'  Ejemplo: {info["example"]}\n', 'example')
    
    def add_keywords_docs(self):
        self.doc_text.insert(tk.END, f'\nPALABRAS CLAVE\n', 'category')
        self.doc_text.insert(tk.END, '─' * 60 + '\n')
        self.doc_text.insert(tk.END, ', '.join(KEYWORDS) + '\n', 'description')
    
    def add_aliases_docs(self):
        self.doc_text.insert(tk.END, f'\nALIAS DE FUNCIONES\n', 'category')
        self.doc_text.insert(tk.END, '─' * 60 + '\n')
        for alias, target in list(CALL_ALIASES.items())[:10]:
            self.doc_text.insert(tk.END, f'  {alias} → {target}\n', 'description')
    
    def filter_docs(self, *args):
        search_term = self.search_var.get().lower()
        category = self.category_var.get()
        
        self.doc_text.config(state=tk.NORMAL)
        self.doc_text.delete('1.0', tk.END)
        
        if not search_term and category == 'Todos':
            self.load_documentation()
            return
        
        self.doc_text.insert(tk.END, f'Resultados de búsqueda: "{search_term}" en {category}\n\n', 'title')
        
        if category in ['Todos', 'Builtins']:
            for name, info in BUILTINS.items():
                if search_term in name.lower() or search_term in info['description'].lower():
                    self.doc_text.insert(tk.END, f'• {name}\n', 'title')
                    self.doc_text.insert(tk.END, f'  {info["signature"]}\n', 'signature')
                    self.doc_text.insert(tk.END, f'  {info["description"]}\n', 'description')
                    self.doc_text.insert(tk.END, f'  Ejemplo: {info["example"]}\n\n', 'example')
        
        if category in ['Todos', 'GFX']:
            for name, info in GFX_FUNCTIONS.items():
                if search_term in name.lower() or search_term in info['description'].lower():
                    self.doc_text.insert(tk.END, f'• {name}\n', 'title')
                    self.doc_text.insert(tk.END, f'  {info["signature"]}\n', 'signature')
                    self.doc_text.insert(tk.END, f'  {info["description"]}\n', 'description')
                    self.doc_text.insert(tk.END, f'  Ejemplo: {info["example"]}\n\n', 'example')
        
        self.doc_text.config(state=tk.DISABLED)

class OPNEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('OPN Editor v1.0')
        self.geometry('1400x900')
        self.configure(bg='#1E1E1E')
        
        self.current_file = None
        self.autocompleter = AutoCompleter()
        self.error_detector = ErrorDetector()
        
        self.create_menu()
        self.create_toolbar()
        self.create_main_layout()
        self.create_status_bar()
        
        self.bind_shortcuts()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        menubar = tk.Menu(self, bg='#2D2D2D', fg='#D4D4D4')
        self.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg='#2D2D2D', fg='#D4D4D4')
        menubar.add_cascade(label='Archivo', menu=file_menu)
        file_menu.add_command(label='Nuevo', command=self.new_file, accelerator='Ctrl+N')
        file_menu.add_command(label='Abrir...', command=self.open_file, accelerator='Ctrl+O')
        file_menu.add_command(label='Guardar', command=self.save_file, accelerator='Ctrl+S')
        file_menu.add_command(label='Guardar como...', command=self.save_file_as, accelerator='Ctrl+Shift+S')
        file_menu.add_separator()
        file_menu.add_command(label='Salir', command=self.on_closing, accelerator='Alt+F4')
        
        edit_menu = tk.Menu(menubar, tearoff=0, bg='#2D2D2D', fg='#D4D4D4')
        menubar.add_cascade(label='Editar', menu=edit_menu)
        edit_menu.add_command(label='Deshacer', command=self.undo, accelerator='Ctrl+Z')
        edit_menu.add_command(label='Rehacer', command=self.redo, accelerator='Ctrl+Y')
        edit_menu.add_separator()
        edit_menu.add_command(label='Cortar', command=self.cut, accelerator='Ctrl+X')
        edit_menu.add_command(label='Copiar', command=self.copy, accelerator='Ctrl+C')
        edit_menu.add_command(label='Pegar', command=self.paste, accelerator='Ctrl+V')
        edit_menu.add_separator()
        edit_menu.add_command(label='Buscar', command=self.find, accelerator='Ctrl+F')
        
        run_menu = tk.Menu(menubar, tearoff=0, bg='#2D2D2D', fg='#D4D4D4')
        menubar.add_cascade(label='Ejecutar', menu=run_menu)
        run_menu.add_command(label='Ejecutar', command=self.run_code, accelerator='F5')
        run_menu.add_command(label='Transpilar', command=self.transpile_code, accelerator='F6')
        run_menu.add_command(label='Verificar errores', command=self.check_errors, accelerator='F7')
        
        view_menu = tk.Menu(menubar, tearoff=0, bg='#2D2D2D', fg='#D4D4D4')
        menubar.add_cascade(label='Ver', menu=view_menu)
        view_menu.add_command(label='Consola', command=self.toggle_console)
        view_menu.add_command(label='Documentación', command=self.toggle_docs)
        view_menu.add_command(label='Errores', command=self.toggle_errors)
        
        help_menu = tk.Menu(menubar, tearoff=0, bg='#2D2D2D', fg='#D4D4D4')
        menubar.add_cascade(label='Ayuda', menu=help_menu)
        help_menu.add_command(label='Documentación', command=self.show_docs)
        help_menu.add_command(label='Acerca de', command=self.show_about)
    
    def create_toolbar(self):
        toolbar = tk.Frame(self, bg='#2D2D2D', height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        buttons = [
            ('📄 Nuevo', self.new_file),
            ('📂 Abrir', self.open_file),
            ('💾 Guardar', self.save_file),
            ('▶️ Ejecutar', self.run_code),
            ('🔧 Transpilar', self.transpile_code),
            ('🔍 Verificar', self.check_errors),
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                toolbar,
                text=text,
                command=command,
                bg='#3C3C3C',
                fg='#D4D4D4',
                relief=tk.FLAT,
                padx=10,
                pady=5,
                font=('Segoe UI', 9)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=5)
    
    def create_main_layout(self):
        main_paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg='#1E1E1E', sashwidth=5)
        main_paned.pack(fill=tk.BOTH, expand=True)
        
        editor_frame = tk.Frame(main_paned, bg='#1E1E1E')
        main_paned.add(editor_frame, width=800)
        
        line_numbers_frame = tk.Frame(editor_frame, bg='#1E1E1E', width=50)
        line_numbers_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.line_numbers = tk.Text(
            line_numbers_frame,
            width=4,
            bg='#1E1E1E',
            fg='#858585',
            font=('Consolas', 11),
            state=tk.DISABLED,
            relief=tk.FLAT
        )
        self.line_numbers.pack(fill=tk.Y)
        
        self.text_editor = scrolledtext.ScrolledText(
            editor_frame,
            bg='#1E1E1E',
            fg='#D4D4D4',
            insertbackground='#AEAFAD',
            font=('Consolas', 11),
            wrap=tk.NONE,
            undo=True,
            maxundo=-1
        )
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.text_editor.bind('<KeyRelease>', self.on_key_release)
        self.text_editor.bind('<Button-1>', self.on_click)
        self.text_editor.bind('<Control-space>', self.show_autocomplete)
        
        right_paned = tk.PanedWindow(main_paned, orient=tk.VERTICAL, bg='#1E1E1E', sashwidth=5)
        main_paned.add(right_paned, width=600)
        
        self.console = ConsoleWidget(right_paned)
        right_paned.add(self.console, height=300)
        
        self.docs_panel = DocumentationPanel(right_paned)
        right_paned.add(self.docs_panel, height=300)
        
        self.errors_frame = tk.Frame(right_paned, bg='#1E1E1E')
        right_paned.add(self.errors_frame, height=200)
        
        tk.Label(
            self.errors_frame,
            text='ERRORES Y ADVERTENCIAS',
            bg='#1E1E1E',
            fg='#4EC9B0',
            font=('Consolas', 10, 'bold')
        ).pack(anchor=tk.W, padx=5, pady=5)
        
        self.errors_list = scrolledtext.ScrolledText(
            self.errors_frame,
            bg='#1E1E1E',
            fg='#D4D4D4',
            font=('Consolas', 9),
            height=10,
            state=tk.DISABLED
        )
        self.errors_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.errors_list.tag_config('error', foreground='#F44747')
        self.errors_list.tag_config('warning', foreground='#CCA700')
    
    def create_status_bar(self):
        self.status_bar = tk.Frame(self, bg='#007ACC', height=25)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_bar,
            text='Listo',
            bg='#007ACC',
            fg='#FFFFFF',
            font=('Segoe UI', 9),
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.cursor_label = tk.Label(
            self.status_bar,
            text='Línea: 1, Col: 1',
            bg='#007ACC',
            fg='#FFFFFF',
            font=('Segoe UI', 9)
        )
        self.cursor_label.pack(side=tk.RIGHT, padx=10)
    
    def bind_shortcuts(self):
        self.bind('<Control-n>', lambda e: self.new_file())
        self.bind('<Control-o>', lambda e: self.open_file())
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<Control-Shift-S>', lambda e: self.save_file_as())
        self.bind('<F5>', lambda e: self.run_code())
        self.bind('<F6>', lambda e: self.transpile_code())
        self.bind('<F7>', lambda e: self.check_errors())
        self.bind('<Control-f>', lambda e: self.find())
    
    def update_line_numbers(self):
        line_count = self.text_editor.get('1.0', tk.END).count('\n')
        line_numbers_string = '\n'.join(str(i) for i in range(1, line_count + 1))
        
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete('1.0', tk.END)
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state=tk.DISABLED)
    
    def update_cursor_position(self):
        cursor_pos = self.text_editor.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        self.cursor_label.config(text=f'Línea: {line}, Col: {int(col) + 1}')
    
    def on_key_release(self, event):
        self.update_line_numbers()
        self.update_cursor_position()
        
        if event.char and event.char.isalnum():
            self.check_errors_realtime()
    
    def on_click(self, event):
        self.update_cursor_position()
    
    def check_errors_realtime(self):
        code = self.text_editor.get('1.0', tk.END)
        issues = self.error_detector.check_syntax(code)
        
        self.errors_list.config(state=tk.NORMAL)
        self.errors_list.delete('1.0', tk.END)
        
        if not issues:
            self.errors_list.insert(tk.END, '✓ No se encontraron problemas\n', 'warning')
        else:
            for issue in issues:
                tag = 'error' if issue['type'] == 'error' else 'warning'
                icon = '❌' if issue['type'] == 'error' else '⚠️'
                self.errors_list.insert(tk.END, f"{icon} Línea {issue['line']}: {issue['message']}\n", tag)
        
        self.errors_list.config(state=tk.DISABLED)
    
    def show_autocomplete(self, event):
        cursor_pos = self.text_editor.index(tk.INSERT)
        text = self.text_editor.get('1.0', cursor_pos)
        
        suggestions = self.autocompleter.get_suggestions(text, cursor_pos)
        
        if suggestions:
            self.console.write(f'Sugerencias: {", ".join(suggestions)}', 'info')
    
    def new_file(self):
        if messagebox.askyesno('Nuevo archivo', '¿Crear un nuevo archivo? Los cambios no guardados se perderán.'):
            self.text_editor.delete('1.0', tk.END)
            self.current_file = None
            self.title('OPN Editor v1.0 - Sin título')
            self.status_label.config(text='Nuevo archivo creado')
    
    def open_file(self):
        filepath = filedialog.askopenfilename(
            title='Abrir archivo',
            filetypes=[('Archivos OPN', '*.prisma'), ('Archivos de datos', '*.opn'), ('Todos los archivos', '*.*')]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_editor.delete('1.0', tk.END)
                self.text_editor.insert('1.0', content)
                self.current_file = filepath
                self.title(f'OPN Editor v1.0 - {os.path.basename(filepath)}')
                self.status_label.config(text=f'Archivo abierto: {filepath}')
                self.update_line_numbers()
                self.check_errors_realtime()
            except Exception as e:
                messagebox.showerror('Error', f'No se pudo abrir el archivo:\n{str(e)}')
    
    def save_file(self):
        if self.current_file:
            try:
                content = self.text_editor.get('1.0', tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status_label.config(text=f'Archivo guardado: {self.current_file}')
                self.console.write(f'✓ Archivo guardado: {self.current_file}', 'success')
            except Exception as e:
                messagebox.showerror('Error', f'No se pudo guardar el archivo:\n{str(e)}')
        else:
            self.save_file_as()
    
    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(
            title='Guardar archivo como',
            defaultextension='.prisma',
            filetypes=[('Archivos OPN', '*.prisma'), ('Archivos de datos', '*.opn'), ('Todos los archivos', '*.*')]
        )
        if filepath:
            try:
                content = self.text_editor.get('1.0', tk.END)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.current_file = filepath
                self.title(f'OPN Editor v1.0 - {os.path.basename(filepath)}')
                self.status_label.config(text=f'Archivo guardado: {filepath}')
                self.console.write(f'✓ Archivo guardado: {filepath}', 'success')
            except Exception as e:
                messagebox.showerror('Error', f'No se pudo guardar el archivo:\n{str(e)}')
    
    def run_code(self):
        if not self.current_file:
            messagebox.showwarning('Advertencia', 'Guarda el archivo antes de ejecutarlo')
            return
        
        self.save_file()
        self.console.write(f'Ejecutando {self.current_file}...', 'info')
        self.console.run_file(self.current_file)
    
    def transpile_code(self):
        if not self.current_file:
            messagebox.showwarning('Advertencia', 'Guarda el archivo antes de transpilarlo')
            return
        
        self.save_file()
        self.console.write(f'Transpilando {self.current_file}...', 'info')
        self.console.transpile_file(self.current_file)
    
    def check_errors(self):
        if not self.current_file:
            code = self.text_editor.get('1.0', tk.END)
            issues = self.error_detector.check_syntax(code)
            
            self.errors_list.config(state=tk.NORMAL)
            self.errors_list.delete('1.0', tk.END)
            
            if not issues:
                self.errors_list.insert(tk.END, '✓ No se encontraron problemas\n', 'warning')
                self.console.write('✓ No se encontraron problemas', 'success')
            else:
                for issue in issues:
                    tag = 'error' if issue['type'] == 'error' else 'warning'
                    icon = '❌' if issue['type'] == 'error' else '⚠️'
                    self.errors_list.insert(tk.END, f"{icon} Línea {issue['line']}: {issue['message']}\n", tag)
                self.console.write(f'Se encontraron {len(issues)} problema(s)', 'warning')
            
            self.errors_list.config(state=tk.DISABLED)
        else:
            self.console.check_file(self.current_file)
    
    def undo(self):
        try:
            self.text_editor.edit_undo()
        except:
            pass
    
    def redo(self):
        try:
            self.text_editor.edit_redo()
        except:
            pass
    
    def cut(self):
        self.text_editor.event_generate('<<Cut>>')
    
    def copy(self):
        self.text_editor.event_generate('<<Copy>>')
    
    def paste(self):
        self.text_editor.event_generate('<<Paste>>')
    
    def find(self):
        search_term = tk.simpledialog.askstring('Buscar', 'Ingresa el texto a buscar:')
        if search_term:
            start_pos = '1.0'
            while True:
                start_pos = self.text_editor.search(search_term, start_pos, tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(search_term)}c'
                self.text_editor.tag_add('search', start_pos, end_pos)
                start_pos = end_pos
            
            self.text_editor.tag_config('search', background='#264F78')
    
    def toggle_console(self):
        pass
    
    def toggle_docs(self):
        pass
    
    def toggle_errors(self):
        pass
    
    def show_docs(self):
        self.docs_panel.load_documentation()
        messagebox.showinfo('Documentación', 'Consulta el panel de documentación a la derecha')
    
    def show_about(self):
        messagebox.showinfo(
            'Acerca de OPN Editor',
            'OPN Editor v1.0\n\n'
            'Editor oficial para el lenguaje OPN\n'
            'Desarrollado con Python y Tkinter\n\n'
            '© 2025 OPN Language Project'
        )
    
    def on_closing(self):
        if messagebox.askyesno('Salir', '¿Estás seguro de que quieres salir?'):
            self.destroy()

def main():
    app = OPNEditor()
    app.mainloop()

if __name__ == '__main__':
    main()
