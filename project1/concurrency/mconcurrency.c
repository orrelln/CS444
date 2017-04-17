// Concurrency 1: The Producer-Consumer Problem
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <stdbool.h>

// Headers
void *ProducerThread(void *item);
bool isBufferFull();

// Vars
pthread_mutex_t mutex;

// Item in buffer should be a struct with 2 numbers
typedef struct { 
        int consumerNum;
        int randWait;
} BufferItem;

// Global Buffer
BufferItem bufferArr[32];


int main(int argc, char *argv[]) {
        //pthread identifier
        pthread_t producerT;

        pthread_create(&producerT, NULL, ProducerThread, NULL);



}



/*
 * Param: item to put into buffer
 * Adds item to the buffer, while adding has exclusing access to buffer
 * if buffer is full, block until producer adds a new item
 * Post: item is added to buffer
 * 
 * http://timmurphy.org/2010/05/04/pthreads-in-c-a-minimal-working-example/
 */
void *ProducerThread(void *item) {
    



    return 0;
}



