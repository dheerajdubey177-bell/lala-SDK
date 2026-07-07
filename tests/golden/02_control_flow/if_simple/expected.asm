.intel_syntax noprefix
.globl main
main:
.L0:
    mov rax, 5
    mov QWORD PTR [rbp-8], rax
    mov r9, QWORD PTR [rbp-8]
    mov rdx, 2
    cmp r9, rdx
    jne .L1
    jmp .L2
.L1:
    mov r11, 1
    mov rax, r11
    ret
.L2:
    jmp .L3
.L3:
    mov rdi, 0
    mov rax, rdi
    ret