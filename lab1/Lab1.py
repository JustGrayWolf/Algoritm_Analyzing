from time import *
import random
import string
import sys


# Other functions
def takeRandomString(size):
    return ''.join(random.choice(string.ascii_letters) for _ in range(size))


def tablePrint(matrix):
    print("\nМатрица:\n")

    for row in matrix:  
        for element in row:
            print("{:4d}".format(element), end="")
        print()



# Algorithms
def levensteinRecursion(s1, s2):
    if (s1 == "" or s2 == ""):
        return len(s1) + len(s2)

    if (s1[-1] == s2[-1]): 
        f = 0 
    else: 
        f = 1

    return min(levensteinRecursion(s1[:-1], s2) + 1,
               levensteinRecursion(s1, s2[:-1]) + 1,
               levensteinRecursion(s1[:-1], s2[:-1]) + f)

def DameraulevensteinRecursion(s1, s2):
    if (s1 == "" or s2 == ""):
        return len(s1) + len(s2)

    if (s1[-1] == s2[-1]): 
        f = 0 
    else: 
        f = 1
    if (len(s1) > 1 and len(s2) > 1 and s1[-2] == s2[-1] and s1[-1] == s2[-2]):
        return min(DameraulevensteinRecursion(s1[:-1], s2) + 1,
               DameraulevensteinRecursion(s1, s2[:-1]) + 1,
               DameraulevensteinRecursion(s1[:-1], s2[:-1]) + f,
                DameraulevensteinRecursion(s1[:-2], s2[:-2]) + 1)
    else:
        return min(DameraulevensteinRecursion(s1[:-1], s2) + 1,
               DameraulevensteinRecursion(s1, s2[:-1]) + 1,
               DameraulevensteinRecursion(s1[:-1], s2[:-1]) + f)

def levensteinTable(s1, s2, isPrint):
    lenI = len(s1) + 1
    lenJ = len(s2) + 1

    table = [[j for j in range(lenJ)] for i in range(2)]
    if (isPrint):
        print("\nМатрица:")
    for i in range(1, lenI):
        for j in range(1, lenJ):
            l = i % 2
            table[l][0] = i
            if (s1[i - 1] == s2[j - 1]):
                f = 0 
            else:
                f = 1
            table[l][j] = min(table[not l][j] + 1,
                              table[l][j-1] + 1,
                              table[not l][j - 1] + f)

            if (isPrint):
                print("{:4d}".format(table[l][j]), end = "");
        if (isPrint):
            print("\n")
    
    return table[lenI % 2][-1]


def processingTableRecursion(table, i, j, s1, s2):
    if (i + 1 < len(table)) and (j + 1 < len(table[0])):
        if s1[j] == s2[i]:
            add = 0
        else:
            add = 1 
        
        if table[i + 1][j + 1] > table[i][j] + add:
            table[i + 1][j + 1] = table[i][j] + add
            processingTableRecursion(table, i + 1, j + 1, s1, s2)
    
    if (j + 1 < len(table[0])) and (table[i][j + 1] > table[i][j] + 1):
        table[i][j + 1] = table[i][j] + 1
        processingTableRecursion(table, i, j + 1, s1, s2)

    if (i + 1 < len(table)) and (table[i + 1][j] > table[i][j] + 1):
        table[i + 1][j] = table[i][j] + 1
        processingTableRecursion(table, i + 1, j, s1, s2)
            
            
def levensteinTableRecursion(s1, s2, isPrint):
    lenI = len(s1) + 1
    lenJ = len(s2) + 1

    maxLen = max(len(s1), len(s2)) + 1

    table = [[maxLen] * lenI for i in range(lenJ)]
    table[0][0] = 0

    processingTableRecursion(table, 0, 0, s1, s2)

    if isPrint:
        tablePrint(table)
    
    return table[-1][-1]


def damerauLevenstein(s1, s2, isPrint):
    lenI = len(s1) + 1
    lenJ = len(s2) + 1
    
    table = [[i + j for j in range(lenJ)] for i in range(lenI)]

    for i in range(1, lenI):
        for j in range(1, lenJ):
            if (s1[i - 1] == s2[j - 1]):
                f = 0
            else:
                f = 1
            
            table[i][j] = min(table[i - 1][j] + 1,
                              table[i][j - 1] + 1,
                              table[i - 1][j - 1] + f)
            
            if (i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]):
                table[i][j] = min(table[i][j], table[i - 2][j - 2] + 1)

    if isPrint:
        tablePrint(table)
    
    return table[-1][-1]



# Unit tests
def doUnitTest(testArray, testName, levFunction, isTable):
    for i in range(len(testArray)):
        if (isTable):
            result = levFunction(testArray[i][0], testArray[i][1], False)
        else:
            result = levFunction(testArray[i][0], testArray[i][1])

        if (result == testArray[i][2]):
            print(testName, "тест", i, "успешно выполнен")
        else:
            print(testName, "тест", i, "провален")
            return False
    
    return True


