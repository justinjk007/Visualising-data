#!/usr/bin/env python2.7
# thou shall not cross 80 columns in thy file

# Convex-Hull creation using Graham Scan Algorithm

from stack import myStack
import sys
from timeit import default_timer as timer
import csv
import math
import matplotlib.pyplot as plt


def scan(data):
    "This method uses grahamScan to create a convex hull from the given points"
    hullX = myStack()    # For the X-coordinates of the hull
    hullY = myStack()    # For the Y-coordinates of the hull
    newPoints = []          # For storing the unused points
    newPoints.append([])    # For the X-coordinates
    newPoints.append([])    # For the Y-coordinates
    backTrackTracker = False
    hullX.stackPush(data[0].pop(0))
    hullY.stackPush(data[1].pop(0))
    '''First element of the data is always the starting point of the hull,
       which is the lowest y-coordinate we calculated
    '''
    M = 1  # This Stores the size of the hull stack
    while True:
        if backTrackTracker is not True:
            hullX.stackPush(data[0].pop(0)) # Pop the 1st item, add to hull
            hullY.stackPush(data[1].pop(0)) # Pop the 1st item, add to hull
            M += 1
        if len(data[0]) == 0:  # This is true when all points are serviced
            return hullX.fullStack(), hullY.fullStack(), newPoints
        if leftOrRight(hullX.atIndex(M-2), hullY.atIndex(M-2),
                       hullX.atIndex(M-1), hullY.atIndex(M-1),
                       data[0][0], data[1][0]) == 'left':
            backTrackTracker = False
        else:  # The points are collinear or makes a right turn
            # Backtracking
            newPoints[0].append(hullX.stackPop())
            newPoints[1].append(hullY.stackPop())
            backTrackTracker = True
            M -= 1


def leftOrRight(p1x, p1y, p2x, p2y, p3x, p3y):
    "Used to determine the right path for the convex points"
    cal1 = (p2x - p1x) * (p3y - p1y)
    cal2 = (p2y - p1y) * (p3x - p1x)
    diff = cal1 - cal2
    if diff < 0:
        return 'right'
    elif diff > 0:
        return 'left'
    elif diff == 0:
        return 1
    else:
        print "The impossible have happened yet again"


def isEmpty(anyList):
    "This method checks if the list is empty or not"
    if not anyList:
        return True  # List is empty
    else:
        return False  # List is not empty


def order(data, P):
    "This method orders the given data so that, index P comes first"
    while P != 0:
        data[0].append(data[0].pop(0))  # Remove xCord add it to the end
        data[1].append(data[1].pop(0))  # Remove yCord add it to the end
        P -= 1                          # Do this until Pth element move to 0
    return data


def heapSort(heap, base):  # O(n log n)
    "Implements Heapsort for max heap, sorting in ascending order"

    def maxHeapify(heap, base, i, size):  # O(log n)
        "This method maintains the Heap property of the heap from root i"
        l = left(i)
        r = right(i)
        if l <= size and base[l] > base[i]:
            large = l
        else:
            large = i
        if r <= size and base[r] > base[large]:
            large = r
        if large != i:
            swap(base, i, large)
            swapData(heap, i, large)
            maxHeapify(heap, base, large, size)  # maxheapify from node = large

    def buildHeap(heap, base):  # O(n)
        "This method builds a min heap, with largest element at index 1/root"
        ArraySize = len(base)-1
        start = int(math.floor(ArraySize/2))
        for i in range(start, 0, -1):
            maxHeapify(heap, base, i, ArraySize)

    def left(i):
        "Returns the index of the left element of the parent node i"
        return 2*i

    def right(i):
        "Returns the index of the right element of the parent node i"
        return (2*i)+1

    def swap(data, i, j):
        "This method swaps the two points i and j in the list data"
        data[i], data[j] = data[j], data[i]  # do THE swap
        return data

    heap[0] = [None] + heap[0]
    heap[1] = [None] + heap[1]
    base = [None] + base
    buildHeap(heap, base)
    heapSize = len(base)-1
    # Here we are reducing the heapsize until to zero, removing the
    # sorted value from the heap each time
    for i in range(heapSize, 1, -1):
        swapData(heap, 1, i)
        swap(base, 1, i)
        heapSize -= 1
        maxHeapify(heap, base, 1, heapSize)
    heap[0].pop(0)          # Remove the None value that was added for ordering
    heap[1].pop(0)          # Remove the None value that was added for ordering
    base.pop(0)          # Remove the None value that was added for ordering
    return heap, base


