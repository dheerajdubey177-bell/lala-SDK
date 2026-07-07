import sys
import ctypes
import os
from compiler.ast.visitors import Visitor
from compiler.ast import *

_raylib = None

class Color(ctypes.Structure):
    _fields_ = [("r", ctypes.c_ubyte), ("g", ctypes.c_ubyte), ("b", ctypes.c_ubyte), ("a", ctypes.c_ubyte)]

def get_raylib():
    global _raylib
    if _raylib: return _raylib
    
    paths = [
        os.path.join(os.path.dirname(sys.executable), "..", "raylib-5.0_win64_mingw-w64", "lib", "raylib.dll"),
        os.path.join(os.path.dirname(sys.executable), "raylib.dll"),
        os.path.join(os.path.dirname(__file__), "..", "..", "raylib-5.0_win64_mingw-w64", "lib", "raylib.dll")
    ]
    
    # Try finding raylib.dll in PATH or standard locations
    for p in paths:
        p = os.path.normpath(p)
        if os.path.exists(p):
            _raylib = ctypes.cdll.LoadLibrary(p)
            break
    
    if not _raylib:
        try:
            _raylib = ctypes.cdll.LoadLibrary("raylib.dll")
        except:
            raise RuntimeError("raylib.dll not found! Please extract raylib.zip")

    _raylib.InitWindow.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
    _raylib.WindowShouldClose.restype = ctypes.c_bool
    _raylib.ClearBackground.argtypes = [Color]
    _raylib.DrawText.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, Color]
    return _raylib

