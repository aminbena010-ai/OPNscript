from pathlib import Path
from typing import Optional, Tuple
import json
import sys


class PackageLoader:
    def __init__(self):
        self.package_paths = [
            Path.cwd() / 'opn.import',
            Path.home() / '.opn' / 'packages'
        ]
        self.cache = {}

    def add_search_path(self, path: str) -> None:
        path_obj = Path(path)
        if path_obj not in self.package_paths:
            self.package_paths.insert(0, path_obj)

    def find_package(self, package_name: str) -> Optional[Path]:
        if package_name in self.cache:
            return self.cache[package_name]
        
        for search_path in self.package_paths:
            package_dir = search_path / package_name
            if package_dir.exists() and (package_dir / 'index.prisma').exists():
                self.cache[package_name] = package_dir
                return package_dir
        
        return None

    def load_package_code(self, package_name: str) -> Optional[str]:
        package_dir = self.find_package(package_name)
        if not package_dir:
            return None
        
        index_file = package_dir / 'index.prisma'
        if not index_file.exists():
            return None
        
        return index_file.read_text(encoding='utf-8')

    def get_package_metadata(self, package_name: str) -> Optional[dict]:
        package_dir = self.find_package(package_name)
        if not package_dir:
            return None
        
        opn_file = package_dir / f'{package_name}.opn'
        if not opn_file.exists():
            return None
        
        try:
            return json.loads(opn_file.read_text(encoding='utf-8'))
        except:
            return None

    def resolve_import(self, module_name: str, source_file: str = None) -> Tuple[str, str]:
        is_opn_package = False
        code = None
        
        package = self.find_package(module_name)
        if package:
            is_opn_package = True
            code = self.load_package_code(module_name)
        
        if not code and not is_opn_package:
            return ('python', module_name)
        
        if code:
            return ('opn', code)
        
        return ('python', module_name)
