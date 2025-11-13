#!/usr/bin/env python3
import os
import sys
import json

def check_files():
    print("=" * 60)
    print("VERIFICACION DEL EDITOR OPN")
    print("=" * 60)
    
    checks = {
        "VSeditor.py": "Editor principal",
        "recursos/colores.json": "Configuracion de colores",
        "recursos/extensions.json": "Mapeo de extensiones",
        "test_example.opn": "Archivo de prueba",
        "FEATURES.md": "Guia de caracteristicas",
        "README_EDITOR.md": "Manual de usuario"
    }
    
    print("\n[FILES] Verificando archivos...")
    all_ok = True
    for file, desc in checks.items():
        path = os.path.join(os.path.dirname(__file__), file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print("[OK]  " + file.ljust(30) + " (" + desc + ")")
        else:
            print("[FAIL] " + file.ljust(30) + " FALTANTE")
            all_ok = False
    
    print("\n[DEPS] Verificando dependencias...")
    dependencies = {
        "PyQt6": "Editor GUI",
        "json": "Configuracion",
        "re": "Resaltado sintaxis"
    }
    
    for lib, desc in dependencies.items():
        try:
            __import__(lib)
            print("[OK]  " + lib.ljust(20) + " (" + desc + ")")
        except ImportError:
            print("[FAIL] " + lib.ljust(20) + " NO INSTALADO - pip install " + lib)
            all_ok = False
    
    print("\n[JSON] Validando archivos JSON...")
    json_files = {
        "recursos/colores.json": "Colores y sintaxis",
        "recursos/extensions.json": "Extensiones"
    }
    
    for file, desc in json_files.items():
        path = os.path.join(os.path.dirname(__file__), file)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    json.load(f)
                print("[OK]  " + file.ljust(30) + " JSON valido")
            except json.JSONDecodeError as e:
                print("[FAIL] " + file.ljust(30) + " ERROR JSON: " + str(e))
                all_ok = False
        else:
            print("[FAIL] " + file.ljust(30) + " NO ENCONTRADO")
            all_ok = False
    
    print("\n[OPN] Verificando configuracion OPN...")
    colores_path = os.path.join(os.path.dirname(__file__), "recursos/colores.json")
    if os.path.exists(colores_path):
        try:
            with open(colores_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if "languages" in config and "opn" in config["languages"]:
                opn_config = config["languages"]["opn"]
                
                has_rules = "rules" in opn_config and len(opn_config["rules"]) > 0
                has_completions = "completions" in opn_config and len(opn_config["completions"]) > 0
                has_execution = "execution_command" in opn_config
                
                status_rules = "OK" if has_rules else "FAIL"
                status_compl = "OK" if has_completions else "FAIL"
                status_exec = "OK" if has_execution else "FAIL"
                
                print("[" + status_rules + "]  Reglas de sintaxis: " + str(len(opn_config.get('rules', []))) + " reglas")
                print("[" + status_compl + "]  Autocompletado: " + str(len(opn_config.get('completions', []))) + " palabras")
                print("[" + status_exec + "]  Comando ejecucion: " + str(opn_config.get('execution_command', 'NO')))
                
                if has_execution:
                    print("     -> Comando: " + opn_config['execution_command'])
            else:
                print("[FAIL] Configuracion OPN no encontrada")
                all_ok = False
        except Exception as e:
            print("[FAIL] Error leyendo colores.json: " + str(e))
            all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("[SUCCESS] TODO VERIFICADO - LISTO PARA USAR")
        print("\nPara iniciar el editor:")
        print("  python vscode/VSeditor.py")
        print("\nO en Windows PowerShell:")
        print("  python .\\vscode\\VSeditor.py")
    else:
        print("[ERROR] FALTAN CONFIGURACIONES - Ver errores arriba")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    check_files()
