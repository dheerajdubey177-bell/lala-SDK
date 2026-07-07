#include <stdio.h>
#include <stdlib.h>

void lala_panic() {
    fprintf(stderr, "fatal: lala program panicked\n");
    exit(1);
}
