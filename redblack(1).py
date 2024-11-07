# File:     redblack.py
# Author:   John Longley
# Date:     October 2024

# Template file for Inf2-IADS (2024-25) Coursework 1, Part B:
# Implementation of dictionaries by red-black trees, space-saving version.

# Provided code:
from enum import Enum

Colour = Enum('Colour', ['Red', 'Black'])
Red, Black = Colour.Red, Colour.Black

def colourStr(c):
    return 'R' if c == Red else 'B'

Dir = Enum('Dir', ['Left', 'Right'])
Left, Right = Dir.Left, Dir.Right

def opposite(d):
    if d == Left:
        return Right
    else:
        return Left

def branchLabel(d):
    if d == Left:
        return 'l'
    else:
        return 'r'

class Node():

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.colour = Red
        self.left = None
        self.right = None

    def getChild(self, branch):
        if branch == Left:
            return self.left
        else:
            return self.right

    def setChild(self, branch, y):
        if branch == Left:
            self.left = y
        else:
            self.right = y

    def __repr__(self):
        return str(self.key) + ':' + str(self.value) + ':' + colourStr(self.colour)

# Use None for all trivial leaf nodes
def colourOf(x):
    if x is None:
        return Black
    else:
        return x.colour

class RedBlackTree():

    def __init__(self):
        self.root = None
        self.stack = []

    def lookup(self, key):
        x = self.root
        while x is not None:
            if x.key == key:
                return x.value
            elif key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
        return None

    def plainInsert(self, key, value):
        # check if key already exists in tree or if tree doesn't have any nodes
        # if key already exists, overwrite only the value
        # if tree DNE then root = new node

        x = self.root
        parent = None
        direction = None
        if x is None:
            self.root = Node(key, value)
            self.stack.append(self.root)
            return

        while True:
            if x is None:
                if direction == Left:
                    parent.left = Node(key, value)
                    parent.left.colour = Red
                    self.stack.append(parent.left)
                else:
                    parent.right = Node(key, value)
                    parent.right.colour = Red
                    self.stack.append(parent.right)
                break
            elif x.key == key:
                x.value = value
                self.stack.append(x)
                break
            elif key < x.key:
                self.stack.append(x)
                parent = x
                direction = Left
                x = x.left
                self.stack.append(direction)
            elif key > x.key:
                self.stack.append(x)
                parent = x
                direction = Right
                x = x.right
                self.stack.append(direction)
        return None

    def tryRedUncle(self):
        x = self.stack.pop()
        x_dir = self.stack.pop()
        parent = self.stack.pop()
        grandparent_dir = self.stack.pop()
        grandparent = self.stack.pop()
        uncle_dir = opposite(grandparent_dir)
        uncle = grandparent.getChild(uncle_dir)
        if parent.colour == Red and uncle and uncle.colour == Red and x.colour == Red:
            parent.colour, uncle.colour, grandparent.colour = Black, Black, Red
            self.stack.append(grandparent)
            self.stack.append(grandparent_dir)
            self.stack.append(parent)
            self.stack.append(x_dir)
            self.stack.append(x)
            return True
        else:
            self.stack.append(grandparent)
            self.stack.append(grandparent_dir)
            self.stack.append(parent)
            self.stack.append(x_dir)
            self.stack.append(x)
            return False


    def repeatRedUncle(self):
        while self.tryRedUncle():
            pass


    # Provided code to support Task 4: # inspect subtree down to the next level of blacks
    def toNextBlackLevel(self, node):
        # and return list of components (subtrees or nodes) in L-to-R order
        # (in cases of interest there will be 7 components A,a,B,b,C,c,D).
        if colourOf(node.left) == Black:  # node.left may be None
            leftHalf = [node.left]
        else:
            leftHalf = self.toNextBlackLevel(node.left)
        if colourOf(node.right) == Black:
            rightHalf = [node.right]
        else:
            rightHalf = self.toNextBlackLevel(node.right)
        return leftHalf + [node] + rightHalf


    def balancedTree(self, comps):
        # build a new (balanced) subtree from list of 7 components
        [A, a, B, b, C, c, D] = comps
        a.colour = Red
        a.left = A
        a.right = B
        c.colour = Red
        c.left = C
        c.right = D
        b.colour = Black
        b.left = a
        b.right = c
        return b

    # TODO: Task 4

    #     def endgame(self):
    #         self.repeatRedUncle()

    #   insert(self,key,value)

    # Provided code:

    # Printing tree contents

    def __str__(self, x):
        if x == None:
            return 'None:B'
        else:
            leftStr = '[ ' + self.__str__(x.left) + ' ] '
            rightStr = ' [ ' + self.__str__(x.right) + ' ]'
            return leftStr + x.__str__() + rightStr

    def __repr__(self):
        return self.__str__(self.root)

    def showStack(self):
        return [x.__str__() if isinstance(x, Node) else branchLabel(x)
                for x in self.stack]

    # All keys by left-to-right traversal

    def keysLtoR_(self, x):
        if x == None:
            return []
        else:
            return self.keysLtoR_(x.left) + [x.key] + self.keysLtoR_(x.right)

    def keysLtoR(self):
        return self.keysLtoR_(self.root)


# End of class RedBlackTree


# Creating a tree by hand:
sampleTree = RedBlackTree()
sampleTree.root = Node(2, 'two')
sampleTree.root.colour = Black
sampleTree.root.left = Node(1, 'one')
sampleTree.root.left.colour = Black
sampleTree.root.right = Node(4, 'four')
sampleTree.root.right.colour = Red
sampleTree.root.right.left = Node(3, 'three')
sampleTree.root.right.left.colour = Black
sampleTree.root.right.right = Node(6, 'six')
sampleTree.root.right.right.colour = Black
sampleTree.plainInsert(5, 'five')
print(sampleTree.showStack())

print(sampleTree.tryRedUncle())


# For fun: sorting algorithm using trees
# Will remove duplicates (not good)

def treeSort(L):
    T = RedBlackTree()
    for x in L:
        T.insert(x, None)
    return T.keysLtoR()

# End of file
