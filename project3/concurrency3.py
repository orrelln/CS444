from multiprocessing import Process, Lock

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
globList = LinkedList()

notSearch = Lock()
notInsert = Lock()
searchTempLock = Lock()
insertTempLock = Lock()
insertCompLock = Lock()

numSearchers = 0
numInserters = 0


def main():
	random.seed()
	data = random.randint(0,10)
	i = Process(target=inserter, args=(data,))
	i.start()
	data = random.randint(0,10)
	i = Process(target=inserter, args=(data,))
	data = random.randint(0,10)
	i = Process(target=inserter, args=(data,))
	data = random.randint(0,10)
	i = Process(target=inserter, args=(data,))
	data = random.randint(0,10)
	i = Process(target=inserter, args=(data,))
	data = random.randint(0,10)
	i = Process(target=inserter, args=(data,))

def inserter(data):
	global globList
	insertTempLock.acquire()
	numInserters += 1
	if numInserters == 1:
		notSearch.acquire()
	insertTempLock.release()

	insertCompLock.acquire()

	# insert here
	print "inserting"
	globList.add(data)

	insertCompLock.release()

	insertTempLock.acquire()
	numInserters -= 1
	if numInserters == 0:
		notSearch.release()
	insertTempLock.release()

def searcher(data):
	global globList
	searchTempLock.acquire()
	numSearchers += 1
	if numSearchers == 1:
		notSearch.acquire()
	searchTempLock.release()
	# search here
	print "searching"
	globList.search(data)

	searchTempLock.acquire()
	numSearchers -= 1
	if numSearchers == 0:
		notSearch.release()
	searchTempLock.release()

def deleter():
	global globList
	notInsert.acquire()
	notSearch.acquire()

	# delete
	print "deleting"
	globList.remove(data)
	
	
	notInsert.release()
	notSearch.release()



if __name__ == __main__:
    main()
