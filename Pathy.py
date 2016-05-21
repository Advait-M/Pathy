#!/usr/bin/env python
"""A game similar to flow free."""

from tkinter import *
from tkinter.ttk import *
import random
import math
import time
import cmath
import copy
import sys
import winsound

__author__ = "Advait Maybhate"
__copyright__ = "Copyright 2016, Pathy"
__credits__ = []
__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Advait Maybhate"
__status__ = "Unstable Release"

root = Tk()
sHeight = 800
sWidth = 800
screen = Canvas(
    root,
    width=sWidth,
    height=sHeight,
    background="black")  # Make main game canvas
size = 6
space = int(400/size)
dotRad = int((space-20)/2)

def hexadecimalToDecimal(m):
    """Returns the decimal version of the hexadecimal number"""
    chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"] #Make a list of hexadecimal characters
    n = str(m) #Convert m to a string and assign it to n so we can index it
    decimal = 0 #Initialize the final decimal value to 0
    for i in range(0, len(n)): #Loop up to the length of the hexadecimal number
        if n[i] != "0": #If the current item at the index is not 0 (if it has any value)
            decimal += 16**(len(n)-i-1) * chars.index(n[i]) #Add 16^length(n)-current index-1 * value of current item to our final decimal
    return decimal #Returns the final decimal integer

def hexadecimal():
    global coloursd
    hexadecimals = "#"
    for i in range(0, 6):
        a = random.randint(48, 70)
        while 58 <= a <= 64:
            a = random.randint(48,70)
        hexadecimals += chr(a)
    ch = False
    for i in range(0, len(coloursd)):
        if abs(hexadecimalToDecimal(hexadecimals[1:]) - hexadecimalToDecimal(coloursd[i][1:])) < 100000:
            ch = True
    if ch:
        return hexadecimal()
    else:
        return hexadecimals

def length(a, b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)

def createPuzzle(n):
    global grid, sols, coloursd
    grid = []
    sols = []
    mini = 3
    numi = n**2
    for s in range(0, n):
        x = s
        tempList = []
        t2 = []
        for d in range(0, n):
            y = d
            if d == 0 or d == n-1:
                tempList.append(1)
            else:
                tempList.append(0)
            t2.append([x,y])
        #grid.append(tempList)
        sols.append(t2)
    #print(sols)
    for i in range(0, numi):
        cur = random.randint(0, len(sols)-1)
        if len(sols[cur]) <= mini:
            continue
        for tryi in range(0, len(sols)):
            if length(sols[cur][0], sols[tryi][0]) == 1:
                 break
        empty = sols[cur][0]
        sols[cur] = sols[cur][1:]
        sols[tryi].insert(0, empty)

        for tryi in range(0, len(sols)):
            if length(sols[cur][-1], sols[tryi][-1]) == 1:
                 break
        empty = sols[cur][-1]
        sols[cur] = sols[cur][:-1]
        sols[tryi].append(empty)

    #print(sols)
    id = 1
    for rows in range(0, n):
        tempList = []
        for cols in range(0, n):
            counter = 0
            for runt in range(0, len(sols)):
                if [rows, cols] == sols[runt][0]:
                    counter = 1
                    break
                elif [rows, cols] == sols[runt][-1]:
                    counter = 2
                    break
            if counter == 1 or counter == 2:
                tempList.append(runt+1)
                id += 1
            else:
                tempList.append(0)


            # if sols[rows][cols][0] == rows and sols[rows][0][1] == 0:
            #     tempList.append(1)
            #     print(rows,cols)
            # elif sols[rows][cols][0] == rows and sols[rows][-1][1] == cols:
            #     tempList.append(1)
            #     #print(rows, cols)
            # else:
            #     tempList.append(0)
        grid.append(tempList)
    coloursd = []
    # print(grid)
    # for i in sols:
    #     print(i)
    for i in range(0, n):
        coloursd.append(hexadecimal())

    for firi in range(0, len(sols)):
        for seci in range(0, len(sols[i])):
            try:
                if length(sols[firi][seci], sols[firi][seci+1]) != 1:
                    print(grid)
                    for w in sols:
                        print(w)
                    createPuzzle(size)
            except IndexError:
                pass

def basicGridOverlay():
    spacing = 50
    for x in range(0, 800, spacing):
        screen.create_line(x, 10, x, 800, fill="white")
        screen.create_text(x, 0, text=str(x), font="Times 8", anchor=N, fill = "white")

    for y in range(0, 800, spacing):
        screen.create_line(20, y, 800, y, fill="white")
        screen.create_text(4, y, text=str(y), font="Times 8", anchor=W, fill = "white")

def overlay(startx, starty, endx, endy, spacing):
    """Makes a grid overlay."""
    endi = endy - 400%spacing
    for x in range(startx, endx+1, spacing):  # Draw vertical lines
        screen.create_line(x, starty, x, endi, fill="yellow")

    for y in range(starty, endy+1, spacing):  # Draw horizontal lines
        screen.create_line(startx, y, endi, y, fill="yellow")


def createBoard():
    global grid, sols, coloursd
    for sx in range(0, len(grid)):
        for sy in range(0, len(grid[sx])):
            if grid[sx][sy] != 0 :
                # print(grid[sx][sy])
                # print(coloursd)
                screen.create_oval(200 + sx * space - dotRad + space / 2, 200 + sy * space - dotRad + space / 2,
                                   200 + sx * space + dotRad + space / 2, 200 + sy * space + dotRad + space / 2,
                                   fill=coloursd[(grid[sx][sy]-1)])
def createSolution():
    global grid, sols, coloursd
    for sx in range(0, len(grid)):
        for sy in range(0, len(grid[sx])):
            # print(grid[sx][sy])
            # print(coloursd)
            for i in range(0, len(sols)):
                try:
                    sols[i].index([sx, sy])
                    break
                except ValueError:
                    pass
            screen.create_oval(200 + sx * space - dotRad + space / 2, 200 + sy * space - dotRad + space / 2,
                                   200 + sx * space + dotRad + space / 2, 200 + sy * space + dotRad + space / 2,
                                   fill=coloursd[i])
def initialize():
    createPuzzle(size)

def runGame():
    global grid, sols
    initialize()
    createBoard()
    #basicGridOverlay()
    #createSolution()
    overlay(200, 200, 600, 600, space)
    screen.update()
    # curx = 2
    # cury = 3
    # screen.create_oval(200+curx*space-dotRad+space/2, 200+cury*space-dotRad+space/2, 200+curx*space+dotRad+space/2, 200+cury*space+dotRad+space/2, fill = "orange")


screen.pack()
runGame()
root.mainloop()