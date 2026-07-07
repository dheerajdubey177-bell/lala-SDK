import subprocess
import shutil
from typing import List, Optional

class LinkerNotFoundError(Exception):
    pass

class LinkDriver:
    def __init__(self):
        # We prefer gcc/clang as they automatically link libc if we need it,
        # and they correctly invoke ld underneath.
        self.system_linker = self._find_linker()

    def _find_linker(self) -> Optional[str]:
        for linker in ["gcc", "clang", "x86_64-w64-mingw32-gcc"]:
            if shutil.which(linker):
                return linker
        return None

    def has_linker(self) -> bool:
        return self.system_linker is not None

    def link(self, object_files: List[str], libraries: List[str], output: str, target: str = "x86_64") -> None:
        """
        Links object files and libraries into an executable.
        Raises LinkerNotFoundError if no system linker is available.
        Raises subprocess.CalledProcessError if linking fails.
        """
        if not self.system_linker:
            raise LinkerNotFoundError("No compatible system linker (gcc/clang) found in PATH.")
        
        args = [self.system_linker]
        args.extend(object_files)
        args.extend(libraries)
        args.extend(["-o", output])
        
        subprocess.run(args, check=True, capture_output=True, text=True)
