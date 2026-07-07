from typing import Dict, Optional, List
from pathlib import Path
from sdk.project.model import Project

class WorkspaceSession:
    """
    A short-lived, immutable view of the workspace for a given operation.
    Provides isolated state to ensure thread safety across LanguageService requests.
    """
    def __init__(self, projects: Dict[str, Project]):
        self.projects = projects

class Workspace:
    """
    The central, stateful registry of the user's workspace.
    Owns Projects, Packages, DocumentManager, SymbolIndex, DependencyGraph, and Caches.
    """
    def __init__(self, root_uri: str):
        self.root_uri = root_uri
        self._projects: Dict[str, Project] = {}
        
        from sdk.language_service.workspace.document import DocumentManager
        self.document_manager = DocumentManager()
        
        from sdk.language_service.cache.cache import WorkspaceCache
        self.cache = WorkspaceCache()
        
        from sdk.language_service.workspace.graph import DependencyGraph
        self.dependency_graph = DependencyGraph()
        
        from sdk.language_service.symbols.index import SymbolIndex
        self.symbol_index = SymbolIndex()
        
    def add_project(self, name: str, project: Project):
        self._projects[name] = project
        
    def snapshot(self) -> WorkspaceSession:
        """Returns an immutable session capturing the current state."""
        return WorkspaceSession(projects=dict(self._projects))

class WorkspaceBuilder:
    """
    Constructs a full Workspace from a root URI, discovering projects and packages.
    """
    @staticmethod
    def build(root_uri: str) -> Workspace:
        workspace = Workspace(root_uri)
        # In a real implementation, this scans for lala.toml files and populates projects
        root_path = Path(root_uri.replace("file://", ""))
        if root_path.exists():
            try:
                from sdk.project.parser import ProjectParser
                project = ProjectParser.load(root_path)
                workspace.add_project(project.package.name, project)
            except Exception:
                pass
        return workspace
