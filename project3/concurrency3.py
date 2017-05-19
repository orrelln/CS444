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
        statement="PRINTING LIST STATE: "
        while current != None:
            statement+=str(current.getData()) + ", "
            current = current.getNext()
        print statement



manager = Manager()

notSearch = manager.Lock()
notInsert = manager.Lock()
searchTempLock = manager.Lock()
insertTempLock = manager.Lock()
insertCompLock = manager.Lock()


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

    i = Process(target=inserter)
    i2 = Process(target=inserter)
    i.start()
    i2.start()

    s = Process(target=searcher)
    s1 = Process(target=searcher)
    s.start()
    s1.start()

    d = Process(target=deleter)
    d2 = Process(target=deleter)
    d.start()
    d2.start()

    d.join()
    d2.join()
    i.join()
    i2.join()
    s.join()
    s1.join()

def inserter():
    while(1):
        global linkedList
        global numInserters
        global insertTempLock
        global insertCompLock
        insertTempLock.acquire()

        numInserters.value += 1
        if numInserters.value == 1:
            notInsert.acquire()

        insertTempLock.release()
        insertCompLock.acquire()
        print "INSERTING"
        data = random.randint(0,10)
        print "inserting " + str(data)
        linkedList.add(data)
        linkedList.printList()
        print "end inserting"
        time.sleep(2.0)
        insertCompLock.release()
        insertTempLock.acquire()

        numInserters.value -= 1
        if numInserters.value == 0:
            notInsert.release()

        insertTempLock.release()
        time.sleep(2.0)

def searcher():
    while(1):
        global linkedList
        global numSearchers
        global searchTempLock
        global notSearch
        searchTempLock.acquire()
        numSearchers.value += 1
        if numSearchers.value == 1:
            notSearch.acquire()

        print "SEARCHING"
        searchTempLock.release()
        data = random.randint(0,10)
        # search here
        print "searching for " + str(data)
        linkedList.printList()
        print "Found " + str(linkedList.search(data))
        print "end searching"
        time.sleep(2.0)
        searchTempLock.acquire()
        numSearchers.value -= 1
        if numSearchers.value == 0:
            notSearch.release()
        searchTempLock.release()
        time.sleep(2.0)

def deleter():
    while(1):
        global linkedList
        global notSearch
        global notInsert
        notInsert.acquire()
        notSearch.acquire()
        print "DELETING"

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
        print "end deleting"
        time.sleep(2.0)
        notInsert.release()
        notSearch.release()
        time.sleep(2.0)


if __name__=='__main__':
    main()
