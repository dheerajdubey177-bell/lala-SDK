import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.session import CompilerSession
from compiler.context import CompilationContext
from compiler.semantics.name_resolution import NameResolutionVisitor
from compiler.semantics.type_resolution import TypeResolutionVisitor
from compiler.semantics.type_checker import TypeCheckingVisitor
from compiler.semantics.bound_tree_builder import BoundTreeBuilder
from compiler.semantics.cfa import ControlFlowAnalyzer

def test_cfa():
    source = """
kaam void test_reachability():
    print("hello")
    lautao
    print("unreachable")

kaam number test_missing_return():
    agar 1:
        lautao 1
    # Missing return on else path!
"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, "test_cfa.lala")
    ast = parser.parse()
    
    session = CompilerSession()
    context = CompilationContext(session, "test_cfa.lala")
    
    # 1. Semantic Pipeline
    NameResolutionVisitor(context).resolve(ast)
    TypeResolutionVisitor(context).resolve(ast)
    TypeCheckingVisitor(context).check(ast)
    
    # 2. Bound AST
    bound_ast = BoundTreeBuilder(context).build(ast)
    
    # 3. Control Flow Analysis
    ControlFlowAnalyzer(context).analyze(bound_ast)
    
    print("Diagnostics:")
    context.diagnostics.print_all()
    
if __name__ == "__main__":
    test_cfa()
