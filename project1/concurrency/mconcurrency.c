// Concurrency 1: The Producer-Consumer Problem
// used the following as reference:
// http://www.dailyfreecode.com/code/solve-producer-consumer-problem-thread-2114.aspx
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <stdbool.h>

// Headers
void *ProducerThread(void *item);
bool isBufferFull();

// Pthread vars
pthread_mutex_t mutex;
pthread_cond_t bufferEmpty = PTHREAD_COND_INITIALIZER;
pthread_cond_t bufferFull = PTHREAD_COND_INITIALIZER;

// Item in buffer should be a struct with 2 numbers
typedef struct { 
        int consumerNum;
        int randWait;
} BufferItem;

// Global Buffer
const int BufferSize = 32
BufferItem bufferArr[BufferSize];
int bufferIdx = 0;



int main(int argc, char *argv[]) {
        // Pthread identifier
        pthread_t producerT;
        signal(SIGINT, interruptHandler);

        // Create producer thread
        pthread_create(&producerT, NULL, ProducerThread, NULL);

        // Join Threads
        pthread_join(producerT, NULL);



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
        while(1) {
                // TODO: create buffer item
                pthread_mutex_lock(&mutex);
                if(isBufferFull) {
                        pthread_cond_wait(&bufferFull, &mutex);
                }
                bufferIdx++;
                // Add buffer item here
                // bufferArr[bufferIdx] = bufferitem here
                
                printf("producing");
                pthread_cond_signal(&bufferEmpty);
                pthread_mutex_unlock(&mutex);
        }
        return 0;
}

bool isBufferFull() {
        if(bufferIdx == BufferSize-1) {
                return true;
        } else {
                return false;
        }
}

// Reference from http://cis.poly.edu/cs3224a/Code/ProducerConsumerUsingPthreads.c
void interruptHandler (int sg) {
        pthread_mutex_destroy(&mutex);
        pthread_cond_destroy(&bufferEmpty);
        pthread_cond_destroy(&bufferFull);
        exit(0);
}



