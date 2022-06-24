import random
import csv
import sys


###################################################

with open('other.txt') as ff:
    linesf = [line.rstrip('\n') for line in ff]

linesf1 =[]

for x in linesf:
    temp = x.lower()

    linesf1.append(temp)


with open('otherlower.txt', 'w') as ffr:
    ffr.write('\n'.join(linesf1))




    



