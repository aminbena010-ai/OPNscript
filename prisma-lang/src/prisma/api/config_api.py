import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ConfigManager:
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = str(Path.home() / '.opn' / 'config')
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.packages_config = self.config_dir / 'packages.json'
        self.paths_config = self.config_dir / 'paths.json'
        self.settings_config = self.config_dir / 'settings.json'
        
        self._init_default_configs()

    def _init_default_configs(self):
        if not self.packages_config.exists():
            self._save_json(self.packages_config, {
                "version": "1.0.0",
                "lastUpdated": datetime.now().isoformat(),
                "packages": []
            })
        
        if not self.paths_config.exists():
            self._save_json(self.paths_config, {
                "version": "1.0.0",
                "lastUpdated": datetime.now().isoformat(),
                "sourcePaths": [],
                "packagePaths": [
                    str(Path.cwd() / 'opn.import'),
                    str(Path.home() / '.opn' / 'packages')
                ],
                "outputPath": str(Path.cwd() / 'opn_build')
            })
        
        if not self.settings_config.exists():
            self._save_json(self.settings_config, {
                "version": "1.0.0",
                "lastUpdated": datetime.now().isoformat(),
                "autoCorrectPaths": True,
                "autoCompile": False,
                "targetLanguage": "python",
                "debugMode": False,
                "encoding": "utf-8"
            })

    def _save_json(self, file_path: Path, data: Dict) -> None:
        file_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def _load_json(self, file_path: Path) -> Dict:
        if not file_path.exists():
            return {}
        return json.loads(file_path.read_text(encoding='utf-8'))

    def add_package(self, package_info: Dict) -> Dict:
        config = self._load_json(self.packages_config)
        
        new_package = {
            "name": package_info.get('name'),
            "version": package_info.get('version', '1.0.0'),
            "path": str(Path(package_info.get('path')).resolve()),
            "main": package_info.get('main', 'index.prisma'),
            "addedAt": datetime.now().isoformat()
        }
        
        config['packages'].append(new_package)
        config['lastUpdated'] = datetime.now().isoformat()
        self._save_json(self.packages_config, config)
        
        return new_package

    def get_packages(self) -> List[Dict]:
        config = self._load_json(self.packages_config)
        return config.get('packages', [])

    def add_source_path(self, path: str) -> None:
        config = self._load_json(self.paths_config)
        abs_path = str(Path(path).resolve())
        
        if abs_path not in config['sourcePaths']:
            config['sourcePaths'].append(abs_path)
            config['lastUpdated'] = datetime.now().isoformat()
            self._save_json(self.paths_config, config)

    def add_package_path(self, path: str) -> None:
        config = self._load_json(self.paths_config)
        abs_path = str(Path(path).resolve())
        
        if abs_path not in config['packagePaths']:
            config['packagePaths'].append(abs_path)
            config['lastUpdated'] = datetime.now().isoformat()
            self._save_json(self.paths_config, config)

    def get_paths(self) -> Dict:
        return self._load_json(self.paths_config)

    def set_output_path(self, path: str) -> None:
        config = self._load_json(self.paths_config)
        config['outputPath'] = str(Path(path).resolve())
        config['lastUpdated'] = datetime.now().isoformat()
        self._save_json(self.paths_config, config)

    def get_settings(self) -> Dict:
        return self._load_json(self.settings_config)

    def update_settings(self, updates: Dict) -> Dict:
        config = self._load_json(self.settings_config)
        config.update(updates)
        config['lastUpdated'] = datetime.now().isoformat()
        self._save_json(self.settings_config, config)
        return config

    def find_package(self, package_name: str) -> Optional[Dict]:
        packages = self.get_packages()
        for pkg in packages:
            if pkg['name'] == package_name:
                return pkg
        return None

    def find_package_in_paths(self, package_name: str) -> Optional[Path]:
        paths = self.get_paths()
        for package_path in paths.get('packagePaths', []):
            pkg_dir = Path(package_path) / package_name
            if pkg_dir.exists():
                return pkg_dir
        return None

    def auto_correct_paths_in_file(self, file_path: str) -> Dict:
        file_path = Path(file_path)
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        import_pattern = r'import\s+([a-zA-Z_]\w*)\s*;'
        import re as re_module
        
        imports = re_module.findall(import_pattern, content)
        corrections = []
        
        for import_name in imports:
            pkg = self.find_package_in_paths(import_name)
            if pkg:
                corrections.append({
                    "package": import_name,
                    "path": str(pkg)
                })
        
        return {
            "file": str(file_path),
            "corrected": len(corrections) > 0,
            "corrections": corrections,
            "originalContent": original_content == content
        }

    def auto_correct_project(self, project_path: str) -> Dict:
        project_path = Path(project_path)
        results = {
            "project": str(project_path),
            "files": [],
            "totalCorrected": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        for file_path in project_path.rglob('*.prisma'):
            correction = self.auto_correct_paths_in_file(str(file_path))
            if correction['corrected']:
                results['files'].append(correction)
                results['totalCorrected'] += len(correction['corrections'])
        
        return results
