import pygame
import numpy as np
import heapq
import time

trangthaixuatphat = ((2, 6, 5), (8, 7, 0), (4, 3, 1))
trangthaidich = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
huongdichuyen = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def tim_o_trong(trangthai):
    # Tìm vị trí ô trống trong ma trận
    for i in range(3):
        for j in range(3):
            if trangthai[i][j] == 0:
                return i, j

def hoandoi(trangthai, x1, y1, x2, y2):
    trangthaimoi = [list(hang) for hang in trangthai]
    trangthaimoi[x1][y1], trangthaimoi[x2][y2] = trangthaimoi[x2][y2], trangthaimoi[x1][y1]
    return tuple(tuple(hang) for hang in trangthaimoi)

def ucs(trangthaibatdau, trangthaimuctieu):
    hangdoiuutien = [(0, trangthaibatdau, [])]  # (chiphi, trangthai, duongdi)
    daxet = set()
    while hangdoiuutien:
        chiphi, trangthai, duongdi = heapq.heappop(hangdoiuutien)
        if trangthai in daxet:
            continue
        daxet.add(trangthai)
        if trangthai == trangthaimuctieu:
            return duongdi + [trangthai]
        x, y = tim_o_trong(trangthai)
        for dx, dy in huongdichuyen:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                trangthaimoi = hoandoi(trangthai, x, y, nx, ny)
                heapq.heappush(hangdoiuutien, (chiphi + 1, trangthaimoi, duongdi + [trangthaimoi]))
    return []

loigiai = ucs(trangthaixuatphat, trangthaidich)
print("So buoc giai:", len(loigiai))
pygame.init()
manhinh = pygame.display.set_mode((300, 300))
pygame.display.set_caption("8-Puzzle UCS")
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
