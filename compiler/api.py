from compiler.context import CompilerContext
from compiler.pass_manager import PassManager, CompilerPass
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.semantics.symbols import SymbolResolutionPass
from compiler.semantics.type_checker import TypeCheckingPass
from compiler.ir.builder import IRBuilderPass
from compiler.optimizer.pipeline import ConstantFoldingPass, DeadCodeEliminationPass
from compiler.backend.cpp_backend import CppBackend
from compiler.diagnostics.reporter import DiagnosticsReporter

class LexerPass(CompilerPass):
    def run(self, context):
        lexer = Lexer(context)
        lexer.tokenize()

class ParserPass(CompilerPass):
    def run(self, context):
        parser = Parser(context)
        context.ast = parser.parse()

def build_ast(source_code, file_path="<memory>"):
    context = CompilerContext()
    context.source_code = source_code
    context.source_file = file_path
    context.diagnostics = DiagnosticsReporter(context)
    
    pm = PassManager(context)
    pm.add_pass(LexerPass())
    pm.add_pass(ParserPass())
    pm.run_all()
    return context

def analyze(context):
    pm = PassManager(context)
    pm.add_pass(SymbolResolutionPass())
    pm.add_pass(TypeCheckingPass())
    pm.run_all()
    return context

def build_hir(context):
    pm = PassManager(context)
    pm.add_pass(IRBuilderPass())
    pm.run_all()
    return context

def optimize(context):
    pm = PassManager(context)
    pm.add_pass(ConstantFoldingPass())
    pm.add_pass(DeadCodeEliminationPass())
    pm.run_all()
    return context

def generate_backend(context):
    backend = CppBackend(context)
    return backend.generate_program()
