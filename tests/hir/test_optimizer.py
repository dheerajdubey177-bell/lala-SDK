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
from compiler.hir.optimizer.pass_manager import OptimizationPipeline
from compiler.hir.optimizer.passes import ConstantFoldingPass, DeadCodeEliminationPass, UnreachableBlockRemovalPass, ConstantBranchFoldingPass, CFGSimplificationPass

def compile_and_optimize(source: str):
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
    
    print("--- UNOPTIMIZED HIR ---")
    print(HIRPrinter().format(hir_prog))
    
    pipeline = OptimizationPipeline(context)
    pipeline.add_pass(ConstantFoldingPass())
    pipeline.add_pass(ConstantBranchFoldingPass())
    pipeline.add_pass(CFGSimplificationPass())
    pipeline.add_pass(DeadCodeEliminationPass())
    pipeline.add_pass(UnreachableBlockRemovalPass())
    
    optimized_prog = pipeline.run(hir_prog)
    
    print("--- OPTIMIZED HIR ---")
    print(HIRPrinter().format(optimized_prog))

def test_optimizer():
    source = """
kaam void main():
    number x = 10 + 20 * 3  # Should fold to 70
    number y = x
    # DCE should remove x and y if we never use them!
    
    agar false:
        print(x) # Unreachable due to false constant (branch would be removed if we had full constant branch folding, but let's test DCE alone)
"""
    compile_and_optimize(source)

if __name__ == "__main__":
    test_optimizer()
