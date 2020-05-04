from map_package.cell import Cell, ExitCell, StunCell, ArmoryCell, RubberCell, TeleportCell
from map_package.graph import Graph


class Map:

    def __init__(self, s_file):
        self.have_key = False
        self.special_set = set()
        self.map_dict = {}
        self.graph = Graph()
        self.file_reading(s_file)
        self.id_matrix = [[0] * self.row_n for i in range(self.str_n)]
        self.add_cells_and_edges()
        for t in self.graph.cells_list:
            if type(t) == TeleportCell:
                to = self.cell_from_coord(t.to_x, t.to_y)
                to.from_teleport = True
        for t in self.graph.cells_list:
            if type(t) == TeleportCell:
                self.correct_teleport_cell(t)
            if type(t) == RubberCell:
                self.correct_rubber_cell(t)

    def file_reading(self, s_file):
        with open(s_file, 'r') as f:
            self.str_n, self.row_n = map(int, f.readline().split())
            self.a = [['.'] * (2 * self.row_n - 1) for i in range(2 * self.str_n - 1)]
            for i in range(2 * self.str_n - 1):
                s = f.readline()
                for j in range(2 * self.row_n - 1):
                    self.a[i][j] = s[j]
                    if self.a[i][j] not in ('.', '|', '_', ' '):
                        self.special_set.add(self.a[i][j])
            for i in range(len(self.special_set)):
                s = f.readline()
                self.map_dict.update({s[0]: s[2:len(s) - 1]})

    def add_cells_and_edges(self):
        for i in range(2 * self.str_n - 1):
            for j in range(2 * self.row_n - 1):
                if i % 2 == 0 and j % 2 == 0:
                    if self.a[i][j] == '.':
                        t = Cell(self.a[i][j], i // 2, j // 2)
                    else:
                        current_s = self.map_dict.get(self.a[i][j])
                        if current_s[0] == 'E':
                            t = ExitCell(self.a[i][j], i // 2, j // 2, current_s[5])
                        if current_s[0] == 'S':
                            t = StunCell(self.a[i][j], i // 2, j // 2, int(current_s[5]))
                        if current_s[0] == 'A':
                            t = ArmoryCell(self.a[i][j], i // 2, j // 2)
                        if current_s[0] == 'R':
                            t = RubberCell(self.a[i][j], i // 2, j // 2, current_s[11])
                        if current_s[0] == 'T':
                            t = TeleportCell(self.a[i][j], i // 2, j // 2, int(current_s[9]), int(current_s[12]))
                    self.graph.add_cell(t)
                    self.id_matrix[i // 2][j // 2] = t.id
        for i in range(self.str_n):
            for j in range(self.row_n):
                if j < self.row_n - 1:
                    if self.a[i * 2][j * 2 + 1] == " ":
                        self.graph.add_edge(self.id_matrix[i][j], self.id_matrix[i][j + 1])
                if i < self.str_n - 1:
                    if self.a[i * 2 + 1][j * 2] == ".":
                        self.graph.add_edge(self.id_matrix[i][j], self.id_matrix[i + 1][j])

    def correct_rubber_cell(self, t):
        old_to = t.edges_to.copy()
        for k in old_to:
            self.graph.delete_direct_edge(t.id, k)
            if t.direction == 'R' and self.check_valid_cell(t.x, t.y + 1) and self.id_matrix[t.x][t.y + 1] in old_to:
                self.graph.add_direct_edge(t.id, self.id_matrix[t.x][t.y + 1])
            if t.direction == 'L' and self.check_valid_cell(t.x, t.y - 1) and self.id_matrix[t.x][t.y - 1] in old_to:
                self.graph.add_direct_edge(t.id, self.id_matrix[t.x][t.y - 1])
            if t.direction == 'U' and self.check_valid_cell(t.x - 1, t.y) and self.id_matrix[t.x - 1][t.y] in old_to:
                self.graph.add_direct_edge(t.id, self.id_matrix[t.x - 1][t.y])
            if t.direction == 'D' and self.check_valid_cell(t.x + 1, t.y) and self.id_matrix[t.x + 1][t.y] in old_to:
                self.graph.add_direct_edge(t.id, self.id_matrix[t.x + 1][t.y])

    def correct_teleport_cell(self, t):
        old_to = t.edges_to.copy()
        t.old_neighbours = t.edges_to.copy()
        if not t.from_teleport:
            for k in old_to:
                self.graph.delete_direct_edge(t.id, k)
        if self.check_valid_cell(t.to_x, t.to_y):
            self.graph.add_direct_edge(t.id, self.id_matrix[t.to_x][t.to_y])

    def check(self):
        visited = [False] * len(self.graph.cells_list)
        for i in range(len(self.graph.cells_list)):
            if type(self.graph.cells_list[i]) == ExitCell:
                self.graph.dfs(i, visited)
        bad_cells = []
        for i in range(len(self.graph.cells_list)):
            if not visited[i]:
                bad_cells.append(self.graph.cells_list[i])
        if len(bad_cells) > 0:
            print('FAILED')
            print('Exit unreachable for cells', end="")
            for i in range(len(bad_cells)):
                print(' ({}, {})'.format(bad_cells[i].x, bad_cells[i].y), end="")
            print("")
            return False
        else:
            print('OK')
            return True

    def print_lab(self):
        """Debug function to print the labyrinth"""
        print('str_n = {}, row_n = {}'.format(self.str_n, self.row_n))
        for i in range(2 * self.str_n - 1):
            for j in range(2 * self.row_n - 1):
                print(self.a[i][j], end="")
            print("")
        print('special_cells:')
        print(self.map_dict)
        print('the graph:')
        self.graph.print_g()
        print('id_matrix:')
        for i in range(self.str_n):
            for j in range(self.row_n):
                print(self.id_matrix[i][j], end=" ")
            print("")

    def check_valid_cell(self, x, y):
        return 0 <= x < self.str_n and 0 <= y < self.row_n

    def cell_from_coord(self, x, y):
        return self.graph.cells_list[self.id_matrix[x][y]]

    def add_key(self, x, y):
        self.have_key = True
        self.key_cell = self.cell_from_coord(x, y)
        self.key_dropped = True
