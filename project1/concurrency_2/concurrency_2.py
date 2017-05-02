import time
import random
from threading import Thread, Lock

class philo:
    def __init__(self):
        self.name = None
        self.loc_in_circle = None
        self.first_fork = None
        self.second_fork = None

    def __init__(self, name, loc):
        self.name = name
        self.loc_in_circle = loc
        ### always get the lowest number fork that you plan to use
        if self.loc_in_circle == 5:
            self.first_fork = 0
            self.second_fork = 4
        else:
            self.first_fork = self.loc_in_circle - 1
            self.second_fork = self.loc_in_circle

    def think(self):
        print "Philo: " + self.name + " is Thinking"
        time.sleep(random.randrange(1,20))

    def eat(self):
        print "Philo: " + self.name + " is eating"
        time.sleep(random.randrange(2,9))

    def get_forks(self):
        forkList[self.first_fork].m.acquire()
        print "Philo: " + self.name + " has aquired Fork: " + str(self.first_fork)
        forkList[self.second_fork].m.acquire()
        print "Philo: " + self.name + " has aquired Fork: " + str(self.second_fork)

    def put_forks(self):
        print "Philo: " + self.name + " is releasing Forks"
        forkList[self.first_fork].m.release()
        forkList[self.second_fork].m.release()

    def print_info(self):
        print "Name: " + str(self.name)
        print "Loc: " + str(self.loc_in_circle)
        print "FF: " + str(self.first_fork)
        print "SF: " + str(self.second_fork)

class fork:
    def __init__(self, num):
        self.m = Lock()
        self.num = num
        self.is_avail = 1

forkList = []

def main():
    ### MARK: - Initialize the problem
    random.seed()
    ### List of forks
    global forkList
    for i in range(1,6):
        forkList.append(fork(i))
    ### List of philosophers
    philoList = []
    philoList.append(philo("test1", 1))
    philoList.append(philo("test2", 2))
    philoList.append(philo("test3", 3))
    philoList.append(philo("test4", 4))
    philoList.append(philo("test5", 5))

    philoList[0].print_info()


    ### MARK: - Create the threads
    t1 = Thread(target = philo_1, args = (philoList[0],))
    t2 = Thread(target = philo_2, args = (philoList[1],))
    t3 = Thread(target = philo_3, args = (philoList[2],))
    t4 = Thread(target = philo_4, args = (philoList[3],))
    t5 = Thread(target = philo_5, args = (philoList[4],))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

### MARK: - separate philosopher threads
def philo_1(philo):
    while(1):
        philo.think()
        philo.get_forks()
        philo.eat()
        philo.put_forks()

def philo_2(philo):
    while(1):
        philo.think()
        philo.get_forks()
        philo.eat()
        philo.put_forks()

def philo_3(philo):
    while(1):
        philo.think()
        philo.get_forks()
        philo.eat()
        philo.put_forks()

def philo_4(philo):
    while(1):
        philo.think()
        philo.get_forks()
        philo.eat()
        philo.put_forks()

def philo_5(philo):
    while(1):
        philo.think()
        philo.get_forks()
        philo.eat()
        philo.put_forks()

if __name__ == '__main__':
    main()
