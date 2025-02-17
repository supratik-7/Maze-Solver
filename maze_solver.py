import tkinter as tk
from tkinter import messagebox
import random
from collections import deque
import time

def create_grid(rows, cols):
    for widget in grid_canvas.winfo_children():
        widget.destroy()
    global grid_buttons, grid_size
    grid_size = (rows, cols)

    # Calculate dynamic button dimensions based on grid size and frame size
    max_width = grid_outer_frame.winfo_width()
    max_height = grid_outer_frame.winfo_height()
    button_width = max(1, int(max_width / (cols * 10)))  # Scaled for better fit
    button_height = max(1, int(max_height / (rows * 20)))

    grid_buttons = [[tk.Button(grid_canvas, width=button_width, height=button_height, bg="white", command=lambda r=r, c=c: toggle_block(r, c))
                     for c in range(cols)] for r in range(rows)]
    for r in range(rows):
        for c in range(cols):
            grid_buttons[r][c].grid(row=r, column=c)

def set_grid():
    try:
        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
        if rows > 0 and cols > 0:
            create_grid(rows, cols)
        else:
            messagebox.showerror("Invalid Input", "Grid size must be positive integers.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integers for grid size.")

def toggle_block(r, c):
    if (r, c) != start_block and (r, c) != end_block:
        current_color = grid_buttons[r][c].cget("bg")
        grid_buttons[r][c].config(bg="black" if current_color == "white" else "white")

def generate_random_maze():
    rows, cols = grid_size
    for r in range(rows):
        for c in range(cols):
            if random.random() < maze_randomness / 100 and (r, c) != start_block and (r, c) != end_block:
                grid_buttons[r][c].config(bg="black")
            else:
                grid_buttons[r][c].config(bg="white")

def select_start_block():
    global selecting_start
    selecting_start = True

def select_end_block():
    global selecting_end
    selecting_end = True

def handle_grid_click(event):
    global selecting_start, selecting_end, start_block, end_block
    widget = event.widget
    row, col = None, None
    for r in range(len(grid_buttons)):
        if widget in grid_buttons[r]:
            row, col = r, grid_buttons[r].index(widget)
            break
    if row is not None and col is not None:
        if selecting_start:
            if start_block:
                grid_buttons[start_block[0]][start_block[1]].config(bg="white", text="")
            start_block = (row, col)
            grid_buttons[row][col].config(bg="green", text="0")
            selecting_start = False
        elif selecting_end:
            if end_block:
                grid_buttons[end_block[0]][end_block[1]].config(bg="white", text="")
            end_block = (row, col)
            grid_buttons[row][col].config(bg="red", text="0")
            selecting_end = False

def assign_path_weights(path):
    for idx, (r, c) in enumerate(path):
        if (r, c) != start_block and (r, c) != end_block:
            weight = abs(end_block[0] - r) + abs(end_block[1] - c)
            grid_buttons[r][c].config(text=str(weight))

def animate_path(path):
    for i, (r, c) in enumerate(path):
        if (r, c) != start_block and (r, c) != end_block:
            grid_buttons[r][c].config(bg="green" if i == 0 else "yellow")
            grid_canvas.update()
            time.sleep(0.1)

def find_shortest_path():
    if not start_block or not end_block:
        messagebox.showwarning("Missing Blocks", "Please select start and end blocks.")
        return

    rows, cols = grid_size
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start_block[0], start_block[1], [])])
    visited = set()

    while queue:
        r, c, path = queue.popleft()
        if (r, c) == end_block:
            path_with_end = path + [(r, c)]
            assign_path_weights(path_with_end)
            animate_path(path_with_end)
            return

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if grid_buttons[nr][nc].cget("bg") != "black":
                    queue.append((nr, nc, path + [(r, c)]))
                    visited.add((nr, nc))

    messagebox.showinfo("No Path", "No path found between start and end blocks.")

def reset_grid():
    for widget in grid_canvas.winfo_children():
        widget.destroy()
    global start_block, end_block, grid_buttons
    start_block = None
    end_block = None
    grid_buttons = []

def set_randomness():
    try:
        global maze_randomness
        maze_randomness = float(randomness_entry.get())
        if not (0 <= maze_randomness <= 100):
            raise ValueError
        messagebox.showinfo("Randomness Set", f"Maze randomness set to {maze_randomness}%")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a value between 0 and 100.")

app = tk.Tk()
app.title("Maze Solver")
app.geometry("1150x700")

main_frame = tk.Frame(app, bg="#f8f9fa")
main_frame.pack(fill=tk.BOTH, expand=True)

