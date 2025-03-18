import numpy as np
import pygame

dich = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

def oVuong(manHinh, trangThai):
    manHinh.fill((255, 255, 255))
    font = pygame.font.Font(None, 50)
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(manHinh, (0, 0, 0), (j * 100, i * 100, 100, 100), 1)
            if trangThai[i][j] != 0:
                o = font.render(str(trangThai[i][j]), True, (0, 0, 0))
                manHinh.blit(o, (j * 100 + 35, i * 100 + 25))
    pygame.display.flip()

class Puzzle:
    def __init__(self, trangThai, cost=0):
        self.trangThai = np.array(trangThai)
        self.viTri0 = tuple(map(int, np.where(self.trangThai == 0)))
        self.cost = cost
    
    def __eq__(self, other):
        return np.array_equal(self.trangThai, other.trangThai)
    
    def __hash__(self):
        return hash(self.trangThai.tobytes())
    
    # Phương thức __lt__ vẫn giữ để có thể so sánh nếu cần,
    # tuy nhiên trong DFS, chúng ta không dựa vào cost để sắp xếp.
    def __lt__(self, other):
        return self.cost < other.cost
    
    def taoTrangThaiMoi(self, huong):
        x, y = self.viTri0
        dichChuyen = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}
        dx, dy = dichChuyen[huong]
        xMoi, yMoi = x + dx, y + dy
        if 0 <= xMoi < 3 and 0 <= yMoi < 3:
            trangThaiMoi = self.trangThai.copy()
            trangThaiMoi[x, y], trangThaiMoi[xMoi, yMoi] = trangThaiMoi[xMoi, yMoi], trangThaiMoi[x, y]
            return Puzzle(trangThaiMoi, self.cost + 1)
        return None

def DFS(trangThaiBanDau):
    # Sử dụng stack (danh sách) với phần tử (Puzzle, đường đi)
    stack = [(Puzzle(trangThaiBanDau), [])]
    daTham = set()
    
    while stack:
        trangThaiHienTai, duongDi = stack.pop()  # Lấy phần tử cuối của stack (LIFO)
        
        # Nếu đã đạt được trạng thái đích, trả về đường đi
        if trangThaiHienTai == Puzzle(dich):
            return duongDi
        
        if trangThaiHienTai not in daTham:
            daTham.add(trangThaiHienTai)
            # Duyệt 4 hướng: L, R, U, D
            for huong in ['L', 'R', 'U', 'D']:
                trangThaiMoi = trangThaiHienTai.taoTrangThaiMoi(huong)
                if trangThaiMoi and trangThaiMoi not in daTham:
                    stack.append((trangThaiMoi, duongDi + [huong])) 
    return None

def chayGiaoDien():
    pygame.init()
    manHinh = pygame.display.set_mode((300, 300))
    # Trạng thái ban đầu của bài 8-puzzle
    trangThai = np.array([[2, 6, 5], [8, 7, 0], [4, 3, 1]])
    # Tìm lời giải bằng thuật toán DFS
    ketQua = DFS(trangThai.tolist())
    
    if ketQua is None:
        print("Không tìm được lời giải!")
        pygame.quit()
        return
    
    oVuong(manHinh, trangThai)
    chay = True
    buoc = 0
    while chay:
        for suKien in pygame.event.get():
            if suKien.type == pygame.QUIT:
                chay = False
            if suKien.type == pygame.KEYDOWN:
                if buoc < len(ketQua):
                    huong = ketQua[buoc]
                    puzzle = Puzzle(trangThai)
                    trangThaiMoi = puzzle.taoTrangThaiMoi(huong)
                    if trangThaiMoi:
                        trangThai = trangThaiMoi.trangThai
                        oVuong(manHinh, trangThai)
                        buoc += 1
    pygame.quit()

chayGiaoDien()
