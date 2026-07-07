.intel_syntax noprefix

.globl _start
_start:
    # Stack is aligned to 16 bytes upon entering _start per SysV ABI

    # Initialize runtime (no-op for v1.0)
    
    # Call lala.main
    call lala.main
    
    # lala.main returns the exit code in RAX
    # Syscall: exit(rax)
    mov rdi, rax    # arg1 = exit code
    mov rax, 60     # syscall number for sys_exit on Linux x86_64
    syscall
