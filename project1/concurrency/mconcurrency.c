// Concurrency 1: The Producer-Consumer Problem
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <time.h>
#include <stdbool.h>

// Headers
void *ProducerThread(void *item);
void *consumer();
bool isBufferFull();

// Global Buffer
BufferItem bufferArr[32];

// Item in buffer should be a struct with 2 numbers
typedef struct { 
    int consumerNum;
    int randWait;
} BufferItem;

pthread_cond_t BufferNotFull=PTHREAD_COND_INITIALIZER;
pthread_cond_t BufferFull=PTHREAD_COND_INITIALIZER;
pthread_cond_t BufferNotEmpty=PTHREAD_COND_INITIALIZER;
pthread_cond_t BufferEmpty=PTHREAD_COND_INITIALIZER;
pthread_mutex_t bufferId=PTHREAD_MUTEX_INITIALIZER;

int main(int argc, char *argv) {

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


/* Requirements/constraints
 * -- While an item is being added to or removed from the buffer, the buffer is
      in an inconsistent state. Therefore, threads must have exclusive access
      to the buffer
 * -- If a consumer thread arrives while the buffer is empty, it blocks until a
      producer adds a new item. 
 * -- If a producer thread has an item to put in the buffer while the buffer is
      full, it blocks until a consumer removes an item.
 */
void *consumer() {
    //struct BufferItem consumeN;
    //struct BufferItem waitTime;
    //fprintf("%d", BufferItem->consumerNum);

    if (&bufferNotFull){
        // Lock thread while removing item from buffer
        pthread_mutex_lock(&bufferId);
        // do thing
        pthread_mutex_unlock(&bufferId);
    }else if (&bufferEmpty){
        // if buffer empty, wait until a "not empty" signal is sent
        pthread_cond_wait(&bufferNotEmpty, &bufferId);
    }else if (&bufferFull){
        // if the buffer is full, lock and have consumer thread remove item
        pthread_mutex_lock(&bufferId);
        // Print first val
        fprintf("Consumed: %d\n", consumeN); //<-- ??
        pthread_mutex_unlock(&bufferId);
        pthread_cond_signal(&bufferNotFull);
    }
}

