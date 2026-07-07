.intel_syntax noprefix
.globl main
main:
.L0:
    mov rdx, 5
    mov QWORD PTR [rbp-8], rdx
    mov r10, QWORD PTR [rbp-8]
    mov rsi, 2
    cmp r10, rsi
    jne .L1
    jmp .L2
.L1:
    mov r11, 1
    mov rax, r11
    ret
.L2:
    jmp .L3
.L3:
    mov r8, 0
    mov rax, r8
    ret