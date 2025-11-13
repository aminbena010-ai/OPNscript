#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Editor estilo VS Code con minimapa lateral, barra de actividad, explorador de archivos y tema oscuro (PyQt6)
# Versión: 1.7 - Autocompletado configurable y ejecución de lenguajes flexible.

import sys, os, re
import json 
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTabWidget,
    QSplitter, QWidget, QVBoxLayout, QMessageBox, QCompleter,
    QPlainTextEdit, QTextEdit, QLineEdit, QPushButton, QDialog,
    QHBoxLayout, QTreeView, QLabel 
)
from PyQt6.QtGui import (
    QAction, QKeySequence, QFont, QColor, QTextCharFormat,
    QSyntaxHighlighter, QPainter, QFileSystemModel, QIcon, QFontMetrics
)
from PyQt6.QtCore import (
    Qt, QRect, QTimer, QSize, pyqtSignal, QDir, QModelIndex, QTime,
    QProcess, QStringListModel # <--- AÑADIDO: QProcess, QStringListModel
)


# ======================================================
#     Configuración de Resaltado (Carga de JSON)
# ======================================================

# --- Variables Globales para la configuración cargada ---
THEME_CONFIG = {
    'palette': {},
    'languages': {'default': {'rules': [], 'completions': [], 'execution_command': None}},
    'extensions': {}, 
    'default_language_id': 'default' 
}

SNIPPETS_CONFIG = {
    'opn': {},
    'python': {},
    'javascript': {},
    'default': {}
}

def _get_json_path(filepath):
    """
    Obtiene la ruta absoluta de un archivo, adaptándose al empaquetado PyInstaller.
    Busca los recursos en el directorio temporal (_MEIPASS) si está congelado.
    """
    
    if getattr(sys, 'frozen', False):
        # En PyInstaller, los recursos están en el directorio temporal (sys._MEIPASS)
        base_path = sys._MEIPASS
    else:
        # Modo desarrollo. Asume que el script está en el root del proyecto.
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta final: [base_path]/recursos/[filepath]
    resource_path = os.path.join(base_path, 'recursos', filepath)
    
    # Fallback para el modo de desarrollo si la estructura de carpetas es diferente
    if not os.path.exists(resource_path) and not getattr(sys, 'frozen', False):
        resource_path = os.path.join(os.getcwd(), 'recursos', filepath)

    return resource_path

def load_theme_config(filepath):
    """Carga la paleta de colores y las reglas de resaltado desde colores.json."""
    global THEME_CONFIG
    json_path = _get_json_path(filepath)
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        THEME_CONFIG['palette'] = data.get('palette', {})
        
        # Cargar las reglas de lenguaje
        language_rules = {}
        for lang, rules in data.get('languages', {}).items():
            language_rules[lang] = {
                'rules': [(r[0], r[1], r[2]) for r in rules.get('rules', [])],
                'completions': rules.get('completions', []),
                'execution_command': rules.get('execution_command', None)
            }
            
        THEME_CONFIG['languages'].update(language_rules)
        print(f"Configuración de tema cargada desde: {json_path}")
        
    except FileNotFoundError:
        print(f"ERROR: Archivo de tema no encontrado en {json_path}. Usando configuración vacía.")
    except Exception as e:
        print(f"ERROR al cargar el tema JSON: {e}")

def load_snippets_config(filepath):
    """Carga los snippets desde snippets.json."""
    global SNIPPETS_CONFIG
    json_path = _get_json_path(filepath)
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        SNIPPETS_CONFIG.update(data)
        print(f"Configuración de snippets cargada desde: {json_path}")
        
    except FileNotFoundError:
        print(f"ERROR: Archivo de snippets no encontrado en {json_path}. Usando snippets vacíos.")
    except Exception as e:
        print(f"ERROR al cargar snippets JSON: {e}")

def load_extension_config(filepath):
    """Carga el mapeo de extensiones desde extensions.json."""
    global THEME_CONFIG
    json_path = _get_json_path(filepath)
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Cargar el mapeo de extensiones
        THEME_CONFIG['extensions'] = data.get('mappings', {})
        # Cargar el ID por defecto
        THEME_CONFIG['default_language_id'] = data.get('default_id', 'default') 
        
        print(f"Configuración de extensiones cargada desde: {json_path}")
        
    except FileNotFoundError:
        print(f"ERROR: Archivo de extensiones no encontrado en {json_path}. Usando configuración vacía.")
        THEME_CONFIG['extensions'] = {}
        THEME_CONFIG['default_language_id'] = 'default'
    except Exception as e:
        print(f"ERROR al cargar el JSON de extensiones: {e}")
        THEME_CONFIG['extensions'] = {}
        THEME_CONFIG['default_language_id'] = 'default'


# Cargar TODAS las configuraciones al inicio
load_theme_config('colores.json')
load_extension_config('extensions.json')
load_snippets_config('snippets.json')


def fmt(color_key, style=""):
    """Crea un QTextCharFormat usando la clave de color de la paleta cargada."""
    # Fallback a un color por defecto si la clave no existe
    color_code = THEME_CONFIG['palette'].get(color_key, "#D4D4D4") 
    
    f = QTextCharFormat()
    f.setForeground(QColor(color_code))
    if "bold" in style:
        f.setFontWeight(QFont.Weight.Bold)
    if "italic" in style:
        f.setFontItalic(True)
    return f

def get_language_id(filepath):
    """Determina la ID del lenguaje basándose en la extensión del archivo, usando el JSON de extensiones."""
    default_id = THEME_CONFIG.get('default_language_id', 'default')
    
    if not filepath or '.' not in filepath:
        return default_id
    
    # Obtener la extensión y limpiarla (ej: '.py' -> 'py')
    ext = os.path.splitext(filepath)[1].lower().lstrip('.')
    
    # Usar el mapeo cargado. Si no se encuentra, retorna el ID por defecto.
    return THEME_CONFIG['extensions'].get(ext, default_id)


