# Language Design Council

This document records the major design decisions for the Lala programming language. It serves as the rationale behind *why* the language behaves the way it does, preventing future changes that accidentally erode its design philosophy.

---

## 1. No Inheritance
**Decision:** Lala uses composition and interfaces instead of traditional OOP inheritance. There is no `extends` or `super` keyword.
**Reasoning:** Deep inheritance trees become brittle and difficult for beginners (and experts) to maintain. Composition (`varg` containing other `varg`s) combined with Interfaces (`swaroop`) offers all the flexibility without the structural constraints.
**Status:** Frozen (v1.0)

## 2. Result Types over Exceptions
**Decision:** Lala does not have `try/catch` or hidden control flow exceptions. Functions that can fail return a Result, and errors are handled explicitly using the `?` operator or `.ok` checking. Unrecoverable errors use `panic`.
**Reasoning:** Exceptions hide control flow and make it difficult for readers to know where an error is handled. Result types force the programmer to confront errors at the call site, leading to safer software.
**Status:** Frozen (v1.0)

## 3. Mixed Hindi + English Keywords
**Decision:** Core types (`number`, `string`, `bool`, `list`, `dict`) are English, while structural control flow (`kaam`, `agar`, `jabtak`, `varg`, `swaroop`) are Hindi.
**Reasoning:** This creates a unique Hindi-inspired personality while keeping the language internationally readable. Changing primitives to `ank` or `shabd` would create unnecessary friction for users reading standard programming tutorials or AI documentation.
**Status:** Frozen (v1.0)

## 4. Standard Library Modules vs Globals
**Decision:** Only absolute essentials (`print`, `input`) are global. Everything else is organized into modules (`graphics.*`, `math.*`, `http.*`).
**Reasoning:** Putting everything in the global namespace causes naming collisions as the language grows (e.g., `file.open()` vs `database.open()`). Modules keep the standard library organized and predictable.
**Status:** Frozen (v1.0)

## 5. No Semicolons or Braces
**Decision:** Lala uses indentation-based blocks (like Python) and does not require semicolons to terminate lines. Parentheses are not required around control flow conditions (`agar age > 18:`).
**Reasoning:** Reduces visual noise. Code becomes cleaner and reads closer to natural language.
**Status:** Frozen (v1.0)

## 6. Variable Declarations
**Decision:** Lala supports explicit typing (`number age = 20`) and inferred typing (`age = 20`). There is no `rakho` keyword or `let`/`var` prefix. 
**Reasoning:** The assignment operator itself is sufficient to declare a variable. This removes unnecessary boilerplate. The type is fixed upon first assignment.
**Status:** Frozen (v1.0)

## 7. Memory Management
**Decision:** Memory is completely abstracted. The user never sees pointers, references, `new`, or `delete`. 
**Reasoning:** Manual memory management is historically the largest source of security vulnerabilities and the steepest learning curve for beginners. Lala's compiler/runtime handles allocations automatically.
**Status:** Frozen (v1.0)

## 8. Concurrency
**Decision:** Excluded from v1.0. Lala is single-threaded.
**Reasoning:** Concurrency introduces massive complexity for both the user and the language runtime. v1.0 focuses on a predictable, easy-to-learn synchronous core. Asynchronous features (`async`/`await`) will be evaluated for v1.1+.
**Status:** Frozen (v1.0)
