from compiler.hir.core import Program
from compiler.context import CompilationContext
from compiler.hir.validator import HIRValidator

class OptimizationResult:
    def __init__(self, program: Program, changed: bool, stats: dict[str, int]):
        self.program = program
        self.changed = changed
        self.stats = stats

class OptimizationPass:
    def optimize(self, program: Program, context: CompilationContext) -> OptimizationResult:
        raise NotImplementedError()
        
    @property
    def name(self) -> str:
        return self.__class__.__name__

class OptimizationPipeline:
    def __init__(self, context: CompilationContext):
        self.context = context
        self.passes: list[OptimizationPass] = []
        self.validator = HIRValidator()
        self.max_iterations = 10
        
    def add_pass(self, opt_pass: OptimizationPass):
        self.passes.append(opt_pass)
        
    def run(self, program: Program) -> Program:
        current_program = program
        
        # We validate the initial unoptimized HIR just to be sure
        self.validator.validate(current_program)
        
        iteration = 0
        while iteration < self.max_iterations:
            any_changed = False
            
            for opt_pass in self.passes:
                result = opt_pass.optimize(current_program, self.context)
                
                if result.changed:
                    any_changed = True
                    current_program = result.program
                    
                    # Validate immediately after mutation to catch bugs early
                    try:
                        self.validator.validate(current_program)
                    except Exception as e:
                        raise RuntimeError(f"HIR Validation failed after {opt_pass.name}: {e}")
                        
                # Optional: collect or print stats
                # if result.stats:
                #     print(f"[{opt_pass.name}] {result.stats}")
                    
            if not any_changed:
                break
                
            iteration += 1
            
        return current_program
