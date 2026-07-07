class ConstantFoldingPass:
    def run(self, context):
        if not context.lir:
            return
            
        for func in context.lir.functions:
            for block in func.blocks:
                new_instrs = []
                for instr in block.instructions:
                    # Very simple folding: if it's a BINARY_OP with two constant operands
                    if instr.opcode == "BINARY_OP":
                        op = instr.operands[0].value
                        left = instr.operands[1]
                        right = instr.operands[2]
                        if not left.is_var and not right.is_var:
                            try:
                                if op == "+":
                                    val = float(left.value) + float(right.value)
                                elif op == "-":
                                    val = float(left.value) - float(right.value)
                                elif op == "*":
                                    val = float(left.value) * float(right.value)
                                elif op == "/":
                                    val = float(left.value) / float(right.value)
                                else:
                                    new_instrs.append(instr)
                                    continue
                                    
                                if val.is_integer():
                                    val = int(val)
                                    
                                from compiler.ir.lir import LIRInstruction, Operand
                                new_instrs.append(LIRInstruction("LOAD_CONST", [Operand(str(val))], dest=instr.dest))
                                continue
                            except:
                                pass
                    new_instrs.append(instr)
                block.instructions = new_instrs

class DeadCodeEliminationPass:
    def run(self, context):
        if not context.lir:
            return
            
        for func in context.lir.functions:
            for block in func.blocks:
                new_instrs = []
                terminated = False
                for instr in block.instructions:
                    if terminated:
                        break # Dead code after JUMP/RETURN
                    new_instrs.append(instr)
                    if instr.opcode in ("JUMP", "RETURN"):
                        terminated = True
                block.instructions = new_instrs
