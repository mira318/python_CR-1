from map_package.cell import Cell, ExitCell, StunCell, ArmoryCell, RubberCell, TeleportCell
import argparse
import random


class Gamer:

    def __init__(self, game_map, gamer_num, start_cell, game_positions_dictionary):
        self.exited = False
        self.map = game_map
        self.copy_positions = game_positions_dictionary
        self.number = gamer_num
        self.is_stunned = False
        self.patrons = 0
        self.with_key = False
        self.current_cell = start_cell
        self.time_left = 0
        self.patron_cell = start_cell
        self.start_cell = start_cell
        self.copy_positions.update({self: self.current_cell})
        self.first_time = True
        self.add_turn_parser()

    def add_turn_parser(self):
        self.turn_parser = argparse.ArgumentParser(description='Choose whats to do')
        turn_subparsers = self.turn_parser.add_subparsers(dest='subcommand')
        parser_up = turn_subparsers.add_parser('up')
        parser_down = turn_subparsers.add_parser('down')
        parser_left = turn_subparsers.add_parser('right')
        parser_right = turn_subparsers.add_parser('left')
        parser_inventory = turn_subparsers.add_parser('inventory', help='check the patrons shelf and the key')
        parser_skip_turn = turn_subparsers.add_parser('skip', help='skip your turn')
        parser_exit = turn_subparsers.add_parser('exit', help='leave the game')
        parser_shoot = turn_subparsers.add_parser('patron',
                                                  help='write "patron" and then direction to shoot')
        parser_shoot.add_argument('direction', choices=['up', 'down', 'left', 'right'],
                                  help='in which direction you shoot')

    def print_gamer(self):
        print('gamer: number {}, exited = {}, stunned = {}, patrons = {}, '
              'patron_cell = ({}, {}), start_cell = ({}, {}), '
              'current_cell = ({}, {}), time left = {}, with_key = {}'.format(self.number, self.exited, self.is_stunned,
                                                                              self.patrons, self.patron_cell.x,
                                                                              self.patron_cell.y, self.start_cell.x,
                                                                              self.start_cell.y, self.current_cell.x,
                                                                              self.current_cell.y, self.time_left,
                                                                              self.with_key))

    def came_to_new_cell(self):
        self.copy_positions.update({self: self.current_cell})
        if self.map.have_key:
            if self.current_cell == self.map.key_cell and self.map.key_dropped:
                print('Congratulations, you came to the cell with key and took it')
                self.map.key_dropped = False
                self.with_key = True
        if type(self.current_cell) == StunCell:
            self.stunned()
        elif type(self.current_cell) == TeleportCell:
            self.teleport(self.map)
        elif type(self.current_cell) == ArmoryCell:
            self.armory()

    def stunned(self):
        print('Sorry, You have been stunned you will stand in this place for {} turns'.format(self.current_cell.time))
        self.is_stunned = True
        self.time_left = self.current_cell.time

    def teleport(self, game_map):
        print('You was teleported')
        self.current_cell = game_map.cell_from_coord(self.current_cell.to_x, self.current_cell.to_y)

    def armory(self):
        print('You are in armory room your patrons amount raised up to 3')
        self.patrons = 3

    def death(self):
        print('Gamer №{}, sorry but you was killed. You go to you start cell, lose all patrons, lose the key on the '
              'current cell if you had it and miss the next turn'.format(self.number + 1))
        self.map.key_cell = self.current_cell
        self.map.key_dropped = True
        # self.with_key = False in init
        self.__init__(self.map, self.number, self.start_cell, self.copy_positions)
        if not self.is_stunned:
            self.is_stunned = True
            self.time_left = 1

    def win(self):
        print('My congratulations, gamer №{}, you won'.format(self.number + 1))

    def right_char(self, str_from_command):
        if str_from_command == 'right' and self.current_cell.direction == 'R' or \
                str_from_command == 'left' and self.current_cell.direction == 'L' or \
                str_from_command == 'up' and self.current_cell.direction == 'U' or \
                str_from_command == 'down' and self.current_cell.direction == 'D':
            return True
        else:
            return False

    def shoot(self, direction):
        self.patrons -= 1
        self.patron_cell = self.current_cell
        still = True
        death_list = []
        while still:
            for gamer, cell in self.copy_positions.items():
                if cell == self.patron_cell and still and gamer.number is not self.number:
                    still = False
                    death_list.append(gamer)
            if death_list:
                random.choice(death_list).death()
            if type(self.patron_cell) == TeleportCell or type(self.patron_cell) == RubberCell:
                still = False
            future_patron_cell = self.patron_cell
            if direction == 'up' and self.map.check_valid_cell(self.patron_cell.x - 1, self.patron_cell.y):
                future_patron_cell = self.map.cell_from_coord(self.patron_cell.x - 1, self.patron_cell.y)
            if direction == 'down' and self.map.check_valid_cell(self.patron_cell.x + 1, self.patron_cell.y):
                future_patron_cell = self.map.cell_from_coord(self.patron_cell.x + 1, self.patron_cell.y)
            if direction == 'left' and self.map.check_valid_cell(self.patron_cell.x, self.patron_cell.y - 1):
                future_patron_cell = self.map.cell_from_coord(self.patron_cell.x, self.patron_cell.y - 1)
            if direction == 'right' and self.map.check_valid_cell(self.patron_cell.x, self.patron_cell.y + 1):
                future_patron_cell = self.map.cell_from_coord(self.patron_cell.x, self.patron_cell.y + 1)
            if future_patron_cell != self.patron_cell and future_patron_cell.id in self.patron_cell.edges_to:
                self.patron_cell = future_patron_cell
            else:
                still = False

    def direction_command(self, direction):
        if type(self.current_cell) == RubberCell:
            self.direction_command_from_rubber_room(direction)
            return 0
        if type(self.current_cell) == ExitCell and self.right_char(direction) and self.with_key:
            self.exited = True
            self.win()
            return 1
        future_cell = self.current_cell
        if direction == 'up' and self.map.check_valid_cell(self.current_cell.x - 1, self.current_cell.y):
            future_cell = self.map.cell_from_coord(self.current_cell.x - 1, self.current_cell.y)
        if direction == 'down' and self.map.check_valid_cell(self.current_cell.x + 1, self.current_cell.y):
            future_cell = self.map.cell_from_coord(self.current_cell.x + 1, self.current_cell.y)
        if direction == 'left' and self.map.check_valid_cell(self.current_cell.x, self.current_cell.y - 1):
            future_cell = self.map.cell_from_coord(self.current_cell.x, self.current_cell.y - 1)
        if direction == 'right' and self.map.check_valid_cell(self.current_cell.x, self.current_cell.y + 1):
            future_cell = self.map.cell_from_coord(self.current_cell.x, self.current_cell.y + 1)
        if future_cell != self.current_cell and future_cell.id in self.current_cell.edges_to:
            self.current_cell = future_cell
            print('You moved successfully!')
            self.came_to_new_cell()
        else:
            if type(self.current_cell) == TeleportCell:
                if future_cell.id in self.current_cell.old_neighbours:
                    """ If you are here, it means that teleport cell didn't influenced you, because of death, start or
                    another portal, so you can go like from ordinary cell """
                    self.current_cell = future_cell
                    print('You moved successfully!')
                    self.came_to_new_cell()
                else:
                    print("Sorry, you can't go this way - there is a wall")
            else:
                print("Sorry, you can't go this way - there is a wall")
        return 0

    def direction_command_from_rubber_room(self, direction):
        if not self.right_char(direction):
            print('You moved successfully!')
            return 0
        else:
            print('Congratulations, you have left a rubber room')
            """if the map correct, you will go to a correct cell and we have checked map before the game"""
            if direction == 'up':
                self.current_cell = self.map.cell_from_coord(self.current_cell.x - 1, self.current_cell.y)
            if direction == 'down':
                self.current_cell = self.map.cell_from_coord(self.current_cell.x + 1, self.current_cell.y)
            if direction == 'left':
                self.current_cell = self.map.cell_from_coord(self.current_cell.x, self.current_cell.y - 1)
            if direction == 'right':
                self.current_cell = self.map.cell_from_coord(self.current_cell.x, self.current_cell.y + 1)
            self.came_to_new_cell()

    def turn_interface(self):
        if not self.exited:
            if not self.is_stunned:
                print('Gamer №{} turn'.format(self.number + 1))
                done_turn = False
                while True:
                    correct = False
                    while not correct:
                        command = input().split()
                        try:
                            args2 = self.turn_parser.parse_args(command)
                            correct = True
                        except Exception:
                            print('Invalid command, try again')
                    if args2.subcommand == 'inventory':
                        print('You have {} patrons'.format(self.patrons))
                        if self.map.have_key:
                            if self.with_key:
                                print('and you have the key!')
                        continue
                    return self.active_command(args2)
            else:
                print('Sorry, gamer №{}, you skip the turn'.format(self.number + 1))
                self.time_left -= 1
                if self.time_left <= 0:
                    self.is_stunned = False
        return 0

    def active_command(self, args):
        if args.subcommand == 'exit':
            self.exited = True
            return 2
        if args.subcommand == 'patron':
            if self.patrons <= 0:
                print("Sorry, but you don't have any patrons to shoot, try something else")
            else:
                self.shoot(args.direction)
            return 0

        if args.subcommand == 'skip':
            return 0
        if args.subcommand in {'up', 'down', 'right', 'left'}:
            return self.direction_command(args.subcommand)