# ======================================================
#     Resaltador de Sintaxis Personalizado
# ======================================================
class CustomSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document, rules):
        super().__init__(document)
        self.rules = rules 
        self.string_char = None

    def highlightBlock(self, text):
        """Aplica las reglas de resaltado al bloque de texto actual."""
        in_string = False
        string_char = None
        
        for i, char in enumerate(text):
            if char in ('"', "'") and (i == 0 or text[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
        
        for pattern_str, color_key, style in self.rules:
            format_obj = fmt(color_key, style)
            
            if color_key == "string":
                for match in re.finditer(pattern_str, text):
                    start, end = match.span()
                    self.setFormat(start, end - start, format_obj)
            else:
                for match in re.finditer(pattern_str, text):
                    start, end = match.span()
                    in_string = False
                    for j in range(start):
                        if text[j] in ('"', "'"):
                            if j == 0 or text[j-1] != '\\':
                                in_string = not in_string
                    
                    if not in_string:
                        self.setFormat(start, end - start, format_obj)


# ======================================================
#     Editor de código con numeración de líneas
# ======================================================
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class ErrorUnderlineFormat(QTextCharFormat):
    def __init__(self):
        super().__init__()
        self.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)
        self.setUnderlineColor(QColor("#F44747"))


class CompletionModel(QStringListModel):
    """Modelo de autocompletado con descripciones."""
    def __init__(self, completions_dict, parent=None):
        super().__init__(parent)
        self.completions_dict = completions_dict
        self.setStringList(list(completions_dict.keys()))
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """Retorna los datos con descripción."""
        if role == Qt.ItemDataRole.DisplayRole:
            completion = self.stringList()[index.row()]
            desc = self.completions_dict.get(completion, {}).get('description', '')
            if desc:
                return f"{completion} - {desc}"
            return completion
        elif role == Qt.ItemDataRole.UserRole:
            return self.stringList()[index.row()]
        return super().data(index, role)


class CodeEditor(QPlainTextEdit):
    textChangedSignal = pyqtSignal()

    def __init__(self, filepath=None):
        super().__init__()
        font_options = ["Fira Code", "Monaco", "Consolas", "DejaVu Sans Mono"]
        selected_font = None
        for font_name in font_options:
            test_font = QFont(font_name, 11)
            fm = QFontMetrics(test_font)
            if fm.horizontalAdvance('A') > 0:
                selected_font = test_font
                break
        if not selected_font:
            selected_font = QFont("Consolas", 11)
        self.setFont(selected_font)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: none;
                padding: 4px;
            }
        """)
        
        self.highlighter = None
        self.set_language_highlighter(filepath)
        
        self.completer = None
        self.set_language_completer(filepath)
        
        self.error_underline_format = ErrorUnderlineFormat()
        self.error_positions = []
        self.current_language = get_language_id(filepath)

        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.textChanged.connect(self.textChangedSignal.emit)
        self.textChanged.connect(self.detect_errors)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def detect_errors(self):
        """Detecta errores de sintaxis básicos y los marca con subrayado ondulado."""
        text = self.toPlainText()
        cursor = self.textCursor()
        extra_selections = []
        
        if self.current_language == 'opn':
            self._detect_opn_errors(text, extra_selections)
        
        cursor.clearSelection()
        self.setExtraSelections(extra_selections)
    
    def _detect_opn_errors(self, text, extra_selections):
        """Detecta errores específicos de OPN."""
        lines = text.split('\n')
        open_braces = 0
        open_brackets = 0
        open_parens = 0
        in_string = False
        string_char = None
        
        for line_num, line in enumerate(lines):
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                continue
            
            for i, char in enumerate(line):
                if char in ('"', "'") and (i == 0 or line[i-1] != '\\'):
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                        string_char = None
            
            if in_string:
                continue
            
            open_braces += line.count('{') - line.count('}')
            open_brackets += line.count('[') - line.count(']')
            open_parens += line.count('(') - line.count(')')
            
            if any(line.strip().startswith(kw) for kw in ['let', 'set', 'return']):
                if ';' not in line and not line.strip().endswith('{'):
                    self._mark_line_error(line_num, extra_selections)
            
            if line.count('{') != line.count('}'):
                pass
        
        if open_braces != 0 or open_brackets != 0 or open_parens != 0:
            self._mark_unmatched_brackets(extra_selections, lines)
    
    def _mark_line_error(self, line_num, extra_selections):
        """Marca una línea completa con error."""
        sel = QTextEdit.ExtraSelection()
        sel.format = self.error_underline_format
        cursor = self.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        for _ in range(line_num):
            cursor.movePosition(cursor.MoveOperation.Down)
        cursor.movePosition(cursor.MoveOperation.EndOfLine, cursor.MoveMode.KeepAnchor)
        sel.cursor = cursor
        extra_selections.append(sel)
    
    def _mark_unmatched_brackets(self, extra_selections, lines):
        """Marca los brackets sin cerrar."""
        for line_num, line in enumerate(lines):
            for match in re.finditer(r'[{(\[]', line):
                closing_bracket = {'{': '}', '(': ')', '[': ']'}[match.group()]
                if closing_bracket not in ''.join(lines[line_num:]):
                    sel = QTextEdit.ExtraSelection()
                    sel.format = self.error_underline_format
                    cursor = self.textCursor()
                    cursor.movePosition(cursor.MoveOperation.Start)
                    for _ in range(line_num):
                        cursor.movePosition(cursor.MoveOperation.Down)
                    cursor.movePosition(cursor.MoveOperation.StartOfLine)
                    cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.MoveAnchor, match.start())
                    cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor)
                    sel.cursor = cursor
                    extra_selections.append(sel)
                    break
    
    def set_language_highlighter(self, filepath):
        """Identifica el lenguaje y aplica el resaltador correcto, usando la configuración global."""
        lang_id = get_language_id(filepath)
        self.current_language = lang_id
        lang_config = THEME_CONFIG['languages'].get(lang_id, THEME_CONFIG['languages']['default'])
        rules = lang_config.get('rules', [])
        
        if self.highlighter:
            self.highlighter.setDocument(None)
            
        self.highlighter = CustomSyntaxHighlighter(self.document(), rules)

    def set_language_completer(self, filepath):
        """Configura el autocompletado para el lenguaje del archivo."""
        lang_id = get_language_id(filepath)
        lang_config = THEME_CONFIG['languages'].get(lang_id, THEME_CONFIG['languages']['default'])
        completion_words = lang_config.get('completions', [])
        lang_snippets = SNIPPETS_CONFIG.get(lang_id, {})

        if not completion_words:
            if self.completer:
                self.completer.setWidget(None)
            self.completer = None
            return

        if not self.completer:
            self.completer = QCompleter(self)
        
        completions_dict = {}
        for word in completion_words:
            if word in lang_snippets:
                completions_dict[word] = lang_snippets[word]
            else:
                completions_dict[word] = {'description': ''}
        
        model = CompletionModel(completions_dict, self.completer)
        self.completer.setModel(model)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)

    def insert_completion(self, completion):
        """Inserta la palabra completada en el editor."""
        completion_text = completion.split(' - ')[0] if ' - ' in completion else completion
        
        tc = self.textCursor()
        extra = len(completion_text) - len(self.completer.completionPrefix())
        tc.movePosition(tc.MoveOperation.Left)
        tc.movePosition(tc.MoveOperation.EndOfWord)
        tc.insertText(completion_text[-extra:])
        self.setTextCursor(tc)
        
        lang_snippets = SNIPPETS_CONFIG.get(self.current_language, {})
        if completion_text in lang_snippets:
            self._expand_snippet(completion_text)

    def text_under_cursor(self):
        """Obtiene la palabra que está bajo el cursor."""
        tc = self.textCursor()
        tc.select(tc.SelectionType.WordUnderCursor)
        return tc.selectedText()

    def _get_indent_level(self, line_text):
        """Calcula el nivel de indentación de una línea."""
        return len(line_text) - len(line_text.lstrip())
    
    def _insert_auto_closing(self, opening, closing):
        """Inserta el símbolo de cierre automáticamente."""
        cursor = self.textCursor()
        cursor.insertText(opening + closing)
        cursor.movePosition(cursor.MoveOperation.Left)
        self.setTextCursor(cursor)
    
    def _create_key_event(self, key):
        """Crea un evento de teclado sintético."""
        from PyQt6.QtGui import QKeyEvent
        return QKeyEvent(QKeyEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier)
    
    def _expand_snippet(self, snippet_key):
        """Expande un snippet en la posición actual."""
        lang_id = self.current_language
        lang_snippets = SNIPPETS_CONFIG.get(lang_id, {})
        snippet = lang_snippets.get(snippet_key)
        
        if not snippet:
            return False
        
        body = snippet.get('body', '')
        if not body:
            return False
        
        cursor = self.textCursor()
        
        block_text = cursor.block().text()
        start_pos = cursor.positionInBlock()
        before_cursor = block_text[:start_pos]
        
        if not before_cursor.endswith(snippet_key):
            return False
        
        # Eliminar la palabra clave que activó el snippet
        cursor.beginEditBlock()
        for _ in range(len(snippet_key)):
            cursor.deletePreviousChar()
        
        # Obtener la indentación de la línea actual
        current_line_text = cursor.block().text()
        base_indent = self._get_indent_level(current_line_text)
        
        # Variables para posicionar el cursor al final
        final_cursor_pos = -1
        
        # Insertar el cuerpo del snippet línea por línea
        lines = body.split('\n')
        for i, line in enumerate(lines):
            # Para la primera línea, no insertamos salto de línea ni indentación base
            if i > 0:
                cursor.insertText('\n')
                # Aplicar indentación base a las líneas nuevas
                if line.strip(): # No indentar líneas vacías
                    cursor.insertText(' ' * base_indent)
            
            # Buscar marcadores de posición ($0, $1, etc.)
            placeholder_match = re.search(r'\$(\d+)', line)
            if placeholder_match and final_cursor_pos == -1:
                # Guardar la posición del primer marcador para el cursor
                final_cursor_pos = cursor.position() + placeholder_match.start()
            
            # Insertar la línea sin los marcadores
            processed_line = re.sub(r'\$\d+', '', line)
            cursor.insertText(processed_line)
        
        # Mover el cursor a la posición del primer marcador encontrado
        if final_cursor_pos != -1:
            cursor.setPosition(final_cursor_pos)
        
        cursor.endEditBlock()
        self.setTextCursor(cursor)
        return True
    
    def _is_word_boundary(self, char):
        """Verifica si un carácter es límite de palabra."""
        return char in ' \t\n(){}[].,;:"\''
    
    def keyPressEvent(self, event):
        """Maneja eventos de teclado con auto-indentation, auto-closing y autocompletado."""
        cursor = self.textCursor()
        
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Tab, Qt.Key.Key_Backtab):
                event.ignore()
                return
        
        key = event.key()
        text = event.text()
        
        if text == ' ':
            cursor_before = self.textCursor()
            cursor_before.movePosition(cursor_before.MoveOperation.StartOfLine)
            line_text = cursor_before.block().text()
            stripped = line_text.strip()
            
            for snippet_key in SNIPPETS_CONFIG.get(self.current_language, {}).keys():
                if stripped == snippet_key:
                    if self._expand_snippet(snippet_key):
                        event.accept()
                        return
        
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            # Lógica mejorada para auto-indentación y creación de bloques
            
            # 1. Comprobar si estamos entre brackets/llaves/paréntesis
            cursor_before = self.textCursor()
            cursor_before.movePosition(cursor_before.MoveOperation.PreviousCharacter, cursor_before.MoveMode.KeepAnchor)
            char_before = cursor_before.selectedText()
            
            cursor_after = self.textCursor()
            cursor_after.movePosition(cursor_after.MoveOperation.NextCharacter, cursor_after.MoveMode.KeepAnchor)
            char_after = cursor_after.selectedText()

            closing_map = {'{': '}', '[': ']', '(': ')'}

            # 2. Si estamos en medio de un par como {}, [], (), crear un bloque
            if char_before in closing_map and closing_map[char_before] == char_after:
                current_line_text = cursor.block().text()
                indent_level = self._get_indent_level(current_line_text)
                
                # Insertar nueva línea con indentación extra
                super().keyPressEvent(event)
                self.textCursor().insertText(' ' * (indent_level + 4))
                
                # Insertar la línea de cierre
                super().keyPressEvent(event)
                self.textCursor().insertText(' ' * indent_level)
                
                # Mover el cursor de vuelta al medio del bloque
                cursor = self.textCursor()
                cursor.movePosition(cursor.MoveOperation.Up)
                cursor.movePosition(cursor.MoveOperation.EndOfLine)
                self.setTextCursor(cursor)
                return

            # 3. Lógica de auto-indentación normal
            cursor.movePosition(cursor.MoveOperation.StartOfLine)
            line_text = cursor.block().text()
            indent_level = self._get_indent_level(line_text)
            extra_indent = 0
            if line_text.strip().endswith(('{', '[', '(', ':')):
                extra_indent = 4

            super().keyPressEvent(event)
            self.textCursor().insertText(' ' * (indent_level + extra_indent))
        
        elif text in ('{', '[', '('):
            closing_map = {'{': '}', '[': ']', '(': ')'}
            next_char = ''
            cursor_next = self.textCursor()
            cursor_next.movePosition(cursor_next.MoveOperation.Right)
            if not cursor_next.atBlockEnd():
                cursor_next.movePosition(cursor_next.MoveOperation.Left, cursor_next.MoveMode.KeepAnchor)
                next_char = cursor_next.selectedText()
            
            if next_char != closing_map[text]:
                self._insert_auto_closing(text, closing_map[text])
            else:
                super().keyPressEvent(event)
            self.detect_errors()
        
        elif text in ('"', "'"):
            cursor.movePosition(cursor.MoveOperation.PreviousCharacter, cursor.MoveMode.KeepAnchor)
            prev_char = cursor.selectedText()
            cursor.movePosition(cursor.MoveOperation.NextCharacter)
            self.setTextCursor(cursor)
            
            if prev_char != '\\':
                self._insert_auto_closing(text, text)
            else:
                super().keyPressEvent(event)
        
        elif text == ':' and self.current_language == 'opn':
            super().keyPressEvent(event)
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.StartOfLine)
            line_text = cursor.block().text()
            if line_text.strip().startswith(('if ', 'else', 'for ')):
                cursor.movePosition(cursor.MoveOperation.EndOfLine)
                self.setTextCursor(cursor)
                cursor.insertText(' {')
                self.setTextCursor(cursor)
        
        elif text in ('}', ']', ')'):
            closing_map = {'}': '{', ']': '[', ')': '('}
            cursor_next = self.textCursor()
            cursor_next.movePosition(cursor_next.MoveOperation.Right, cursor_next.MoveMode.KeepAnchor)
            if cursor_next.selectedText() == text:
                self.textCursor().movePosition(self.textCursor().MoveOperation.Right)
            else:
                super().keyPressEvent(event)
            self.detect_errors()
        
        elif text == ';':
            super().keyPressEvent(event)
            self.detect_errors()
        
        else:
            super().keyPressEvent(event)
        
        prefix = self.text_under_cursor()
        if self.completer and prefix and len(prefix) > 0:
            self.completer.setCompletionPrefix(prefix)
            self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))
            cr = self.cursorRect()
            cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
        
    def line_number_area_width(self):
        # Calcular ancho basado en el número de dígitos en el total de líneas
        digits = len(str(self.blockCount()))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        # Establecer el margen izquierdo para el área de números de línea
        self.setViewportMargins(self.line_number_area_width() if self.line_number_area.isVisible() else 0, 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        # Posicionar el widget de números de línea correctamente
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#252526")) # Color de fondo

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#858585")) # Color del texto
                painter.drawText(0, top, self.line_number_area.width() - 5, self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra = []
        if not self.isReadOnly():
            sel = QTextEdit.ExtraSelection()
            # Resaltado de línea actual estilo VS Code
            sel.format.setBackground(QColor("#2a2d2e"))
            sel.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            sel.cursor = self.textCursor()
            sel.cursor.clearSelection()
            extra.append(sel)
        self.setExtraSelections(extra)


# ======================================================
#     Minimapa lateral sincronizado
# ======================================================
class MiniMap(QPlainTextEdit):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setReadOnly(True)
        # Deshabilitar barras de desplazamiento
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFont(QFont("Consolas", 3)) # Fuente muy pequeña
        self.setStyleSheet("background-color: #202020; color: #555555; border: none;")

        # Conectar el desplazamiento y cambios de contenido del editor
        self.editor.verticalScrollBar().valueChanged.connect(self.sync_scroll)
        self.editor.textChangedSignal.connect(self.update_content)
        self.update_content()

    def sync_scroll(self):
        # Calcular la proporción de desplazamiento del editor principal y aplicarla al minimapa
        editor_scroll_bar = self.editor.verticalScrollBar()
        minimap_scroll_bar = self.verticalScrollBar() 

        editor_max = editor_scroll_bar.maximum()
        if editor_max > 0:
            ratio = editor_scroll_bar.value() / editor_max
        else:
            ratio = 0 # Manejar editor vacío

        new_value = int(ratio * minimap_scroll_bar.maximum())
        minimap_scroll_bar.setValue(new_value)

    def update_content(self):
        # Actualizar el contenido del texto desde el editor principal
        self.setPlainText(self.editor.toPlainText())
        self.sync_scroll()

    def mousePressEvent(self, event):
        # Permitir hacer clic en el minimapa para saltar a esa ubicación en el editor principal
        ratio = event.position().y() / max(1, self.height())
        editor_max = self.editor.verticalScrollBar().maximum()
        new_value = int(ratio * max(1, editor_max))
        self.editor.verticalScrollBar().setValue(new_value)


# ======================================================
#     Diálogo de búsqueda / reemplazo
# ======================================================
class FindReplaceDialog(QDialog):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setWindowTitle("Buscar y reemplazar")
        self.setStyleSheet("background-color: #1E1E1E; color: #CCCCCC;")
        self.setFixedWidth(350)

        layout = QVBoxLayout()
        
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Buscar...")
        self.find_input.setStyleSheet("background-color: #3C3C3C; color: #CCCCCC; border: 1px solid #007ACC; padding: 5px;")
        
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Reemplazar por...")
        self.replace_input.setStyleSheet("background-color: #3C3C3C; color: #CCCCCC; border: 1px solid #3C3C3C; padding: 5px;")


        self.btn_find = QPushButton("Buscar siguiente")
        self.btn_replace = QPushButton("Reemplazar")
        self.btn_replace_all = QPushButton("Reemplazar todo")

        # Estilo de botón azul de VS Code
        button_style = "background-color: #007ACC; color: white; border: none; padding: 6px 12px; margin-top: 5px; border-radius: 3px;"
        for btn in [self.btn_find, self.btn_replace, self.btn_replace_all]:
            btn.setStyleSheet(button_style)

        self.btn_find.clicked.connect(self.find_next)
        self.btn_replace.clicked.connect(self.replace)
        self.btn_replace_all.clicked.connect(self.replace_all)

        layout.addWidget(self.find_input)
        layout.addWidget(self.replace_input)
        layout.addWidget(self.btn_find)
        layout.addWidget(self.btn_replace)
        layout.addWidget(self.btn_replace_all)
        self.setLayout(layout)

    def find_next(self):
        text = self.find_input.text()
        # Buscar la siguiente ocurrencia, volviendo al inicio si se llega al final
        if not self.editor.find(text):
            self.editor.moveCursor(self.editor.textCursor().MoveOperation.Start)
            self.editor.find(text)

    def replace(self):
        cursor = self.editor.textCursor()
        # Reemplazar solo si el texto está seleccionado
        if cursor.hasSelection():
            cursor.insertText(self.replace_input.text())
        self.find_next() # Mover a la siguiente ocurrencia

    def replace_all(self):
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        
        # Evitar reemplazo innecesario si los textos son iguales o el texto de búsqueda está vacío
        if find_text == replace_text or not find_text:
            return

        # Reemplazar todas las ocurrencias en el documento completo
        content = self.editor.toPlainText().replace(find_text, replace_text)
        self.editor.setPlainText(content)


# ======================================================
#     Explorador de Archivos (Tree View)
# ======================================================
class FileExplorer(QWidget):
    # Señal para notificar a la ventana principal de que se abra un archivo
    openFileRequested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Etiqueta para mostrar el nombre del proyecto o "EXPLORER" por defecto
        self.project_label = QLabel("EXPLORER")
        self.project_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.project_label.setStyleSheet("color: #CCCCCC; padding: 10px 5px 5px 10px; background-color: #252526; border-bottom: 1px solid #333333;")
        self.layout.addWidget(self.project_label)
        
        self.model = QFileSystemModel()
        # Filtrar para no mostrar archivos ocultos ni directorios como . y ..
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        
        # Ocultar columnas innecesarias (Tamaño, Tipo, Fecha)
        for i in range(1, 4):
            self.tree.hideColumn(i)
        
        # Configurar estilo oscuro de VS Code para el explorador
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet("""
            QTreeView {
                background-color: #252526;
                color: #CCCCCC;
                border: none;
                padding: 5px;
            }
            QTreeView::item:selected {
                background-color: #094771; /* Color de selección azul de VS Code */
            }
            QTreeView::branch:open:has-children:!has-siblings:adjoins-item,
            QTreeView::branch:open:has-children:siblings {
                /* Asegura que los íconos de expansión/contracción sean visibles */
                padding: 1px;
            }
        """)

        self.layout.addWidget(self.tree)
        
        # Conexión de doble clic para abrir archivo
        self.tree.doubleClicked.connect(self._on_double_click)
        
        self.root_path = None

    def set_root_path(self, path):
        """Establece la carpeta raíz del explorador, actualiza la vista y la etiqueta del proyecto."""
        self.root_path = path
        
        # Actualizar la etiqueta del proyecto con el nombre de la carpeta
        project_name = os.path.basename(path)
        self.project_label.setText(f"PROJECT: {project_name.upper()}")
        
        self.model.setRootPath(path)
        root_index = self.model.index(path)
        self.tree.setRootIndex(root_index)
        self.tree.setColumnWidth(0, 200) # Ajustar ancho de la columna
        
    def _on_double_click(self, index: QModelIndex):
        """Maneja el doble clic para abrir archivos."""
        if not self.model.isDir(index):
            file_path = self.model.filePath(index)
            self.openFileRequested.emit(file_path)


# ======================================================
#     Barra de Actividad (Activity Bar - Extrema Izquierda)
# ======================================================
class ActivityBar(QWidget):
    # Señal emitida con el nombre de la vista a activar o desactivar (ej: 'explorer', '')
    view_requested = pyqtSignal(str) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(48) # Ancho típico de VS Code para la barra de actividad
        self.setStyleSheet("background-color: #333333;")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 0) # Pequeño margen superior
        self.layout.setSpacing(15)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Estilo común para los botones (usando texto o un símbolo simple)
        button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #858585; /* Color por defecto */
                font-size: 20px;
                padding: 5px;
            }
            QPushButton:hover {
                color: #CCCCCC; /* Hover */
            }
            QPushButton:checked {
                color: white; /* Estado activo */
                border-left: 2px solid white; /* Indicador lateral blanco */
                padding-left: 3px;
            }
        """
        
        # 1. Archivos (Explorer)
        self.btn_files = QPushButton("🗂") # Icono de carpeta/archivos (Unicode)
        self.btn_files.setCheckable(True)
        self.btn_files.setToolTip("Explorer (Ctrl+Shift+E)")
        self.btn_files.setStyleSheet(button_style)
        self.btn_files.clicked.connect(lambda: self._handle_click('explorer'))

        # 2. Buscar (Search)
        self.btn_search = QPushButton("🔎") 
        self.btn_search.setCheckable(True)
        self.btn_search.setToolTip("Search (Ctrl+Shift+F)")
        self.btn_search.setStyleSheet(button_style)
        self.btn_search.clicked.connect(lambda: self._handle_click('search'))

        # 3. Git (Source Control)
        self.btn_git = QPushButton("🔄") 
        self.btn_git.setCheckable(True)
        self.btn_git.setToolTip("Source Control (Ctrl+Shift+G)")
        self.btn_git.setStyleSheet(button_style)
        self.btn_git.clicked.connect(lambda: self._handle_click('git'))

        # 4. Debugging (Run and Debug)
        self.btn_debug = QPushButton("▶️") 
        self.btn_debug.setCheckable(True)
        self.btn_debug.setToolTip("Run and Debug (Ctrl+Shift+D)")
        self.btn_debug.setStyleSheet(button_style)
        self.btn_debug.clicked.connect(lambda: self._handle_click('debug'))
        
        # 5. Extensiones (Plugins)
        self.btn_plugins = QPushButton("🧩") 
        self.btn_plugins.setCheckable(True)
        self.btn_plugins.setToolTip("Extensions (Ctrl+Shift+X)")
        self.btn_plugins.setStyleSheet(button_style)
        self.btn_plugins.clicked.connect(lambda: self._handle_click('plugins'))
        
        self.buttons = [self.btn_files, self.btn_search, self.btn_git, self.btn_debug, self.btn_plugins]

        for btn in self.buttons:
            self.layout.addWidget(btn)
            
        # Un espaciador al final para empujar los botones hacia arriba
        self.layout.addStretch(1)

    def _handle_click(self, view_name):
        """Maneja el clic, desactiva otros botones y emite la señal."""
        sender_btn = self.sender()
        
        # Si el botón que se hizo clic está ahora desmarcado, es un toggle off.
        if not sender_btn.isChecked():
            self.view_requested.emit('') # Emitir cadena vacía para ocultar el panel
            return

        # Desactivar todos los demás botones (excepto el que acaba de ser marcado)
        for btn in self.buttons:
            if btn is not sender_btn:
                btn.setChecked(False)
        
        # Emitir la vista solicitada (solo ocurre si el botón se marcó)
        self.view_requested.emit(view_name)


