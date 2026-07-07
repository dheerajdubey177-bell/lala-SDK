from .object_file import ObjectFile

class ObjectValidator:
    def validate(self, obj: ObjectFile):
        section_names = set()
        for sec in obj.sections:
            if sec.name in section_names:
                raise ValueError(f"Duplicate section name: {sec.name}")
            section_names.add(sec.name)
            
        symbol_names = set()
        for sym in obj.symbols:
            if sym.name in symbol_names:
                raise ValueError(f"Duplicate symbol name: {sym.name}")
            symbol_names.add(sym.name)
            if sym.section is not None and sym.section not in section_names:
                raise ValueError(f"Symbol {sym.name} references non-existent section: {sym.section}")
                
        for rel in obj.relocations:
            if rel.section not in section_names:
                raise ValueError(f"Relocation in non-existent section: {rel.section}")
            if rel.symbol_name not in symbol_names:
                raise ValueError(f"Relocation references undefined symbol: {rel.symbol_name}")
