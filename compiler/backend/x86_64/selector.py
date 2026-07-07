from compiler.mir.core import (
    Function, StackSlot, ConstInstruction, MoveInstruction,
    BinaryInstruction, UnaryInstruction, CompareInstruction,
    LoadInstruction, StoreInstruction, BranchInstruction,
    ReturnInstruction, JumpInstruction, CallInstruction
)
from compiler.backend.register_file import PhysicalRegister
from .machine_ir import MachineFunction, MachineBlock, Immediate, MemoryOperand, LabelOperand, MachineOperand
from .addressing import Address
from .registers import ID_TO_REG, X86Register, RBP
from .builder import MachineBuilder

from compiler.backend.target import TargetBackend

class InstructionSelector:
    def __init__(self, target: TargetBackend):
        self.target = target
        
    def select_function(self, pmir_func: Function) -> MachineFunction:
        mfunc = MachineFunction(pmir_func.name, [])
        
        for block in pmir_func.blocks:
            mblock = MachineBlock(f".L{block.id.id}", [])
            builder = MachineBuilder(mblock)
            
            for instr in block.instructions:
                self._select_instruction(instr, builder)
                
            mfunc.blocks.append(mblock)
            
        return mfunc
        
    def _translate_operand(self, op: PhysicalRegister | StackSlot) -> MachineOperand:
        if isinstance(op, PhysicalRegister):
            if op.id not in ID_TO_REG:
                raise ValueError(f"Unknown physical register ID {op.id}")
            return ID_TO_REG[op.id]
        elif isinstance(op, StackSlot):
            # Map stack slot to [rbp - offset]
            # In a real compiler, StackModel determines exact offset. We'll approximate.
            offset = -8 * (op.id + 1)
            return MemoryOperand(Address(base=RBP, displacement=offset))
        return op
        
    def _select_instruction(self, instr, builder: MachineBuilder):
        if isinstance(instr, ConstInstruction):
            dst = self._translate_operand(instr.target)
            builder.mov(dst, Immediate(instr.value))
            
        elif isinstance(instr, MoveInstruction):
            dst = self._translate_operand(instr.target)
            src = self._translate_operand(instr.source)
            builder.mov(dst, src)
            
        elif isinstance(instr, BinaryInstruction):
            dst = self._translate_operand(instr.target)
            left = self._translate_operand(instr.left)
            right = self._translate_operand(instr.right)
            
            # x86 two-operand expansion: dst = left op right
            # MOV dst, left
            # OP dst, right
            if dst != left:
                builder.mov(dst, left)
                
            if instr.op == "add":
                builder.add(dst, right)
            elif instr.op == "sub":
                builder.sub(dst, right)
            elif instr.op == "mul":
                builder.imul(dst, right)
            else:
                raise NotImplementedError(f"Unsupported binary op: {instr.op}")
                
        elif isinstance(instr, CompareInstruction):
            dst = self._translate_operand(instr.target)
            left = self._translate_operand(instr.left)
            right = self._translate_operand(instr.right)
            
            # CMP left, right
            # SETcc dst (approximated here, ideally we'd use AL or similar, but keeping it simple)
            # Actually, we should probably just emit the CMP here and wait for Branch Instruction?
            # For this basic mock, let's assume we do CMP left, right, and then Branch handles it.
            builder.cmp(left, right)
            # A real selector would emit SETcc into dst, but for now we'll just emit CMP 
            # and assume the next instruction is the branch checking dst.
            
        elif isinstance(instr, LoadInstruction):
            dst = self._translate_operand(instr.target)
            src = self._translate_operand(instr.source_ptr)
            builder.mov(dst, src) # If src is StackSlot, this moves Memory -> Reg
            
        elif isinstance(instr, StoreInstruction):
            dst = self._translate_operand(instr.target_ptr)
            src = self._translate_operand(instr.source)
            builder.mov(dst, src) # Memory <- Reg
            
        elif isinstance(instr, JumpInstruction):
            builder.jmp(f".L{instr.target_block.id}")
            
        elif isinstance(instr, BranchInstruction):
            # In our simple MIR, branch relies on a previous compare setting a boolean.
            # In x86, we usually fuse CMP + Jcc. 
            # For this MVP, we'll just emit JNE assuming we tested truthiness.
            # A more robust selector merges CompareInstruction + BranchInstruction.
            builder.jne(f".L{instr.true_block.id}")
            builder.jmp(f".L{instr.false_block.id}")
            
        elif isinstance(instr, CallInstruction):
            builder.call(LabelOperand(instr.func_name))
            
        elif isinstance(instr, ReturnInstruction):
            if instr.value is not None:
                src = self._translate_operand(instr.value)
                # Query ABI
                ret_loc = self.target.calling_convention().how_is_returned(None) # type doesn't matter for now
                from compiler.backend.calling_convention import ReturnedInRegister
                if isinstance(ret_loc, ReturnedInRegister):
                    # We need the X86Register corresponding to the backend physical register
                    ret_x86_reg = ID_TO_REG[ret_loc.register.id]
                    builder.mov(ret_x86_reg, src)
                else:
                    raise NotImplementedError("Only register returns are supported for now")
                    
            builder.ret()
            
        elif instr.__class__.__name__ == "GetRetvalInstruction":
            dst = self._translate_operand(instr.target)
            ret_loc = self.target.calling_convention().how_is_returned(None)
            from compiler.backend.calling_convention import ReturnedInRegister
            if isinstance(ret_loc, ReturnedInRegister):
                ret_x86_reg = ID_TO_REG[ret_loc.register.id]
                builder.mov(dst, ret_x86_reg)
                
        else:
            # We skip SetArg for this minimal pass, assuming ABI handles it
            pass
