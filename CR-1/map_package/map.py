from map_package.graph import Graph
from map_package.cell import Cell, Teleport, Stun, RubberRoom, Exit, Armory


class Map:

    def __init__(self, map_file):
        self.have_key = False
        self.special_cells_set = set()
        self.special_cells_dict = {}
        self.graph = Graph()
        self.file_reading(map_file)
        self.id_matrix = [[0] * self.row_number for i in range(self.col_number)]
        self.add_cells_and_edges()
        for cell in self.graph.cells_list:
            cell.get_info_from_map(self)

    def file_reading(self, map_file):
        with open(map_file, 'r') as opened_map_file:
            self.col_number, self.row_number = map(int, opened_map_file.readline().split())
            self.char_array = [['.'] * (2 * self.row_number - 1) for i in range(2 * self.col_number - 1)]
            for i in range(2 * self.col_number - 1):
                current_string = opened_map_file.readline()
                for j in range(2 * self.row_number - 1):
                    self.char_array[i][j] = current_string[j]
                    if self.char_array[i][j] not in ('.', '|', '_', ' '):
                        self.special_cells_set.add(self.char_array[i][j])
            for i in range(len(self.special_cells_set)):
                cell_symbol, cell_code = opened_map_file.readline().split(maxsplit=1)
                self.special_cells_dict.update({cell_symbol: cell_code})

    def add_cells_and_edges(self):
        for i in range(2 * self.col_number - 1):
            for j in range(2 * self.row_number - 1):
                if i % 2 == 0 and j % 2 == 0:
                    if self.char_array[i][j] == '.':
                        cell_from_current_char = Cell()
                    else:
                        current_string = self.special_cells_dict.get(self.char_array[i][j])
                        cell_from_current_char = eval(current_string)
                    self.graph.add_cell(cell_from_current_char)
                    self.id_matrix[i // 2][j // 2] = cell_from_current_char.id
                    cell_from_current_char.set_coord(i // 2, j // 2)
        for i in range(self.col_number):
            for j in range(self.row_number):
                if j < self.row_number - 1:
                    if self.char_array[i * 2][j * 2 + 1] == " ":
                        self.graph.add_edge(self.id_matrix[i][j], self.id_matrix[i][j + 1])
                if i < self.col_number - 1:
                    if self.char_array[i * 2 + 1][j * 2] == ".":
                        self.graph.add_edge(self.id_matrix[i][j], self.id_matrix[i + 1][j])

    def check(self):
        visited = [False] * len(self.graph.cells_list)
        for ind, cell in enumerate(self.graph.cells_list):
            if type(cell) == Exit:
                self.graph.dfs(ind, visited)
        bad_cells = []
        for ind, cell in enumerate(self.graph.cells_list):
            if not visited[ind]:
                bad_cells.append(cell)
        if bad_cells:
            print('FAILED')
            print('Exit unreachable for cells', end="")
            for i in range(len(bad_cells)):
                print(' ({}, {})'.format(bad_cells[i].x, bad_cells[i].y), end="")
            print("")
            return False
        else:
            print('OK')
            return True

    def __str__(self):
        """Debug function to print the labyrinth"""
        to_print = 'str_number = {}, row_number = {}'.format(self.col_number, self.row_number)
        for i in range(2 * self.col_number - 1):
            for j in range(2 * self.row_number - 1):
                to_print += self.char_array[i][j] + ' '
            to_print += '\n'
        to_print += 'special_cells:' + self.special_cells_dict.__str__()
        to_print += 'the graph:' + self.graph.__str__()
        to_print += 'id_matrix:'
        for i in range(self.col_number):
            for j in range(self.row_number):
                to_print += self.id_matrix[i][j].__str__() + ' '
            to_print += '\n'
        return to_print

    def check_valid_cell(self, x, y):
        return 0 <= x < self.col_number and 0 <= y < self.row_number

    def cell_from_coord(self, x, y):
        return self.graph.cells_list[self.id_matrix[x][y]]

    def add_key(self, x, y):
        self.have_key = True
        self.key_cell = self.cell_from_coord(x, y)
        self.key_cell.key = True
        self.key_dropped = True
