# from errors import ConfigFormatError
from collections import deque
import random


class Cell:
    def __init__(self, i: int, j: int) -> None:
        self.bords = "1111"
        self.i = i
        self.j = j
        self.mat_i = i * 3 + 1
        self.mat_j = j * 3 + 1
        self.is_entry = False
        self.is_exit = False
        self.is_f2 = False
        self.is_visited = False


class MazeGenerator:
    def __init__(self, width, height, entry, exit):
        self.cells = [[Cell(i, j) for j in range(0, width)]
                      for i in range(0, height)]
        self.cells[entry[1]][entry[0]].is_entry = True
        self.cells[exit[1]][exit[0]].is_exit = True
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.solution = dict()

    def gen_f2(self) -> None:
        ns = int((self.height - 5) / 2)
        ws = int((self.width - 5) / 2)
        self.cells[ns][ws].is_f2 = True
        self.cells[ns+1][ws].is_f2 = True
        self.cells[ns+2][ws].is_f2 = True
        self.cells[ns+2][ws+1].is_f2 = True
        self.cells[ns+2][ws+2].is_f2 = True
        self.cells[ns+3][ws+2].is_f2 = True
        self.cells[ns+4][ws+2].is_f2 = True
        self.cells[ns][ws+4].is_f2 = True
        self.cells[ns][ws+5].is_f2 = True
        self.cells[ns][ws+6].is_f2 = True
        self.cells[ns+1][ws+6].is_f2 = True
        self.cells[ns+2][ws+6].is_f2 = True
        self.cells[ns+2][ws+5].is_f2 = True
        self.cells[ns+2][ws+4].is_f2 = True
        self.cells[ns+3][ws+4].is_f2 = True
        self.cells[ns+4][ws+4].is_f2 = True
        self.cells[ns+4][ws+5].is_f2 = True
        self.cells[ns+4][ws+6].is_f2 = True

    def renew(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.bords = "1111"
                cell.is_f2 = False
                cell.is_visited = False

    def get_neighboor(self, i: int, j: int) -> list[Cell]:
        neighboors = []
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        cells = self.cells
        for di, dj in directions:
            if 0 <= di + i < self.height:
                if 0 <= dj + j < self.width:
                    cell = cells[di + i][dj + j]
                    if not (cell.is_f2 or cell.is_visited):
                        neighboors.append(cell)
        return neighboors

    def berlini_pat(self, i1: int, j1: int, i2: int, j2: int) -> None:
        direct = (i2 - i1, j2 - j1)
        directions = {
            (-1, 0): 0,
            (0, 1): 1,
            (1, 0): 2,
            (0, -1): 3
        }
        n = directions[direct]
        first = self.cells[i1][j1].bords
        first = first[:n] + '0' + first[n + 1:]
        n = (n + 2) % 4
        second = self.cells[i2][j2].bords
        second = second[:n] + '0' + second[n + 1:]
        self.cells[i1][j1].bords = first
        self.cells[i2][j2].bords = second

    def solve(self) -> None:
        parent = dict()
        parent[(self.entry[1], self.entry[0])] = None
        visited = set()
        visited.add((self.entry[1], self.entry[0]))
        cells = deque()
        cells.append((self.entry[1], self.entry[0]))
        while cells:
            leave = False
            current = cells.popleft()
            neighboors = self.solve_neighboors(current[0], current[1])
            for neighboor in neighboors:
                if neighboor.is_exit:
                    parent[(neighboor.i,
                            neighboor.j)] = current
                    leave = True
                    break
                elif (neighboor.i,
                      neighboor.j) not in visited:
                    parent[(neighboor.i,
                            neighboor.j)] = current
                    cells.append((neighboor.i, neighboor.j))
                    visited.add((neighboor.i,
                                 neighboor.j))
            if leave:
                break
        self.solution = parent

    def check_walls(self, i1: int, j1: int, i2: int, j2: int) -> bool:
        direct = (i2 - i1, j2 - j1)
        directions = {
            (-1, 0): 0,
            (0, 1): 1,
            (1, 0): 2,
            (0, -1): 3
        }
        n = directions[direct]
        firstR = self.cells[i1][j1].bords
        firstE = firstR[:n] + '0' + firstR[n + 1:]
        n = (n + 2) % 4
        secondR = self.cells[i2][j2].bords
        secondE = secondR[:n] + '0' + secondR[n + 1:]
        if firstR != firstE or secondR != secondE:
            return False
        return True

    def solve_neighboors(self, i: int, j: int) -> list[Cell]:
        neighboors = []
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        cells = self.cells
        for di, dj in directions:
            if 0 <= di + i < self.height:
                if 0 <= dj + j < self.width:
                    cell = cells[di + i][dj + j]
                    if not cell.is_f2 and self.check_walls(
                        i,
                        j,
                        cell.i,
                        cell.j
                    ):
                        neighboors.append(cell)
        return neighboors

    def generator(self, seed: str | None = None, alg: int = 0,
                  perfect: bool = True, is_ft: bool = False) -> None:
        if alg not in range(0, 2):
            print("ERROR ALGO NOT FOUND")
            return
        self.renew()
        if is_ft:
            self.gen_f2()
        if seed:
            random.seed(seed)
        if alg == 0:
            self.alg1()
        elif alg == 1:
            self.alg2()
        self.solve()

    def alg1(self) -> None:
        stack = [self.cells[self.entry[1]][self.entry[0]]]
        stack[-1].is_visited = True
        while stack:
            neighboors = self.get_neighboor(stack[-1].i, stack[-1].j)
            if neighboors == []:
                stack.pop()
                continue
            else:
                cell = random.choice(neighboors)
                self.berlini_pat(stack[-1].i, stack[-1].j, cell.i, cell.j)
                cell.is_visited = True
                stack.append(cell)

    def alg2(self) -> None:
        pass
