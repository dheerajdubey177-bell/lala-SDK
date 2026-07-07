from compiler.hir import core as hir
from compiler.semantics.types import PrimitiveType
from .core import MachineType, BlockID
from .builder import MIRBuilder

class HIRLoweringPass:
    def __init__(self):
        self.builder = MIRBuilder()
        # map HIR ValueID to MIR VirtualRegister or StackSlot
        self.val_map = {}
        # map HIR BlockID to MIR BlockID
        self.block_map = {}
        
    def _map_type(self, type_obj) -> MachineType:
        if isinstance(type_obj, PrimitiveType):
            if type_obj.name == "number":
                return MachineType.I64 # Or F64, but let's stick to I64 for now
            elif type_obj.name == "bool":
                return MachineType.I1
            elif type_obj.name == "string":
                return MachineType.PTR
            elif type_obj.name == "void":
                return MachineType.PTR # shouldn't really be used as a value
        return MachineType.PTR

    def lower(self, program: hir.Program):
        for func in program.functions:
            self._lower_function(func)
        return self.builder.program

    def _lower_function(self, func: hir.Function):
        self.builder.start_function(func.name)
        self.val_map.clear()
        self.block_map.clear()
        
        # Pre-create blocks to handle forward jumps
        for block in func.blocks:
            self.block_map[block.id.id] = BlockID(block.id.id)
            
        for block in func.blocks:
            self.builder.start_block(self.block_map[block.id.id])
            for instr in block.instructions:
                self._lower_instruction(instr)
                
    def _lower_instruction(self, instr: hir.Instruction):
        if isinstance(instr, hir.Constant):
            t = self._map_type(instr.type)
            v = self.builder.const(t, instr.value)
            self.val_map[instr.target.id] = v
            
        elif isinstance(instr, hir.Allocate):
            # Allocate creates a stack slot
            slot = self.builder.alloc_stack_slot()
            self.val_map[instr.target.id] = slot
            
        elif isinstance(instr, hir.Store):
            # Target could be a StackSlot
            target_ptr = self.val_map[instr.target_ptr.id]
            source_val = self.val_map[instr.value.id]
            self.builder.store(target_ptr, source_val)
            
        elif isinstance(instr, hir.Load):
            t = self._map_type(instr.type)
            source_ptr = self.val_map[instr.source_ptr.id]
            v = self.builder.load(t, source_ptr)
            self.val_map[instr.target.id] = v
            
        elif isinstance(instr, hir.BinaryOp):
            left = self.val_map[instr.left.id]
            right = self.val_map[instr.right.id]
            
            # Map operator
            op = instr.op
            if op == "ADD": v = self.builder.add(left, right)
            elif op == "SUB": v = self.builder.sub(left, right)
            elif op == "MUL": v = self.builder.mul(left, right)
            elif op == "DIV": v = self.builder.div(left, right)
            elif op == "MOD": v = self.builder.rem(left, right)
            elif op == "AND": v = self.builder.bit_and(left, right)
            elif op == "OR": v = self.builder.bit_or(left, right)
            elif op == "EQ": v = self.builder.cmp_eq(left, right)
            elif op == "NEQ": v = self.builder.cmp_ne(left, right)
            elif op == "LT": v = self.builder.cmp_lt(left, right)
            elif op == "LTE": v = self.builder.cmp_le(left, right)
            elif op == "GT": v = self.builder.cmp_gt(left, right)
            elif op == "GTE": v = self.builder.cmp_ge(left, right)
            else:
                raise NotImplementedError(f"BinaryOp {op} not implemented")
            
            self.val_map[instr.target.id] = v
            
        elif isinstance(instr, hir.UnaryOp):
            operand = self.val_map[instr.operand.id]
            op = instr.op
            if op == "NOT": v = self.builder.bit_not(operand)
            elif op == "NEG":
                # Implement NEG as 0 - operand
                zero = self.builder.const(operand.type, 0)
                v = self.builder.sub(zero, operand)
            else:
                raise NotImplementedError(f"UnaryOp {op} not implemented")
            self.val_map[instr.target.id] = v
            
        elif isinstance(instr, hir.IntrinsicCall):
            for i, arg in enumerate(instr.args):
                self.builder.set_arg(i, self.val_map[arg.id])
            v = self.builder.call(f"intrinsic_{instr.intrinsic_id.name}", MachineType.I64 if instr.target else None)
            if instr.target and v:
                self.val_map[instr.target.id] = v
                
        elif isinstance(instr, hir.RuntimeCall):
            for i, arg in enumerate(instr.args):
                self.builder.set_arg(i, self.val_map[arg.id])
            v = self.builder.call(instr.func_name, self._map_type(instr.type) if instr.target else None)
            if instr.target and v:
                self.val_map[instr.target.id] = v
                
        elif isinstance(instr, hir.Call):
            for i, arg in enumerate(instr.arguments):
                self.builder.set_arg(i, self.val_map[arg.id])
            v = self.builder.call(instr.func_name, self._map_type(instr.type) if instr.target else None)
            if instr.target and v:
                self.val_map[instr.target.id] = v
                
        elif isinstance(instr, hir.Jump):
            self.builder.jmp(self.block_map[instr.target_block.id])
            
        elif isinstance(instr, hir.Branch):
            cond = self.val_map[instr.condition.id]
            self.builder.br(cond, self.block_map[instr.true_block.id], self.block_map[instr.false_block.id])
            
        elif isinstance(instr, hir.Return):
            if instr.value:
                self.builder.ret(self.val_map[instr.value.id])
            else:
                self.builder.ret()
        else:
            raise NotImplementedError(f"Lowering for {type(instr)} not implemented")
