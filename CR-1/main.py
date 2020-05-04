from game_package.game import Game
from map_package.map import Map
import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Choose mode: the game or the map check and give parameters')
    parser.add_argument("mode", help='check or game')
    parser.add_argument("--field", help='file with the field, should be in the same directory', default='input_map_1')
    parser.add_argument("--gamers", help='amount of gamers', type=int)
    parser.add_argument("--positions", help='file with the gamers positions')
    parser.add_argument("--key", help='write this flag if you use the map with a key', action='store_true')
    return parser


def took_keyboard_pos(given_map):
    took = False
    while not took:
        try:
            x, y = map(int, input().split())
            if given_map.check_valid_cell(x, y):
                took = True
            else:
                print('Invalid coord, please try again')
        except ValueError:
            print('Invalid coord, please try again')
        except EOFError:
            print('Invalid coord, please try again')
    return x, y


def took_position_from_file(args, given_map, cells_list):
    with open(args.positions, 'r') as f:
        for i in range(gamer_number):
            took = False
            while not took:
                x, y = map(int, f.readline().split())
                if given_map.check_valid_cell(x, y):
                    took = True
                    cells_list.append(given_map.cell_from_coord(x, y))
                else:
                    print('Invalid line in position file, move forward')


"""MAIN"""
parser = create_parser()
args = parser.parse_args()
given_map = Map(args.field)
if args.mode == "check":
    given_map.check()
if args.mode == "game":
    if given_map.check():
        gamer_number = 0
        cells_list = []
        if args.gamers is None or args.positions is None:
            print('Field size = {} x {}'.format(given_map.str_n, given_map.row_n))
        if args.gamers is None:
            print('Enter the number of gamers')
            gamer_number = int(input())
        else:
            gamer_number = args.gamers
        if args.positions is None:
            for i in range(gamer_number):
                print('Enter the position of the gamer № {}'.format(i + 1))
                x, y = took_keyboard_pos(given_map)
                cells_list.append(given_map.cell_from_coord(x, y))
        else:
            took_position_from_file(args, given_map, cells_list)
        if args.key:
            print('Enter the location of the key')
            x, y = took_keyboard_pos(given_map)
            given_map.add_key(x, y)
        my_game = Game(given_map, gamer_number, cells_list)
        my_game.run()
    else:
        print('Sorry, but the game should be honest, try with another map')
