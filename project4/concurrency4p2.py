from multiprocessing import Process, Lock, Manager, Semaphore
# from threading import Thread, Lock

import sys

import random
import time

from multiprocessing.managers import BaseManager

manager = Manager()

numLocks = manager.Value('i',0)
canConnect = manager.Value('i',0)
chairLock = manager.Semaphore(int(sys.argv[1]))
barberLock = manager.Lock()


def main():
    random.seed(1)
    cList = []

    B = Process(target=barber)
    for i in range(0, int(sys.argv[1]) + 3):
        cList.append(Process(target=customer, args=(i,)))

    B.start()
    for i in range(0, int(sys.argv[1]) + 3):
        cList[i].start()

    B.join()
    for i in range(0, int(sys.argv[1]) + 3):
        cList[i].join()

def customer(val):
    global numLocks
    global canConnect
    global chairLock
    global barberLock
    while(1):
        time.sleep(random.random())
        print(val, "customer has arrived")
        numLocks.value += 1
        if numLocks.value == 1:
            print(val, "customer wakes up barber")
        if chairLock.acquire(blocking=False) == True:
            if barberLock.acquire(blocking=False) == False:
                print(val, "customer sits down in chair")
                barberLock.acquire()
                print(val, "customer leaves chair")
            chairLock.release()
            print(val, "customer sits down in barber chair")
            time.sleep(0.1)
            canConnect.value = 1
            get_hair_cut(val)
            canConnect.value = 0
            barberLock.release()
        numLocks.value -= 1
        print(val, "customer leaves the store")
        time.sleep(random.random() * 10 + 9)


def barber():
    global numLocks
    global canConnect
    global chairLock
    global barberLock
    sleep = 0
    while(1):
        if canConnect.value == 1:
            cut_hair()
            sleep = 0

        if numLocks.value == 0 and sleep == 0:
            print("barber is sleeping")
            sleep = 1



def get_hair_cut(val):
    print(val, "customer starts getting haircut")
    time.sleep(3)
    print(val, "customer recieves haircut")

def cut_hair():
    print("barber starts giving haircut")
    time.sleep(3)
    print("barber finishes haircut")
    time.sleep(0.1)

if __name__=='__main__':
    main()