# Heading frame
heading_frame = tk.Frame(main_frame, bg="#212529")
heading_frame.pack(fill=tk.X, pady=5)
heading_label = tk.Label(heading_frame, text="Micro-mouse Maze Solver", font=("Helvetica", 20, "bold"), fg="white", bg="#212529")
heading_label.pack()

control_frame = tk.Frame(main_frame, bg="#f8f9fa", relief=tk.GROOVE, borderwidth=2)
control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

grid_outer_frame = tk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=2, bg="#dee2e6")
grid_outer_frame.place(relx=0.5, rely=0.5, anchor="center")

canvas_scrollbar_y = tk.Scrollbar(grid_outer_frame, orient=tk.VERTICAL)
canvas_scrollbar_x = tk.Scrollbar(grid_outer_frame, orient=tk.HORIZONTAL)

grid_canvas = tk.Canvas(grid_outer_frame, yscrollcommand=canvas_scrollbar_y.set, xscrollcommand=canvas_scrollbar_x.set, bg="#f8f9fa")
canvas_scrollbar_y.config(command=grid_canvas.yview)
canvas_scrollbar_x.config(command=grid_canvas.xview)
canvas_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
canvas_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
grid_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

grid_buttons = []
start_block = None
end_block = None
selecting_start = False
selecting_end = False
maze_randomness = 30

# All options under one frame
options_frame = tk.Frame(control_frame, bg="#f8f9fa")
options_frame.pack(fill=tk.X, padx=5, pady=5)

# Input grid size
size_label = tk.Label(options_frame, text="Grid Size (Rows x Cols):", font=("Helvetica", 12, "bold"), bg="#f8f9fa")
size_label.grid(row=0, column=0, columnspan=2, sticky="w")

rows_entry = tk.Entry(options_frame, width=10, font=("Helvetica", 12))
rows_entry.grid(row=1, column=0, sticky="w")

cols_entry = tk.Entry(options_frame, width=10, font=("Helvetica", 12))
cols_entry.grid(row=1, column=1, sticky="w")

set_grid_btn = tk.Button(options_frame, text="Set Grid", command=set_grid, font=("Helvetica", 12, "bold"), bg="#007bff", fg="white", activebackground="#0056b3")
set_grid_btn.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

# Maze randomness option
randomness_label = tk.Label(options_frame, text="Obstacle Percentage(0-100%):", font=("Helvetica", 12, "bold"), bg="#f8f9fa")
randomness_label.grid(row=3, column=0, sticky="w")

randomness_entry = tk.Entry(options_frame, width=10, font=("Helvetica", 12))
randomness_entry.grid(row=3, column=1, sticky="w")

set_randomness_btn = tk.Button(options_frame, text="Set Obstacle Percentage", command=set_randomness, font=("Helvetica", 12, "bold"), bg="#007bff", fg="white", activebackground="#0056b3")
set_randomness_btn.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

# Maze generation options
maze_mode = tk.StringVar(value="manual")

manual_radio = tk.Radiobutton(options_frame, text="Manual Maze", variable=maze_mode, value="manual", font=("Helvetica", 12), bg="#f8f9fa")
manual_radio.grid(row=5, column=0, columnspan=2, sticky="w")

random_radio = tk.Radiobutton(options_frame, text="Random Maze", variable=maze_mode, value="random", command=generate_random_maze, font=("Helvetica", 12), bg="#f8f9fa")
random_radio.grid(row=6, column=0, columnspan=2, sticky="w")

# Buttons for start, end, and find path
start_btn = tk.Button(options_frame, text="Set Start", command=select_start_block, font=("Helvetica", 12, "bold"), bg="#28a745", fg="white", activebackground="#218838")
start_btn.grid(row=7, column=0, columnspan=2, pady=5, sticky="w")

end_btn = tk.Button(options_frame, text="Set End", command=select_end_block, font=("Helvetica", 12, "bold"), bg="#dc3545", fg="white", activebackground="#c82333")
end_btn.grid(row=8, column=0, columnspan=2, pady=5, sticky="w")

path_btn = tk.Button(options_frame, text="Find Path", command=find_shortest_path, font=("Helvetica", 12, "bold"), bg="#17a2b8", fg="white", activebackground="#117a8b")
path_btn.grid(row=9, column=0, columnspan=2, pady=5, sticky="w")

reset_btn = tk.Button(options_frame, text="Reset", command=reset_grid, font=("Helvetica", 12, "bold"), bg="#ffc107", fg="black", activebackground="#e0a800")
reset_btn.grid(row=10, column=0, columnspan=2, pady=5, sticky="w")

# Bind grid click events
grid_canvas.bind_all("<Button-1>", handle_grid_click)

app.mainloop()
