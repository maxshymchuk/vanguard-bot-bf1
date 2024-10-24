from PIL import Image, ImageGrab

def capture_screen(x: int, y: int, width: int, height: int) -> Image:
    screenshot = ImageGrab.grab(bbox = (x, y, x + width, y + height))
    return screenshot