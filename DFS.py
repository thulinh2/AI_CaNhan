import pygame
import time

trangthaixuatphat = ((2, 6, 5),(1,4,3),(7,8,0))
trangthaidich = ((1, 2, 3),
                 (4, 5, 6),
                 (7, 8, 0))

huongdichuyen = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def timotrong(trangthai):
    for i in range(3):
        for j in range(3):
            if trangthai[i][j] == 0:
                return i, j

def hoandoi(trangthai, x1, y1, x2, y2):
    trangthaimoi = [list(hang) for hang in trangthai]
    trangthaimoi[x1][y1], trangthaimoi[x2][y2] = trangthaimoi[x2][y2], trangthaimoi[x1][y1]
    return tuple(tuple(hang) for hang in trangthaimoi)

def dfs(trangthaibatdau, trangthaimuctieu):
    nganxep = [(trangthaibatdau, [trangthaibatdau])]
    daxet = set()
    while nganxep:
        trangthai, duongdi = nganxep.pop()
        if trangthai == trangthaimuctieu:
            return duongdi
        if trangthai in daxet:
            continue
        daxet.add(trangthai)
        x, y = timotrong(trangthai)
        for dx, dy in huongdichuyen:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                trangthaimoi = hoandoi(trangthai, x, y, nx, ny)
                if trangthaimoi not in daxet:
                    nganxep.append((trangthaimoi, duongdi + [trangthaimoi]))
    return []

loigiai = dfs(trangthaixuatphat, trangthaidich)
print("So buoc giai:", len(loigiai))

pygame.init()
manhinh = pygame.display.set_mode((300, 300))
pygame.display.set_caption("8-Puzzle DFS")
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

dangchay = True
buoc = 0

vetrangthai(loigiai[0])
while dangchay:
    time.sleep(2)
    for sukien in pygame.event.get():
        if sukien.type == pygame.QUIT:
            dangchay = False
    if buoc < len(loigiai) - 1:
        buoc += 1
        vetrangthai(loigiai[buoc])
    else:
        dangchay = False

pygame.quit()