def toXandY(unorderedData):
    "This method converts seperates x and y co-ordinates for plotting"
    orderedData = []
    orderedData.append([])        # Add a new sublist every time
    orderedData.append([])        # Add a new sublist every time
    listSize = len(unorderedData)
    for x in range(0, listSize):
        orderedData[0].append(unorderedData[x][0])  # Seperates the x-cords
    for y in range(0, listSize):
        orderedData[1].append(unorderedData[y][1])  # Seperates the y-cords
    return orderedData


def euclideanDistance(p, q):
    "This calculates the Euclidean Distance b/w p & q, in the standard way"
    distance = math.sqrt(((p[0]-q[0])**2) + ((p[1]-q[1])**2))
    return distance


def slope(data, P=0):
    "Calculates slopes between data-points and P"
    m = []
    m.append(0)  # Dummy value for Pth Value slope
    listSize = len(data[0])
    for i in range(1, listSize):  # Starting from 1 excluding P point
        m.append((data[1][i] - data[1][P])/(data[0][i] - data[0][P]))
    return m  # Return the list with slopes


def draw(xCords, yCords, xLabel, yLabel, what, filename):
    "This method draws the Convex-Hull plot using Matplotlib"
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title("Convex-Hull - "+filename)
    if what == 1:
        plt.scatter(xCords, yCords, color="g", s=20)
    else:
        plt.plot(xCords, yCords, '-o', color="r")  # Make the boundaries


def swapData(data, i, j):
    "This method swapDatas the two points i and j in the list data"
    data[0][i], data[0][j] = data[0][j], data[0][i]  # SwapData x-Cords
    data[1][i], data[1][j] = data[1][j], data[1][i]  # SwapData y-cords
    return data


def parse(file_name):
    "Parses the data sets from the csv file we are given to work with"
    file = open(file_name)
    rawFile = csv.reader(file)    # Reading the csv file into a raw form
    rawData = list(rawFile)       # Converting the raw data into list from.
    file.close()
    return rawData


def main():
    print ""
    newData = []
    try:
        file_name = sys.argv[1]
    except IndexError:
        print "Please pass the file name and try again!"
        print "Take a look at the README!"
        return 1
    if file_name.endswith(".csv"):
        start = timer()
        data = parse(file_name)   # Calling the parse funtion we made
    else:
        print "Wrong file format!!!"
        print "This program can only parse CSV files"
        return 1

    labels = data.pop(0)            # Necessary evil
    listSize = len(data)
    print "Number of Data points serviced: " + str(listSize)
    for i in range(0, listSize):    # Converting the string list to float
        newData.append([])          # Add a new sublsit every time
        for j in range(0, 2):       # Append converted data to the new list
            newData[i].append(float(data[i][j]))
    # Finding the starting point P
    DataXandY = toXandY(newData)     # DataXandY -> [[Xs][Ys]]
    P = DataXandY[1].index(min(DataXandY[1]))  # Locating the minimum y-cord
    DataXandY = swapData(DataXandY, 0, P)
    P = 0                            # Because it was swaped
    slopes = slope(DataXandY, P)

    # Sort the points based on slopes, using heapsort
    DataXandY, slopes = heapSort(DataXandY, slopes)

    PIndex = slopes.index(0)
    DataXandY = order(DataXandY, PIndex)  # Order data so that P comes first

    hullX, hullY, newPoints = scan(DataXandY)   # Call the graham scan algorithm

    hullX.append(hullX[0])  # Add the first x at end -> Full circle
    hullY.append(hullY[0])  # Add the first y at end -> Full circle
    end = timer()
    draw(hullX, hullY, labels[0], labels[1], 2, file_name)  # Draw the hull
    draw(newPoints[0], newPoints[1], labels[0], labels[1], 1, file_name)
    print "Time elapsed: " + str(end-start) + " seconds"
    plt.show()


if __name__ == "__main__":
    main()
