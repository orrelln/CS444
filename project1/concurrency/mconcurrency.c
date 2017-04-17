// Concurrency 1: The Producer-Consumer Problem
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

//item in buffer should be a struct with 2 numbers
struct BufferItem { 
    int consumerNum;
    int randWait;
}

int main(int argc, char *argv) {

}

