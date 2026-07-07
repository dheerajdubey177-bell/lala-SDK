import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.session import CompilerSession
from compiler.context import CompilationContext
from compiler.semantics.name_resolution import NameResolutionVisitor

def test_name_resolution():
    source = """
laao graphics

kaam main(age):
    number count = 0
    graphics.circle(count, age)
    print(count)
    print(unknown_var)
"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, "test.lala")
    ast = parser.parse()
    
    session = CompilerSession()
    context = CompilationContext(session, "test.lala")
    resolver = NameResolutionVisitor(context)
    resolver.resolve(ast)
    
    print("Diagnostics:")
    context.diagnostics.print_all()
    
    print("Resolved Symbols:")
    for node_id, sym in context.resolved_symbols.items():
        print(f"Node {node_id} -> {sym.__class__.__name__}('{sym.name}')")

if __name__ == "__main__":
    test_name_resolution()
