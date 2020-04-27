class Cell:

    def __init__(self, c, coord_x, coord_y):
        self.id = 0
        self.t_char = c
        self.edges_to = []
        self.edges_from = []
        self.x = coord_x
        self.y = coord_y
        self.key = False

    def add_to(self, id):
        self.edges_to.append(id)

    def add_from(self, id):
        self.edges_from.append(id)

    def delete_to(self, id):
        if id in self.edges_to:
            self.edges_to.remove(id)

    def delete_from(self, id):
        if id in self.edges_from:
            self.edges_from.remove(id)


    def print_cell(self):
        print('c = {}, id = {}, coord_x = {}, '
              'coord_y = {}'.format(self.t_char, self.id, self.x, self.y))
        print('edges_to:', self.edges_to)
        print('edges_from:', self.edges_from)


class ExitCell(Cell):
    def __init__(self, c, coord_x, coord_y, direction):
        self.direction = direction
        super().__init__(c, coord_x, coord_y)

    def print_cell(self):
        print('It is ExitCell\n')
        super().print_cell()


class StunCell(Cell):
    def __init__(self, c, coord_x, coord_y, s_time):
        self.time = s_time
        super().__init__(c, coord_x, coord_y)

    def print_cell(self):
        print('It is StunCell, time = {}\n'.format(self.time))
        super().print_cell()


class ArmoryCell(Cell):
    def __init__(self, c, coord_x, coord_y):
        super().__init__(c, coord_x, coord_y)

    def print_cell(self):
        print('It is ArmoryCell\n')
        super().print_cell()


class RubberCell(Cell):
    def __init__(self, c, coord_x, coord_y, direction):
        self.direction = direction
        super().__init__(c, coord_x, coord_y)

    def print_cell(self):
        print('It is RubberCell, direction = {}\n'.format(self.direction))
        super().print_cell()


class TeleportCell(Cell):
    def __init__(self, c, coord_x, coord_y, x, y):
        self.to_x = x
        self.to_y = y
        super().__init__(c, coord_x, coord_y)

    def print_cell(self):
        print('It is TeleportCell to ({}, {})\n'.format(self.to_x, self.to_y))
        super().print_cell()


