from multiprocessing import Process, Lock, Manager, Semaphore
# from threading import Thread, Lock

import sys

import random
import time

from multiprocessing.managers import BaseManager

manager = Manager()

numLocks = manager.Value('i',0)
canConnect = manager.Value('i',1)
sempLock = manager.Semaphore(3)


def main():
    random.seed(1)
    
    i1 = Process(target=proc, args=(1,))
    i2 = Process(target=proc, args=(2,))
    i3 = Process(target=proc, args=(3,))
    i4 = Process(target=proc, args=(4,))
    i5 = Process(target=proc, args=(5,))
    i6 = Process(target=proc, args=(6,))

    i1.start()
    i2.start()
    i3.start()
    i4.start()
    i5.start()
    i6.start()

    i6.join()
    i1.join()
    i2.join()
    i3.join()
    i4.join()
    i5.join()

def proc(val):
    global numLocks
    global canConnect
    global sempLock
    while(1):
        sempLock.acquire();
        if canConnect.value == 1:
            print(val, " is using resource")
            time.sleep(random.random())
            numLocks.value += 1
            if numLocks.value == 3:
                canConnect.value = 0
                print("resource is full")
            time.sleep(random.randint(3, 5))
            print(val, " is done using resource")
            numLocks.value -= 1
            if numLocks.value == 0:
                print("resource completely freed")
                canConnect.value = 1
        sempLock.release();

if __name__=='__main__':
    main()
