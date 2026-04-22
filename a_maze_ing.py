import parceing
from errors import ConfigFormatError
from generator import MazeGenerator
from math import ceil, floor


class Render:
    def __init__(self, config, cells, solution):
        self.config = config
        self.entry_col = 32
        self.exit_col = 31
        self.cells = cells
        self.solution = solution
        self.show_path = False

    def render_matrix(self) -> None:
        # print(config)
        border_symb = f"\033[{self.config.Color.value}m█\033[0m"
        entry_symb = f"\033[{self.entry_col}m█\033[0m"
        exit_symb = f"\033[{self.exit_col}m█\033[0m"
        f2 = f"\033[{36}m█\033[0m"
        path = f"\033[{33}m█\033[0m"
        self.matrix = [[border_symb for j in range(0, self.config.width * 3)]
                       for i in range(0, self.config.height * 3)]
        for row in self.cells:
            for cell in row:
                if cell.is_entry:
                    self.matrix[cell.mat_i][cell.mat_j] = entry_symb
                elif cell.is_exit:
                    self.matrix[cell.mat_i][cell.mat_j] = exit_symb
                else:
                    self.matrix[cell.mat_i][cell.mat_j] = " "
                bords = cell.bords
                if bords[0] == '0':
                    self.matrix[cell.mat_i - 1][cell.mat_j] = " "
                if bords[1] == '0':
                    self.matrix[cell.mat_i][cell.mat_j + 1] = " "
                if bords[2] == '0':
                    self.matrix[cell.mat_i + 1][cell.mat_j] = " "
                if bords[3] == '0':
                    self.matrix[cell.mat_i][cell.mat_j - 1] = " "
        for row in self.cells:
            for cell in row:
                if cell.is_f2:
                    if cell.is_entry:
                        raise ConfigFormatError("ENTRY overlap with 42 patern")
                    elif cell.is_exit:
                        raise ConfigFormatError("EXIT overlap with 42 pattern")
                    bords = cell.bords
                    self.matrix[cell.mat_i - 1][cell.mat_j] = f2
                    self.matrix[cell.mat_i - 1][cell.mat_j - 1] = f2
                    self.matrix[cell.mat_i - 1][cell.mat_j + 1] = f2
                    self.matrix[cell.mat_i][cell.mat_j + 1] = f2
                    self.matrix[cell.mat_i - 1][cell.mat_j + 1] = f2
                    self.matrix[cell.mat_i + 1][cell.mat_j + 1] = f2
                    self.matrix[cell.mat_i + 1][cell.mat_j] = f2
                    self.matrix[cell.mat_i][cell.mat_j - 1] = f2
                    self.matrix[cell.mat_i - 1][cell.mat_j - 1] = f2
                    self.matrix[cell.mat_i + 1][cell.mat_j - 1] = f2
                    self.matrix[cell.mat_i][cell.mat_j] = f2
            current = (self.config.exit[1], self.config.exit[0])
            while current and self.show_path:
                ci, cj = current
                if self.solution[current] is None:
                    break

                pi, pj = self.solution[current]
                ci_mat = ci * 3 + 1
                cj_mat = cj * 3 + 1
                step = ((pi - ci) * 3, (pj - cj) * 3)
                cell = self.cells[ci][cj]

                if cell.is_entry:
                    self.matrix[ci_mat][cj_mat] = path
                    current = self.solution[current]
                    continue

                if not cell.is_exit:
                    self.matrix[ci_mat][cj_mat] = path

                self.matrix[
                    ci_mat + floor(step[0] / 2)
                ][cj_mat + floor(step[1] / 2)] = path

                self.matrix[
                    ci_mat + ceil(step[0] / 2)
                ][cj_mat + ceil(step[1] / 2)] = path

                current = self.solution[current]

    def print_mat(self) -> None:
        self.render_matrix()
        for row in self.matrix:
            for symb in row:
                print(symb, end="")
            print()


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
        self.is_path = False


class Maze:
    def __init__(self, width: int, height: int, config) -> None:
        self.cells = [[Cell(i, j) for j in range(0, width)]
                      for i in range(0, height)]
        self.cells[config.entry[1]][config.entry[0]].is_entry = True
        self.cells[config.exit[1]][config.exit[0]].is_exit = True
        self.width = width
        self.height = height
        self.gen = MazeGenerator(config, self.cells, config.seed, self.gen_f2)
        # self.solution = dict()
        self.gen.generate(False)
        self.solution = self.gen.solution
        self.ren = Render(config, self.cells, self.solution)

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


def menu(config) -> None:
    new = MazeGenerator(config.width, config.height, config.entry, config.exit)
    new.generator(config.seed)
    ren = Render(config, new.cells, new.solution)
    ren.show_path = False
    while True:
        ren.print_mat()
        print("Select one of the options:")
        print("1 - regenerate a new maze and display it")
        print("2 - show/hide a valid shortest path from entry to the exit")
        print("3 - change maze wall Color")
        print("4 - Exit")
        try:
            option = int(input("Enter option:"))
            if not (option >= 1 and option <= 4):
                raise ValueError()
            if option == 1:
                new.generator()
                ren.solution = new.solution
            elif option == 2:
                ren.show_path = not ren.show_path
            elif option == 3:
                print("Choose from: yellow, blue, white")
                config.Color = input("Input new Color:")
            elif option == 4:
                break
        except (TypeError, ValueError):
            print("Wrong option type! Input a number from [1; 3]!")
        except ConfigFormatError as e:
            print(e)


def main() -> None:
    config = parceing.parce()
    if not config:
        return
    menu(config)
    # maze = Maze(config.width, config.height, config)
    # menu(config, maze)


if __name__ == "__main__":
    main()
