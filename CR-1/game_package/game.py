from game_package.gamer import Gamer
from enum import Enum


class TurnRes(Enum):
    Not_game_end_situation = 0
    Current_gamer_win = 1
    Current_gamer_escaped = 2


class Game:

    def __init__(self, game_map, gamer_number, starting_locations):
        self.game_map = game_map
        self.gamer_list = []
        self.players_amount = gamer_number
        self.gamers_positions = {}
        self.gamer_list = [Gamer(game_map, i, starting_locations[i], self.gamers_positions)
                           for i in range(self.players_amount)]
        self.current_gamer = 0

    def print_game(self):
        print('Game: amount = {}, current_gamer = {}'.format(self.players_amount, self.current_gamer))
        print(self.gamer_list)
        print(self.gamers_positions)
        print('have map:')
        self.game_map.print_lab()
        for gamer in self.gamer_list:
            gamer.print_gamer()
        print('the whole game uses map')
        self.game_map.print_lab()

    def run(self):
        p = TurnRes
        while 1:
            res = self.gamer_list[self.current_gamer].turn_interface()
            if res == p.Current_gamer_win:
                print('Game finished, because gamer №{} has found the exit'.format(self.current_gamer + 1))
                break
            else:
                if res == p.Current_gamer_escaped:
                    self.players_amount -= 1
                    if self.players_amount <= 0:
                        print('Game will be finished, because all gamers left')
                        break
                else:
                    self.current_gamer = (self.current_gamer + 1) % len(self.gamer_list)
