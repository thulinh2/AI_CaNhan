import tkinter as tk
from tkinter import messagebox
import time
import heapq
from collections import deque

###############################
# Cấu hình bài toán 8-puzzle
###############################

goal_state = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

initial_state = (2, 6, 5,
                 0, 8, 7,
                 4, 3, 1)

def get_neighbors(state):
    neighbors = []
    index = state.index(0)
    row, col = index // 3, index % 3
    directions = []
    if row > 0:
        directions.append((-1, 0))
    if row < 2:
        directions.append((1, 0))
    if col > 0:
        directions.append((0, -1))
    if col < 2:
        directions.append((0, 1))
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        new_index = new_row * 3 + new_col
        new_state = list(state)
        new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
        neighbors.append((tuple(new_state), None, 1))
    return neighbors

def manhattan(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_row = (tile - 1) // 3
        goal_col = (tile - 1) % 3
        cur_row = i // 3
        cur_col = i % 3
        distance += abs(goal_row - cur_row) + abs(goal_col - cur_col)
    return distance

###############################
# Các thuật toán tìm kiếm
###############################

def dfs(start):
    stack = [(start, [start])]
    visited = set()
    while stack:
        state, path = stack.pop()
        if state == goal_state:
            return path
        if state in visited:
            continue
        visited.add(state)
        for neighbor, _, _ in get_neighbors(state):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return None

def bfs(start):
    queue = deque([(start, [start])])
    visited = set([start])
    while queue:
        state, path = queue.popleft()
        if state == goal_state:
            return path
        for neighbor, _, _ in get_neighbors(state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

def ucs(start):
    heap = [(0, start, [start])]
    visited = {}
    while heap:
        cost, state, path = heapq.heappop(heap)
        if state == goal_state:
            return path
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        for neighbor, _, step_cost in get_neighbors(state):
            new_cost = cost + step_cost
            heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))
    return None

def ids(start):
    def dls(state, path, depth):
        if depth == 0:
            if state == goal_state:
                return path
            return None
        for neighbor, _, _ in get_neighbors(state):
            if neighbor not in path:
                result = dls(neighbor, path + [neighbor], depth - 1)
                if result is not None:
                    return result
        return None

    depth = 0
    while True:
        result = dls(start, [start], depth)
        if result is not None:
            return result
        depth += 1

def greedy_search(start):
    heap = [(manhattan(start), start, [start])]
    visited = set()
    while heap:
        h, state, path = heapq.heappop(heap)
        if state == goal_state:
            return path
        if state in visited:
            continue
        visited.add(state)
        for neighbor, _, _ in get_neighbors(state):
            if neighbor not in visited:
                heapq.heappush(heap, (manhattan(neighbor), neighbor, path + [neighbor]))
    return None

def a_star(start):
    heap = [(manhattan(start), 0, start, [start])]
    visited = {}
    while heap:
        f, cost, state, path = heapq.heappop(heap)
        if state == goal_state:
            return path
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        for neighbor, _, step_cost in get_neighbors(state):
            new_cost = cost + step_cost
            heapq.heappush(heap, (new_cost + manhattan(neighbor), new_cost, neighbor, path + [neighbor]))
    return None

def ida_star(start):
    def search(path, g, threshold):
        state = path[-1]
        f = g + manhattan(state)
        if f > threshold:
            return f
        if state == goal_state:
            return path
        mini = float('inf')
        for neighbor, _, step_cost in get_neighbors(state):
            if neighbor not in path:
                path.append(neighbor)
                temp = search(path, g + step_cost, threshold)
                if isinstance(temp, list):
                    return temp
                if temp < mini:
                    mini = temp
                path.pop()
        return mini

    threshold = manhattan(start)
    path = [start]
    while True:
        temp = search(path, 0, threshold)
        if isinstance(temp, list):
            return temp
        if temp == float('inf'):
            return None
        threshold = temp

###############################
# Giao diện Tkinter
###############################

class EightPuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Nguyễn Thị Thu Linh: 23110254")
        self.stop_flag = False
        self.current_solution = None
        self.current_index = 0

        # Khung trái
        self.left_frame = tk.Frame(self.master, bg="#ecf0f1", bd=2, relief="groove")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Tạo một Frame chứa các nút thuật toán ở phía trên
        self.algo_frame = tk.Frame(self.left_frame, bg="#ecf0f1")
        self.algo_frame.pack(side=tk.TOP, fill=tk.Y)

        # Các thuật toán
        self.algos = {
            "BFS": bfs,
            "DFS": dfs,
            "UCS": ucs,
            "IDS": ids,
            "A*": a_star,
            "IDA*": ida_star,
            "Greedy": greedy_search
        }

        # Khởi tạo dictionary chứa các nút
        self.algo_buttons = {}
        for algo_name in ["BFS", "DFS", "UCS", "IDS", "A*", "IDA*", "Greedy"]:
            btn = tk.Button(
                self.algo_frame, 
                text=algo_name, 
                width=10,
                command=lambda name=algo_name: self.run_algorithm(name),
                bg="#d3d3d3",             # Màu nền xám nhạt mặc định
                fg="black",
                activebackground="#a9a9a9",  # Màu nền khi nhấn (xám đậm hơn một chút)
                activeforeground="white",
                font=("Arial", 10, "normal")
            )
            btn.pack(padx=5, pady=5)
            self.algo_buttons[algo_name] = btn

        # Tạo một Frame riêng để chứa 3 nút Stop, Continue, Reset ở dưới
        self.bottom_btn_frame = tk.Frame(self.left_frame, bg="#ecf0f1")
        # Ghim frame này xuống cuối
        self.bottom_btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Nút Stop
        self.stop_button = tk.Button(self.bottom_btn_frame, text="Stop", width=10, command=self.stop_animation)
        self.stop_button.pack(pady=5)

        # Nút Continue
        self.continue_button = tk.Button(self.bottom_btn_frame, text="Continue", width=10, command=self.continue_animation)
        self.continue_button.pack(pady=5)

        # Nút Reset
        self.reset_button = tk.Button(self.bottom_btn_frame, text="Reset", width=10, command=self.reset)
        self.reset_button.pack(pady=5)

        # Khung chính (bên phải)
        self.main_frame = tk.Frame(self.master, bg="white")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Khung Start
        self.start_frame = tk.Frame(self.main_frame, bg="white")
        self.start_frame.grid(row=0, column=0, padx=10, pady=10)
        self.start_label = tk.Label(self.start_frame, text="Start", fg="red", font=("Arial", 16, "bold"), bg="white")
        self.start_label.pack()
        self.start_cells = self.create_puzzle_board(self.start_frame, bg_color="#2ecc71")  # xanh

        # Khung End
        self.end_frame = tk.Frame(self.main_frame, bg="white")
        self.end_frame.grid(row=0, column=1, padx=10, pady=10)
        self.end_label = tk.Label(self.end_frame, text="End", fg="red", font=("Arial", 16, "bold"), bg="white")
        self.end_label.pack()
        self.end_cells = self.create_puzzle_board(self.end_frame, bg_color="#2ecc71")  # xanh

        # Khung Current
        self.current_frame = tk.Frame(self.main_frame, bg="white")
        self.current_frame.grid(row=1, column=0, padx=10, pady=10)
        self.current_label = tk.Label(self.current_frame, text="Current", fg="Purple", font=("Arial", 16, "bold"), bg="white")
        self.current_label.pack()
        self.current_cells = self.create_puzzle_board(self.current_frame, bg_color="#9b59b6")  # tím

        # Khung Detail
        self.detail_frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="groove")
        self.detail_frame.grid(row=1, column=1, padx=10, pady=10)
        self.detail_label_title = tk.Label(self.detail_frame, text="Detail", font=("Arial", 16, "bold"), bg="white")
        self.detail_label_title.pack(pady=5)
        self.detail_step_label = tk.Label(self.detail_frame, text="Step :", font=("Arial", 14), bg="white")
        self.detail_step_label.pack(pady=5)

        # Khởi tạo giá trị
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.draw_board(self.start_cells, self.initial_state)
        self.draw_board(self.end_cells, self.goal_state)
        self.current_state = self.initial_state
        self.draw_board(self.current_cells, self.current_state)

    def create_puzzle_board(self, parent, bg_color="#2ecc71"):
        cells = []
        board_frame = tk.Frame(parent, bg="white")
        board_frame.pack()
        for i in range(3):
            row_cells = []
            for j in range(3):
                lbl = tk.Label(board_frame, text="", font=("Arial", 18, "bold"),
                               width=2, height=1, bd=2, relief="ridge",
                               bg=bg_color, fg="white")
                lbl.grid(row=i, column=j, padx=3, pady=3)
                row_cells.append(lbl)
            cells.append(row_cells)
        return cells

    def draw_board(self, cells, state):
        for i in range(3):
            for j in range(3):
                val = state[i * 3 + j]
                text = str(val) if val != 0 else ""
                cells[i][j].config(text=text)

    def run_algorithm(self, algo_name):
        self.stop_flag = False
        # Đặt lại màu nền cho tất cả các nút về mặc định
        for name, button in self.algo_buttons.items():
            button.config(bg="#d3d3d3", fg="black", font=("Arial", 10, "normal"))
        
        # Cập nhật nút của thuật toán được chọn với màu nền đậm hơn
        self.algo_buttons[algo_name].config(bg="#808080", fg="white", font=("Arial", 10, "bold"))
        
        algo_func = self.algos[algo_name]
        solution = algo_func(self.initial_state)
        if solution is None:
            messagebox.showinfo("Thông báo", "Không tìm thấy bước giải!")
            return
        
        self.current_solution = solution
        self.current_index = 0
        self.animate_solution(self.current_solution, self.current_index)


    def animate_solution(self, solution, index):
        # Nếu đang dừng thì thoát
        if self.stop_flag:
            return

        if index < len(solution):
            state = solution[index]
            self.draw_board(self.current_cells, state)
            self.detail_step_label.config(text=f"Step : {index}")
            # Lưu lại chỉ số tiếp theo
            self.current_index = index + 1
            # Gọi animate kế tiếp sau 700ms
            self.master.after(700, lambda: self.animate_solution(solution, self.current_index))

    def stop_animation(self):
        self.stop_flag = True

    def continue_animation(self):
        # Nếu còn trạng thái để chạy tiếp
        if self.current_solution and self.current_index < len(self.current_solution):
            self.stop_flag = False
            self.animate_solution(self.current_solution, self.current_index)

    def reset(self):
        self.stop_flag = True
        self.current_state = self.initial_state
        self.draw_board(self.current_cells, self.current_state)
        self.detail_step_label.config(text="Step :")
        self.current_solution = None
        self.current_index = 0
        # Đặt lại giao diện cho các nút về trạng thái ban đầu (màu xám nhạt)
        for button in self.algo_buttons.values():
            button.config(bg="#d3d3d3", fg="black", font=("Arial", 10, "normal"))


###############################
# Chạy chương trình
###############################
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    
    app = EightPuzzleGUI(root)
    root.mainloop()