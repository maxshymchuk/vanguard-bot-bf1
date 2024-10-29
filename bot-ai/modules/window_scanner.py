import pygetwindow as gw
import time
import globals
import config

def scan_window_thread() -> None:
    print(f'Scanning for {config.window_title}')
    while not globals.threads_stop.is_set():
        with globals.threads_lock:
            try:
                globals.current_window = gw.getWindowsWithTitle(config.window_title)[0]
            except IndexError:
                globals.current_window = None
        time.sleep(3) # 3 second interval to check window still exists