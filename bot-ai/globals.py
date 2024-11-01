import threading

game_id = None
current_window = None
current_map = None

round_ended = False

threads_lock = threading.Lock()
threads_stop = threading.Event()
