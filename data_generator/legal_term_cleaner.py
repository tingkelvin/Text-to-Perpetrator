import random
import csv
import sys


###################################################

with open('legal_term.txt') as ff:
    linesf = [line.rstrip('\n') for line in ff]

linesf1 =[]
linesf2 =[]


for x in linesf:
    if (x!=""):
        linesf1.append(x)
    

for x in linesf1:
    last_char = x[-1]
    if (last_char != '.'):
        x=x+"."
        linesf2.append(x)
    else:

        linesf2.append(x)
    
# for x in linesf2:
#     print(x)
with open('lt.txt', 'w') as ffr:
    ffr.write('\n'.join(linesf2))


    



