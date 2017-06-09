#include <stdio.h>

int main(void) {
        // Define our system call numbers
        int sys_call_free = 353;
        int sys_call_used = 354;

        // Create dummy arrays to artificially make process large
        int * dummy_int0, dummy_int1, dummy_int2, dummy_int3, dummy_int4; 
        dummy_int0 = (int*)malloc(100000);
        dummy_int1 = (int*)malloc(50000);
        dummy_int2 = (int*)malloc(60000);
        dummy_int3 = (int*)malloc(910000);
        dummy_int4 = (int*)malloc(13000);

        // Print our statistics
        printf("Free Bytes: %d\n", syscall(sys_call_free));
        //printf("Used Bytes: %d\n", syscall(sys_call_used));
        return 0;
}

