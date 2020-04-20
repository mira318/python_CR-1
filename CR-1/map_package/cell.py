class Cell:

    def __init__(self, c, coord_x, coord_y):
        self.id = 0
        self.t_char = c
        self.neighbours = []
        self.x = coord_x
        self.y = coord_y

    def add_neighbour(self, id):
        self.neighbours.append(id)

    def print_cell(self):
        print('c = {}, id = {}, coord_x = {}, '
              'coord_y = {}'.format(self.t_char, self.id, self.x, self.y))
        print('neighbours:', self.neighbours)


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
        print('It is TeleportCell to ({}, {})\n'.format(self.x, self.y))
        super().print_cell()


