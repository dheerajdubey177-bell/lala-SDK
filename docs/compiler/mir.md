# Machine Intermediate Representation (MIR)

The MIR is the lowest-level intermediate representation in the Lala compiler pipeline before architecture-specific backend lowering. It acts as an abstraction over machine concepts.

## Invariants
1. **Target-Independent**: MIR strictly avoids architecture-specific concepts like `rdi`, `rax`, or Windows/System V ABI specific registers. It uses abstract Virtual Registers and explicit memory boundaries.
2. **Flat Instruction Set**: MIR uses linear execution paths organized into explicit `BasicBlock`s capped with exactly one terminator.
3. **Typing**: All higher-level semantic types (`Number`, `String`, `List`) must be lowered to primitive machine types (`i1`, `i8`, `i16`, `i32`, `i64`, `f32`, `f64`, `ptr`).
4. **Single Definition**: Every virtual register is defined exactly once. Every use refers to a previously defined register.

---

## Primitives

### Types
```text
i1    : Boolean flag (e.g. for branching or cmp results)
i8    : 1-byte integer
i16   : 2-byte integer
i32   : 4-byte integer
i64   : 8-byte integer
f32   : 4-byte float
f64   : 8-byte float
ptr   : Generic machine pointer (size is target dependent)
```

### Virtual Registers
Instead of naming generic variables, MIR binds evaluation results to sequentially allocated Virtual Registers.
* Notation: `v17:i64`

### Stack Slots
Local allocations are placed in specific `stack_slot` references, which are treated as `ptr` types by MIR memory operations.
* Notation: `stack0:ptr`

---

## Instruction Set

* **Memory**
  * `load target:v_reg, source:ptr`
  * `store target:ptr, source:v_reg`
* **Arithmetic & Logic**
  * `mov target:v_reg, source:value`
  * `add target, left, right`
  * `sub`, `mul`, `div`, `rem`
  * `and`, `or`, `xor`, `not`
* **Comparisons**
  * `cmp_eq target:i1, left, right`
  * `cmp_ne`, `cmp_lt`, `cmp_le`, `cmp_gt`, `cmp_ge`
* **Control Flow**
  * `jmp target_block`
  * `br cond:i1, true_block, false_block`
  * `ret [value]`
* **Subroutines**
  * Abstract calling convention prepares arguments without hardware registers:
    ```text
    arg0 = v1:i64
    arg1 = v2:ptr
    call foo
    v3:i64 = retval
    ```

---

## Memory Model

MIR memory access is strictly pointer-based.
Even stack allocations conceptually yield pointers:
```text
stack0 : ptr
v1:i64 = const 10
store stack0, v1
v2:i64 = load stack0
```
