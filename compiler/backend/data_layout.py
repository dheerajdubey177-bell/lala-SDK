from dataclasses import dataclass

@dataclass(frozen=True)
class DataLayout:
    endianness: str  # "little" or "big"
    pointer_size: int  # in bytes
    
    # Primitive sizes in bytes
    i8_size: int = 1
    i16_size: int = 2
    i32_size: int = 4
    i64_size: int = 8
    
    # Primitive alignments in bytes
    i8_align: int = 1
    i16_align: int = 2
    i32_align: int = 4
    i64_align: int = 8
    
    # Max natural alignment (e.g. 16 for some SIMD)
    max_natural_alignment: int = 8
    
    # Layout policies
    struct_layout_policy: str = "c_style"
    array_element_stride: str = "packed"
    
    # C-ABI representations
    enum_representation: str = "i32"
    boolean_representation: str = "i8"
    char_width: int = 4 # e.g. 4 for UTF-32, 1 for UTF-8
