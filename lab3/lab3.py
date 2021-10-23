import matplotlib.pyplot as plt
from time import *
import sys

def f():
    array = [1,85,7,4,28,4,4,85]
    BubbleSort(array, 8)
    print(array)
    array = [1,85,7,4,28,4,4,85]
    ShakerSort(array, 8)
    print(array)
    array = [1,85,7,4,28,4,4,85]
    InsertionSort(array, 8)
    print(array)
    DrawGraph("lol", [[0,3],[1,3],[3,5]], [[3.5,4],[2,5]], [[5,5],[6,6]])
        
def BubbleSort(array, n):
    fl = 1
    for i in range(0, n - 1):
        if fl :
            fl = 0
            for j in range(1, n - i):
                if (array[j-1] > array[j]):
                    fl = 1
                    array[j], array[j - 1] = array[j - 1], array[j] 
        else:
            break;

'''
def QSort(array, l, r):
    m = int((l + r) / 2)
    x = array[m]
    i = l
    j = r
    while (i < j):
        while array[i] < x:
            i += 1
        while array[j] > x:
            j -= 1
        if (i <= j):
            b = array[i]
            array[i] = array[j]
            array[j] = b
            i += 1
            j -= 1
    if l < j:
        QSort(array, l, j)
    if r > i:
        QSort(array, i, r)
'''

def ShakerSort(array, n): 
    f = 1
    s = 0
    e = n - 1
    while f: 
        
        swapped = False
          
        for i in range(s, e): 
            if (array[i] > array[i + 1]) : 
                array[i], array[i + 1] = array[i + 1], array[i] 
                f = 1
  
        if not(f): 
            break

        f = 0

        e -= 1

        for i in range(e, s, -1): 
            if (array[i] > array[i + 1]):
                array[i], array[i + 1] = array[i + 1], array[i] 
                f = 1
 
        s = s + 1

def InsertionSort(array, n):
    for i in range(0, n - 1):
        b = array[i]
        j = i - 1
        while j >=0 and b < array[j] :
            array[j+1] = array[j]
            j -= 1
        array[j+1] = b
    
def check(f, s, Sort, name):
    i = 0
    k = 10
    res = []
    array = []
    for c in f:
        array.append(int(c))
        i += 1
        if i % 200 == 0:
            t = 0
            for j in range(k):
                t1 = process_time()
                Sort(array, i)
                t += process_time() - t1
            t /= k
            res.append([i, t])
            print("Время на {0} в {1} случае при массиве {2} эллементов = {3}".format(name,s,i,t))
    return res

def DrawGraph(name, data1, data2, data3):
    fig, ax = plt.subplots(figsize=(5, 3))
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    x3=[]
    y3=[]
    for i in data1:
        x1.append(i[0])
        y1.append(i[1])
    for i in data2:
        x2.append(i[0])
        y2.append(i[1])
    for i in data3:
        x3.append(i[0])
        y3.append(i[1])
    ax.plot(x1,y1,"g-",x2,y2,"b-",x3,y3,"r-")
    #ax.stackplot(labels=['Лучший случай', 'Худший случай', 'Средний случай'])
    ax.set_title(name)
    ax.legend(['Лучший случай', "Худший случай", "Случайный массив"])
    plt.grid(True)
    ax.set_ylabel("")
    ax.set_xlabel("кол-во эл.")
    fig.tight_layout()
    plt.show()
    

def TEST():
    
    f = open("BubbleBEST.txt", 'r')
    res1 = check(f, "Лучшем", BubbleSort, "Сортировку пузырьком")
    f.close()
    f = open("BubbleWORST.txt", 'r')
    res2 = check(f, "Худшем", BubbleSort, "Сортировку пузырьком")
    f.close()
    f = open("RANDOM.txt", 'r')
    res3 = check(f, "Случайном", BubbleSort, "Сортировку пузырьком")
    f.close()
    DrawGraph("Сортировка пузырьком", res1, res2, res3)

    
    f = open("ShakeBEST.txt", 'r')
    res1 = check(f, "Лучшем", ShakerSort, "Сортировку шейком")
    f.close()
    f = open("ShakeWORST.txt", 'r')
    res2 = check(f, "Худшем", ShakerSort, "Сортировку шейком")
    f.close()
    f = open("RANDOM.txt", 'r')
    res3 = check(f, "Случайном", ShakerSort, "Сортировку шейком")
    f.close()
    DrawGraph("Сортировка шейком", res1, res2, res3)

    
    f = open("InsertBEST.txt", 'r')
    res = check(f, "Лучшем", InsertionSort, "Сортировку вставкой")
    f.close()
    f = open("InsertWORST.txt", 'r')
    res = check(f, "Худшем", InsertionSort, "Сортировку вставкой")
    f.close()
    f = open("RANDOM.txt", 'r')
    res3 = check(f, "Случайном", InsertionSort, "Сортировку вставкой")
    f.close()
    DrawGraph("Сортировка вставкой", res1, res2, res3)

TEST()
    
            
            
    
    
    
            
