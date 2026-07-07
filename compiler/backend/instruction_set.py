from dataclasses import dataclass

@dataclass(frozen=True)
class InstructionSet:
    supports_add: bool = True
    supports_sub: bool = True
    supports_mul: bool = True
    supports_div: bool = True
    supports_remainder: bool = True
    supports_shifts: bool = True
    supports_compare: bool = True
    supports_conditional_move: bool = False
    supports_vector: bool = False
    supports_atomics: bool = False
    supports_fma: bool = False
