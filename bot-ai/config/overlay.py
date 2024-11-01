import tkinter as tk
from typing import List
import config
from classes import Box, Coordinate

class ConfigOverlay:
    def __init__(self, config_coordinates_strings: List[str], config_boxes_strings: List[str]):

        self.config_coordinates_strings = config_coordinates_strings
        self.config_boxes_strings = config_boxes_strings

        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.2)    
        self.root.state("zoomed")
        #root.overrideredirect(True) 
        self.root.configure(background='grey')

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

    def execute_setup(self) -> tuple[bool, List[Coordinate], List[Box]]:
        print("Starting config setup")
        self.step_idx = 0
        self.setup_complete = False
        self.coordinate_list: List[Coordinate] = []
        self.box_list: List[Box] = []

        print(f'Click on {self.config_coordinates_strings[0]}')
        self.canvas.bind("<Button-1>", self._get_click_position_coord)
        
        self.root.mainloop()
        return self.setup_complete, self.coordinate_list, self.box_list

    def _get_click_position_coord(self, event):
        self.coordinate_list.append(Coordinate(event.x, event.y))
        self.step_idx += 1
        if self.step_idx < len(self.config_coordinates_strings):
            # Next coordinate setup
            print(f'Click on {self.config_coordinates_strings[self.step_idx]}')
        else:
            # Finished coordinates, Goto box setup
            self.step_idx = 0
            self.root.withdraw()
            input('Press enter once on the third person view to continue')
            self.root.deiconify()
            self.root.state("zoomed")
            print(f'Drag box over {self.config_boxes_strings[self.step_idx]} then press enter')
            self.canvas.bind("<Button-1>", self._start_selection)
            self.canvas.bind("<B1-Motion>", self._update_selection)
            self.canvas.bind("<ButtonRelease-1>", self._end_selection)
            self.root.bind("<Return>", self._confirm_selection_box)

    def _start_selection(self, event):
        if self.rect is not None:
            self.canvas.delete(self.rect)
            
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=1)

    def _update_selection(self, event):
        # Update the rectangle as the mouse moves
        if self.rect is not None:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def _end_selection(self, event):
        self.box_end_x = event.x
        self.box_end_y = event.y

    def _confirm_selection_box(self, event):
        if self.rect is not None:
            self.canvas.itemconfig(self.rect, outline='green')
            width = self.start_x + self.box_end_x
            height = self.start_y + self.box_end_y
            self.box_list.append(Box(self.start_x, self.start_y, width, height))
            
            self.root.after(500, self._delete_selection_box)
        
    def _delete_selection_box(self):
        self.canvas.delete(self.rect)
        self.rect = None
        
        self.step_idx += 1
        if self.step_idx < len(self.config_boxes_strings):
            print(f'Drag box over {self.config_boxes_strings[self.step_idx]} then press enter')
        else:
            # Finished setup
            self.setup_complete = True
            self.root.destroy()