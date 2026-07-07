; Windows crt0 for Lala
; This uses standard MSVC / MASM syntax or NASM depending on assembler.
; We will assume NASM/YASM syntax for simplicity, or we can use GCC/Mingw syntax.
; Let's write it in Intel syntax for gas (Mingw-w64) so gcc can build it.
.intel_syntax noprefix

.globl mainCRTStartup
mainCRTStartup:
    # Windows aligns stack to 16 bytes but requires 32-byte shadow space.
    sub rsp, 40       # 32 bytes shadow + 8 bytes alignment padding (if needed)

    # Initialize runtime (no-op for v1.0)

    # Call lala.main
    call lala.main

    # Exit process
    mov rcx, rax      # Exit code in RCX for ExitProcess
    # We would call ExitProcess here. For now, just return to kernel32 if we came from main
    add rsp, 40
    ret
