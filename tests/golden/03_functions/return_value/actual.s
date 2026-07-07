.intel_syntax noprefix
.globl get_value
get_value:
.L0:
    mov rdx, 42
    mov rax, rdx
    ret

.intel_syntax noprefix
.globl main
main:
.L0:
    call get_value
    mov rdx, rax
    mov rax, rdx
    ret