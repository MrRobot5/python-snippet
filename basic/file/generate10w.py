import time

s = time.clock()
f = open("10w.txt", "w")
for i in range(0, 1000000):
    f.write(str(i) + "\n")

e = time.clock()
print(e - s)
