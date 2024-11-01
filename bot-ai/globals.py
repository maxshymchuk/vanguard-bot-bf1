import threading

game_id = None
current_window = None
current_map = None

threads_lock = threading.Lock()
threads_stop = threading.Event()
