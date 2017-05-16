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


# define global linked list


def main():
    pass

def inserter():
    pass

def searcher():
    pass

def deleter():
    pass



if __name__ == __main__:
    main()
