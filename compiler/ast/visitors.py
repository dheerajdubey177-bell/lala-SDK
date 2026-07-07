from .base import Node

class Visitor:
    def visit(self, node: Node):
        if node is None:
            return None
        method_name = f"visit_{node.__class__.__name__}"
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    def generic_visit(self, node: Node):
        raise NotImplementedError(f"No visit_{node.__class__.__name__} method defined in {self.__class__.__name__}")
