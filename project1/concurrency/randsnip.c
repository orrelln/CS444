#include "mt199937ar.c"

//global asm registers
int eax, ebx, ecx, edx;

//puts cpu information into registers
void registerSet() {
    //sets eax to 1 to check for ecx 30th bit rdrnd
    //https://en.wikipedia.org/wiki/CPUID
    eax = 0x01;

    //set registers from the result of running opcode cpuid
    //even though ebx and ecx are never used, required for cpuid to work correctly
    asm volatile("cpuid" : "=a"(eax), "=b"(ebx), "=c"(ecx), "=d"(edx) : "a"(eax));
}

//https://hackage.haskell.org/package/crypto-random-0.0.9/src/cbits/rdrand.c
//implmentation of rdrand or Mersenne Twister to generate random numbers
int rdrandShell(int *randVal) {
    unsigned char err;

    //outputs a random value and a status code
    asm volatile("rdrand %0; setc %1" : "=r" (*randVal), "=qm" (err));

    //returns 1 if rdrand is successful
    return (int) err;
}

//generates a value between min and max using rdrand or
int randNum(int min, int max) {
    int randVal = 0;
    registerSet();

    //http://stackoverflow.com/questions/8920840/a-function-to-check-if-the-nth-bit-is-set-in-a-byte
    //checks if 30th bit of ecx(rrdrand support) is set to 1
    if (1<<30 & ecx)
        rdrandShell(&randVal);
    else
        randVal = (int)genrand_int32();

    //as value is random number from 0 to 0xffffffff, must take absolute value and reduce to range betwwen min and max
    randVal = abs(randVal); //possibly not necessary
    randVal = randVal % max + min;
    return randVal;
}
