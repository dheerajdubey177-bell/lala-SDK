#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// A tiny stub for runtime IO if we decide to compile C into liblala_runtime.a
// Eventually, these could be pure assembly doing syscalls to avoid libc.

void lala_print_int(int64_t val) {
    printf("%lld\n", (long long)val);
}
