import random
f = open("InsertWORST.txt", "w")
for i in range(2000, 0, -1):
    f.write(str(i ))
    f.write("\n")
f.close()
