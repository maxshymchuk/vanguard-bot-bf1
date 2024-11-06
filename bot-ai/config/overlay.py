import tkinter as tk
from typing import List
from classes import Box
import pydirectinput
from modules.image_enhancer import enhance_image, enhance_weapon_image
from modules.recognition import recognize_text
from modules.screenshot import ScreenshotManager, crop_image_array
import pygetwindow as gw
import config
import time
from helpers import print_on_same_line
from modules.utils import available_nickname_symbols, available_weapon_symbols

class ConfigOverlay:
    def __init__(self, config_boxes_strings: List[str]):

        self.config_boxes_strings = config_boxes_strings

        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.2)
        self.root.state("zoomed")
        self.root.configure(background='grey')

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.current_instruction_text = ''
        self.instruction_text = self.canvas.create_text(0, 0, text=self.current_instruction_text, anchor="nw", font=("Arial", 14), fill="white")
        bbox = self.canvas.bbox(self.instruction_text)
        self.instruction_rect = self.canvas.create_rectangle(bbox, fill="black", outline="")

        self.DELAY = int(1000 / 60) # Limit to 60fps
        self.update_id = None

    def update_frame(self):
        self.update_id = self.root.after(self.DELAY, self.update_frame)

    def execute_setup(self) -> tuple[bool, List[Box]]:
        print("Starting config setup")
        self.step_idx = 0
        self.setup_complete = False
        self.box_list: List[Box] = []

        print(f'Drag box over {self.config_boxes_strings[self.step_idx]} then press enter')
        self.current_instruction_text = f'Drag box over {self.config_boxes_strings[self.step_idx]} then press enter'
        self.canvas.bind("<Motion>", self._draw_instructions)
        self.canvas.bind("<Button-1>", self._start_selection)
        self.canvas.bind("<B1-Motion>", self._update_selection)
        self.canvas.bind("<ButtonRelease-1>", self._end_selection)
        self.root.bind("<Return>", self._confirm_selection_box)

        self.update_frame()
        self.root.mainloop()
        return self.setup_complete, self.box_list
        
    def _update_instruction(self, event, text: str):
        self.current_instruction_text = text
        self._draw_instructions(event)
        print(text)

    def _draw_instructions(self, event):
        self.canvas.itemconfig(self.instruction_text, text=self.current_instruction_text)
        self.canvas.coords(self.instruction_text, event.x + 20, event.y + 20)
        bbox = self.canvas.bbox(self.instruction_text)
        self.canvas.coords(self.instruction_rect, bbox[0] - 5, bbox[1] - 5, bbox[2] + 5, bbox[3] + 5)
        self.canvas.tag_lower(self.instruction_rect, self.instruction_text)

    def _start_selection(self, event):
        if self.rect is not None:
            self.canvas.delete(self.rect)
        self.start_x = event.x
        self.start_y = event.y
        self.screen_start_x = event.x_root
        self.screen_start_y = event.y_root
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=1)

    def _update_selection(self, event):
        self._draw_instructions(event)
        # Update the rectangle as the mouse moves
        if self.rect is not None:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def _end_selection(self, event):
        self.box_end_y = event.y
        self.screen_box_end_x = event.x_root
        self.screen_box_end_y = event.y_root

    def _confirm_selection_box(self, event):
        if self.rect is not None:
            self.canvas.itemconfig(self.rect, outline='green')
            width = self.screen_box_end_x - self.screen_start_x
            height = self.screen_box_end_y - self.screen_start_y
            # TODO: maybe check for negatives
            self.box_list.append(Box(self.screen_start_x, self.screen_start_y, width, height))

            self.root.after(500, self._delete_selection_box, event)

    def _delete_selection_box(self, event):
        self.canvas.delete(self.rect)
        self.rect = None

        self.step_idx += 1
        if self.step_idx < len(self.config_boxes_strings):
            self._update_instruction(event, f'Drag box over {self.config_boxes_strings[self.step_idx]} then press enter')
        else:
            # Finished setup
            self.setup_complete = True
            if self.update_id is not None:
                self.root.after_cancel(self.update_id)
            self.root.destroy()

def test_overlay():

    active_window = gw.getActiveWindow()

    while not active_window or active_window.title != config.window_title:
        print_on_same_line(f'Window ({config.window_title}) must be active for config test')
        active_window = gw.getActiveWindow()
        time.sleep(1)

    pydirectinput.keyDown('f3')
    time.sleep(0.05)
    pydirectinput.keyUp('f3')

    screenshotmanager = ScreenshotManager()

    for i in range(0, 3):

        time.sleep(0.5)

        game_img = screenshotmanager.capture(active_window.top, active_window.left, active_window.width, active_window.height)
        player_name_img, _ = enhance_image(crop_image_array(game_img, config.player_name_box))
        player = recognize_text(player_name_img, available_nickname_symbols)

        weapon_icon_image = crop_image_array(game_img, config.weapon_icon_box)

        slot1_image = enhance_weapon_image(crop_image_array(game_img, config.weapon_name_box))
        slot1_text = recognize_text(slot1_image, available_weapon_symbols)

        slot2_image = enhance_weapon_image(crop_image_array(game_img, config.weapon_name_slot2_box))
        slot2_text = recognize_text(slot2_image, available_weapon_symbols)

        gadget_slot1_image = enhance_weapon_image(crop_image_array(game_img, config.gadget_slot_1_box))
        gadget_slot2_image = enhance_weapon_image(crop_image_array(game_img, config.gadget_slot_2_box))
        gadget_slot1_text = recognize_text(gadget_slot1_image, available_weapon_symbols)
        gadget_slot2_text = recognize_text(gadget_slot2_image, available_weapon_symbols)

        screenshots = [(player_name_img, player), (weapon_icon_image, 'icon'), (slot1_image, 'slot 1'), (slot2_image, 'slot 2'), (gadget_slot1_image, 'gadget slot 1'),
                       (gadget_slot2_image, 'gadget slot 2')]
        texts = [player, slot1_text, slot2_text, gadget_slot1_text, gadget_slot2_text]
        screenshotmanager.new_folder(f'{player}-TEST_SCREENSHOT')
        screenshotmanager.save_screenshots(screenshots, texts)
        print(f'Screenshot {i + 1} taken for player {player}')

        pydirectinput.keyDown('e')
        time.sleep(0.05)
        pydirectinput.keyUp('e')

    print('Screenshots complete')


