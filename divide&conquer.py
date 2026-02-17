import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import heapq
import threading
import os
from copy import deepcopy

# PATH 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CONSTANTS 
TILE = 160
BOARD_SIZE = 480
BG_COLOR = "misty rose"

GOAL = (1,2,3,4,5,6,7,8,0)
DIRS=[(-1,0),(1,0),(0,-1),(0,1)]


# MOVE GENERATOR
def neighbors(state):
    i=state.index(0)
    r,c=divmod(i,3)
    res=[]
    for dr,dc in DIRS:
        nr,nc=r+dr,c+dc
        if 0<=nr<3 and 0<=nc<3:
            j=nr*3+nc
            lst=list(state)
            lst[i],lst[j]=lst[j],lst[i]
            res.append(tuple(lst))
    return res

# A* SOLVER (CONQUER STEP)
def astar(start, goal_check):

    pq=[]
    heapq.heappush(pq,(h(start),0,start,[start]))
    visited=set()

    while pq:
        f,g,state,path=heapq.heappop(pq)

        if goal_check(state):
            return path

        if state in visited:
            continue
        visited.add(state)

        for nxt in neighbors(state):
            if nxt not in visited:
                heapq.heappush(pq,(g+1+h(nxt),g+1,nxt,path+[nxt]))

    return None  

# Divide & Conquer Solver
def dnc_solver(state):

    if state == GOAL:
        return [state]

    path_total=[state]
    current=state

    # ---- DIVIDE → solve first row ----
    if current[:3] != GOAL[:3]:

        def row_goal(s):
            return s[:3]==GOAL[:3]

        path=astar(current,row_goal)
        path_total+=path[1:]
        current=path[-1]

    # ---- CONQUER → solve remaining ----
    def full_goal(s):
        return s==GOAL

    path=astar(current,full_goal)
    path_total+=path[1:]

    # ---- COMBINE ----
    return path_total
    
# HEURISTIC
def h(state):
    dist=0
    for i,v in enumerate(state):
        if v==0: continue
        goal=v-1
        r1,c1=divmod(i,3)
        r2,c2=divmod(goal,3)
        dist+=abs(r1-r2)+abs(c1-c2)
    return dist

