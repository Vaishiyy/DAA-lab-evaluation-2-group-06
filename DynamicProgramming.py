import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from copy import deepcopy
from collections import deque
import random
import os

# CONSTANTS 

TILE = 160
BOARD_SIZE = 480
BG_COLOR = "misty rose"

GOAL = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]]

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# DP (BFS) SOLVER 

def state_to_string(state):
    return ''.join(str(cell) for row in state for cell in row)

def string_to_state(s):
    nums = list(map(int, s))
    return [nums[i:i+3] for i in range(0, 9, 3)]

def find_zero(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

# GAMEPLAY

def move_user(self, r, c):
zr, zc = find_zero(self.user_state)
if abs(r - zr) + abs(c - zc) == 1:
    self.user_state[zr][zc], self.user_state[r][c] = \
        self.user_state[r][c], 0
    self.user_steps += 1
    self.update_boards()

    if self.user_state == GOAL:
        messagebox.showinfo(
            "User Solved",
            f"You solved it in {self.user_steps} steps!")

def shuffle(self):
state = deepcopy(GOAL)
for _ in range(150):
    zr, zc = find_zero(state)
    dr, dc = random.choice(DIRS)
    nr, nc = zr + dr, zc + dc
    if 0 <= nr < 3 and 0 <= nc < 3:
        state[zr][zc], state[nr][nc] = state[nr][nc], 0

self.user_state = deepcopy(state)
self.ai_state = deepcopy(state)
self.user_steps = 0
self.ai_steps = 0
self.update_boards()

# ---------- DP MACHINE ----------

def solve_ai(self):
self.ai_steps = 0
path = solve_with_dp(deepcopy(self.ai_state))
self.animate_ai(path, 0)
