import pygame
import time
import sys

trangthaixuatphat = ((2, 6, 5),(8,7,0),(4, 3, 1))
trangthaidich = ((1, 2, 3),(4, 5, 6),(7, 8, 0))
huongdichuyen = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def tim_o_trong(trangthai):
    for i in range(3):
        for j in range(3):
            if trangthai[i][j] == 0:
                return i, j

def hoandoi(trangthai, x1, y1, x2, y2):
    trangthaimoi = [list(hang) for hang in trangthai]
    trangthaimoi[x1][y1], trangthaimoi[x2][y2] = trangthaimoi[x2][y2], trangthaimoi[x1][y1]
    return tuple(tuple(hang) for hang in trangthaimoi)
# Triển khai Depth-Limited Search (DLS)
def dls(trangthai, trangthaimuctieu, depth, daxet, duongdi):
    # Nếu không còn độ sâu nào để tìm
    if depth == 0:
        if trangthai == trangthaimuctieu:
            return duongdi
        else:
            return None
    # Nếu chưa đến đích, ta mở rộng các trạng thái con
    x, y = tim_o_trong(trangthai)
    for dx, dy in huongdichuyen:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            trangthaimoi = hoandoi(trangthai, x, y, nx, ny)
            if trangthaimoi not in daxet:
                daxet.add(trangthaimoi)
                ketqua = dls(trangthaimoi, trangthaimuctieu, depth - 1, daxet, duongdi + [trangthaimoi])
                if ketqua is not None:
                    return ketqua
    return None

# Triển khai Iterative Deepening Search (IDS)
def IDS(trangthaibatdau, trangthaimuctieu):
    # Giới hạn tối đa, 8-Puzzle thường không cần quá 31 bước để giải
    for gioihan in range(32):
        daxet = set()
        daxet.add(trangthaibatdau)
        duongdi = [trangthaibatdau]
        ketqua = dls(trangthaibatdau, trangthaimuctieu, gioihan, daxet, duongdi)
        if ketqua is not None:
            return ketqua
    return []

loigiai = IDS(trangthaixuatphat, trangthaidich)
print("So buoc giai:", len(loigiai))
pygame.init()
manhinh = pygame.display.set_mode((300, 300))
pygame.display.set_caption("8-Puzzle Iterative Deepening")
phongchu = pygame.font.Font(None, 50)

def vetrangthai(trangthai):
    manhinh.fill((255, 255, 255))
    for i in range(3):
        for j in range(3):
            giatri = trangthai[i][j]
            if giatri != 0:
                pygame.draw.rect(manhinh, (0, 0, 0), (j * 100, i * 100, 100, 100), 2)
                chu = phongchu.render(str(giatri), True, (0, 0, 0))
                manhinh.blit(chu, (j * 100 + 35, i * 100 + 30))
    pygame.display.flip()
clock = pygame.time.Clock()
dangchay = True
buoc = 0

if len(loigiai) > 0:
    vetrangthai(loigiai[0])
else:
    print("Khong tim thay loi giai.")
while dangchay:
    for sukien in pygame.event.get():
        if sukien.type == pygame.QUIT:
            dangchay = False
    if buoc < len(loigiai) - 1:
        pygame.time.delay(2000) 
        buoc += 1
        vetrangthai(loigiai[buoc])
    else:
        pass
    clock.tick(60)
pygame.quit()
sys.exit()
