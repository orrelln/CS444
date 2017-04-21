#include "mt19937ar.c"


//generates a value between min and max using rdrand or Mersenne Twister
int randNum(int min, int max) {
    int eax, ebx, ecx, edx;
    unsigned char err;
    int randVal = 0;
    eax = 0x01;

    //set registers from the result of running opcode cpuid
    //even though ebx and ecx are never used, required for cpuid to work correctly
    __asm__ __volatile__("cpuid" : "=a"(eax), "=b"(ebx), "=c"(ecx), "=d"(edx) : "a"(eax));

    //http://stackoverflow.com/questions/8920840/a-function-to-check-if-the-nth-bit-is-set-in-a-byte
    //checks if 30th bit of ecx(rrdrand support) is set to 1
    //https://hackage.haskell.org/package/crypto-random-0.0.9/src/cbits/rdrand.c
    if (1<<30 & ecx)
        __asm__ __volatile__("rdrand %0; setc %1" : "=r" (randVal), "=qm" (err));
    else
        randVal = (int)genrand_int32();

    //as value is random number from 0 to 0xffffffff, must take absolute value and reduce to range betwwen min and max
    randVal = abs(randVal);
    randVal = randVal % (max - 1) + min;
    return randVal;
}
