from .diagnostics.reporter import DiagnosticReporter
from .semantics.types import TypeRegistry
from .semantics.intrinsics import IntrinsicRegistry
import time

class CompilerSession:
    def __init__(self):
        self.diagnostics = DiagnosticReporter()
        self.type_registry = TypeRegistry()
        self.intrinsic_registry = IntrinsicRegistry()
        self.runtime_manifests = {} # Lazy loaded
        
        # Statistics
        self.files_compiled = 0
        self.start_time = time.time()
        
    def get_runtime_manifest(self, module_name: str) -> dict | None:
        if module_name in self.runtime_manifests:
            return self.runtime_manifests[module_name]
            
        import os, json
        manifest_path = os.path.join(os.path.dirname(__file__), "..", "runtime", f"{module_name}.json")
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                    self.runtime_manifests[module_name] = manifest
                    return manifest
            except Exception as e:
                return None
        return None
