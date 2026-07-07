from compiler.hir.core import *
from compiler.context import CompilationContext

class ConstantEvaluator:
    def __init__(self, context: CompilationContext):
        self.context = context
        
    def evaluate_binary(self, op: str, left_val, right_val, result_type: Type):
        try:
            if op == "ADD":
                return left_val + right_val
            elif op == "SUB":
                return left_val - right_val
            elif op == "MUL":
                return left_val * right_val
            elif op == "DIV":
                if right_val == 0:
                    return None # Cannot evaluate division by zero at compile time safely here
                return left_val / right_val
            elif op == "GT":
                return left_val > right_val
            elif op == "LT":
                return left_val < right_val
            elif op == "GTE":
                return left_val >= right_val
            elif op == "LTE":
                return left_val <= right_val
            elif op == "EQ":
                return left_val == right_val
            elif op == "NEQ":
                return left_val != right_val
            elif op == "AND":
                return left_val and right_val
            elif op == "OR":
                return left_val or right_val
        except Exception:
            return None
        return None
