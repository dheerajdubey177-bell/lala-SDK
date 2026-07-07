.intel_syntax noprefix
.globl get_value
get_value:
.L0:
    mov rax, 42
    mov rax, rax
    ret

.intel_syntax noprefix
.globl main
main:
.L0:
    call get_value
    mov rax, rax
    mov rax, rax
    ret