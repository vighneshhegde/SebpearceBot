import random
numLines = 0
i = 0
f = open("bullshit.txt")
for line in f:
    numLines += 1
f.close()
f = open("bullshit.txt")
randNum = random.randint(1, numLines)
for i, line in enumerate(f):
    if i == randNum:
        bullshitLine = line
        print(bullshitLine)
        break
f.close()


