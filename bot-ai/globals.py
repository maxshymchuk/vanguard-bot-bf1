import threading
import argparse

game_id = None
config_inited = False
current_window = None

threads_lock = threading.Lock()
threads_stop = threading.Event()

parser = argparse.ArgumentParser(prog = 'Vanguard Bot Tool', add_help = False )
parser.add_argument('-c', '--config', action = 'store_true')
parser.add_argument('-v', '--verbose', action = 'store_true')