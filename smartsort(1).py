# File:    smartsort.py
# Author:  John Longley
# Date:    October 2024

# Template file for Inf2-IADS (2024-25) Coursework 1, Part A:
# Implementation of hybrid Merge Sort / Insert Sort,
# with optimization for already sorted segments.

import peekqueue
from peekqueue import PeekQueue

# Global variables

comp = lambda x,y: x<=y   # comparison function used for sorting

insertSortThreshold = 10

sortedRunThreshold = 10


# TODO: Task 1. Hybrid Merge/Insert Sort
def insertSort(A,m,n):
    for i in range(m, n):
        x = A[i]
        j = i-1
        while (comp(0, j)) and (comp(x, A[j])):
            A[j+1] = A[j]
            j = j-1
        A[j+1] = x

def merge(C,D,m,p,n):
    left = m # beginning of left half
    right = p # beginning of right half
    new = m # beginning of where to put the new sorted result into D

    while (comp(left, p-1)) and (comp(right, n-1)): # while both halves have items left
        if comp(C[left], C[right]): # if left is smaller than right
            D[new] = C[left] # put left into D
            left += 1 # increment left
        else:
            D[new] = C[right] # put right into D
            right += 1 # increment right
        new += 1 # move to next position in D

    while comp(left, p-1): # if there are still items left in the left half but not in the right half, put all of them into D
        D[new] = C[left] 
        left += 1 
        new += 1
    
    while comp(right, n-1): # if there are still items left in the right half but not in the left half, put all of them into D
        D[new] = C[right]
        right += 1
        new += 1

def greenMergeSort(A,B,m,n):
    if comp(n-m, insertSortThreshold):
        insertSort(A, m, n)
        return
    if comp(m, n):
        middle = (m+n)//2
        greenMergeSort(A, B, m, middle)
        greenMergeSort(A, B, middle, n)
        merge(A, B, m, middle, n)
        for i in range(m, n):
            A[i] = B[i]

# Provided code:

def greenMergeSortAll(A):
    B = [None] * len(A)
    greenMergeSort(A,B,0,len(A))
    return A


# TODO: Task 2. Detecting already sorted runs.
def allSortedRuns(A):
    length = len(A)

    pointer = 1
    num = 0

    Q = PeekQueue()

    while pointer < length:
        if comp(A[pointer-1], A[pointer]):
            pointer += 1
            num += 1
        else:
            if comp(sortedRunThreshold, num+1):
                Q.push((pointer - num - 1, pointer))
            num = 0
            pointer += 1
    return Q

def isWithinRun(Q, i, j):
    while Q.peek():
        pair = Q.pop()
        if comp(pair[0], i) and comp(j, pair[1]):
            return True
    return False 

def smartMergeSort(A,B,Q,m,n):
    if isWithinRun(Q, m, n):
        return 
    
    if comp(n-m, insertSortThreshold):
        insertSort(A, m, n)
        return
    
    if comp(m, n):
        middle = (m+n)//2
        smartMergeSort(A, B, Q, m, middle)
        smartMergeSort(A, B, Q, middle, n)
        merge(A, B, m, middle, n)

        for i in range(m, n):
            A[i] = B[i]  

# Provided code:

def smartMergeSortAll(A):
    B = [None] * len(A)
    Q = allSortedRuns(A)
    smartMergeSort(A,B,Q,0,len(A))
    return A


# TODO: Task 3. Asymptotic analysis of smartMergeSortAll

# 1. Justification of O(n lg n) bound.
# 
#
#
#
# (continue as necessary)

# 2. Runtime analysis for nearly-sorted inputs.
#
#
#
#
# (continue as necessary)


# Functions added for automarking purposes - please don't touch these!

def set_comp(f):
    global comp
    comp = f

def set_insertSortThreshold(n):
    global insertSortThreshold
    insertSortThreshold = n

def set_sortedRunThreshold(n):
    global sortedRunThreshold
    sortedRunThreshold = n

def set_insertSort(f):
    global insertSort
    insertSort = f

# End of file
