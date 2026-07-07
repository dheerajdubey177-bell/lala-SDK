.intel_syntax noprefix
.globl main
main:
.L0:
    mov rdx, 5
    mov QWORD PTR [rbp-8], rdx
    mov r10, 3
    mov QWORD PTR [rbp-16], r10
    mov rsi, QWORD PTR [rbp-8]
    mov rcx, QWORD PTR [rbp-16]
    mov r11, rsi
    add r11, rcx
    mov rax, r11
    ret