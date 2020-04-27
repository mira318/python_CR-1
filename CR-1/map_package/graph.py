class Graph:
    def __init__(self):
        self.cells_list = []    # id == index in cells_list

    def add_cell(self, new_cell):
        new_cell.id = len(self.cells_list)
        self.cells_list.append(new_cell)

    def add_direct_edge(self, id_from, id_to):
        self.cells_list[id_from].add_to(id_to)
        self.cells_list[id_to].add_from(id_from)

    def add_edge(self, id_1, id_2):
        self.add_direct_edge(id_1, id_2)
        self.add_direct_edge(id_2, id_1)

    def delete_direct_edge(self, id_from, id_to):
        self.cells_list[id_from].delete_to(id_to)
        self.cells_list[id_to].delete_from(id_from)

    def print_g(self):
        for i in range(len(self.cells_list)):
            print('i = {}, cell = '.format(i), end="")
            self.cells_list[i].print_cell()
            print("")

    def dfs(self, cell_id, visited):
        visited[cell_id] = True
        cur_cell = self.cells_list[cell_id]
        for i in range(len(cur_cell.edges_from)):
            if not visited[cur_cell.edges_from[i]]:
                self.dfs(cur_cell.edges_from[i], visited)
