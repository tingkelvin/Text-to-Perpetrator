import random
import csv
import sys


###################################################

with open('Sentence_f.txt') as ff:
    linesf = [line.rstrip('\n') for line in ff]

linesf1 =[]
linesf2 =[]
for x in linesf:
    last_char = x[-1]
    if (last_char == '.' or last_char == '!'or last_char == "/"):
        linesf1.append(x)

for x in linesf1:
    if (('He' not in x) and 
        ('She' not in x) and 
        (' he ' not in x) and 
        (' she ' not in x)):
        linesf2.append(x) 

with open('f.txt', 'w') as ffr:
    ffr.write('\n'.join(linesf2))

###################################################

with open('Sentence_m.txt') as fm:
    linesm = [line.rstrip('\n') for line in fm]

linesm1 =[]
linesm2 =[]
for x in linesm:
    last_char = x[-1]
    if (last_char == '.' or last_char == '!'or last_char == "/"):
        linesm1.append(x)

for x in linesm1:
    if (('He' not in x) and 
        ('She' not in x) and 
        (' he ' not in x) and 
        (' she ' not in x)):
        linesm2.append(x) 

with open('m.txt', 'w') as fmr:
    fmr.write('\n'.join(linesm2))

###################################################

with open('Sentence_f.txt') as fb:
    linesb = [line.rstrip('\n') for line in fb]

linesb1 =[]
linesb2 =[]
for x in linesb:
    last_char = x[-1]
    if (last_char == '.' or last_char == '!'or last_char == "/"):
        linesb1.append(x)

for x in linesb1:
    if (('He' not in x) and 
        ('She' not in x) and 
        (' he ' not in x) and 
        (' she ' not in x)):
        linesb2.append(x) 

with open('b.txt', 'w') as fbr:
    fbr.write('\n'.join(linesb2))



    



