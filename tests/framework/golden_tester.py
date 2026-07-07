import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add the project root to sys.path so we can import compiler
sys.path.insert(0, str(Path(__file__).parent.parent.parent.absolute()))

from compiler.context import CompilationContext
from compiler.session import CompilerSession
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.semantics.name_resolution import NameResolutionVisitor
from compiler.semantics.type_checker import TypeCheckingVisitor
from compiler.semantics.bound_tree_builder import BoundTreeBuilder
from compiler.hir.builder import HIRBuilder
from compiler.mir.lowering import HIRLoweringPass
from compiler.backend.allocator.pmir_builder import PMIRBuilder
from compiler.backend.x86_64.selector import InstructionSelector
from compiler.backend.x86_64.printer import IntelAssemblyPrinter
from compiler.backend.x86_64.validator import MachineValidator
from compiler.backend.target import TargetBackend
from compiler.backend.reference_target import ReferenceTarget
from compiler.backend.allocator.liveness import LivenessAnalyzer
from compiler.backend.allocator.intervals import IntervalBuilder
from compiler.backend.allocator.linear_scan import LinearScanAllocator, AllocationContext
from compiler.backend.allocator.spiller import SpillInsertionPass

def parse_metadata(path: Path) -> dict:
    meta = {"name": "test", "architecture": "x86_64", "optimization": "O0", "exit_code": 0}
    if not path.exists():
        return meta
    
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"')
                if key == "exit_code":
                    meta[key] = int(val)
                else:
                    meta[key] = val
    return meta

from compiler.context import CompilationContext
from compiler.session import CompilerSession

def compile_to_asm(source_code: str) -> str:
    session = CompilerSession()
    context = CompilationContext(session, "<memory>")
    
    # 1. Lex
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    # 2. Parse
    parser = Parser(tokens, "<memory>")
    ast = parser.parse()
    
    if context.diagnostics.has_errors():
        return "ERROR: " + str(context.diagnostics.diagnostics), b''
        
    # 3. Semantics
    NameResolutionVisitor(context).resolve(ast)
    TypeCheckingVisitor(context).check(ast)
    bound_ast = BoundTreeBuilder(context).build(ast)
    
    if context.diagnostics.has_errors():
        return "ERROR: " + str(context.diagnostics.diagnostics), b''
        
    # 4. HIR
    hir_prog = HIRBuilder(context).build(bound_ast)
    
    # 5. MIR
    mir_prog = HIRLoweringPass().lower(hir_prog)
    
    # 6. PMIR
    from compiler.backend.x86_64.target import X86_64Target
    target = X86_64Target()
    
    pmir_prog = type(mir_prog)() # empty program to hold pmir functions
    pmir_prog.functions = []
    
    for mir_func in mir_prog.functions:
        liveness_res = LivenessAnalyzer().analyze(mir_func)
        intervals = IntervalBuilder().build(mir_func, liveness_res)
        
        alloc_ctx = AllocationContext(target, liveness_res, intervals)
        LinearScanAllocator().allocate(alloc_ctx)
        
        spilled_func = SpillInsertionPass(alloc_ctx).run(mir_func)
        pmir_func = PMIRBuilder(alloc_ctx).build(spilled_func)
        pmir_prog.functions.append(pmir_func)
    
    # 7. Machine IR & ASM
    selector = InstructionSelector(target)
    validator = MachineValidator()
    printer = IntelAssemblyPrinter()
    
    from compiler.backend.x86_64.encoder import MachineEncoder
    from compiler.backend.x86_64.machine_ir import MachineProgram
    from compiler.backend.x86_64.object_builder import ObjectBuilder
    from compiler.object.elf.writer import ELFWriter
    from compiler.object.validator import ObjectValidator
    
    encoder = MachineEncoder()
    builder = ObjectBuilder()
    obj_validator = ObjectValidator()
    elf_writer = ELFWriter()
    
    mprog = MachineProgram(functions=[])
    asm_parts = []
    for pmir_func in pmir_prog.functions:
        mfunc = selector.select_function(pmir_func)
        validator.validate(mfunc)
        mprog.functions.append(mfunc)
        asm_parts.append(printer.print_function(mfunc))
        
    code_image = encoder.encode(mprog)
    obj = builder.build(code_image)
    obj_validator.validate(obj)
    elf_bytes = elf_writer.write_object(obj)
        
    return "\n\n".join(asm_parts), elf_bytes

def run_test(test_dir: Path, bless: bool):
    print(f"Running golden test: {test_dir.name}...", end=" ")
    
    input_file = test_dir / "input.lala"
    if not input_file.exists():
        print("SKIPPED (no input.lala)")
        return True
        
    meta = parse_metadata(test_dir / "metadata.toml")
    
    source = input_file.read_text(encoding="utf-8")
    
    # E2E Compile
    try:
        asm, elf_bytes = compile_to_asm(source)
    except Exception as e:
        print(f"FAILED (Compiler Exception: {e})")
        return False
        
    if asm.startswith("ERROR:"):
        print(f"FAILED ({asm})")
        return False
        
    asm_file = test_dir / "actual.s"
    with open(asm_file, "w") as f:
        f.write(asm)
        
    obj_file = test_dir / "actual.o"
    with open(obj_file, "wb") as f:
        f.write(elf_bytes)
        
    # Execute Oracle (assemble and run)
    exe_file = test_dir / "program.exe"
    
    from compiler.driver.link_driver import LinkDriver
    driver = LinkDriver()
    
    if not driver.has_linker():
        print("SKIPPED (No compatible linker detected)")
        # Still write bless files for object and asm
        if bless:
            (test_dir / "expected.asm").write_text(asm)
            (test_dir / "expected.o").write_bytes(elf_bytes)
        return True

    try:
        driver.link([str(obj_file)], [], str(exe_file))
        
        # Run
        res = subprocess.run([str(exe_file)], capture_output=True, text=True)
        
        # Compare exit code
        if res.returncode != meta["exit_code"]:
            print(f"FAILED (Exit code {res.returncode} != expected {meta['exit_code']})")
            return False
            
        # If bless, write outputs
        if bless:
            (test_dir / "expected.asm").write_text(asm)
            (test_dir / "expected.o").write_bytes(elf_bytes)
            (test_dir / "expected.stdout").write_text(res.stdout)
            (test_dir / "expected.stderr").write_text(res.stderr)
            
        print("PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED (Linking error: {e.stderr})")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bless", action="store_true", help="Update expected files")
    args = parser.parse_args()
    
    golden_dir = Path("tests/golden")
    if not golden_dir.exists():
        print("No tests found.")
        return
        
    failures = 0
    for root, dirs, files in os.walk(golden_dir):
        root_path = Path(root)
        if "input.lala" in files:
            success = run_test(root_path, args.bless)
            if not success:
                failures += 1
                
    if failures > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
