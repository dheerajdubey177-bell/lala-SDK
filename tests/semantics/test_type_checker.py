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

def test_type_checker():
    source = """
kaam main():
    number age = 20
    age = "hello"  # Should fail LALA3001
    
    agar 25:       # Should fail LALA3001
        age = age + 1

    number val = 5 + "abc" # Should fail LALA3001
"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, "test_types.lala")
    ast = parser.parse()
    
    session = CompilerSession()
    context = CompilationContext(session, "test_types.lala")
    
    name_res = NameResolutionVisitor(context)
    name_res.resolve(ast)
    
    type_res = TypeResolutionVisitor(context)
    type_res.resolve(ast)
    
    type_check = TypeCheckingVisitor(context)
    type_check.check(ast)
    
    print("Diagnostics:")
    context.diagnostics.print_all()
    
if __name__ == "__main__":
    test_type_checker()
