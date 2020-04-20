class Graph:
    def __init__(self):
        self.cells_list = []    # id == index in cells_list

    def add_cell(self, new_cell):
        new_cell.id = len(self.cells_list)
        self.cells_list.append(new_cell)

    def add_edge(self, id_1, id_2):
        self.cells_list[id_1].add_neighbour(id_2)
        self.cells_list[id_2].add_neighbour(id_1)

    def print_g(self):
        for i in range(len(self.cells_list)):
            print('i = {}, cell = '.format(i), end="")
            self.cells_list[i].print_cell()

    def dfs(self, cell_id, visited):
        visited[cell_id] = True
        cur_cell = self.cells_list[cell_id]
        for i in range(len(cur_cell.neighbours)):
            if not visited[cur_cell.neighbours[i]]:
                self.dfs(cur_cell.neighbours[i], visited)
