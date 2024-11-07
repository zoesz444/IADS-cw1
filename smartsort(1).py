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

def insertSort(A,m,n):
    # start at index one as comparing to previous item
    for i in range(m+1, n):
        x = A[i]
        j = i - 1
        while j >= m and (comp(x, A[j])):
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = x

def merge(C,D,m,p,n):
    left = m # beginning of left half
    right = p # beginning of right half
    new = m # beginning of where to put the new sorted result into D

    while left < p and right < n: # while both halves have items left to sort
        if comp(C[left], C[right]):
            D[new] = C[left] # put left into D
            left += 1
        else:
            D[new] = C[right] # put right into D
            right += 1
        new += 1 # move to next position in D
    while left < p: # if only left items left, add them all to D
        D[new] = C[left] 
        left += 1
        new += 1
    while right < n: # if only right items left, add them all to D
        D[new] = C[right]
        right += 1
        new += 1

def greenMergeSort(A,B,m,n):
    # if the number of items is below the threshold use insertsort
    if n-m <= insertSortThreshold:
        insertSort(A, m, n)
        return
    # otherwise use recursive mergesort
    if m <= n:
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

def allSortedRuns(A):
    length = len(A)
    pointer = 1
    num = 0
    Q = PeekQueue()
    # while there are still items to check
    while pointer < length:
        if comp(A[pointer-1], A[pointer]):
            pointer += 1
            num += 1
        else:
            if sortedRunThreshold <= num+1:
                # add pair to queue
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

    if n-m <= insertSortThreshold:
        insertSort(A, m, n)
        return
    
    if m <= n:
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

# 1. Justification of O(n lg n) bound.
# The worst case scenario is when none of the items are sorted. The first thing that must be checked is if any of the
# items are already sorted - this takes n time. Then it splits the list into its individual components where for each
# split of length k it checks if k is already sorted. This takes lg(n) time. As every time the list must be checked
# for being sorted again, it takes n lg(n) time.
# (continue as necessary)

# 2. Runtime analysis for nearly-sorted inputs.
# As the isWithinRun function will not apply here, and neither will using insertSort, we just use a standard mergeSort
# which has n lg(n) worst-case runtime.
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
