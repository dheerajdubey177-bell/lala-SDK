class CompilerContext:
    def __init__(self):
        # Configuration
        self.source_code = ""
        self.source_file = ""
        self.options = {}

        # Pipeline data
        self.tokens = []
        self.ast = None
        self.hir = None
        self.lir = None
        
        # Semantic data (Tables)
        self.symbol_table = None
        self.type_table = None
        
        # Diagnostics
        self.diagnostics = None # Will point to DiagnosticsReporter
