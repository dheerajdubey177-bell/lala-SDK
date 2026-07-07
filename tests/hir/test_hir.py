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
from compiler.hir.builder import HIRBuilder
from compiler.hir.printer import HIRPrinter
from compiler.hir.validator import HIRValidator

def compile_to_hir(source: str):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, "test.lala")
    ast = parser.parse()
    
    session = CompilerSession()
    context = CompilationContext(session, "test.lala")
    
    NameResolutionVisitor(context).resolve(ast)
    TypeResolutionVisitor(context).resolve(ast)
    TypeCheckingVisitor(context).check(ast)
    
    bound_ast = BoundTreeBuilder(context).build(ast)
    
    hir_prog = HIRBuilder(context).build(bound_ast)
    HIRValidator().validate(hir_prog)
    
    return HIRPrinter().format(hir_prog)

def test_hir_if_else():
    source = """
kaam void main():
    number age = 20
    agar age > 18:
        print(age)
    warna:
        print(0)
"""
    print(compile_to_hir(source))

if __name__ == "__main__":
    test_hir_if_else()
