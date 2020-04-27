from map_package.cell import Cell, ExitCell, StunCell, ArmoryCell, RubberCell, TeleportCell
import argparse


class Gamer:

    def __init__(self, game_map, gamer_num, start_cell, game_positions_dictionary):
        self.exited = False
        self.map = game_map
        self.copy_positions = game_positions_dictionary
        self.number = gamer_num
        self.is_stunned = False
        self.patrons = 0
        self.current_cell = start_cell
        self.time_left = 0
        self.patron_cell = start_cell
        self.start_cell = start_cell
        self.copy_positions.update({self.current_cell: self})
        print('Gamer №{},'.format(self.number + 1), end="")
        self.came_to_new_cell()
        self.turn_parser = argparse.ArgumentParser(description='Choose whats to do')
        turn_subparsers = self.turn_parser.add_subparsers(dest='subcommand')
        parser_up = turn_subparsers.add_parser('up')
        parser_down = turn_subparsers.add_parser('down')
        parser_left = turn_subparsers.add_parser('right')
        parser_right = turn_subparsers.add_parser('left')
        parser_inventory = turn_subparsers.add_parser('inventory', help='check the patrons shelf')
        parser_skip_turn = turn_subparsers.add_parser('skip', help='skip your turn')
        parser_exit = turn_subparsers.add_parser('exit', help='leave the game')
        parser_shoot = turn_subparsers.add_parser('patron',
                                                  help='write "patron" and then direction to shoot')
        parser_shoot.add_argument('direction', choices=['up', 'down', 'left', 'right'],
                                  help='in which direction you shoot')

    def print_gamer(self):
        print('gamer: number {}, exited = {}, stunned = {}, patrons = {}, patron_cell = ({}, {}), '
              'start_cell = ({}, {}), current_cell = ({}, {}), time left = {}'.format(self.number, self.exited,
                                    self.is_stunned, self.patrons, self.patron_cell.x, self.patron_cell.y,
                                    self.start_cell.x, self.start_cell.y, self.current_cell.x,
                                    self.current_cell.y, self.time_left))
        #print('have map')
        #self.map.print_lab()

    def came_to_new_cell(self):
        self.copy_positions.update({self.current_cell: self})
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
        self.came_to_new_cell()

    def armory(self):
        print('You are in armory room your patrons amount raised up to 3')
        self.patrons = 3

    def death(self):
        print('Gamer №{}, sorry but you was killed. You go to you start cell, lose all patrons '
              'and miss the next turn'.format(self.number + 1))
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
        still = True
        while still:
            if direction == 'up':
                if self.map.check_valid_cell(self.patron_cell.x - 1, self.patron_cell.y):
                    self.patron_cell = self.map.cell_from_coord(self.patron_cell.x - 1, self.patron_cell.y)
            if direction == 'down':
                if self.map.check_valid_cell(self.patron_cell.x + 1, self.patron_cell.y):
                    self.patron_cell = self.map.cell_from_coord(self.patron_cell.x + 1, self.patron_cell.y)
            if direction == 'left':
                if self.map.check_valid_cell(self.patron_cell.x, self.patron_cell.y - 1):
                    self.patron_cell = self.map.cell_from_coord(self.patron_cell.x, self.patron_cell.y - 1)
            if direction == 'right':
                if self.map.check_valid_cell(self.patron_cell.x, self.patron_cell.y + 1):
                    self.patron_cell = self.map.cell_from_coord(self.patron_cell.x, self.patron_cell.y + 1)
            if self.patron_cell in self.copy_positions:
                self.copy_positions[self.patron_cell].death()
                still = False

    def turn_interface(self):
        if not self.exited:
            if not self.is_stunned:
                print('Gamer №{} turn'.format(self.number + 1))
                done_turn = False
                while not done_turn:
                    done = False
                    while not done:
                        command = input().split()
                        try:
                            args2 = self.turn_parser.parse_args(command)
                            done = True
                        except:
                            pass

                    if type(self.current_cell) == ExitCell:
                        if self.right_char(args2.subcommand):
                            self.exited = True
                            self.win()
                            return 1
                    if args2.subcommand == 'inventory' or args2.subcommand == 'exit':
                        if args2.subcommand == 'inventory':
                            print('You have {} patrons'.format(self.patrons))
                        elif args2.subcommand == 'exit':
                            self.exited = True
                            return 2

                    else:
                        done_turn = True
                        future_cell = self.current_cell
                        if args2.subcommand == 'up':
                            if self.map.check_valid_cell(self.current_cell.x - 1, self.current_cell.y):
                                future_cell = self.map.cell_from_coord(self.current_cell.x - 1, self.current_cell.y)
                        if args2.subcommand == 'down':
                            if self.map.check_valid_cell(self.current_cell.x + 1, self.current_cell.y):
                                future_cell = self.map.cell_from_coord(self.current_cell.x + 1, self.current_cell.y)
                        if args2.subcommand == 'left':
                            if self.map.check_valid_cell(self.current_cell.x, self.current_cell.y - 1):
                                future_cell = self.map.cell_from_coord(self.current_cell.x, self.current_cell.y - 1)
                        if args2.subcommand == 'right':
                            if self.map.check_valid_cell(self.current_cell.x, self.current_cell.y + 1):
                                future_cell = self.map.cell_from_coord(self.current_cell.x, self.current_cell.y + 1)

                        if future_cell != self.current_cell:
                            if type(self.current_cell) == RubberCell:
                                if not self.right_char(args2.subcommand):
                                    print('You moved successfully!')
                                else:
                                    print('Congratulations, you have left a rubber room')
                                    if future_cell.id in self.current_cell.edges_to:
                                        self.current_cell = future_cell
                                        self.came_to_new_cell()

                            else:
                                if future_cell.id in self.current_cell.edges_to:
                                    self.current_cell = future_cell
                                    print('You moved successfully!')
                                    self.came_to_new_cell()
                                else:
                                    print("Sorry, you can't go this way - there is a wall")

                        else:

                            if args2.subcommand == 'patron':
                                self.patrons -= 1
                                self.patron_cell = self.current_cell
                                self.shoot(args2.direction)
                            else:
                                print("Sorry, you can't go this way - there is a wall")
                                return 0

            else:
                print('Sorry, gamer №{}, you skip the turn'.format(self.number + 1))
                self.time_left -= 1
                if self.time_left <= 0:
                    self.is_stunned = False
        return 0
