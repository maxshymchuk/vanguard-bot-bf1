import threading
import argparse

game_id = None
config_inited = False
current_window = None

threads_lock = threading.Lock()
threads_stop = threading.Event()

parser = argparse.ArgumentParser(prog = 'Vanguard Bot Tool', exit_on_error = False, argument_default = argparse.SUPPRESS)#, add_help = False
parser.add_argument('-s', '--start', action = 'store_true')
parser.add_argument('-c', '--config', action = 'store_true')
parser.add_argument('-v', '--verbose', action = 'store_true')
parser.add_argument('--ally-color', help='ALLY_COLOR = RGB [int, int, int]')
parser.add_argument('--enemy-color', help='ENEMY_COLOR = RGB [int, int, int]')
parser.add_argument('--squad-color', help='SQUAD_COLOR = RGB [int, int, int]')