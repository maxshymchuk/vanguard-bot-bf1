import threading

game_id = None
current_window = None

teams = None
current_map = None
round_ended = False

bot_cycle_paused = False

threads_lock = threading.Lock()
threads_stop = threading.Event()
