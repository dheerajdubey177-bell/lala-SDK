class Symbol:
    def __init__(self, name: str):
        self.name = name

class VariableSymbol(Symbol):
    def __init__(self, name: str, is_parameter: bool = False):
        super().__init__(name)
        self.is_parameter = is_parameter
        self.resolved_type = None  # Populated in Type Resolution (8.2)

class FunctionSymbol(Symbol):
    def __init__(self, name: str):
        super().__init__(name)
        self.parameters = []
        self.return_type = None

class ClassSymbol(Symbol):
    pass

class InterfaceSymbol(Symbol):
    pass

class ModuleSymbol(Symbol):
    def __init__(self, name: str):
        super().__init__(name)
        self.scope = None # The module's inner scope

class Scope:
    def __init__(self, parent=None, name="<anonymous>"):
        self.parent: Scope | None = parent
        self.name: str = name
        self.symbols: dict[str, Symbol] = {}
        self.children: list[Scope] = []
        if parent:
            parent.children.append(self)

    def define(self, symbol: Symbol) -> bool:
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True

    def resolve(self, name: str, current_only: bool = False) -> Symbol | None:
        if name in self.symbols:
            return self.symbols[name]
        if current_only or not self.parent:
            return None
        return self.parent.resolve(name)
