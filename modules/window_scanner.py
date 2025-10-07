import pygetwindow as gw
import time
import globals
import config

def scan_window_thread() -> None:
    print(f'Scanning for {config.window_title}')
    while not globals.threads_stop.is_set():
        with globals.threads_lock:
            try:
                globals.current_window = gw.getActiveWindow()
                if globals.current_window.title != config.window_title:
                    globals.current_window = None
            except IndexError:
                globals.current_window = None
        time.sleep(3)