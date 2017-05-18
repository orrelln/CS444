from multiprocessing import Process, Lock, Manager
# from threading import Thread, Lock

import sys

import random
import time

from multiprocessing.managers import BaseManager

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

	def size(self):
		current = self.head
		count = 0
		while current != None:
			count = count + 1
			current = current.getNext()
		return count

    def printList(self):
        current = self.head
        sys.stdout.write("PRINTING LIST STATE: ")
        while current != None:
            sys.stdout.write(str(self.head.getData()) + ", ")
            sys.stdout.flush()
            current = current.getNext()
        sys.stdout.write("\n")
        sys.stdout.flush()
        


# define global linked list
# globList = LinkedList()

notSearch = Lock()
notInsert = Lock()
searchTempLock = Lock()
insertTempLock = Lock()
insertCompLock = Lock()


manager = Manager()
numSearchers = manager.Value('i',0)
numInserters = manager.Value('i',0)

# Creation of linkedlist manager to share data between processes
class MyManager(BaseManager):
    pass

MyManager.register('link', LinkedList)
man = MyManager()
man.start()
linkedList = man.link()

def main():
    random.seed()

    # global linkedList
    # linkedList.add(0)
    # linkedList.add(1)
    # linkedList.add(2)
    # linkedList.add(3)

    # linkedList.remove(3)
    # if linkedList.search(4):
        # linkedList.remove(4)


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
        global linkedList
        global numInserters
        insertTempLock.acquire()

        numInserters.value += 1
        idInsert = numInserters.value
        if numInserters.value == 1:
            notSearch.acquire()

        insertTempLock.release()
        insertCompLock.acquire()

        # insert here
        print "inserting " + str(idInsert)
        linkedList.add(idInsert)
        linkedList.printList()
        time.sleep(5.0)
        print "end inserting"
        print

        insertCompLock.release()
        insertTempLock.acquire()

        numInserters.value -= 1
        if numInserters.value == 0:
            notSearch.release()

        insertTempLock.release()

def searcher():
    while(1):
        global linkedList
        global numSearchers
        searchTempLock.acquire()

        numSearchers.value += 1
        idSearcher = numSearchers.value
        if numSearchers.value == 1:
            notSearch.acquire()

        searchTempLock.release()

        # search here
        print "searching for " + str(idSearcher)
        linkedList.printList()
        print "Found " + str(linkedList.search(idSearcher))
        time.sleep(2.0)
        print "end searching"
        print

        searchTempLock.acquire()
        numSearchers.value -= 1
        if numSearchers.value == 0:
            notSearch.release()
        searchTempLock.release()

def deleter():
    while(1):
        global linkedList
        notInsert.acquire()
        notSearch.acquire()

        # delete
        data = random.randint(0,10)
        print "attempting to delete " + str(data)
        linkedList.printList()
        if linkedList.search(data):
            linkedList.remove(data)
            print "successfully deleted"
            linkedList.printList()
        else:
            print "item not found"
        time.sleep(2.0)
        print "end deleting"
        print

        notInsert.release()
        notSearch.release()



if __name__ == "__main__":
    main()
