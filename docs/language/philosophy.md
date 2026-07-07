# The Philosophy of Lala

## 1. What problems is Lala trying to solve?
Lala was created to make programming universally approachable for beginners, particularly native Hindi speakers, without sacrificing the power, safety, and batteries-included nature of modern ecosystems. Many languages force beginners to choose between simple syntax (Python) with slow performance, or high performance (C++/Rust) with overwhelming complexity. Lala bridges this gap. 

## 2. Who is it for?
Lala is for absolute beginners, hobbyists, game developers, and educators. It is designed to be the language you use to build your first game, your first AI script, or your first database app, in minutes rather than weeks.

## 3. What things will it intentionally never support?
- **Manual Memory Management**: No `new`, `delete`, pointers, or borrowing rules. Memory is handled silently.
- **Inheritance**: No complex `class Dragon extends FlyingMonster`. Lala strongly prefers Composition and Interfaces.
- **Hidden Control Flow**: No traditional `try/catch` exceptions that silently jump across the call stack.

## 4. The Four Laws of Lala

### Law 1: Complexity belongs to the runtime, not the programmer.
Every new feature must satisfy this law. The compiler and runtime do all the hard work. The user never manages heap allocation, reference counts, pointers, or `std::shared_ptr`. The user writes `player = Player()` and the runtime absorbs the complexity.

### Law 2: One obvious way.
Lala does not provide five ways to solve the same problem. There is no `new`, `malloc`, `shared_ptr`, `unique_ptr`, or `stack allocation`. There is only one obvious way to initialize an object.

### Law 3: Safe by default.
Lala protects the programmer. Operations like out-of-bounds array access (`numbers[100]`) produce clean, well-defined runtime errors, never undefined behavior or raw memory crashes. Unrecoverable errors panic safely.

### Law 4: Zero-cost simplicity.
Simple syntax does not mean slow code. A basic `har n in numbers:` loop compiles down into highly optimized backend code. The beginner gets simple syntax, and the backend delivers native performance.

### Law 5: Approachable Aesthetics
Lala blends standard English data types (`number`, `string`, `list`, `bool`) with Hindi control-flow keywords (`kaam`, `agar`, `warna`, `jabtak`, `lautao`). This keeps the language internationally readable for APIs and AI models, while retaining its unique cultural identity.