def _get_color(name):
    if name == "lala.RAYWHITE": return Color(245, 245, 245, 255)
    if name == "lala.DARKGRAY": return Color(80, 80, 80, 255)
    if name == "lala.RED": return Color(230, 41, 55, 255)
    if name == "lala.GREEN": return Color(0, 228, 48, 255)
    if name == "lala.BLUE": return Color(0, 121, 241, 255)
    if name == "lala.BLACK": return Color(0, 0, 0, 255)
    return Color(0,0,0,255)

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class Interpreter(Visitor):
    def __init__(self):
        self.globals = {}
        self.locals_stack = [{}]
        
    @property
    def current_env(self):
        return self.locals_stack[-1]
        
    def _set_var(self, name, value):
        for env in reversed(self.locals_stack):
            if name in env:
                env[name] = value
                return
        self.globals[name] = value
        
    def _get_var(self, name):
        for env in reversed(self.locals_stack):
            if name in env:
                return env[name]
        if name in self.globals:
            return self.globals[name]
        
        # Raylib Constants Fallback
        if name in ["RAYWHITE", "DARKGRAY", "RED", "BLUE", "GREEN", "BLACK", 
                    "lala.RAYWHITE", "lala.DARKGRAY", "lala.RED", "lala.BLUE", "lala.GREEN", "lala.BLACK"]:
            return name
            
        raise RuntimeError(f"Undefined variable '{name}'")
        
    def evaluate(self, ast: Program):
        self.visit(ast)
        
        if "main" in self.globals:
            try:
                self.globals["main"]()
            except ReturnException as e:
                return e.value
        return 0
        
    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.visit(stmt)
            
    def visit_ImportDecl(self, node: ImportDecl):
        pass
        
    def visit_FunctionDecl(self, node: FunctionDecl):
        def _callable(*args):
            self.locals_stack.append({})
            for (ptype, pname), arg in zip(node.params, args):
                self.current_env[pname] = arg
            try:
                for stmt in node.body:
                    self.visit(stmt)
            except ReturnException as r:
                return r.value
            finally:
                self.locals_stack.pop()
                
        self.globals[node.name] = _callable
        
    def visit_ExpressionStatement(self, node: ExpressionStatement):
        self.visit(node.expression)
        
    def visit_VariableDecl(self, node: VariableDecl):
        val = None
        if node.initializer:
            val = self.visit(node.initializer)
        self.current_env[node.name] = val
        
    def visit_AssignmentExpression(self, node: AssignmentExpression):
        val = self.visit(node.value)
        if isinstance(node.target, IdentifierExpression):
            self._set_var(node.target.name, val)
        return val
        
    def visit_BinaryExpression(self, node: BinaryExpression):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.operator.name
        
        if op == "ADD": return left + right
        if op == "SUB": return left - right
        if op == "MUL": return left * right
        if op == "DIV": return left / right
        if op == "MOD": return left % right
        if op == "EQ": return left == right
        if op == "NEQ": return left != right
        if op == "LT": return left < right
        if op == "LTE": return left <= right
        if op == "GT": return left > right
        if op == "GTE": return left >= right
        if op == "AND": return left and right
        if op == "OR": return left or right
        
        raise RuntimeError(f"Unsupported binary op {op}")
        
    def visit_IdentifierExpression(self, node: IdentifierExpression):
        if node.name == "print":
            return print
            
        if getattr(node, 'name', '').startswith("lala."):
            prop = node.name.split('.')[1]
            if prop == "print":
                return print
            elif prop == "banau_window":
                return lambda w,h,title: get_raylib().InitWindow(int(w), int(h), str(title).encode('utf-8'))
            elif prop == "window_khuli_hai":
                return lambda: not get_raylib().WindowShouldClose()
            elif prop == "shuru_drawing":
                return lambda: get_raylib().BeginDrawing()
            elif prop == "background":
                return lambda c: get_raylib().ClearBackground(_get_color(c))
            elif prop == "text_likho":
                return lambda t,x,y,s,c: get_raylib().DrawText(str(t).encode('utf-8'), int(x), int(y), int(s), _get_color(c))
            elif prop == "khatam_drawing":
                return lambda: get_raylib().EndDrawing()
            elif prop == "window_band_karo":
                return lambda: get_raylib().CloseWindow()
                
        return self._get_var(node.name)
        
    def visit_NumberLiteral(self, node: NumberLiteral):
        return node.value
        
    def visit_StringLiteral(self, node: StringLiteral):
        return node.value
        
    def visit_BoolLiteral(self, node: BoolLiteral):
        return node.value
        
    def visit_CallExpression(self, node: CallExpression):
        callee = self.visit(node.callee)
        args = [self.visit(a) for a in node.arguments]
        if callable(callee):
            return callee(*args)
        raise RuntimeError("Not callable")
        
    def visit_ReturnStatement(self, node: ReturnStatement):
        val = None
        if node.value:
            val = self.visit(node.value)
        raise ReturnException(val)
        
    def visit_IfStatement(self, node: IfStatement):
        if self.visit(node.condition):
            for stmt in node.body:
                self.visit(stmt)
            return
            
        for elif_cond, elif_body in node.elifs:
            if self.visit(elif_cond):
                for stmt in elif_body:
                    self.visit(stmt)
                return
                
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)
                
    def visit_WhileStatement(self, node: WhileStatement):
        while self.visit(node.condition):
            try:
                for stmt in node.body:
                    self.visit(stmt)
            except BreakException:
                break
            except ContinueException:
                continue

    def visit_MemberExpression(self, node: MemberExpression):
        obj = self.visit(node.object_expr)
        
        # Hack for print if user tries lala.print
        if isinstance(node.object_expr, IdentifierExpression) and node.object_expr.name == "lala":
            if node.property_name == "print":
                return print
            elif node.property_name == "banau_window":
                return lambda w,h,title: print(f"[RAYLIB STUB] banau_window({w}, {h}, '{title}')")
            elif node.property_name == "window_khuli_hai":
                if not hasattr(self, '_window_counter'):
                    self._window_counter = 0
                self._window_counter += 1
                return lambda: self._window_counter < 5
            elif node.property_name == "shuru_drawing":
                return lambda: None
            elif node.property_name == "background":
                return lambda c: None
            elif node.property_name == "text_likho":
                return lambda t,x,y,s,c: print(f"[RAYLIB STUB] Drawing text: {t}")
            elif node.property_name == "khatam_drawing":
                return lambda: None
            elif node.property_name == "window_band_karo":
                return lambda: print("[RAYLIB STUB] window_band_karo()")
                
        if hasattr(obj, node.property_name):
            return getattr(obj, node.property_name)
        raise RuntimeError(f"Unknown member {node.property_name}")
