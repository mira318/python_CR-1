from enum import Enum


class LeaveRes(Enum):
    STAYED = 0
    LEFT = 1
    CURRENT_GAMER_WIN = 2


def change_coord_from_direction(direction):
    if direction == 'up' or direction == 'UP':
        return -1, 0
    if direction == 'down' or direction == 'DOWN':
        return 1, 0
    if direction == 'left' or direction == 'LEFT':
        return 0, -1
    if direction == 'right' or direction == 'RIGHT':
        return 0, 1


class Cell:

    def __init__(self):
        self.id = 0
        self.edges_to = []
        self.edges_from = []
        self.x = -1
        self.y = -1
        self.key = False
        self.patron_stun = False

    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        to_print = 'id = {}, coord_x = {}, ' \
                   'coord_y = {}'.format(self.id, self.x, self.y)
        to_print += ' ' + self.edges_to.__str__() + ' '
        to_print += self.edges_from.__str__()
        return to_print

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

    def get_info_from_map(self, map):
        pass

    def arrive(self, player_came, gamer_positions):
        gamer_positions.update({player_came: self})
        if self.key:
            player_came.with_key = True
            print('Congratulations gamer №{}, you have found the key'.format(player_came.player_id + 1))
            self.key = False

    def try_to_leave(self, player, future_cell, direction, map_have_key):
        if future_cell.id in self.edges_to:
            print('You moved successfully!')
            return LeaveRes.LEFT
        else:
            print("You can't go this way - there is a wall")
            return LeaveRes.STAYED


class Exit(Cell):
    def __init__(self, direction):
        self.direction = direction
        super().__init__()

    def __str__(self):
        return 'It is Exit\n' + super().__str__()

    def try_to_leave(self, player, future_cell, direction, map_have_key):
        if direction.upper() == self.direction:
            if not map_have_key or (map_have_key and player.with_key):
                player.win()
            return LeaveRes.CURRENT_GAMER_WIN
        else:
            return super().try_to_leave(player, future_cell, direction, map_have_key)


class Stun(Cell):
    def __init__(self, stun_time):
        self.time = stun_time
        super().__init__()

    def print_cell(self):
        return 'It is Stun, time = {}\n'.format(self.time) + super().__str__()

    def arrive(self, player_came, gamer_positions):
        print('Sorry, You have been stunned you will stand in this place for {} turns'.format(self.time))
        player_came.is_stunned = True
        player_came.time_left = self.time
        super().arrive(player_came, gamer_positions)

    def try_to_leave(self, player, future_cell, direction, map_have_key):
        """Yes, it is even useless. Just to remind: if you are trying to leave it mean that you spent all stunning time
        and now it is like from ordinary cell"""
        return super().try_to_leave(player, future_cell, direction, map_have_key)


class Armory(Cell):
    def __init__(self):
        super().__init__()

    def print_cell(self):
        return 'It is Armory\n' + super().__str__()

    def arrive(self, player_came, gamer_positions):
        print('You are in armory room your patrons amount raised up by 3')
        player_came.patrons += 3
        super().arrive(player_came, gamer_positions)


class RubberRoom(Cell):
    def __init__(self, direction):
        self.direction = direction
        super().__init__()
        self.patron_stun = True

    def print_cell(self):
        'It is RubberRoom, direction = {}\n'.format(self.direction) + super().__str__()

    def get_info_from_map(self, map):
        old_to = self.edges_to.copy()
        for old_direct_neighbour in old_to:
            map.graph.delete_direct_edge(self.id, old_direct_neighbour)
        x_change, y_change = change_coord_from_direction(self.direction)
        if map.check_valid_cell(self.x + x_change, self.y + y_change) and \
                map.id_matrix[self.x + x_change][self.y + y_change] in old_to:
            map.graph.add_direct_edge(self.id, map.id_matrix[self.x + x_change][self.y + y_change])

    def try_to_leave(self, player, future_cell, direction, map_have_key):
        """If you are trying to go from a rubber room with the right char you go to a correct cell,
        because the map correct"""
        if direction.upper() == self.direction:
            print('Congratulations, you have left a rubber room')
            return super().try_to_leave(player, future_cell, direction, map_have_key)
        else:
            print('You moved successfully!')
            return LeaveRes.STAYED


class Teleport(Cell):
    def __init__(self, to_x, to_y):
        self.old_neighbours = []
        self.teleport_to_x = to_x
        self.teleport_to_y = to_y
        super().__init__()
        self.patron_stun = True

    def __str__(self):
        return 'It is Teleport to ({}, {})\n'.format(self.teleport_to_x, self.teleport_to_y) + super().__str__()

    def get_info_from_map(self, map):
        self.teleport_to = map.cell_from_coord(self.teleport_to_x, self.teleport_to_y)
        old_to = self.edges_to.copy()
        self.old_neighbours = self.edges_to.copy()
        for old_to_id in old_to:
            map.graph.delete_direct_edge(self.id, old_to_id)
        if map.check_valid_cell(self.teleport_to_x, self.teleport_to_y):
            map.graph.add_direct_edge(self.id, self.teleport_to.id)

    def arrive(self, player_came, gamer_positions):
        print('You was teleported')
        player_came.current_cell = self.teleport_to
        super().arrive(player_came, gamer_positions)

    def try_to_leave(self, player, future_cell, direction, map_have_key):
        """If you trying to go somewhere from a teleport cell, it means that you wasn't
        teleported because of the start of the game, death or another teleport. So we look at presaved old neighbours.
        Exit and teleport can't be the same cell, because of format"""
        if future_cell.id in self.old_neighbours:
            print('You moved successfully!')
            return LeaveRes.LEFT
        else:
            print("You can't go this way - there is a wall")
            return LeaveRes.STAYED
