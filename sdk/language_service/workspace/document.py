from typing import Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class DocumentSnapshot:
    """
    An immutable snapshot of a document at a specific version.
    """
    uri: str
    content: str
    version: int
    
class Document:
    """
    Mutable state of a single document, producing immutable snapshots.
    """
    def __init__(self, uri: str, content: str, version: int):
        self._uri = uri
        self._content = content
        self._version = version
        self._dirty = False
        
    def update(self, content: str, version: int):
        self._content = content
        self._version = version
        self._dirty = True
        
    def snapshot(self) -> DocumentSnapshot:
        return DocumentSnapshot(self._uri, self._content, self._version)

class DocumentManager:
    """
    Manages text and snapshots of all open documents.
    Strictly handles text management; parsing is delegated elsewhere.
    """
    def __init__(self):
        self._documents: dict[str, Document] = {}
        
    def open(self, uri: str, content: str, version: int):
        self._documents[uri] = Document(uri, content, version)
        
    def close(self, uri: str):
        if uri in self._documents:
            del self._documents[uri]
            
    def update(self, uri: str, content: str, version: int):
        if uri in self._documents:
            self._documents[uri].update(content, version)
        else:
            self.open(uri, content, version)
            
    def snapshot(self, uri: str) -> Optional[DocumentSnapshot]:
        doc = self._documents.get(uri)
        return doc.snapshot() if doc else None
        
    def text(self, uri: str) -> Optional[str]:
        doc = self._documents.get(uri)
        return doc.snapshot().content if doc else None
        
    def version(self, uri: str) -> Optional[int]:
        doc = self._documents.get(uri)
        return doc.snapshot().version if doc else None
