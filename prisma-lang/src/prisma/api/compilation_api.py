import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from .config_api import ConfigManager


class FunctionExtractor:
    def __init__(self):
        self.function_pattern = re.compile(
            r'func\s+(\w+)\s*\((.*?)\)\s*(?:->|{)',
            re.MULTILINE | re.DOTALL
        )
        self.docstring_pattern = re.compile(
            r'//\s*(.*?)(?=\n(?:func|class|let|\Z))',
            re.MULTILINE | re.DOTALL
        )

    def extract_functions(self, code: str) -> List[Dict]:
        functions = []
        for match in self.function_pattern.finditer(code):
            func_name = match.group(1)
            params_str = match.group(2).strip()
            
            params = []
            if params_str:
                for param in params_str.split(','):
                    param = param.strip()
                    if param:
                        parts = param.split(':')
                        param_name = parts[0].strip()
                        param_type = parts[1].strip() if len(parts) > 1 else "any"
                        params.append({
                            "name": param_name,
                            "type": param_type
                        })
            
            functions.append({
                "name": func_name,
                "parameters": params,
                "description": "",
                "category": "core",
                "returnType": "any"
            })
        
        return functions

    def extract_with_documentation(self, code: str) -> List[Dict]:
        functions = self.extract_functions(code)
        
        for func in functions:
            doc_match = re.search(
                rf'//\s*(.*?)func\s+{func["name"]}\s*\(',
                code,
                re.DOTALL
            )
            if doc_match:
                doc_text = doc_match.group(1).strip()
                doc_lines = [line.strip().lstrip('//').strip() 
                           for line in doc_text.split('\n') if line.strip()]
                if doc_lines:
                    func["description"] = ' '.join(doc_lines)
        
        return functions


class ProjectCompiler:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.source_files = []
        self.all_code = ""
        self.functions = []
        self.metadata = {}
        self.extractor = FunctionExtractor()

    def discover_source_files(self, extensions: List[str] = None) -> List[Path]:
        if extensions is None:
            extensions = ['.prisma', '.opn']
        
        self.source_files = []
        for ext in extensions:
            self.source_files.extend(self.project_path.rglob(f'*{ext}'))
        
        self.source_files = sorted([
            f for f in self.source_files 
            if f.name != 'index.prisma'
        ])
        
        return self.source_files

    def consolidate_code(self) -> str:
        consolidated = []
        
        for file_path in self.source_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                if content.strip():
                    consolidated.append(f"\n// === From: {file_path.name} ===\n")
                    consolidated.append(content)
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
        
        self.all_code = '\n'.join(consolidated)
        return self.all_code

    def extract_all_functions(self) -> List[Dict]:
        self.functions = self.extractor.extract_with_documentation(self.all_code)
        return self.functions

    def generate_index_prisma(self, output_path: Path) -> str:
        header = f"// Auto-generated index.prisma\n// Generated: {datetime.now().isoformat()}\n// Source files: {len(self.source_files)}\n\n"
        content = header + self.all_code
        
        output_path.write_text(content, encoding='utf-8')
        return content

    def generate_functions_json(self, output_path: Path) -> Dict:
        categories = {}
        for func in self.functions:
            cat = func.get('category', 'core')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(func['name'])
        
        functions_doc = {
            "metadata": {
                "version": "1.0.0",
                "format": "opn-functions-doc-v1",
                "generatedAt": datetime.now().isoformat(),
                "generatedBy": "OPN Compiler"
            },
            "statistics": {
                "sourceFiles": len(self.source_files),
                "totalFunctions": len(self.functions),
                "categories": len(categories),
                "averageParametersPerFunction": round(sum(len(f.get('parameters', [])) for f in self.functions) / max(1, len(self.functions)), 2)
            },
            "configuration": {
                "layers": {
                    "core": "Core functions provided by the package",
                    "utils": "Utility functions for common tasks",
                    "effects": "Visual effects and animations",
                    "shapes": "Shape drawing and rendering",
                    "colors": "Color definitions and manipulation",
                    "advanced": "Advanced functionality"
                },
                "autoCompletion": {
                    "enabled": True,
                    "provider": "opn",
                    "triggerCharacters": [".", "("]
                },
                "ide": {
                    "vscode": True,
                    "vseditor": True,
                    "snippets": True
                }
            },
            "categories": categories,
            "functions": self.functions,
            "sourceFiles": [f.name for f in self.source_files]
        }
        
        output_path.write_text(
            json.dumps(functions_doc, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        return functions_doc

    def generate_opn_metadata(self, output_path: Path, metadata: Dict) -> Dict:
        opn_file = {
            "name": metadata.get("name", "unknown"),
            "version": metadata.get("version", "1.0.0"),
            "description": metadata.get("description", ""),
            "author": metadata.get("author", ""),
            "main": "index.prisma",
            "functions": [func["name"] for func in self.functions]
        }
        
        output_path.write_text(
            json.dumps(opn_file, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        return opn_file

    def compile_project(self, output_dir: str, metadata: Dict) -> Dict:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        self.discover_source_files()
        self.consolidate_code()
        self.extract_all_functions()
        
        self.generate_index_prisma(output_path / "index.prisma")
        functions_doc = self.generate_functions_json(output_path / "functions.json")
        opn_metadata = self.generate_opn_metadata(output_path / f"{metadata.get('name', 'package')}.opn", metadata)
        
        return {
            "success": True,
            "project_path": str(self.project_path),
            "output_path": str(output_path),
            "source_files": len(self.source_files),
            "functions": len(self.functions),
            "files_generated": 3,
            "timestamp": datetime.now().isoformat()
        }


def compile_project(
    project_path: str,
    output_dir: str,
    name: str,
    version: str = "1.0.0",
    description: str = "",
    author: str = ""
) -> Dict:
    compiler = ProjectCompiler(project_path)
    
    metadata = {
        "name": name,
        "version": version,
        "description": description,
        "author": author
    }
    
    return compiler.compile_project(output_dir, metadata)


def quick_compile(
    source_path: str,
    package_name: str = None,
    version: str = "1.0.0"
) -> Dict:
    source_path = Path(source_path)
    
    if package_name is None:
        package_name = source_path.name if source_path.is_dir() else source_path.stem
    
    output_dir = str(source_path.parent / f"{package_name}_build")
    
    result = compile_project(
        project_path=str(source_path),
        output_dir=output_dir,
        name=package_name,
        version=version,
        description=f"Auto-compiled package: {package_name}",
        author="OPN Build System"
    )
    
    config = ConfigManager()
    config.add_package({
        "name": package_name,
        "version": version,
        "path": output_dir,
        "main": "index.prisma"
    })
    
    return result
