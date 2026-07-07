from .base import Node, Span, NodeKind
from .statements import Statement
from .expressions import Expression

class Declaration(Statement):
    pass

class FunctionDecl(Declaration):
    def __init__(self, span: Span, name: str, params: list[tuple[str|None, str]], return_type: str | None, body: list[Statement]):
        super().__init__(span, NodeKind.FUNCTION_DECL)
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body

class ClassDecl(Declaration):
    def __init__(self, span: Span, name: str, body: list[Statement]):
        super().__init__(span, NodeKind.CLASS_DECL)
        self.name = name
        self.body = body

class InterfaceDecl(Declaration):
    def __init__(self, span: Span, name: str, body: list[Statement]):
        super().__init__(span, NodeKind.INTERFACE_DECL)
        self.name = name
        self.body = body

class ImportDecl(Declaration):
    def __init__(self, span: Span, module_path: str, alias: str | None):
        super().__init__(span, NodeKind.IMPORT_DECL)
        self.module_path = module_path
        self.alias = alias

class VariableDecl(Declaration):
    def __init__(self, span: Span, type_name: str | None, name: str, value: Expression | None):
        super().__init__(span, NodeKind.VARIABLE_DECL)
        self.type_name = type_name
        self.name = name
        self.value = value
