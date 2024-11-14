import threading
from modules.screenshot import ScreenshotManager

game_id = None
current_window = None

teams_lock = threading.Lock()
teams = None
round_ended = False

kick_lock = threading.Lock()
kick_list = set()
players_kicked = 0

last_player = ''
same_player_count = 0
no_player_count = 0
player_count_too_low = False
rotate_key = 'e'


screenshotmanager = ScreenshotManager()

bot_cycle_paused = False

threads_lock = threading.Lock()
threads_stop = threading.Event()
