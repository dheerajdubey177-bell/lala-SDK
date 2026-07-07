# ELF Magic Header
EI_MAG0 = 0x7F
EI_MAG1 = ord('E')
EI_MAG2 = ord('L')
EI_MAG3 = ord('F')

ELFCLASS64 = 2
ELFDATA2LSB = 1
EV_CURRENT = 1

# Object file type
ET_REL = 1

# Machine architecture
EM_X86_64 = 62

# Section Header Types
SHT_NULL = 0
SHT_PROGBITS = 1
SHT_SYMTAB = 2
SHT_STRTAB = 3
SHT_RELA = 4

# Section Flags
SHF_WRITE = 0x1
SHF_ALLOC = 0x2
SHF_EXECINSTR = 0x4
SHF_INFO_LINK = 0x40

# Symbol Bindings
STB_LOCAL = 0
STB_GLOBAL = 1
STB_WEAK = 2

# Symbol Types
STT_NOTYPE = 0
STT_OBJECT = 1
STT_FUNC = 2
STT_SECTION = 3

# Symbol Visibility
STV_DEFAULT = 0

# Special Section Indices
SHN_UNDEF = 0
SHN_ABS = 0xfff1
SHN_COMMON = 0xfff2

# X86-64 Relocation Types
R_X86_64_NONE = 0
R_X86_64_64 = 1
R_X86_64_PC32 = 2
R_X86_64_PLT32 = 4
