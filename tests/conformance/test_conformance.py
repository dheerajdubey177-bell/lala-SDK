import sys
import os
import glob

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
from compiler.mir.lowering import HIRLoweringPass
from compiler.mir.validator import MIRValidator
from compiler.mir.printer import MIRPrinter
from compiler.mir.optimizer import MIROptimizationPipeline

def run_conformance_test(test_dir: str):
    print(f"Running conformance test: {test_dir}")
    
    with open(os.path.join(test_dir, "input.lala"), "r") as f:
        source = f.read()
        
    with open(os.path.join(test_dir, "expected.hir"), "r") as f:
        expected_hir = f.read().strip()
        
    with open(os.path.join(test_dir, "expected_O3.hir"), "r") as f:
        expected_o3 = f.read().strip()
        
    expected_mir_path = os.path.join(test_dir, "expected.mir")
    expected_mir = None
    if os.path.exists(expected_mir_path):
        with open(expected_mir_path, "r") as f:
            expected_mir = f.read().strip()
        
    # Compile to HIR
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, "input.lala")
    ast = parser.parse()
    
    session = CompilerSession()
    context = CompilationContext(session, "input.lala")
    
    NameResolutionVisitor(context).resolve(ast)
    TypeResolutionVisitor(context).resolve(ast)
    TypeCheckingVisitor(context).check(ast)
    
    bound_ast = BoundTreeBuilder(context).build(ast)
    hir_prog = HIRBuilder(context).build(bound_ast)
    
    actual_hir = HIRPrinter().format(hir_prog).strip()
    if actual_hir != expected_hir:
        print("[FAIL] Unoptimized HIR does not match expected")
        print("Expected:\n" + expected_hir)
        print("Actual:\n" + actual_hir)
        sys.exit(1)
        
    # Optimize
    pipeline = OptimizationPipeline(context)
    pipeline.add_pass(ConstantFoldingPass())
    pipeline.add_pass(ConstantBranchFoldingPass())
    pipeline.add_pass(DeadCodeEliminationPass())
    pipeline.add_pass(UnreachableBlockRemovalPass())
    
    optimized_prog = pipeline.run(hir_prog)
    actual_o3 = HIRPrinter().format(optimized_prog).strip()
    
    if actual_o3 != expected_o3:
        print("[FAIL] Optimized HIR does not match expected_O3")
        print("Expected:\n" + expected_o3)
        print("Actual:\n" + actual_o3)
        sys.exit(1)
        
    # MIR Lowering
    lowering = HIRLoweringPass()
    mir_prog = lowering.lower(optimized_prog)
    MIRValidator().validate(mir_prog)
    
    # MIR Optimization
    mir_optimizer = MIROptimizationPipeline()
    mir_optimized = mir_optimizer.run(mir_prog)
    MIRValidator().validate(mir_optimized)
    
    if expected_mir is not None:
        actual_mir = MIRPrinter().format(mir_prog).strip()
        if actual_mir != expected_mir:
            print("[FAIL] MIR does not match expected_mir")
            print("Expected:\n" + expected_mir)
            print("Actual:\n" + actual_mir)
            sys.exit(1)
            
    expected_o3_mir_path = os.path.join(test_dir, "expected_O3.mir")
    if os.path.exists(expected_o3_mir_path):
        with open(expected_o3_mir_path, "r") as f:
            expected_o3_mir = f.read().strip()
        actual_o3_mir = MIRPrinter().format(mir_optimized).strip()
        if actual_o3_mir != expected_o3_mir:
            print("[FAIL] Optimized MIR does not match expected_O3.mir")
            print("Expected:\n" + expected_o3_mir)
            print("Actual:\n" + actual_o3_mir)
            sys.exit(1)
    else:
        if expected_mir is None:
            print("--- MIR OUTPUT ---")
            print(MIRPrinter().format(mir_prog).strip())
        if not os.path.exists(expected_o3_mir_path):
            print("--- OPTIMIZED MIR OUTPUT ---")
            print(MIRPrinter().format(mir_optimized).strip())
        
    print(f"[PASS] {os.path.basename(test_dir)} passed.")

if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(__file__), "optimizer")
    for item in os.listdir(base_dir):
        test_dir = os.path.join(base_dir, item)
        if os.path.isdir(test_dir):
            run_conformance_test(test_dir)
