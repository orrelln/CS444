#!/usr/bin/python

import sys, os

# ascii_lowercase contains only lowercase letters
from string import ascii_letters

# import choice (to choose random letters) and randint (for random integers)
from random import randint, sample

n = int(sys.argv[1])

# randomstring() joins together 10 random letters to form a string
def randomstring():
    s = ascii_letters # Assign lowercase alphabet to variable s
    return ''.join(sample(s, 15))

# create test_dir if it DNE
if not os.path.exists("test_dir"):
    os.makedirs("test_dir")

# cd to test_dir
os.chdir("test_dir")
for i in range(1, n+1):
    filename = 'file' + str(i)
    f = open(filename, 'w')   

    randstr = randomstring()
    f.write(randstr + '\n')
    f.close()
