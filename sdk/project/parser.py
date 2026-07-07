import tomllib
from pathlib import Path
from typing import Optional
from .model import Project, Package, BuildConfiguration, SourceFile

class ProjectParser:
    @staticmethod
    def load(project_dir: Path) -> Project:
        toml_path = project_dir / "lala.toml"
        if not toml_path.exists():
            raise FileNotFoundError(f"Missing lala.toml in {project_dir}")
            
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
            
        pkg_data = data.get("package", {})
        deps_data = data.get("dependencies", {})
        build_data = data.get("build", {})
        
        package = Package(
            name=pkg_data.get("name", "unknown"),
            version=pkg_data.get("version", "0.1.0"),
            dependencies=deps_data
        )
        
        build_config = BuildConfiguration(
            optimization=build_data.get("optimization", "O0"),
            target=build_data.get("target", "x86_64"),
            entry=build_data.get("entry", "lala.main")
        )
        
        project = Project(
            root_dir=project_dir,
            package=package,
            build_config=build_config,
            source_files=[]
        )
        
        # Load all .lala files in src/
        src_dir = project_dir / "src"
        if src_dir.exists():
            for p in src_dir.rglob("*.lala"):
                project.source_files.append(SourceFile.load(p))
                
        # If no src/, maybe it's just a single file project
        if not project.source_files:
            for p in project_dir.glob("*.lala"):
                project.source_files.append(SourceFile.load(p))
                
        return project
