import threading

game_id = None
current_window = None

teams = None

bot_cycle_paused = False

round_ended = False

threads_lock = threading.Lock()
threads_stop = threading.Event()
