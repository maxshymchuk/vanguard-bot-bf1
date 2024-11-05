import globals
import keyboard

def on_press():
    globals.bot_cycle_paused = not globals.bot_cycle_paused
    if globals.bot_cycle_paused:
        print("Paused")
    else:
        print("Unpaused")

def register_hotkey():
    keyboard.add_hotkey('p', on_press)