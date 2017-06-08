import sys
import random
import time
from multiprocessing import Process, Lock, Manager
from multiprocessing.managers import BaseManager


class smoker:
    def __init__(self):
        self.name = None
        self.resource = None

    def __init__(self, name, res):
        self.name = name
        self.resource = res


class agent:
    def __init__(self):
        self.name = None
        self.resource = None

    def choose_resource(self):
        self.resource = random.sample(range(0,3), 2)

    def print_resource(self):
        print "The Agent has chosen resources: "
        for i in self.resource:
            if i == 0:
                print "Tobacco"
            elif i == 1:
                print "Paper"
            elif i == 2:
                print "Matches"
            else: 
                print "error"
                print i

    def needed_resource(self):
        if 0 not in self.resource:
            return 0
        elif 1 not in self.resource:
            return 1
        elif 2 not in self.resource:
            return 2
    
    
        
manager = Manager()

tobacco_res = manager.Lock()
paper_res = manager.Lock()
matches_res = manager.Lock()


def main():
    random.seed()
    a = Process(target=agent_man)
    s0 = Process(target=smoker_one)
    s1 = Process(target=smoker_two)
    s2 = Process(target=smoker_three)

    a.start()
    time.sleep(0.5)
    s0.start()
    s1.start()
    s2.start()

    a.join()
    s0.join()
    s1.join()
    s2.join()


def agent_man():
    global tobacco_res
    global paper_res
    global matches_res
    ag = agent()
    tobacco_res.acquire()
    paper_res.acquire()
    matches_res.acquire()
    while(1):
        print
        print "Agent is choosing"
        ag.choose_resource()
        ag.print_resource()
        which_lock = ag.needed_resource()
        if which_lock == 0:
            tobacco_res.release()
            time.sleep(1.0)
            tobacco_res.acquire()
        elif which_lock == 1:
            paper_res.release()
            time.sleep(1.0)
            paper_res.acquire()
        elif which_lock == 2:
            matches_res.release()
            time.sleep(1.0)
            matches_res.acquire()
        else:
            print "error"


def smoker_one():
    global tobacco_res
    smo = smoker("Tobacco Man", 0)
    while(1):
        tobacco_res.acquire()
        print smo.name + " is now making a cig"
        time.sleep(.5)
        tobacco_res.release()
        print smo.name + " is now smoking"
        time.sleep(1.0)


def smoker_two():
    global paper_res
    smo = smoker("Paper Man", 1)
    while(1):
        paper_res.acquire()
        print smo.name + " is now making a cig"
        time.sleep(0.5)
        paper_res.release()
        print smo.name + " is now smoking"
        time.sleep(1.0)

def smoker_three():
    global matches_res
    smo = smoker("Matches Man", 2)
    while(1):
        matches_res.acquire()
        print smo.name + " is now making a cig"
        time.sleep(0.5)
        matches_res.release()
        print smo.name + " is now smoking"
        time.sleep(1.0)


if __name__=='__main__':
    main()
