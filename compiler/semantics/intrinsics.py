from enum import Enum, auto

class IntrinsicID(Enum):
    PRINT = auto()
    INPUT = auto()
    LEN = auto()
    TYPEOF = auto()

class RuntimeID(Enum):
    GRAPHICS_WINDOW = auto()
    GRAPHICS_CIRCLE = auto()
    GRAPHICS_BEGIN_DRAWING = auto()
    GRAPHICS_END_DRAWING = auto()
    GRAPHICS_CLEAR_BACKGROUND = auto()
    FILE_OPEN = auto()
    HTTP_GET = auto()
    AI_CHAT = auto()
    
class IntrinsicRegistry:
    def __init__(self):
        self.intrinsics = {
            "print": IntrinsicID.PRINT,
            "input": IntrinsicID.INPUT,
            "len": IntrinsicID.LEN,
            "typeof": IntrinsicID.TYPEOF
        }

    def resolve(self, name: str) -> IntrinsicID | None:
        return self.intrinsics.get(name)
