# 🚀 OPN Language

**OPN** is a friendly, multi-paradigm programming language that transpiles to Python. It features an integrated IDE, graphics API, and is designed for both education and practical development.

## ✨ Features

- 🎯 **Simple Syntax**: Easy to learn, powerful to use
- 🔄 **Python Transpiler**: Compiles to clean, readable Python code
- 🎨 **Graphics API**: Built-in Tkinter-based graphics library
- 💻 **Integrated IDE**: Full-featured editor with autocomplete and error detection
- 📚 **Interactive REPL**: Test code instantly
- 🔧 **Extensible**: Easy to add custom functions and modules
- 📦 **Two File Types**: `.prisma` for code, `.opn` for data

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/opn-language.git
cd opn-language/prisma-lang

# Install the package
pip install -e .

# Or install from PyPI (when published)
pip install opn-language
```

### Your First Program

Create a file `hello.prisma`:

```prisma
func main() {
    py.print("Hello, OPN!");
}
```

Run it:

```bash
opn hello.prisma
```

## 📖 Documentation

Comprehensive documentation is available in the [`docs/`](../docs) folder:

- [Getting Started](../docs/getting_started.md) - Your first steps with OPN
- [File Types](../docs/file_types.md) - Understanding `.prisma` vs `.opn` files
- [Graphics API](../docs/gfx_api.md) - Complete graphics reference
- [Editor Guide](../docs/editor.md) - Using the integrated IDE
- [REPL](../docs/repl.md) - Interactive console usage
- [Examples](../docs/gfx_examples.md) - Code examples and tutorials

## 🎨 Graphics Example

```prisma
func main() {
    gfx.setup_canvas(800, 600, "My Graphics");
    
    gfx.draw_circle(400, 300, 100, gfx.Azul);
    gfx.draw_point(400, 300, gfx.Rojo, 10);
    
    gfx.update_screen();
    gfx.init();
}
```

## 💻 Using the IDE

Launch the integrated editor:

```bash
opn editor
```

Features:
- ✅ Syntax highlighting
- ✅ Autocomplete (Ctrl+Space)
- ✅ Real-time error detection
- ✅ Integrated console with commands
- ✅ Built-in documentation
- ✅ Run and transpile from the editor

## 🔧 CLI Commands

```bash
# Run a program
opn run program.prisma
opn program.prisma              # 'run' is implicit

# Transpile to Python
opn transpile program.prisma
opn transpile program.prisma -o output.py

# Launch the editor
opn editor

# Start the REPL
opn
```

## 📦 File Types

OPN uses two file extensions:

- **`.prisma`** - Executable code files
- **`.opn`** - Data and configuration files

Example structure:
```
my_project/
├── main.prisma          # Main program
├── utils.prisma         # Utility functions
└── config.opn           # Configuration data
```

## 🛠️ Development

### Project Structure

```
opn-language/
├── prisma-lang/
│   ├── src/
│   │   └── prisma/
│   │       ├── config/          # Configuration files
│   │       ├── transpiler.py    # Core transpiler
│   │       ├── cli.py           # Command-line interface
│   │       ├── editor.py        # Integrated IDE
│   │       ├── pygfx_api.py     # Graphics API
│   │       └── repl.py          # Interactive console
│   ├── setup.py
│   └── pyproject.toml
├── docs/                        # Documentation
└── tests/                       # Test files
```

### Running Tests

```bash
cd prisma-lang
pytest
```

### Building for Distribution

```bash
# Build the package
python -m build

# Install locally
pip install -e .

# Upload to PyPI (requires credentials)
python -m twine upload dist/*
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Features Roadmap

- [x] Python transpiler
- [x] Graphics API (Tkinter)
- [x] Integrated IDE
- [x] REPL
- [x] Error detection
- [x] Autocomplete
- [ ] Debugger
- [ ] Package manager
- [ ] Standard library expansion
- [ ] VSCode extension
- [ ] Web playground

## 📚 Examples

### Basic Program
```prisma
func greet(name) {
    py.print("Hello,", name, "!");
}

func main() {
    greet("World");
}
```

### Graphics Program
```prisma
func draw_smiley() {
    gfx.setup_canvas(400, 400, "Smiley");
    
    gfx.draw_circle(200, 200, 100, gfx.Amarillo);
    gfx.draw_circle(170, 180, 10, gfx.Negro);
    gfx.draw_circle(230, 180, 10, gfx.Negro);
    gfx.draw_circle(200, 220, 50, gfx.Negro);
    
    gfx.update_screen();
    gfx.init();
}

func main() {
    draw_smiley();
}
```

### Data File (config.opn)
```opn
let APP_CONFIG = {
    "name": "My App",
    "version": "1.0.0",
    "debug": true
};

let COLORS = {
    "primary": gfx.Azul,
    "secondary": gfx.Verde
};
```

## 🔗 Links

- [Documentation](../docs/README.md)
- [GitHub Repository](https://github.com/yourusername/opn-language)
- [Issue Tracker](https://github.com/yourusername/opn-language/issues)

## 💬 Community

- Report bugs in the [Issue Tracker](https://github.com/yourusername/opn-language/issues)
- Ask questions in [Discussions](https://github.com/yourusername/opn-language/discussions)
- Share your projects!

## 🙏 Acknowledgments

- Built with Python
- Graphics powered by Tkinter
- Inspired by modern programming languages

---

**Made with ❤️ by the OPN Language Project**
