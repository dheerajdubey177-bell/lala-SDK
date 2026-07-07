from dataclasses import dataclass
from enum import Enum, auto

class StackGrowthDirection(Enum):
    UP = auto()
    DOWN = auto()

@dataclass(frozen=True)
class StackModel:
    growth_direction: StackGrowthDirection = StackGrowthDirection.DOWN
    frame_alignment: int = 16
    spill_slot_alignment: int = 8
    
    # Red zone in bytes below the stack pointer that is safe from interrupt handlers
    red_zone_size: int = 0 
    
    # Shadow space reserved by caller for callee to spill register arguments
    shadow_space_size: int = 0
    
    # Frame layout policy describes the order of regions relative to the frame pointer
    # E.g. ["incoming_args", "saved_regs", "locals", "spills", "outgoing_args"]
    frame_layout_policy: tuple[str, ...] = (
        "incoming_args",
        "saved_regs",
        "locals",
        "spills",
        "outgoing_args"
    )
