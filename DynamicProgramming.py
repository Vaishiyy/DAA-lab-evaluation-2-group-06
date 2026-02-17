import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from copy import deepcopy
import random
from collections import deque
import os

# PATH SETUP 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#  CONSTANTS 

TILE = 160
BOARD_SIZE = 480
BG_COLOR = "misty rose"

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#  DP TABLE 

dp_table = {}


def build_dp_table():
    if dp_table:
        return

    queue = deque([GOAL_STATE])
    dp_table[GOAL_STATE] = None

    while queue:
        curr = queue.popleft()

        idx = curr.index(0)
        r, c = divmod(idx, 3)

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                ni = nr * 3 + nc
                nxt = list(curr)
                nxt[idx], nxt[ni] = nxt[ni], nxt[idx]
                nxt = tuple(nxt)

                if nxt not in dp_table:
                    dp_table[nxt] = curr
                    queue.append(nxt)

def reconstruct_path(start):
    if start not in dp_table:
        return []

    path = [start]
    curr = start

    while curr != GOAL_STATE:
        curr = dp_table[curr]
        path.append(curr)

    return path
    
class PuzzleApp:
        def find_zero(self, state):
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    return r, c

    def move_user(self, r, c):
        if not self.round_active or self.ai_solving or self.user_finished:
            return

        zr, zc = self.find_zero(self.user_state)

        if abs(r - zr) + abs(c - zc) == 1:
            self.user_state[zr][zc], self.user_state[r][c] = self.user_state[r][c], 0
            self.user_steps += 1
            self.update_boards()

            if self.user_state == self.goal_grid:
                self.user_finished = True
                self.round_active = False
                self.status_lbl.config(text="Status: User solved. Click AI Solve for result.")
                messagebox.showinfo("User Solved", f"You solved it in {self.user_steps} moves.")

    def shuffle(self):
        state = deepcopy(self.goal_grid)

        for _ in range(150):
            zr, zc = self.find_zero(state)
            dr, dc = random.choice(DIRS)
            nr, nc = zr + dr, zc + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                state[zr][zc], state[nr][nc] = state[nr][nc], 0

        self.user_state = deepcopy(state)
        self.ai_state = deepcopy(state)

        self.user_steps = 0
        self.ai_steps = 0

        self.user_finished = False
        self.ai_finished = False
        self.ai_solving = False
        self.round_active = True

        self.status_lbl.config(text="Status: Round active")
        self.update_boards()

    def solve(self):
        if not self.round_active and not self.user_finished:
            messagebox.showinfo("Ai Solve", "Press Shuffle to start a round first.")
            return

        if self.ai_solving or self.ai_finished:
            return

        self.ai_solving = True
        self.round_active = False
        self.status_lbl.config(text="Status: AI solving...")
        self.update_boards()

        start = tuple(x for row in self.ai_state for x in row)
        path = reconstruct_path(start)

        if not path:
            self.ai_solving = False
            self.status_lbl.config(text="Status: No solution from current state")
            messagebox.showinfo("AI Solver", "No solution exists!")
            return

        self.animate(path, 0)

