from game_package.gamer import Gamer


class Game:

    def __init__(self, given_map, gamer_number, cell_list):
        self.game_map = given_map
        self.gamer_list = []
        self.amount = gamer_number
        self.current_positions = {}
        for i in range(self.amount):
            cur_gamer = Gamer(given_map, i, cell_list[i], self.current_positions)
            self.gamer_list.append(cur_gamer)
        self.current_gamer = 0

    def print_game(self):
        print('Game: amount = {}, current_gamer = {}'.format(self.amount, self.current_gamer))
        print(self.gamer_list)
        print(self.current_positions)
        print('have map:')
        self.game_map.print_lab()
        for i in range(self.amount):
            self.gamer_list[i].print_gamer()
        print('the whole game uses map')
        self.game_map.print_lab()

    def run(self):
        finish = False
        while not finish:
            res = self.gamer_list[self.current_gamer].turn_interface()
            if res == 1:
                finish = True
                print('Game finished, because gamer №{} has found the exit'.format(self.current_gamer + 1))
            else:
                if res == 2:
                    self.amount -= 1
                    if self.amount <= 0:
                        finish = True
                        print('Game will be finished, because all gamers left')
                else:
                    self.current_gamer = (self.current_gamer + 1) % len(self.gamer_list)
