from typing import Dict, Set

class DependencyGraph:
    """
    Tracks relationships between documents to enable incremental cache invalidation.
    For example, if A imports B, and B changes, A's semantic cache must be invalidated.
    """
    def __init__(self):
        # Maps a URI to the set of URIs that depend on it
        self._dependents: Dict[str, Set[str]] = {}
        # Maps a URI to the set of URIs it depends on
        self._dependencies: Dict[str, Set[str]] = {}

    def add_dependency(self, source_uri: str, target_uri: str):
        """Records that source_uri depends on target_uri."""
        if source_uri not in self._dependencies:
            self._dependencies[source_uri] = set()
        self._dependencies[source_uri].add(target_uri)
        
        if target_uri not in self._dependents:
            self._dependents[target_uri] = set()
        self._dependents[target_uri].add(source_uri)

    def get_affected_documents(self, uri: str) -> Set[str]:
        """Returns all documents that transitively depend on this URI."""
        affected = set()
        queue = [uri]
        
        while queue:
            current = queue.pop(0)
            deps = self._dependents.get(current, set())
            for dep in deps:
                if dep not in affected:
                    affected.add(dep)
                    queue.append(dep)
                    
        return affected
