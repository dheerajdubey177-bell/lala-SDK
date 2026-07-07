import struct
from compiler.object.object_file import ObjectFile
from compiler.object.section import SectionFlags
from compiler.object.symbol import SymbolBinding, SymbolKind
from compiler.object.relocation import RelocationKind
from . import constants

class StringTableBuilder:
    def __init__(self):
        self.data = bytearray(b'\x00')
        self.offsets = {"": 0}

    def add(self, s: str) -> int:
        if s in self.offsets:
            return self.offsets[s]
        offset = len(self.data)
        self.offsets[s] = offset
        self.data.extend(s.encode('utf-8'))
        self.data.append(0)
        return offset

    def get_bytes(self) -> bytes:
        return bytes(self.data)

class ELFWriter:
    def write_object(self, obj: ObjectFile) -> bytes:
        shstrtab = StringTableBuilder()
        strtab = StringTableBuilder()

        # Add section names to shstrtab
        shstrtab.add("")
        shstrtab.add(".symtab")
        shstrtab.add(".strtab")
        for sec in obj.sections:
            shstrtab.add(sec.name)
            
        rela_sections = {}
        for rel in obj.relocations:
            shstrtab.add(f".rela{rel.section}")
            rela_sections.setdefault(rel.section, []).append(rel)

        # 1. Gather all symbols, assign string table offsets, and build symtab
        # ELF requires all LOCAL symbols to precede GLOBAL symbols.
        # It also requires a NULL symbol at index 0.
        # But we'll just sort them: LOCAL first, then GLOBAL.
        sorted_symbols = []
        local_symbols = [s for s in obj.symbols if s.binding == SymbolBinding.LOCAL]
        global_symbols = [s for s in obj.symbols if s.binding == SymbolBinding.GLOBAL]
        
        # Determine section indices for symbols
        sec_name_to_idx = { sec.name: idx + 1 for idx, sec in enumerate(obj.sections) } # +1 because 0 is NULL section
        
        # Helper to pack Elf64_Sym
        def pack_sym(name_offset, info, other, shndx, value, size):
            return struct.pack("<IBBHQQ", name_offset, info, other, shndx, value, size)
            
        symtab_bytes = bytearray()
        symtab_bytes.extend(pack_sym(0, 0, 0, constants.SHN_UNDEF, 0, 0)) # NULL symbol
        
        sym_name_to_idx = {}
        sym_idx = 1
        
        # Write local section symbols first (useful for relocations against sections)
        # Often tools like `as` create STT_SECTION local symbols.
        # We will map them to ensure everything is perfect.
        for sec in obj.sections:
            idx = sec_name_to_idx[sec.name]
            info = (constants.STB_LOCAL << 4) | constants.STT_SECTION
            symtab_bytes.extend(pack_sym(0, info, constants.STV_DEFAULT, idx, 0, 0))
            sym_idx += 1
            
        local_sym_count = sym_idx
        
        for sym in global_symbols:
            name_off = strtab.add(sym.name)
            bind = constants.STB_GLOBAL
            
            if sym.kind == SymbolKind.FUNC:
                typ = constants.STT_FUNC
            elif sym.kind == SymbolKind.OBJECT:
                typ = constants.STT_OBJECT
            else:
                typ = constants.STT_NOTYPE
                
            info = (bind << 4) | typ
            
            if sym.section is None:
                shndx = constants.SHN_UNDEF
            else:
                shndx = sec_name_to_idx[sym.section]
                
            symtab_bytes.extend(pack_sym(name_off, info, constants.STV_DEFAULT, shndx, sym.offset, sym.size))
            sym_name_to_idx[sym.name] = sym_idx
            sym_idx += 1

        # 2. Build .rela sections
        # Elf64_Rela: r_offset(8), r_info(8), r_addend(8 signed)
        rela_section_bytes = {}
        for target_sec, rels in rela_sections.items():
            rbytes = bytearray()
            for rel in rels:
                if rel.symbol_name not in sym_name_to_idx:
                    raise Exception(f"Undefined symbol in relocation: {rel.symbol_name}")
                sym_index = sym_name_to_idx[rel.symbol_name]
                
                # Default to R_X86_64_PC32
                r_type = constants.R_X86_64_PC32 
                if rel.kind == RelocationKind.ABS64:
                    r_type = constants.R_X86_64_64
                    
                r_info = (sym_index << 32) | (r_type & 0xffffffff)
                rbytes.extend(struct.pack("<QQq", rel.offset, r_info, rel.addend))
            rela_section_bytes[f".rela{target_sec}"] = bytes(rbytes)

        # 3. Layout the file
        # The file starts with ELF Header (64 bytes).
        file_bytes = bytearray()
        
        # Reserve space for ELF Header
        file_bytes.extend(b'\x00' * 64)
        
        section_headers = []
        
        # Helper to record section header
        def record_shdr(name, type_, flags, addr, offset, size, link, info, addralign, entsize):
            section_headers.append(struct.pack("<IIQQQQIIQQ", shstrtab.add(name), type_, flags, addr, offset, size, link, info, addralign, entsize))
            
        # NULL Section (index 0)
        record_shdr("", constants.SHT_NULL, 0, 0, 0, 0, 0, 0, 0, 0)
        
        # Write actual sections
        for sec in obj.sections:
            flags = 0
            if SectionFlags.ALLOC in sec.flags: flags |= constants.SHF_ALLOC
            if SectionFlags.EXEC in sec.flags: flags |= constants.SHF_EXECINSTR
            if SectionFlags.WRITE in sec.flags: flags |= constants.SHF_WRITE
            
            # Align offset in file
            align = sec.alignment
            rem = len(file_bytes) % align
            if rem != 0:
                file_bytes.extend(b'\x00' * (align - rem))
                
            offset = len(file_bytes)
            file_bytes.extend(sec.bytes_data)
            record_shdr(sec.name, constants.SHT_PROGBITS, flags, 0, offset, len(sec.bytes_data), 0, 0, align, 0)
            
        # Write symtab
        align = 8
        rem = len(file_bytes) % align
        if rem != 0: file_bytes.extend(b'\x00' * (align - rem))
        symtab_offset = len(file_bytes)
        file_bytes.extend(symtab_bytes)
        # link = index of strtab, info = one greater than the symbol table index of the last local symbol
        strtab_idx = len(section_headers) + 2 + len(rela_section_bytes) # We will write .strtab later
        
        # Write rela sections
        for rsec_name, rbytes in rela_section_bytes.items():
            align = 8
            rem = len(file_bytes) % align
            if rem != 0: file_bytes.extend(b'\x00' * (align - rem))
            r_offset = len(file_bytes)
            file_bytes.extend(rbytes)
            # link = symtab index, info = target section index
            target_name = rsec_name[5:] # remove .rela
            target_idx = sec_name_to_idx[target_name]
            
            # The symtab index will be the next one we push
            symtab_header_idx = len(section_headers) 
            record_shdr(rsec_name, constants.SHT_RELA, constants.SHF_INFO_LINK, 0, r_offset, len(rbytes), symtab_header_idx, target_idx, 8, 24)

        # Record Symtab Header
        symtab_header_idx = len(section_headers)
        strtab_header_idx = symtab_header_idx + 1
        record_shdr(".symtab", constants.SHT_SYMTAB, 0, 0, symtab_offset, len(symtab_bytes), strtab_header_idx, local_sym_count, 8, 24)

        # Write strtab
        offset = len(file_bytes)
        file_bytes.extend(strtab.get_bytes())
        record_shdr(".strtab", constants.SHT_STRTAB, 0, 0, offset, len(strtab.get_bytes()), 0, 0, 1, 0)
        
        # Write shstrtab
        offset = len(file_bytes)
        file_bytes.extend(shstrtab.get_bytes())
        shstrtab_idx = len(section_headers)
        record_shdr(".shstrtab", constants.SHT_STRTAB, 0, 0, offset, len(shstrtab.get_bytes()), 0, 0, 1, 0)
        
        # Write section headers
        shoff = len(file_bytes)
        for sh in section_headers:
            file_bytes.extend(sh)
            
        # Finally, fill in the ELF Header
        # e_ident: 16 bytes
        e_ident = bytearray([constants.EI_MAG0, constants.EI_MAG1, constants.EI_MAG2, constants.EI_MAG3])
        e_ident.append(constants.ELFCLASS64)
        e_ident.append(constants.ELFDATA2LSB)
        e_ident.append(constants.EV_CURRENT)
        e_ident.append(0) # OSABI (0 = System V)
        e_ident.extend(b'\x00' * 8)
        
        ehdr = struct.pack("<16sHHIQQQIHHHHHH",
            bytes(e_ident),
            constants.ET_REL,
            constants.EM_X86_64,
            constants.EV_CURRENT,
            0, # e_entry
            0, # e_phoff
            shoff, # e_shoff
            0, # e_flags
            64, # e_ehsize
            0, # e_phentsize
            0, # e_phnum
            64, # e_shentsize
            len(section_headers), # e_shnum
            shstrtab_idx # e_shstrndx
        )
        
        file_bytes[0:64] = ehdr
        
        return bytes(file_bytes)
