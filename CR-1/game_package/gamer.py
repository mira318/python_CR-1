class Gamer:

    def __init__(self, gamer_num, start_cell):
        self.exited = False
        self.player_id = gamer_num
        self.is_stunned = False
        self.patrons = 0
        self.with_key = False
        self.current_cell = start_cell
        self.time_left = 0
        self.start_cell = start_cell

    def __str__(self):
        to_print = 'gamer: player_id {}, exited = {}, stunned = {}, patrons = {}, start_cell = ({}, {}), ' \
                   'current_cell = ({}, {}), time left = {}, with_key = {}'.format(self.player_id,
                                                                                   self.exited, self.is_stunned,
                                                                                   self.patrons, self.start_cell.x,
                                                                                   self.start_cell.y,
                                                                                   self.current_cell.x,
                                                                                   self.current_cell.y, self.time_left,
                                                                                   self.with_key)
        return to_print

    def death(self):
        print('Gamer №{}, sorry but you was killed. You go to you start cell, lose all patrons, lose the key on the '
              'current cell if you had it and miss the next turn'.format(self.player_id + 1))
        # self.with_key = False in init
        self.__init__(self.player_id, self.start_cell)
        self.is_stunned = True
        self.time_left = 1

    def win(self):
        print('My congratulations, gamer №{}, you won'.format(self.player_id + 1))
