from dataclasses import dataclass
from typing import Optional
from .registers import X86Register

@dataclass(frozen=True)
class Address:
    """Represents an x86 effective address: base + index*scale + displacement"""
    base: Optional[X86Register] = None
    index: Optional[X86Register] = None
    scale: int = 1 # 1, 2, 4, 8
    displacement: int = 0
    
    def __post_init__(self):
        assert self.scale in (1, 2, 4, 8), f"Invalid scale: {self.scale}"
        # A valid memory operand must have at least one of these
        assert self.base or self.index or self.displacement != 0, "Empty address"
        
    def __str__(self):
        parts = []
        if self.base: parts.append(self.base.name)
        if self.index: parts.append(f"{self.index.name}*{self.scale}")
        if self.displacement != 0:
            if self.displacement > 0 and parts:
                parts.append(f"+ {self.displacement}")
            else:
                parts.append(str(self.displacement))
        return f"[{''.join(parts)}]"
