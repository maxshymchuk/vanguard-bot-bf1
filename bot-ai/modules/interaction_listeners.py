import globals
import keyboard
import config

def on_press():
    globals.bot_cycle_paused = not globals.bot_cycle_paused
    if globals.bot_cycle_paused:
        print("Paused")
    else:
        print("Unpaused")

def register_hotkey():
    keyboard.add_hotkey(config.pause_hotkey, on_press)