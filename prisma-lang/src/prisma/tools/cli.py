from __future__ import annotations

import argparse
import sys
from pathlib import Path
import os

# --- Solución al ImportError ---
# Este bloque permite que el script se ejecute directamente (ej. `python prisma/cli.py`).
# Ajusta el sys.path para que Python pueda encontrar los otros módulos del paquete.
if __name__ == "__main__" and __package__ is None:
    src_dir = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(src_dir))
    from prisma.core import TranspilerError, transpile
    from prisma.tools.repl import run_repl
    from prisma.api import pygfx_api
    from prisma.api import server_api
    from prisma.api import compilation_api
    from prisma.api import config_api
    import cmd
else:
    from prisma.core import TranspilerError, transpile
    from prisma.tools.repl import run_repl
    from prisma.api import pygfx_api
    from prisma.api import server_api
    from prisma.api import compilation_api
    from prisma.api import config_api
    import cmd


def read_source(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def write_output(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")


def run_code(code: str) -> None:
    # 1. Creamos el diccionario de nombres (namespace) para la ejecución.
    # 2. Es CRUCIAL inyectar el módulo 'pygfx_api' con el nombre 'gfx',
    #    ya que el código transpiliado lo busca directamente como 'gfx'.
    namespace = {
        "__name__": "__main__",
        "gfx": pygfx_api,
        "server": server_api # <--- ¡Inyectamos la API del servidor aquí!
    }
    
    try:
        # 1. Inicializa la API de gráficos
        pygfx_api.init()
        # 2. Ejecutamos el código transpiliado del usuario
        exec(compile(code, "<opn>", "exec"), namespace)
        
        # 3. Si se creó una ventana de Tkinter, iniciamos su bucle principal.
        if pygfx_api._ROOT is not None:
            print("[GFX TK] Iniciando bucle de eventos de Tkinter...")
            pygfx_api._ROOT.mainloop()
    finally:
        # 4. Nos aseguramos de que Tkinter se cierre correctamente, incluso si hay un error
        pygfx_api.quit()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OPN Language - Transpile and execute OPN code")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    run_parser = subparsers.add_parser("run", help="Run a .prisma script or start the REPL (default)")
    run_parser.add_argument(
        "source", nargs="?", default=None, help="Path to a .prisma file (code) or .opn file (data). If omitted, starts the REPL."
    )
    run_parser.add_argument("-o", "--output", help="Write the generated Python to the given file")
    run_parser.add_argument("--no-run", action="store_true", help="Only transpile the code without executing it.")
    
    transpile_parser = subparsers.add_parser("transpile", help="Transpile OPN code to Python without executing")
    transpile_parser.add_argument("source", help="Path to a .prisma or .opn file")
    transpile_parser.add_argument("-o", "--output", help="Output file for generated Python code")
    
    editor_parser = subparsers.add_parser("editor", help="Launch the OPN Editor GUI")

    package_parser = subparsers.add_parser("package", help="Manage OPN packages")
    package_parser.add_argument("action", choices=["install", "publish"], help="Package action")
    package_parser.add_argument("name", help="Package name")

    compile_parser = subparsers.add_parser("compile", help="Compile OPN project to package")
    compile_parser.add_argument("project_path", help="Path to project directory containing source files")
    compile_parser.add_argument("-o", "--output", required=True, help="Output directory for compiled package")
    compile_parser.add_argument("-n", "--name", required=True, help="Package name")
    compile_parser.add_argument("-v", "--version", default="1.0.0", help="Package version (default: 1.0.0)")
    compile_parser.add_argument("-d", "--description", default="", help="Package description")
    compile_parser.add_argument("-a", "--author", default="", help="Package author")

    build_parser = subparsers.add_parser("build", help="Quick build package from directory")
    build_parser.add_argument("source", help="Source directory with .prisma files")
    build_parser.add_argument("-n", "--name", help="Package name (auto-detected from folder if not specified)")
    build_parser.add_argument("-v", "--version", default="1.0.0", help="Version number")

    config_parser = subparsers.add_parser("config", help="Manage OPN configuration")
    config_subparsers = config_parser.add_subparsers(dest="config_action", help="Configuration action")
    config_subparsers.add_parser("init", help="Initialize OPN configuration")
    config_subparsers.add_parser("show", help="Show current configuration")
    
    path_parser = config_subparsers.add_parser("add-source", help="Add source path")
    path_parser.add_argument("path", help="Path to add")
    
    path_parser2 = config_subparsers.add_parser("add-package", help="Add package path")
    path_parser2.add_argument("path", help="Package path to add")

    fix_paths_parser = subparsers.add_parser("fix-paths", help="Auto-correct file paths in project")
    fix_paths_parser.add_argument("project_path", help="Project directory to scan")

    return parser




def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    
    raw_argv = argv or sys.argv[1:]
    if raw_argv and not raw_argv[0].startswith("-") and raw_argv[0] not in ["run", "package", "transpile", "editor", "compile", "build", "config", "fix-paths"]:
        raw_argv = ["run"] + raw_argv
    
    args = parser.parse_args(raw_argv if argv is None else argv)
    cmd = args.command

    if cmd is None:
        run_repl()
        return 0

    if cmd == "run":
        if args.source is None:
            run_repl()
            return 0
        try:
            source_path = args.source
            file_ext = Path(source_path).suffix.lower()
            
            if file_ext not in ['.prisma', '.opn']:
                print(f"Warning: File extension '{file_ext}' is not standard. Use .prisma for code or .opn for data.", file=sys.stderr)
            
            source = read_source(source_path)
            python_code = transpile(source, source_file=source_path)

            if args.output:
                write_output(args.output, python_code)

            if not args.no_run and not args.output:
                run_code(python_code)
            elif not args.no_run and args.output is None:
                sys.stdout.write(python_code)
        except (FileNotFoundError, TranspilerError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    elif cmd == "transpile":
        try:
            source_path = args.source
            source = read_source(source_path)
            python_code = transpile(source, source_file=source_path)
            
            if args.output:
                write_output(args.output, python_code)
                print(f"Transpiled to: {args.output}")
            else:
                sys.stdout.write(python_code)
        except (FileNotFoundError, TranspilerError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    elif cmd == "editor":
        try:
            from prisma.tools.editor import main as editor_main
            editor_main()
        except ImportError as e:
            print(f"Error: Could not launch editor. Make sure tkinter is installed.\n{e}", file=sys.stderr)
            return 1

    elif cmd == "compile":
        try:
            if not Path(args.project_path).exists():
                print(f"Error: Project path does not exist: {args.project_path}", file=sys.stderr)
                return 1
            
            result = compilation_api.compile_project(
                project_path=args.project_path,
                output_dir=args.output,
                name=args.name,
                version=args.version,
                description=args.description,
                author=args.author
            )
            
            print(f"✓ Compilation successful!")
            print(f"  Project: {result['project_path']}")
            print(f"  Output: {result['output_path']}")
            print(f"  Source files: {result['source_files']}")
            print(f"  Functions extracted: {result['functions']}")
            print(f"  Files generated: {result['files_generated']}")
            
        except Exception as e:
            print(f"Error during compilation: {e}", file=sys.stderr)
            return 1
    
    elif cmd == "build":
        try:
            if not Path(args.source).exists():
                print(f"Error: Source path does not exist: {args.source}", file=sys.stderr)
                return 1
            
            result = compilation_api.quick_compile(
                source_path=args.source,
                package_name=args.name,
                version=args.version
            )
            
            print(f"[BUILD] Package created successfully!")
            print(f"  Name: {result['project_path']}")
            print(f"  Output: {result['output_path']}")
            print(f"  Functions: {result['functions']}")
            print(f"  Location: {result['output_path']}")
            
        except Exception as e:
            print(f"Error during build: {e}", file=sys.stderr)
            return 1
    
    elif cmd == "config":
        try:
            config_manager = config_api.ConfigManager()
            
            if args.config_action == "init":
                print("OPN Configuration initialized at:")
                print(f"  {config_manager.config_dir}")
                print("\nConfiguration files:")
                print(f"  - {config_manager.packages_config}")
                print(f"  - {config_manager.paths_config}")
                print(f"  - {config_manager.settings_config}")
            
            elif args.config_action == "show":
                print("\n=== Packages ===")
                packages = config_manager.get_packages()
                if packages:
                    for pkg in packages:
                        print(f"  {pkg['name']} v{pkg['version']}: {pkg['path']}")
                else:
                    print("  No packages registered")
                
                print("\n=== Paths ===")
                paths = config_manager.get_paths()
                print(f"  Source paths: {len(paths.get('sourcePaths', []))}")
                for path in paths.get('sourcePaths', []):
                    print(f"    - {path}")
                print(f"  Package paths: {len(paths.get('packagePaths', []))}")
                for path in paths.get('packagePaths', []):
                    print(f"    - {path}")
                print(f"  Output: {paths.get('outputPath', 'not set')}")
                
                print("\n=== Settings ===")
                settings = config_manager.get_settings()
                for key, value in settings.items():
                    if key != 'lastUpdated':
                        print(f"  {key}: {value}")
            
            elif args.config_action == "add-source":
                config_manager.add_source_path(args.path)
                print(f"Added source path: {args.path}")
            
            elif args.config_action == "add-package":
                config_manager.add_package_path(args.path)
                print(f"Added package path: {args.path}")
        
        except Exception as e:
            print(f"Config error: {e}", file=sys.stderr)
            return 1
    
    elif cmd == "fix-paths":
        try:
            config_manager = config_api.ConfigManager()
            result = config_manager.auto_correct_project(args.project_path)
            
            print(f"[FIX-PATHS] Scan complete")
            print(f"  Project: {result['project']}")
            print(f"  Files scanned: {len(result['files'])}")
            print(f"  Total corrections: {result['totalCorrected']}")
            
            if result['files']:
                print("\nCorrected imports:")
                for file_info in result['files']:
                    print(f"  {file_info['file']}")
                    for correction in file_info['corrections']:
                        print(f"    - {correction['package']}")
        
        except Exception as e:
            print(f"Error fixing paths: {e}", file=sys.stderr)
            return 1
    
    elif cmd == "package":
        print(f"Package manager: {args.action} {args.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
