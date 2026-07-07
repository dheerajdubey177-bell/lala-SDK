.intel_syntax noprefix
.globl main
main:
.L0:
    mov rdx, 100
    mov QWORD PTR [rbp-8], rdx
    mov r10, QWORD PTR [rbp-8]
    mov QWORD PTR [rbp-16], r10
    mov rsi, QWORD PTR [rbp-16]
    mov rax, rsi
    ret