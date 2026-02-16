import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from copy import deepcopy
import random
import os
from collections import deque

# ------------------ PATH SETUP (IMPORTANT FIX) ------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ CONSTANTS ------------------

TILE = 160
BOARD_SIZE = 480
BG_COLOR = "misty rose"

GOAL = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]]

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# ------------------ UTILITY FUNCTIONS ------------------

def find_zero(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def state_to_tuple(state):
    return tuple(state[r][c] for r in range(3) for c in range(3))










# ------------------ GUI APPLICATION ------------------

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        root.title("8-Puzzle — User vs Divide & Conquer")
        root.geometry("1200x800")
        root.configure(bg=BG_COLOR)

        self.user_state = deepcopy(GOAL)
        self.dnc_state  = deepcopy(GOAL)

        self.user_steps = 0
        self.dnc_steps  = 0

        self.image_name = "dog.jpg"

        self.build_top()
        self.build_sidebar()
        self.build_center()
        self.load_image()
        self.update_boards()

    def build_top(self):
        bar = tk.Frame(self.root, bg="Dark slate grey", height=80)
        bar.pack(fill="x")

        tk.Label(
            bar,
            text="8-Puzzle — User vs Divide & Conquer",
            bg="Dark slate grey",
            fg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=10)

    def build_sidebar(self):
        side = tk.Frame(self.root, bg="Dark slate grey", width=200)
        side.pack(side="left", fill="y")

        images = ["dog.jpg", "girl.jpg", "bike.jpg",
                  "tiger.jpg", "mickey.jpg", "snowwhite.jpg"]

        for img in images:
            img_path = os.path.join(BASE_DIR, img)
            if not os.path.exists(img_path):
                continue
            im = Image.open(img_path).resize((90, 90))
            tk_img = ImageTk.PhotoImage(im)
            b = tk.Button(side, image=tk_img, bd=0,
                          command=lambda x=img: self.change_image(x))
            b.image = tk_img
            b.pack(pady=10)

    def build_center(self):
        center = tk.Frame(self.root, bg=BG_COLOR)
        center.pack(expand=True)

        boards = tk.Frame(center, bg=BG_COLOR)
        boards.pack()

        self.user_tiles = self.create_board(boards, "USER",             self.move_user)
        self.dnc_tiles  = self.create_board(boards, "DIVIDE & CONQUER", None)

        controls = tk.Frame(center, bg=BG_COLOR)
        controls.pack(pady=20)

        tk.Button(controls, text="Shuffle", font=("Segoe UI", 14),
                  width=12, command=self.shuffle).pack(side="left", padx=10)

        tk.Button(controls, text="Solve (D&C)", font=("Segoe UI", 14),
                  width=12, command=self.solve_dnc).pack(side="left", padx=10)

        self.info_lbl = tk.Label(
            center,
            text="User Steps: 0 | D&C Steps: 0",
            font=("Segoe UI", 14),
            bg=BG_COLOR
        )
        self.info_lbl.pack()

        self.phase_lbl = tk.Label(
            center,
            text="",
            font=("Segoe UI", 12, "italic"),
            bg=BG_COLOR,
            fg="dark slate grey"
        )
        self.phase_lbl.pack()

    def create_board(self, parent, title, command):
        frame = tk.Frame(parent, bg=BG_COLOR)
        frame.pack(side="left", padx=40)

        tk.Label(frame, text=title,
                 font=("Segoe UI", 16, "bold"),
                 bg=BG_COLOR).pack()

        board = tk.Frame(frame, bg="black",
                         width=BOARD_SIZE, height=BOARD_SIZE)
        board.pack(pady=10)
        board.pack_propagate(False)

        tiles = []
        for r in range(3):
            for c in range(3):
                b = tk.Button(board, bd=0, bg="black",
                              activebackground="black",
                              command=(lambda r=r, c=c: command(r, c))
                              if command else None)
                b.grid(row=r, column=c)
                tiles.append(b)
        return tiles

    def load_image(self):
        img_path = os.path.join(BASE_DIR, self.image_name)
        img = Image.open(img_path).resize((BOARD_SIZE, BOARD_SIZE))
        self.cuts = []
        for i in range(8):
            r, c = divmod(i, 3)
            piece = img.crop(
                (c * TILE, r * TILE,
                 (c + 1) * TILE, (r + 1) * TILE))
            self.cuts.append(ImageTk.PhotoImage(piece))
        self.cuts.append(None)

    def change_image(self, img):
        self.image_name = img
        self.load_image()
        self.update_boards()

    def update_boards(self):
        self.update_board(self.user_tiles, self.user_state)
        self.update_board(self.dnc_tiles,  self.dnc_state)
        self.info_lbl.config(
            text=f"User Steps: {self.user_steps} | D&C Steps: {self.dnc_steps}")

    def update_board(self, tiles, state):
        for i in range(9):
            r, c = divmod(i, 3)
            v = state[r][c]
            tiles[i].config(image="" if v == 0 else self.cuts[v - 1])

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
        self.dnc_state  = deepcopy(state)
        self.user_steps = 0
        self.dnc_steps  = 0
        self.phase_lbl.config(text="")
        self.update_boards()

    def solve_dnc(self):
        self.dnc_steps = 0
        path = dnc_solver(deepcopy(self.dnc_state))
        self.animate_dnc(path, 0)

    def animate_dnc(self, path, i):
        if i < len(path):
            state = path[i]

            # Show which D&C phase (subproblem) is currently being solved
            row0_done = all(state[0][c] == GOAL[0][c] for c in range(3))
            row1_done = all(state[1][c] == GOAL[1][c] for c in range(3))

            if row0_done and row1_done:
                self.phase_lbl.config(
                    text="D&C Phase 3 — Solving bottom row [7, 8]")
            elif row0_done:
                self.phase_lbl.config(
                    text="D&C Phase 2 — Solving middle row [4, 5, 6]")
            else:
                self.phase_lbl.config(
                    text="D&C Phase 1 — Solving top row [1, 2, 3]")

            if i > 0:
                self.dnc_steps += 1
            self.dnc_state = deepcopy(state)
            self.update_boards()
            self.root.after(400, lambda: self.animate_dnc(path, i + 1))
        else:
            self.phase_lbl.config(text="D&C: All 3 subproblems solved!")
