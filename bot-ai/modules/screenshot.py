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
        self.close()

    def capture_box(self, box: Box) -> np.array:
        monitor = {"top": box.y, "left": box.x, "width": box.width, "height": box.height}
        
        sct_img = self.sct.grab(monitor)
        
        img_np = np.array(sct_img)[:, :, :3] 

        return img_np
    
    def save_screenshots(screenshot_names : List[tuple[np.array, str]], title: str, texts: List[str] = []):
        postfix = f'{math.trunc(time.time())}-{title}'
        path = f'{config.screenshots_path}/screenshot-{postfix}'
        os.makedirs(path)

        for screenshot, text in screenshot_names:
            Image.fromarray(screenshot).save(f'{path}/{text}')

        with open(f'{path}/text.txt', 'w') as f:
            for text in texts:
                f.write(text)
