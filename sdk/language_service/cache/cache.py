from typing import Optional, Dict

class WorkspaceCache:
    """
    Manages granular caches for parsed and semantic artifacts.
    Provides targeted invalidation to minimize recomputation.
    """
    def __init__(self):
        # We index by document URI
        self._parse_cache: Dict[str, object] = {}
        self._semantic_cache: Dict[str, object] = {}
        self._hir_cache: Dict[str, object] = {}
        self._doc_cache: Dict[str, object] = {}
        self._diag_cache: Dict[str, list] = {}
        
    def invalidate_document(self, uri: str):
        """Invalidates all cached artifacts for a specific document."""
        self._parse_cache.pop(uri, None)
        self._semantic_cache.pop(uri, None)
        self._hir_cache.pop(uri, None)
        self._doc_cache.pop(uri, None)
        self._diag_cache.pop(uri, None)

    # Example granular getters/setters
    def get_ast(self, uri: str) -> Optional[object]:
        return self._parse_cache.get(uri)
        
    def set_ast(self, uri: str, ast: object):
        self._parse_cache[uri] = ast
        
    def get_diagnostics(self, uri: str) -> Optional[list]:
        return self._diag_cache.get(uri)
        
    def set_diagnostics(self, uri: str, diags: list):
        self._diag_cache[uri] = diags
