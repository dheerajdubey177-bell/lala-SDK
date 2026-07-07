import os
import hashlib
import json
from collections import defaultdict
from compiler.context import CompilerContext
from compiler.api import build_ast, analyze, build_hir, optimize, generate_backend
from compiler.backend.cpp_backend import CppBackend

class BuildManager:
    def __init__(self, project_root):
        self.project_root = project_root
        self.cache_dir = os.path.join(project_root, ".lala_cache")
        self.src_dir = os.path.join(project_root, "src")
        
        self.env_metadata = {
            "compiler": "0.5.0",
            "language": "0.5",
            "optimization": "debug",
            "backend": "cpp"
        }
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
    def compute_cache_key(self, source_code):
        hasher = hashlib.sha256()
        hasher.update(source_code.encode('utf-8'))
        hasher.update(json.dumps(self.env_metadata, sort_keys=True).encode('utf-8'))
        return hasher.hexdigest()
        
    def resolve_module_path(self, module_name):
        # Convert e.g. "math" to "src/math.lala" or "math/main.lala"
        parts = module_name.split(".")
        base_path = os.path.join(self.src_dir, *parts)
        if os.path.exists(base_path + ".lala"):
            return base_path + ".lala"
        elif os.path.isdir(base_path) and os.path.exists(os.path.join(base_path, "main.lala")):
            return os.path.join(base_path, "main.lala")
        return None

    def parse_file(self, file_path):
        with open(file_path, "r") as f:
            source_code = f.read()
            
        return build_ast(source_code, file_path)

    def get_imports(self, ast):
        imports = []
        from compiler.frontend.ast import ImportNode
        for stmt in ast.statements:
            if isinstance(stmt, ImportNode):
                imports.append(stmt.module_path)
        return imports

    def build_project(self, entry_file="src/main.lala"):
        entry_path = os.path.join(self.project_root, entry_file)
        if not os.path.exists(entry_path):
            print(f"Error: Entry file {entry_path} not found.")
            return False
            
        # 1. Parse and build dependency graph
        parsed_contexts = {}
        visited = set()
        stack = [entry_path]
        graph = defaultdict(list)
        
        while stack:
            curr_path = stack.pop()
            if curr_path in visited:
                continue
            visited.add(curr_path)
            
            context = self.parse_file(curr_path)
            if context.diagnostics.has_errors():
                context.diagnostics.print_diagnostics()
                return False
                
            parsed_contexts[curr_path] = context
            imports = self.get_imports(context.ast)
            
            for imp in imports:
                imp_path = self.resolve_module_path(imp)
                if not imp_path:
                    print(f"Error: Module '{imp}' not found.")
                    return False
                graph[curr_path].append(imp_path)
                stack.append(imp_path)
                
        # 2. Topological sort
        topo_order = []
        temp_mark = set()
        perm_mark = set()
        
        def visit(n):
            if n in perm_mark:
                return True
            if n in temp_mark:
                print("Error: Dependency cycle detected!")
                return False
                
            temp_mark.add(n)
            for m in graph[n]:
                if not visit(m): return False
            temp_mark.remove(n)
            perm_mark.add(n)
            topo_order.append(n)
            return True
            
        if not visit(entry_path):
            return False
            
        print("Build Order:", topo_order)
        
        # 3. Semantic Passes & IR
        # (Mocking standard library modules for now)
        global_symbols = {} 
        
        for file_path in topo_order:
            context = parsed_contexts[file_path]
            print(f"Compiling {file_path}...")
            
            context = analyze(context)
            
            if context.diagnostics.has_errors():
                context.diagnostics.print_diagnostics()
                return False
                
            # TODO: Extract 'bahar' exports from this context and add to global_symbols
            
            # Backend for each file (just mocking for now, we usually link at the end)
            backend = CppBackend(context)
            cpp_code = backend.generate_program()
            
            build_dir = os.path.join(self.project_root, "build")
            if not os.path.exists(build_dir):
                os.makedirs(build_dir)
                
            base_name = os.path.basename(file_path).replace(".lala", "")
            cpp_file = os.path.join(build_dir, f"{base_name}_build.cpp")
            
            with open(cpp_file, "w") as f:
                f.write(cpp_code)
                
            # Compile with g++
            exe_file = os.path.join(build_dir, f"{base_name}.exe")
            sdk_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            raylib_inc = os.path.join(sdk_root, "sdk", "vendor", "raylib", "include")
            raylib_lib = os.path.join(sdk_root, "sdk", "vendor", "raylib", "lib")
            runtime_inc = os.path.join(sdk_root, "sdk", "runtime")
            
            gpp_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin\g++.exe")
            if not os.path.exists(gpp_path):
                gpp_path = "g++" # Fallback to PATH
                
            cmd = [
                gpp_path, cpp_file, "-o", exe_file,
                "-I", runtime_inc,
                "-I", raylib_inc,
                "-L", raylib_lib,
                "-lraylib", "-lgdi32", "-lwinmm"
            ]
            
            print(f"Executing: {' '.join(cmd)}")
            import subprocess
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print("g++ compilation failed:")
                print(result.stderr)
                return False
                
        print(f"Compilation complete.")
        return True