def unitTests(levFunction, isTable):
    # Тесты при пустых входных строках
    test_empty = [["f", "f", 0], ["f", "", 1], ["", "f", 1]]
    # Тесты на поиск совпадений
    test_match = [["asd", "asd", 0], ["f", "f", 0], ["F", "f", 1]]
    # Остальные тесты
    test_others = [["a", "s", 1], ["asd", "bsf", 2], ["asd", "as", 1], ["a", "adws", 3]]

    if doUnitTest(test_empty, "Пустой", levFunction, isTable):
        print()
        if doUnitTest(test_match, "Совпадающий", levFunction, isTable):
            print()
            if doUnitTest(test_others, "Случайный", levFunction, isTable):
                print("\nВыполнено!\n")



# Time tests
def doTimeTestsRecursion(levFunction, iterations, strLength):
    t1 = process_time()

    for _ in range(iterations):
        s1 = takeRandomString(strLength)
        s2 = takeRandomString(strLength)
        levFunction(s1, s2)

    t2 = process_time()

    return (t2 - t1) / iterations


def doTimeTestsTable(levFunction, iterations, strLength):
    t1 = process_time()

    for _ in range(iterations):
        s1 = takeRandomString(strLength)
        s2 = takeRandomString(strLength)
        levFunction(s1, s2, False)

    t2 = process_time()

    return (t2 - t1) / iterations


def timeTests(levFunction, isTable, isRecursion):
    lengthsArray = [7, 8, 9, 10, 11]
    iterations   = [100, 100, 50, 20, 10]

    if (isRecursion):
        lastIndex = 3
    else:
        lastIndex = len(lengthsArray)

    for i in range(lastIndex):
        if (isTable):
            timeResult = doTimeTestsTable(levFunction, iterations[i], lengthsArray[i])
        else:
            timeResult = doTimeTestsRecursion(levFunction, iterations[i], lengthsArray[i])
        
        print("Для длины =", lengthsArray[i], "\tвремя =", timeResult)



def main():
    done = False

    while(not done):

        print("Меню: ")
        print("[1] - Рекурсивный алгоритм Левенштейна")
        print("[2] - Алгоритм Левенштейна с 2 строками")
        print("[3] - Рекурсивный алгоритм Дамерау-Левенштейна")
        print("[4] - Дамерау-Левенштейн")
        print("[5] - Тест")
        print("[6] - Тест времени")
        print("[0] - Выход\n")

        try:
            action = int(input("Выбор: "))
        except:
            print("\nОшибка \n")
            continue

        if (action == 0):
            done = True
            continue
        elif (action != 5 and action != 6):
            word1 = input(">> Первое слово: ")
            word2 = input(">> Второе слово: ")

        if (action == 1):
            result = levensteinRecursion(word1, word2)
        elif (action == 2):
            result = levensteinTable(word1, word2, True)
        elif (action == 3):
            result = DameraulevensteinRecursion(word1, word2)
        elif (action == 4):
            result = damerauLevenstein(word1, word2, True)
        elif(action == 5):
            result = False

            print(">>ТЕСТ РЕКУРСИВНОГО АЛГОРИТМА:\n")
            unitTests(levensteinRecursion, False)

            print(">>ТЕСТ АЛГОРИТМА ЛЕВЕНШТЕЙНА:\n")
            unitTests(levensteinTable, True)

            print(">>ТЕСТ РЕКУРСИВНОГО АЛГОРИТМА ДАМЕРАУ-ЛЕВЕНШТЕЙНА:\n")
            unitTests(DameraulevensteinRecursion, False)

            print(">>ТЕСТ АЛГОРИТМА ДАМЕРАУ-ЛЕВЕНШТЕЙНА:\n")
            unitTests(damerauLevenstein, True)
        elif(action == 6):
            print("\n>>ВРЕМЕННОЙ ТЕСТ РЕКУРСИВНОГО АЛГОРИТМА:")
            timeTests(levensteinRecursion, False, False)

            print("\n>>ВРЕМЕННОЙ ТЕСТ АЛГОРИТМА ЛЕВЕНШТЕЙНА:")
            timeTests(levensteinTable, True, False)

            print("\n>>ВРЕМЕННОЙ ТЕСТ РЕКУРСИВНОГО АЛГОРИТМА ДАМЕРАУ-ЛЕВЕНШТЕЙНА:\n")
            timeTests(DameraulevensteinRecursion,False, False) 

            print("\n>>ВРЕМЕННОЙ ТЕСТ АЛГОРИТМА ДАМЕРАУ-ЛЕВЕНШТЕЙНА:")
            timeTests(damerauLevenstein, True, False)
            
            result = False

        if (result):
            print("\n>>> Результат: ", result, "\n")


main()
