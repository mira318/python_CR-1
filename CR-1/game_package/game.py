import copy
from enum import Enum
import argparse
import random

from map_package.cell import RubberRoom, LeaveRes, Teleport, change_coord_from_direction
from game_package.gamer import Gamer


class TurnRes(Enum):
    NOT_TURN_END = -1
    NOT_GAME_END = 0
    CURRENT_GAMER_WIN = 1
    CURRENT_GAMER_ESCAPED = 2


class Game:

    def __init__(self, game_map, gamer_number, starting_locations):
        self.game_map = game_map
        self.gamer_list = []
        self.players_amount = gamer_number
        self.gamer_positions = {}
        self.gamer_list = [Gamer(i, starting_locations[i]) for i in range(self.players_amount)]
        for i in range(self.players_amount):
            self.gamer_positions.update({self.gamer_list[i]: starting_locations[i]})
        self.current_gamer_number = 0
        self.current_gamer = self.gamer_list[self.current_gamer_number]
        self.add_turn_parser()

    def __str__(self):
        to_print = 'Game: amount = {}, current_gamer = {}'.format(self.players_amount, self.current_gamer)
        to_print += self.gamer_list.__str__()
        to_print += self.gamer_positions.__str__()
        to_print += 'have map:' + self.game_map.__str__()
        for gamer in self.gamer_list:
            to_print += gamer.__str__()
        to_print += 'the whole game uses map' + self.game_map.__str__()
        return to_print

    def add_turn_parser(self):
        self.turn_parser = argparse.ArgumentParser(description='Choose whats to do')
        turn_subparsers = self.turn_parser.add_subparsers(dest='subcommand')
        for direction in ['up', 'down', 'right', 'left']:
            turn_subparsers.add_parser(direction)
        parser_inventory = turn_subparsers.add_parser('inventory', help='check the patrons shelf and the key')
        parser_skip_turn = turn_subparsers.add_parser('skip', help='skip your turn')
        parser_exit = turn_subparsers.add_parser('exit', help='leave the game')
        parser_shoot = turn_subparsers.add_parser('patron',
                                                  help='write "patron" and then direction to shoot')
        parser_shoot.add_argument('direction', choices=['up', 'down', 'left', 'right'],
                                  help='in which direction you shoot')

    def turn_interface(self):
        if not self.current_gamer.exited:
            if not self.current_gamer.is_stunned:
                print('Gamer №{} turn'.format(self.current_gamer_number + 1))
                while True:
                    command = input().split()
                    try:
                        player_args = self.turn_parser.parse_args(command)
                    except BaseException:
                        print('Invalid command, try again')
                        continue
                    if player_args.subcommand == 'inventory':
                        print('You have {} patrons'.format(self.current_gamer.patrons))
                        if self.game_map.have_key:
                            if self.current_gamer.with_key:
                                print('and you have the key!')
                        continue
                    return self.active_command(player_args)
            else:
                print('Sorry, gamer №{}, you skip the turn'.format(self.current_gamer_number + 1))
                self.current_gamer.time_left -= 1
                if self.current_gamer.time_left <= 0:
                    self.current_gamer.is_stunned = False
        return TurnRes.NOT_GAME_END

    def active_command(self, player_args):
        if player_args.subcommand == 'exit':
            self.current_gamer.exited = True
            return TurnRes.CURRENT_GAMER_ESCAPED
        if player_args.subcommand == 'patron':
            if self.current_gamer.patrons <= 0:
                print("Sorry, but you don't have any patrons to shoot, try something else")
                return TurnRes.NOT_TURN_END
            else:
                self.shoot(player_args.direction)
                return TurnRes.NOT_GAME_END

        if player_args.subcommand == 'skip':
            return TurnRes.NOT_GAME_END
        if player_args.subcommand in {'up', 'down', 'right', 'left'}:
            return self.direction_command(player_args.subcommand)

    def shoot(self, direction):
        self.current_gamer.patrons -= 1
        patron_cell = copy.deepcopy(self.current_gamer.current_cell)
        still = True
        death_list = []
        while still:
            for gamer, cell in self.gamer_positions.items():
                if cell == patron_cell and still and gamer.player_id is not self.current_gamer_number:
                    still = False
                    death_list.append(gamer)
            if death_list:
                dead_gamer = random.choice(death_list)
                dead_gamer.current_cell.key = True
                dead_gamer.death()
            if patron_cell.patron_stun:
                still = False
            future_patron_cell = patron_cell
            x_change, y_change = change_coord_from_direction(direction)
            if self.game_map.check_valid_cell(patron_cell.x + x_change, patron_cell.y + y_change):
                future_patron_cell = self.game_map.cell_from_coord(patron_cell.x + x_change, patron_cell.y + y_change)
            if future_patron_cell != patron_cell and future_patron_cell.id in patron_cell.edges_to:
                patron_cell = future_patron_cell
            else:
                still = False

    def direction_command(self, direction):
        future_cell = self.current_gamer.current_cell
        x_change, y_change = change_coord_from_direction(direction)
        if self.game_map.check_valid_cell(self.current_gamer.current_cell.x + x_change,
                                          self.current_gamer.current_cell.y + y_change):
            future_cell = self.game_map.cell_from_coord(self.current_gamer.current_cell.x + x_change,
                                                        self.current_gamer.current_cell.y + y_change)
        leaving_res = self.current_gamer.current_cell.try_to_leave(self.current_gamer, future_cell, direction)
        if leaving_res == LeaveRes.CURRENT_GAMER_WIN:
            return TurnRes.CURRENT_GAMER_WIN
        if leaving_res == LeaveRes.LEFT:
            self.current_gamer.current_cell = future_cell
            future_cell.arrive(self.current_gamer, self.gamer_positions)
        return TurnRes.NOT_GAME_END

    def run(self):
        while True:
            res = self.turn_interface()
            if res == TurnRes.CURRENT_GAMER_WIN:
                print('Game finished, because gamer №{} has found the exit'.format(self.current_gamer_number + 1))
                break
            else:
                if res == TurnRes.CURRENT_GAMER_ESCAPED:
                    self.players_amount -= 1
                    if self.players_amount <= 0:
                        print('Game will be finished, because all gamers left')
                        break
                else:
                    if res == TurnRes.NOT_GAME_END:
                        self.current_gamer_number = (self.current_gamer_number + 1) % len(self.gamer_list)
                        self.current_gamer = self.gamer_list[self.current_gamer_number]
