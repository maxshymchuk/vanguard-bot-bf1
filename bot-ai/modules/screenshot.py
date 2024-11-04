from typing import List
import mss
from classes import Box
import numpy as np
import time
import math
import config
from PIL import Image
import os

class ScreenshotManager:
    def __init__(self):
        self.sct = mss.mss()

    def __del__(self):
        self.sct.close()

    def capture(self, top, left, width, height) -> np.array:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        
        sct_img = self.sct.grab(monitor)
        
        img_np = np.array(sct_img)[:, :, :3] 

        return img_np
    
    def new_folder(self, title):
        postfix = f'{math.trunc(time.time())}-{title}'
        self.path = f'{config.screenshots_path}/screenshot-{postfix}'
        os.makedirs(self.path)
    
    def save_screenshots(self, screenshot_names : List[tuple[np.array, str]], texts: List[str] = []):
        for screenshot, text in screenshot_names:
            Image.fromarray(screenshot).save(f'{self.path}/{text}.png')

        with open(f'{self.path}/text.txt', 'w') as f:
            f.writelines(text + '\n' for text in texts)

def crop_image_array(image: np.array, box: Box):
    #print(f'{box.y} {box.height} {box.x} {box.width}')
    return image[box.y:box.height + box.y, box.x:box.width + box.x]