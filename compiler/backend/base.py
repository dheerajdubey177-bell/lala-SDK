class Backend:
    def __init__(self, context):
        self.context = context
        self.output = []

    def emit(self, code):
        self.output.append(code)

    def generate_program(self):
        raise NotImplementedError()
        
    def generate_function(self, func_ir):
        raise NotImplementedError()
        
    def generate_block(self, block_ir):
        raise NotImplementedError()
        
    def generate_instruction(self, instr_ir):
        raise NotImplementedError()
