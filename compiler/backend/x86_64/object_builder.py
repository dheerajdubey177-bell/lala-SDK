from compiler.object.object_file import ObjectFile
from compiler.object.section import Section, SectionFlags
from compiler.object.symbol import Symbol, SymbolKind, SymbolBinding
from compiler.object.relocation import Relocation, RelocationKind
from compiler.backend.x86_64.code_image import CodeImage, FixupKind

class ObjectBuilder:
    def build(self, code_image: CodeImage) -> ObjectFile:
        obj = ObjectFile()
        
        # 1. Create .text section
        text_section = Section(
            name=".text",
            flags=[SectionFlags.ALLOC, SectionFlags.EXEC],
            alignment=16,
            bytes_data=code_image.bytes_data
        )
        obj.sections.append(text_section)
        
        # 2. Extract symbols
        for func in code_image.functions:
            sym = Symbol(
                name=func.name,
                kind=SymbolKind.FUNC,
                binding=SymbolBinding.GLOBAL,
                section=".text",
                offset=func.offset,
                size=func.length
            )
            obj.symbols.append(sym)
            
        # 3. Process fixups into relocations
        # A Fixup targets a label. In ELF, if it's an external symbol, we might need a PLT32 or PC32 reloc.
        # For now, map FixupKind.REL32 -> RelocationKind.REL32
        for fixup in code_image.fixups:
            if fixup.kind == FixupKind.REL32:
                # addend calculation: X86_64 REL32 adds the addend + offset to PC. 
                # Our encoded CALL/JMP leaves the 4 bytes at 0. 
                # The PC during execution is offset + 4 (size of the displacement itself).
                # ELF R_X86_64_PC32 computes: S + A - P. 
                # To match exactly our offset logic, A typically is -4.
                addend = -4
                
                rel = Relocation(
                    section=".text",
                    offset=fixup.offset,
                    symbol_name=fixup.target_label,
                    kind=RelocationKind.REL32,
                    addend=addend
                )
                obj.relocations.append(rel)
                
            # If we add external symbols we don't know about yet, we should add them to the symbol table
            # as UNDEFINED (section=None) so the linker can resolve them.
            found = any(s.name == fixup.target_label for s in obj.symbols)
            if not found:
                obj.symbols.append(Symbol(
                    name=fixup.target_label,
                    kind=SymbolKind.NOTYPE,
                    binding=SymbolBinding.GLOBAL,
                    section=None,
                    offset=0,
                    size=0
                ))
                
        return obj
