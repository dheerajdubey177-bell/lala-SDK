.intel_syntax noprefix
.globl main
main:
.L0:
    mov rax, 100
    mov QWORD PTR [rbp-8], rax
    mov r9, QWORD PTR [rbp-8]
    mov QWORD PTR [rbp-16], r9
    mov rdx, QWORD PTR [rbp-16]
    mov rax, rdx
    ret