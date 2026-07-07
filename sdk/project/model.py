from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

@dataclass
class SourceFile:
    path: Path
    content: str
    
    @classmethod
    def load(cls, path: Path) -> "SourceFile":
        return cls(path=path, content=path.read_text(encoding="utf-8"))

@dataclass
class BuildConfiguration:
    optimization: str = "O0"
    target: str = "x86_64"
    entry: str = "lala.main"

@dataclass
class Package:
    name: str
    version: str
    dependencies: Dict[str, str] = field(default_factory=dict)
    
@dataclass
class Project:
    root_dir: Path
    package: Package
    build_config: BuildConfiguration
    source_files: List[SourceFile] = field(default_factory=list)

@dataclass
class Workspace:
    root_dir: Path
    projects: List[Project] = field(default_factory=list)
