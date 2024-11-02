import globals
import keyboard
from pynput.mouse import Controller, Button

mouse = Controller()

def on_press():
    globals.bot_cycle_paused = not globals.bot_cycle_paused
    if globals.bot_cycle_paused:
        print("Paused")
    else:
        print("Unpaused")

def register_hotkey():
    keyboard.add_hotkey('ctrl', on_press)

def mouse_click_on(x, y):
    mouse.position = x, y
    mouse.press(Button.left)
    mouse.release(Button.left)