class CompilerPass:
    def run(self, context):
        raise NotImplementedError("Passes must implement run(context)")

class PassManager:
    def __init__(self, context):
        self.context = context
        self.passes = []

    def add_pass(self, compiler_pass):
        self.passes.append(compiler_pass)

    def run_all(self):
        for compiler_pass in self.passes:
            compiler_pass.run(self.context)
            if self.context.diagnostics and self.context.diagnostics.has_errors():
                break # Stop on errors
