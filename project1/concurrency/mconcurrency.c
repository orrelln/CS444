// Concurrency 1: The Producer-Consumer Problem
// used the following as reference:
// http://www.dailyfreecode.com/code/solve-producer-consumer-problem-thread-2114.aspx
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <time.h>
#include <stdbool.h>
#include <signal.h>
#include <unistd.h>
#include "randsnip.c"
#define BufferSize 32

// Headers
void *ProducerThread();
void *ConsumerThread();
int isBufferFull();
void interruptHandler(int);

// Pthread vars
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t bufferNotEmpty = PTHREAD_COND_INITIALIZER;
pthread_cond_t bufferNotFull = PTHREAD_COND_INITIALIZER;

// Item in buffer should be a struct with 2 numbers
typedef struct {
        int consumerNum;
        int randWait;
} BufferItem;

// Global Buffer
BufferItem bufferArr[BufferSize];
int bufferIdx = 0;



int main(int argc, char *argv[]) {
        // Pthread identifier
        pthread_t producerT;
        pthread_t consumerT;
        signal(SIGINT, interruptHandler);

        // Create producer thread
        pthread_create(&producerT, NULL, ProducerThread, NULL);
        pthread_create(&consumerT, NULL, ConsumerThread, NULL);

        // Join Threads
        pthread_join(producerT, NULL);
        pthread_join(consumerT, NULL);
}



/*
 * Param: item to put into buffer
 * Adds item to the buffer, while adding has exclusing access to buffer
 * if buffer is full, block until producer adds a new item
 * Post: item is added to buffer
 *
 * http://timmurphy.org/2010/05/04/pthreads-in-c-a-minimal-working-example/
 */
void *ProducerThread() {
        while(1) {
                // TODO: create buffer item
                pthread_mutex_lock(&mutex);
                if(bufferIdx == BufferSize-1) {
                        pthread_cond_wait(&bufferNotFull, &mutex);
                }
                bufferIdx++;

                BufferItem bItem;
                bItem.consumerNum = randNum(1, 100);
                bItem.randWait = randNum(2,9);

                // Add buffer item here
                bufferArr[bufferIdx] = bItem;

                printf("producing buffer item num:%d wait:%d\n", 
                                bItem.consumerNum,
                                bItem.randWait,
                                bufferIdx);

                pthread_cond_signal(&bufferNotEmpty);
                pthread_mutex_unlock(&mutex);
        }
        return 0;
}


// Reference from http://cis.poly.edu/cs3224a/Code/ProducerConsumerUsingPthreads.c
void interruptHandler (int sg) {
        printf("interrupt received, quitting\n");
        pthread_mutex_destroy(&mutex);
        pthread_cond_destroy(&bufferNotEmpty);
        pthread_cond_destroy(&bufferNotFull);
        exit(0);
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
void *ConsumerThread() {
    while(1) {
            printf("consuming----\n");
        // TODO: create buffer item
        pthread_mutex_lock(&mutex);
        if(bufferIdx == 0) {
                pthread_cond_wait(&bufferNotEmpty, &mutex);
        }
        BufferItem bItem = bufferArr[bufferIdx];
        bufferIdx--;

        // TODO: Delete from array later??

        // wait some time from randWait
        sleep(bItem.randWait);

        printf("consuming buffer item num:%d\n",
                bItem.consumerNum);

        pthread_cond_signal(&bufferNotFull);
        pthread_mutex_unlock(&mutex);
    }
    return 0;
}
