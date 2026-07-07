from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SymbolLocation:
    uri: str
    line: int
    character: int

@dataclass
class Symbol:
    name: str
    kind: str # 'function', 'variable', 'type', 'module', etc.
    definition: SymbolLocation
    references: List[SymbolLocation]

class SymbolTable:
    """
    A local symbol table for a single file.
    """
    def __init__(self, uri: str):
        self.uri = uri
        self.symbols: Dict[str, Symbol] = {}

class SymbolIndex:
    """
    The global registry of all functions, variables, and types in the workspace.
    Supports incremental updates by replacing local file tables.
    """
    def __init__(self):
        # Index of symbols by URI (so we can quickly drop a file's symbols)
        self._file_tables: Dict[str, SymbolTable] = {}
        # Global lookup index (name -> list of Symbols)
        self._global_index: Dict[str, List[Symbol]] = {}
        
    def update_file(self, uri: str, table: SymbolTable):
        """
        Incrementally updates the global index by removing the old file's symbols 
        and inserting the new ones.
        """
        # Remove old symbols
        old_table = self._file_tables.get(uri)
        if old_table:
            for name, sym in old_table.symbols.items():
                if name in self._global_index:
                    self._global_index[name] = [s for s in self._global_index[name] if s.definition.uri != uri]
                    if not self._global_index[name]:
                        del self._global_index[name]
                        
        # Insert new symbols
        self._file_tables[uri] = table
        for name, sym in table.symbols.items():
            if name not in self._global_index:
                self._global_index[name] = []
            self._global_index[name].append(sym)
            
    def find_definition(self, name: str) -> Optional[SymbolLocation]:
        symbols = self._global_index.get(name, [])
        return symbols[0].definition if symbols else None
        
    def find_references(self, name: str) -> List[SymbolLocation]:
        symbols = self._global_index.get(name, [])
        refs = []
        for s in symbols:
            refs.extend(s.references)
        return refs
