from compiler.ast.base import BinaryOperator, UnaryOperator
from .types import Type, PrimitiveType, UnknownType, TypeRegistry

class TypeSystem:
    def __init__(self, registry: TypeRegistry):
        self.registry = registry

    def is_assignable(self, target_type: Type, value_type: Type) -> bool:
        if isinstance(target_type, UnknownType) or isinstance(value_type, UnknownType):
            return True # Assume OK to prevent cascading errors
        
        # Exact match for now
        return target_type is value_type

    def binary_result(self, op: BinaryOperator, left: Type, right: Type) -> Type | None:
        if isinstance(left, UnknownType) or isinstance(right, UnknownType):
            return self.registry.UNKNOWN

        if left is self.registry.NUMBER and right is self.registry.NUMBER:
            if op in [BinaryOperator.ADD, BinaryOperator.SUB, BinaryOperator.MUL, BinaryOperator.DIV, BinaryOperator.MOD]:
                return self.registry.NUMBER
            if op in [BinaryOperator.LT, BinaryOperator.LTE, BinaryOperator.GT, BinaryOperator.GTE, BinaryOperator.EQ, BinaryOperator.NEQ]:
                return self.registry.BOOL
                
        if left is self.registry.STRING and right is self.registry.STRING:
            if op == BinaryOperator.ADD:
                return self.registry.STRING
            if op in [BinaryOperator.EQ, BinaryOperator.NEQ]:
                return self.registry.BOOL
                
        if left is self.registry.BOOL and right is self.registry.BOOL:
            if op in [BinaryOperator.AND, BinaryOperator.OR, BinaryOperator.EQ, BinaryOperator.NEQ]:
                return self.registry.BOOL
                
        return None

    def unary_result(self, op: UnaryOperator, operand: Type) -> Type | None:
        if isinstance(operand, UnknownType):
            return self.registry.UNKNOWN
            
        if op == UnaryOperator.NEGATE and operand is self.registry.NUMBER:
            return self.registry.NUMBER
            
        if op == UnaryOperator.NOT and operand is self.registry.BOOL:
            return self.registry.BOOL
            
        return None
