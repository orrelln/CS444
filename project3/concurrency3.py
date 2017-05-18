from multiprocessing import Process, Lock, Manager
# from threading import Thread, Lock

import random
import time

# http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementinganUnorderedListLinkedLists.html

class Node:
    def __init__(self,initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self,newdata):
        self.data = newdata

    def setNext(self,newnext):
        self.next = newnext

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self,item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def search(self,item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()

        return found

    def remove(self,item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())


# define global linked list
# globList = LinkedList()

notSearch = Lock()
notInsert = Lock()
searchTempLock = Lock()
insertTempLock = Lock()
insertCompLock = Lock()

# numSearchers = 0
# numInserters = 0

manager = Manager()
numSearchers = manager.Value('i',0)
numInserters = manager.Value('i',0)
linkedList = manager.list()
linkedList.append(LinkedList())

def main():
    random.seed()
    # i = Thread(target=inserter)
    # i.start()

    # s = Thread(target=searcher)
    # s.start()

    # s1 = Thread(target=searcher)
    # s1.start()

    # d = Thread(target=deleter)
    # d.start()
    # i.join()
    # s.join()
    # s1.join()
    # d.join()


    i = Process(target=inserter)
    i.start()

    s = Process(target=searcher)
    s.start()

    s1 = Process(target=searcher)
    s1.start()

    data = random.randint(0,10)
    d = Process(target=deleter)
    d.start()

    i.join()
    s.join()
    s1.join()
    d.join()

def inserter():
    while(1):
        global LinkedList
        global numInserters
        insertTempLock.acquire()
        numInserters.value += 1
        if numInserters.value == 1:
            notSearch.acquire()
        insertTempLock.release()

        insertCompLock.acquire()
        # insert here
        print "inserting"

        data = random.randint(0,10)
        LinkedList[0].add(data)
        time.sleep(2.0)
        print "end inserting"

        insertCompLock.release()
        insertTempLock.acquire()
        numInserters.value -= 1
        if numInserters.value == 0:
            notSearch.release()
        insertTempLock.release()

def searcher():
    while(1):
        global LinkedList
        global numSearchers
        searchTempLock.acquire()
        numSearchers.value += 1
        print "searcher " + str(numSearchers)
        if numSearchers.value == 1:
            notSearch.acquire()
            print "not search lock acquired"
        searchTempLock.release()

        # search here
        print "searching"
        data = random.randint(0,10)
        # globList.search(data)
        LinkedList[0].search(data)
        time.sleep(2.0)
        print "end searching"

        searchTempLock.acquire()
        numSearchers.value -= 1
        if numSearchers.value == 0:
            notSearch.release()
        searchTempLock.release()

def deleter():
    while(1):
        global LinkedList
        notInsert.acquire()
        notSearch.acquire()

        # delete
        print "deleting"
        data = random.randint(0,10)
        # globList.remove(data)
        time.sleep(2.0)
        print "end deleting"

        notInsert.release()
        notSearch.release()



if __name__ == "__main__":
    main()
