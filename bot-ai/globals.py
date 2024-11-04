import threading
from modules.screenshot import ScreenshotManager

game_id = None
current_window = None

teams = None
round_ended = False

screenshotmanager = ScreenshotManager()

bot_cycle_paused = False

threads_lock = threading.Lock()
threads_stop = threading.Event()
