import sys
import os
import glob
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.ast.printer import ASTPrinter
from compiler.ast.validator import ASTValidator

def run_parser_tests():
    test_dir = Path(__file__).parent / "parser"
    lala_files = glob.glob(str(test_dir / "*.lala"))
    
    passed = 0
    failed = 0

    for lala_file in lala_files:
        base_path = os.path.splitext(lala_file)[0]
        ast_file = base_path + ".ast"
        
        print(f"Testing {os.path.basename(lala_file)}...")
        
        if not os.path.exists(ast_file):
            print(f"  [ERROR] Missing expected .ast file for {lala_file}")
            failed += 1
            continue
            
        with open(lala_file, 'r', encoding='utf-8') as f:
            source = f.read()
            
        with open(ast_file, 'r', encoding='utf-8') as f:
            expected_ast = f.read().strip()
            
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            parser = Parser(tokens, os.path.basename(lala_file))
            ast = parser.parse()
            
            # Validate AST invariants
            validator = ASTValidator()
            validator.validate(ast)
            
            # Print AST
            printer = ASTPrinter()
            actual_ast = printer.print(ast).strip()
            
            if actual_ast == expected_ast:
                print("  [PASS] AST matches")
                passed += 1
            else:
                print("  [FAIL] AST mismatch")
                print("--- Expected ---")
                print(expected_ast)
                print("--- Actual ---")
                print(actual_ast)
                print("----------------")
                failed += 1
                
        except Exception as e:
            print(f"  [FAIL] Compilation error: {e}")
            failed += 1
            
    print(f"\nParser Tests: {passed} passed, {failed} failed.")
    return failed == 0

if __name__ == "__main__":
    success = run_parser_tests()
    sys.exit(0 if success else 1)
