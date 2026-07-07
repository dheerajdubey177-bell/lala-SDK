.intel_syntax noprefix
.globl main
main:
.L0:
    mov rax, 5
    mov QWORD PTR [rbp-8], rax
    mov r9, 3
    mov QWORD PTR [rbp-16], r9
    mov rdx, QWORD PTR [rbp-8]
    mov r11, QWORD PTR [rbp-16]
    mov rdi, rdx
    add rdi, r11
    mov rax, rdi
    ret