# ======================================================
#     Panel de Consola / Salida (NUEVO)
# ======================================================
class ConsolePanel(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True) 
        self.setFont(QFont("Consolas", 10))
        # Estilo oscuro de VS Code para el panel inferior
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1E1E1E; /* Mismo que el editor */
                color: #CCCCCC;
                border: none;
                padding: 5px;
            }
        """)
        self.appendPlainText("Consola de salida iniciada. (Ctrl+` para mostrar/ocultar)")
        self.setMaximumHeight(200) # Limitar la altura máxima inicial

    def output(self, text):
        """Método simple para añadir texto a la consola y hacer scroll."""
        if text:
             # Usamos appendPlainText para agregar texto y automáticamente añadir un salto de línea
             self.appendPlainText(text)
             self.ensureCursorVisible()
             
    def setPlainText(self, text):
        """Establece el texto de la consola, limpiando el contenido anterior."""
        super().setPlainText(text)
        self.ensureCursorVisible() # Asegura que el texto inicial sea visible


# ======================================================
#     Ventana principal
# ======================================================
class VSCodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Code Edit")
        
        # --- Configuración del icono de la aplicación (NUEVO) ---
        # El archivo 'Code.ico' debe estar en la carpeta raíz para el modo dev y
        # debe ser incluido en PyInstaller con --add-data "Code.ico;."
        self.setWindowIcon(QIcon("Code.ico")) 
        
        self.resize(1200, 700)
        self.setMinimumSize(800, 600) # Pequeña mejora: Establecer tamaño mínimo

        # 1. Barra de Actividad (Izquierda Extrema)
        self.activity_bar = ActivityBar()
        self.activity_bar.view_requested.connect(self.toggle_side_panel)

        # 2. Explorador de Archivos (Panel Lateral)
        self.file_explorer = FileExplorer()
        self.file_explorer.openFileRequested.connect(self.open_file_from_explorer)

        # 3. Área de Pestañas (Editor/Minimapa)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self._sync_view_actions_to_current_tab)
        
        # 4. Panel de Consola (NUEVO)
        self.console_panel = ConsolePanel()
        self.process = None # <--- Referencia a la instancia de QProcess
        
        # 5. Contenedor de Editor/Consola (División Vertical) (NUEVO SPLITTER)
        # Esto agrupa las Pestañas del Editor (tabs) con la Consola (console_panel)
        self.editor_console_splitter = QSplitter(Qt.Orientation.Vertical)
        self.editor_console_splitter.addWidget(self.tabs)
        self.editor_console_splitter.addWidget(self.console_panel)
        self.editor_console_splitter.setSizes([500, 200]) # Altura inicial: 500 para editor, 200 para consola
        
        # Ocultar la consola por defecto
        self.console_panel.hide() 

        # 6. Splitter Principal (Panel Lateral | Editor/Consola) (División Horizontal)
        self.side_panel_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Añadir el explorador y el nuevo splitter vertical al splitter horizontal.
        self.side_panel_splitter.addWidget(self.file_explorer)
        self.side_panel_splitter.addWidget(self.editor_console_splitter) # Usar el splitter vertical
        self.side_panel_splitter.setSizes([250, 950])
        
        # Ocultar el explorador al inicio 
        self.file_explorer.hide()

        # 7. Contenedor Principal (ActivityBar | Splitter Horizontal)
        main_content_widget = QWidget()
        main_layout = QHBoxLayout(main_content_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        main_layout.addWidget(self.activity_bar)
        main_layout.addWidget(self.side_panel_splitter)
        
        self.setCentralWidget(main_content_widget)

        # Almacena {tab_index: file_path}
        self.open_files = {} 
        
        # Crear Acciones y Menú
        self._create_actions()
        self._create_menu_bar() 
        
        # Auto-Guardado Simple
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.auto_save_all)
        self.autosave_timer.start(60000)

        # Estilo de Ventana Principal y Pestañas
        self.setStyleSheet("""
            QMainWindow { background-color: #252526; } /* Fondo principal */
            QTabWidget::pane { border: none; background: #1E1E1E; } /* Fondo del área del editor */
            
            QMenuBar {
                background: #333333;
                color: #CCCCCC;
                padding: 2px;
            }
            QMenuBar::item:selected {
                background: #007ACC;
            }
            QMenu {
                background: #252526;
                color: #CCCCCC;
                border: 1px solid #007ACC;
            }
            QMenu::item:selected {
                background: #007ACC;
                color: white;
            }
            
            QTabBar::tab { 
                background: #2D2D2D; 
                color: #CCCCCC; 
                padding: 6px 12px; 
                border-top: 2px solid transparent;
            }
            QTabBar::tab:selected { 
                background: #1E1E1E; 
                border-top: 2px solid #007ACC; /* Borde de pestaña activa de VS Code */
                color: white; 
            }
        """)
        
        # Asegurar que al menos una pestaña esté abierta al inicio
        self.new_file() 
        
    # ---- Acciones
    def _create_actions(self):
        # --- Archivo ---
        self.new_action = QAction("Nuevo Archivo", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction("Abrir Archivo...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.triggered.connect(self.open_file)
        
        # ACCIÓN: Abrir Carpeta para el explorador
        self.open_folder_action = QAction("Abrir Carpeta (Directorio Principal)...", self)
        self.open_folder_action.triggered.connect(self.open_folder)

        self.save_action = QAction("Guardar", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.triggered.connect(self.save_file)
        
        self.save_as_action = QAction("Guardar Como...", self)
        self.save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.save_as_action.triggered.connect(self.save_file_as)

        self.exit_action = QAction("Salir", self)
        self.exit_action.triggered.connect(self.close)

        # --- Edición ---
        self.undo_action = QAction("Deshacer", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(lambda: self._current_editor().undo() if self._current_editor() else None) 

        self.redo_action = QAction("Rehacer", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(lambda: self._current_editor().redo() if self._current_editor() else None)

        self.find_action = QAction("Buscar / Reemplazar", self)
        self.find_action.setShortcut(QKeySequence("Ctrl+F"))
        self.find_action.triggered.connect(self.open_find_dialog)
        
        # --- Vista ---
        self.toggle_minimap_action = QAction("Mostrar Minimapa", self, checkable=True, checked=True)
        self.toggle_minimap_action.setShortcut(QKeySequence("Ctrl+Shift+M"))
        self.toggle_minimap_action.triggered.connect(self.toggle_minimap)
        
        self.toggle_linenum_action = QAction("Mostrar Numeración de Líneas", self, checkable=True, checked=True)
        self.toggle_linenum_action.setShortcut(QKeySequence("Ctrl+L"))
        self.toggle_linenum_action.triggered.connect(self.toggle_line_numbers)
        
        # ACCIÓN NUEVA: Consola
        self.toggle_console_action = QAction("Mostrar Consola/Output", self, checkable=True, checked=False)
        self.toggle_console_action.setShortcut(QKeySequence("Ctrl+`")) 
        self.toggle_console_action.triggered.connect(self.toggle_console)
        
        self.run_action = QAction("Ejecutar Archivo", self)
        self.run_action.setShortcut(QKeySequence("F5")) 
        self.run_action.triggered.connect(self.execute_current_file) 
        
    # ---- Menú
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # Menu Archivo
        file_menu = menu_bar.addMenu("Archivo")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.open_folder_action) # Añadir Abrir Carpeta
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Menu Edición
        edit_menu = menu_bar.addMenu("Edición")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_action)
        
        # Menu Vista (ACTUALIZADO)
        view_menu = menu_bar.addMenu("Vista")
        view_menu.addAction(self.toggle_linenum_action)
        view_menu.addAction(self.toggle_minimap_action)
        view_menu.addSeparator() 
        view_menu.addAction(self.toggle_console_action) # Nueva acción
        
        # Menu Ejecución (NUEVO)
        execution_menu = menu_bar.addMenu("Ejecutar")
        execution_menu.addAction(self.run_action) 

    # Helper para obtener el widget de editor actual
    def _current_editor(self):
        widget = self.tabs.currentWidget()
        if not widget:
            return None
        # El editor es el primer widget en el QHBoxLayout de la pestaña
        return widget.layout().itemAt(0).widget() 
    
    # Helper para obtener el widget de minimapa actual
    def _current_minimap(self):
        widget = self.tabs.currentWidget()
        if not widget:
            return None
        # El minimapa es el segundo widget en el QHBoxLayout de la pestaña
        return widget.layout().itemAt(1).widget() 

    # Helper para obtener la ruta del archivo actual
    def _current_filepath(self):
        idx = self.tabs.currentIndex()
        if idx == -1:
            return None
        return self.open_files.get(idx)

    # --------------------------------------------------------------------------
    #                       Lógica de Ejecución (QProcess)
    # --------------------------------------------------------------------------

    def _parse_execution_command(self, command_str, file_path):
        """Analiza el comando de ejecución y devuelve (program, arguments)."""
        if "{python_executable}" in command_str:
            command_str = command_str.replace("{python_executable}", sys.executable)
        
        command_str = command_str.replace("{file}", file_path)
        
        parts = command_str.split()
        program = parts[0]
        arguments = parts[1:] if len(parts) > 1 else []
        
        return program, arguments

    def execute_current_file(self):
        """Prepara y ejecuta el archivo actual en su lenguaje específico."""
        file_path = self._current_filepath()
        if not file_path:
            self.console_panel.output("\n[ERROR] No hay archivo abierto para ejecutar.")
            self.toggle_console(True)
            return
        
        lang_id = get_language_id(file_path)
        lang_config = THEME_CONFIG['languages'].get(lang_id, {})
        execution_command = lang_config.get('execution_command')

        if not execution_command:
            self.console_panel.output(f"\n[ERROR] No hay un comando de ejecución configurado para '{lang_id}'.")
            self.toggle_console(True)
            return

        command_str = execution_command.replace("{python_executable}", sys.executable).replace("{file}", file_path)
        
        program, arguments = self._parse_execution_command(execution_command, file_path)

        # 2. Guardar el archivo si está modificado
        current_index = self.tabs.currentIndex()
        if self.tabs.tabText(current_index).endswith('*'):
            self.save_file()
            if self.tabs.tabText(current_index).endswith('*'):
                 self.console_panel.output("\n[ADVERTENCIA] Guarda los cambios antes de ejecutar o el guardado fue cancelado.")
                 self.toggle_console(True)
                 return

        # 3. Preparar Consola
        self.console_panel.setPlainText(f"--- Ejecutando: {command_str} ---\n")
        self.toggle_console(True) # Asegurar que la consola esté visible

        # 4. Iniciar QProcess
        if self.process and self.process.state() != QProcess.ProcessState.NotRunning:
            self.process.kill() 
            self.process.waitForFinished() # Esperar a que el proceso anterior se detenga

        self.process = QProcess(self)
        
        # Conectar señales para manejo de salida asíncrona
        self.process.readyReadStandardOutput.connect(self._process_stdout)
        self.process.readyReadStandardError.connect(self._process_stderr)
        self.process.finished.connect(self._process_finished)
        self.process.errorOccurred.connect(self._process_error)

        try:
            # Establecer el directorio de trabajo a la raíz del proyecto OPN4
            project_root = os.path.join(os.path.dirname(file_path), '..', '..', 'prisma-lang', 'src')
            if os.path.exists(project_root):
                self.process.setWorkingDirectory(os.path.abspath(project_root))
            else:
                script_dir = os.path.dirname(file_path)
                self.process.setWorkingDirectory(script_dir)
            
            self.process.start(program, arguments)
        except Exception as e:
            self.console_panel.output(f"\n[ERROR DE INICIO] No se pudo iniciar el proceso: {e}")
            self.process = None


    def _process_stdout(self):
        """Lee la salida estándar (stdout) y la redirige a la consola."""
        if self.process:
            # Lee todos los datos disponibles y los decodifica como texto
            data = self.process.readAllStandardOutput().data().decode("utf-8", errors="ignore")
            self.console_panel.output(data.rstrip()) 
            
    def _process_stderr(self):
        """Lee la salida de error estándar (stderr) y la redirige a la consola."""
        if self.process:
            data = self.process.readAllStandardError().data().decode("utf-8", errors="ignore")
            # Usa un formato distintivo para errores
            self.console_panel.output(f"\n[ERROR DE EJECUCIÓN]\n{data.rstrip()}")
    
    def _process_finished(self, exitCode, exitStatus):
        """Maneja la finalización del proceso."""
        if exitStatus == QProcess.ExitStatus.NormalExit:
            status_text = "FINALIZADO NORMALMENTE"
        else:
            status_text = "FINALIZADO CON ERROR DE SALIDA"
            
        self.console_panel.output(f"\n--- Proceso {status_text} (Código: {exitCode}) ---")
        self.process = None # Libera la referencia
        
    def _process_error(self, error):
        """Maneja los errores del proceso de QProcess."""
        if error != QProcess.ProcessError.UnknownError: # El error desconocido puede ser solo informativo
            error_map = {
                QProcess.ProcessError.FailedToStart: "No se pudo iniciar el programa (ejecutable no encontrado o permisos).",
                QProcess.ProcessError.Crashed: "El programa falló durante la ejecución.",
                QProcess.ProcessError.Timedout: "El proceso agotó el tiempo de espera.",
                # ... (otros errores)
            }
            error_msg = error_map.get(error, f"Error QProcess desconocido: {error.name}")
            self.console_panel.output(f"\n[ERROR FATAL DE PROCESO] {error_msg}")
        self.process = None

    # Sincroniza el estado de las acciones de vista (checked) con el estado de la pestaña
    def _sync_view_actions_to_current_tab(self, index):
        # Cuando se cambia de pestaña, actualiza el estado checked de los menús
        editor = self._current_editor()
        minimap = self._current_minimap()
        
        if editor and minimap:
            self.toggle_linenum_action.setChecked(editor.line_number_area.isVisible())
            self.toggle_minimap_action.setChecked(minimap.isVisible())
            
    # ---- Lógica de Apertura de Archivos (Unificada)
    def _open_file_content(self, path):
        """Crea una nueva pestaña con el contenido del archivo dado."""
        # 1. Comprobar si ya está abierto y cambiar a la pestaña existente
        for idx, file_path in self.open_files.items():
            if file_path == path:
                self.tabs.setCurrentIndex(idx)
                return True
        
        # 2. Leer el contenido del archivo
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error de Apertura", f"No se pudo abrir el archivo:\n{e}")
            return False

        # 3. Crear el nuevo editor y minimapa
        # IMPORTANTE: Pasamos la ruta para que CodeEditor configure el resaltador correcto
        editor = CodeEditor(filepath=path) 
        editor.setPlainText(text)
        minimap = MiniMap(editor)
        
        # Aplicar la configuración de vista
        if not self.toggle_linenum_action.isChecked():
            editor.line_number_area.hide()
            editor.update_line_number_area_width(0)
            
        if not self.toggle_minimap_action.isChecked():
            minimap.hide()

        # 4. Configurar el widget de pestaña
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        layout.addWidget(editor)
        layout.addWidget(minimap)
        layout.setStretch(0, 4)
        layout.setStretch(1, 1)

        widget = QWidget()
        widget.setLayout(layout)

        # 5. Añadir la pestaña
        idx = self.tabs.addTab(widget, os.path.basename(path))
        self.tabs.setCurrentIndex(idx)
        self.open_files[idx] = path
        
        editor.textChangedSignal.connect(lambda: self._mark_tab_dirty(idx))
        return True # Retorna éxito

    # ---- Funciones principales

    def toggle_side_panel(self, view_name):
        """Muestra/Oculta el panel lateral según el botón de la ActivityBar presionado."""
        
        # Implementación simple: solo manejamos el explorador.
        if view_name == 'explorer':
            # Mostrar el explorador si está oculto
            if self.file_explorer.isHidden():
                self.file_explorer.show()
                # Asegurar que el splitter tenga un tamaño inicial decente
                current_sizes = self.side_panel_splitter.sizes()
                if current_sizes[0] < 50:
                     self.side_panel_splitter.setSizes([250, self.width() - 250])
            else:
                # Ocultar el explorador (si está visible)
                self.file_explorer.hide()
                self.activity_bar.btn_files.setChecked(False)
                
        else:
            # Para otras vistas o si se hizo clic en el mismo botón para ocultar (view_name == '')
            if not self.file_explorer.isHidden():
                self.file_explorer.hide()
                self.activity_bar.btn_files.setChecked(False)

    def open_folder(self):
        """Permite al usuario seleccionar una carpeta para establecer el espacio de trabajo."""
        directory = QFileDialog.getExistingDirectory(self, "Abrir Carpeta (Directorio Principal)", options=QFileDialog.Option.ShowDirsOnly)
        if directory:
            self.file_explorer.set_root_path(directory)
            # Opcional: Actualizar el título de la ventana
            self.setWindowTitle(f"PyCode - {os.path.basename(directory)}")
            # Asegurar que el explorador se muestre y el botón de archivos esté marcado
            self.file_explorer.show()
            self.activity_bar.btn_files.setChecked(True)


    def open_file_from_explorer(self, path):
        """Maneja la solicitud de apertura de archivo desde el explorador."""
        self._open_file_content(path)

    def new_file(self):
        # Crear CodeEditor sin ruta (usará 'default' rules)
        editor = CodeEditor(filepath=None)
        minimap = MiniMap(editor)
        
        # Aplicar la configuración de vista al nuevo archivo
        if not self.toggle_linenum_action.isChecked():
            editor.line_number_area.hide()
            editor.update_line_number_area_width(0)
            
        if not self.toggle_minimap_action.isChecked():
            minimap.hide()

        # Usar QHBoxLayout para la división editor/minimapa
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        layout.addWidget(editor)
        layout.addWidget(minimap)
        layout.setStretch(0, 4) # Editor ocupa 4 unidades
        layout.setStretch(1, 1) # Minimapa ocupa 1 unidad (cuando es visible)

        widget = QWidget()
        widget.setLayout(layout)

        idx = self.tabs.addTab(widget, "Sin título")
        self.tabs.setCurrentIndex(idx)
        self.open_files[idx] = None
        
        # Cuando el texto cambia, marcar la pestaña como no guardada
        editor.textChangedSignal.connect(lambda: self._mark_tab_dirty(idx))

    def open_file(self):
        # Usar la ruta del proyecto actual como ubicación predeterminada si existe
        initial_path = self.file_explorer.root_path if self.file_explorer.root_path else ""
        
        # Esta lista de filtros debería idealmente cargarse desde extensions.json para ser consistente.
        file_filters = "Archivos Prisma (*.prisma);;Archivos Python (*.py);;Archivos de JavaScript (*.js *.jsx *.ts *.tsx);;Archivos de Texto (*.txt);;Todos los Archivos (*)"
        
        path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", initial_path, file_filters)
        if not path:
            return
            
        # Comprobar si el archivo ya está abierto
        if path in self.open_files.values():
            QMessageBox.information(self, "Ya Abierto", f"El archivo '{os.path.basename(path)}' ya está abierto.")
            # Cambiar a la pestaña si ya está abierta
            for idx, file_path in self.open_files.items():
                if file_path == path:
                    self.tabs.setCurrentIndex(idx)
                    return
            return

        self._open_file_content(path)

    def _mark_tab_dirty(self, index):
        current_text = self.tabs.tabText(index)
        if not current_text.endswith('*'):
            self.tabs.setTabText(index, current_text + '*')

    def save_file(self):
        idx = self.tabs.currentIndex()
        if idx == -1:
            return
            
        path = self.open_files.get(idx)
        if path:
            self._save_to_path(idx, path)
        else:
            self.save_file_as()

    def save_file_as(self):
        idx = self.tabs.currentIndex()
        if idx == -1:
            return
        
        editor = self._current_editor()
        if not editor:
            return

        current_filepath = self.open_files.get(idx)
        
        # Determinar el ID del lenguaje para el archivo/editor actual.
        # Para archivos existentes, usa su ruta. Para archivos nuevos, usa el lenguaje actual del editor.
        lang_id = editor.current_language if current_filepath is None else get_language_id(current_filepath)
        
        # Nombre de archivo predeterminado basado en el nombre de la pestaña actual
        suggested_filename = self.tabs.tabText(idx).strip('*')
        
        # Preparar filtros de archivo
        prisma_filter = "Archivos Prisma (*.prisma)"
        python_filter = "Archivos Python (*.py)"
        javascript_filter = "Archivos de JavaScript (*.js *.jsx *.ts *.tsx)"
        text_filter = "Archivos de Texto (*.txt)"
        all_files_filter = "Todos los Archivos (*)"
        
        filters_list = []
        selected_filter = "" # Para establecer el filtro por defecto en el diálogo

        if lang_id == 'opn':
            filters_list.append(prisma_filter)
            selected_filter = prisma_filter
            # Ajustar suggested_filename para 'opn' si es un archivo nuevo o no tiene extensión .prisma
            base_name, ext = os.path.splitext(suggested_filename)
            if base_name == "Sin título" or not ext or ext.lower() != ".prisma":
                suggested_filename = base_name.replace("Sin título", "untitled") + ".prisma"
        
        # Añadir otros filtros comunes, asegurando que no haya duplicados
        if python_filter not in filters_list: filters_list.append(python_filter)
        if javascript_filter not in filters_list: filters_list.append(javascript_filter)
        if text_filter not in filters_list: filters_list.append(text_filter)
        if all_files_filter not in filters_list: filters_list.append(all_files_filter)
        
        file_filters = ";;".join(filters_list)
        
        path, _ = QFileDialog.getSaveFileName(self, "Guardar como", suggested_filename, file_filters, selected_filter=selected_filter)
        if not path:
            return
            
        self._save_to_path(idx, path)
        self.tabs.setTabText(idx, os.path.basename(path)) # Actualizar título de la pestaña
        self.open_files[idx] = path # Actualizar ruta almacenada
        
        # IMPORTANTE: Si guardamos por primera vez, necesitamos actualizar el resaltador
        editor = self._current_editor()
        if editor:
            editor.set_language_highlighter(path)
            editor.set_language_completer(path)

    def _save_to_path(self, idx, path):
        editor = self._current_editor()
        if editor is None: return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
            
            # Quitar marcador de no guardado al guardar con éxito
            current_text = self.tabs.tabText(idx)
            if current_text.endswith('*'):
                self.tabs.setTabText(idx, current_text.rstrip('*'))
                
        except Exception as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo guardar el archivo:\n{e}")

    def auto_save_all(self):
        # Auto-guardado solo guarda archivos que ya tienen una ruta
        for idx in range(self.tabs.count()):
            path = self.open_files.get(idx)
            if path:
                try:
                    widget = self.tabs.widget(idx)
                    editor = widget.layout().itemAt(0).widget()
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(editor.toPlainText())
                except Exception as e:
                    print(f"Error en auto-guardado de {path}: {e}")
                    pass
        # Opcional: Mostrar un mensaje de auto-guardado en la consola
        self.console_panel.output(f"[{QTime.currentTime().toString(Qt.DateFormat.ISODate)}] Auto-guardado completado.")


    def open_find_dialog(self):
        editor = self._current_editor()
        if not editor:
            return
        # Abrir diálogo, que gestionará la lógica de búsqueda/reemplazo
        dlg = FindReplaceDialog(editor)
        dlg.exec()
        
    def toggle_minimap(self, checked):
        # Alternar visibilidad del minimapa en la pestaña actual
        minimap = self._current_minimap()
        if minimap:
            if checked:
                minimap.show()
            else:
                minimap.hide()

    def toggle_line_numbers(self, checked):
        # Alternar visibilidad de la numeración de líneas en la pestaña actual
        editor = self._current_editor()
        if editor:
            editor.line_number_area.setVisible(checked)
            # Volver a calcular los márgenes para mostrar/ocultar el área
            editor.update_line_number_area_width(0)
            
    # NUEVA FUNCIÓN: Alternar Consola (Actualizada para sincronizar el estado)
    def toggle_console(self, checked):
        """Muestra u oculta el panel de la consola y actualiza la acción del menú."""
        # Asegurar que el estado del QAction se mantenga sincronizado
        self.toggle_console_action.setChecked(checked)
        
        if checked:
            self.console_panel.show()
            # Asegurar que el splitter tenga una altura inicial adecuada si la consola estaba minimizada
            current_sizes = self.editor_console_splitter.sizes()
            if current_sizes[1] < 10:
                self.editor_console_splitter.setSizes([self.height() - 200, 200])
        else:
            self.console_panel.hide()


    def close_tab(self, index):
        # Comprobar si el archivo tiene cambios sin guardar
        if self.tabs.tabText(index).endswith('*'):
            reply = QMessageBox.question(self, "Guardar Cambios",
                "El archivo tiene cambios sin guardar. ¿Deseas guardarlos antes de cerrar?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Cancel:
                return # Detener el proceso de cierre
            
            if reply == QMessageBox.StandardButton.Save:
                self.tabs.setCurrentIndex(index)
                self.save_file()
                # Si save_file falla o se cancela el Guardar Como, el marcador puede permanecer.
                if self.tabs.tabText(index).endswith('*'):
                     return # Cancelar el cierre si el guardado no fue exitoso/se canceló

        # Eliminar pestaña e información de archivos abiertos
        self.tabs.removeTab(index)
        self.open_files.pop(index, None)
        
    def closeEvent(self, event):
        # Comprobar todas las pestañas en busca de cambios no guardados antes de cerrar
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i).endswith('*'):
                self.tabs.setCurrentIndex(i)
                reply = QMessageBox.question(self, "Guardar Cambios",
                    f"El archivo '{self.tabs.tabText(i).rstrip('*')}' tiene cambios sin guardar. ¿Deseas guardarlos?",
                    QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

                if reply == QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
                
                if reply == QMessageBox.StandardButton.Save:
                    self.save_file()
                    # Si el guardado falló, abortar el cierre
                    if self.tabs.tabText(i).endswith('*'):
                        event.ignore()
                        return
        
        event.accept()


def main():
    app = QApplication(sys.argv)
    win = VSCodeEditor() 
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()