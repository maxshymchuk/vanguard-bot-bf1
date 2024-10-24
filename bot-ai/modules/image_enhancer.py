import math
import globals
import cv2 as cv
import numpy as np

def getColorIntervalFromRGB(rgb: tuple[int, int, int], treshold = 80) -> tuple:
    r, g, b = rgb
    hsv = cv.cvtColor(np.uint8([[[r, g, b]]]), cv.COLOR_RGB2HSV)[0][0]
    min = np.array([hsv[0] - treshold, 110, 100])
    max = np.array([hsv[0] + treshold, 255, 255])
    return min, max

def createMasksByColors(image_hsv, *colors) -> tuple:
    masks = []
    for color in colors:
        lower, upper = getColorIntervalFromRGB(color)
        masks.append(cv.inRange(image_hsv, lower, upper))
    return tuple(masks)

def enhance_image(image, target_height = 100):
    image_array = np.array(image)

    height, width = image_array.shape[:2]
    ratio = target_height / height
    image_array = cv.resize(image_array, (math.trunc(ratio * width), math.trunc(ratio * height)), interpolation = cv.INTER_CUBIC)

    image_hsv = cv.cvtColor(image_array, cv.COLOR_RGB2HSV)

    masks = createMasksByColors(image_hsv, globals.allyColor, globals.enemyColor, globals.squadColor)

    mask = cv.bitwise_not(cv.bitwise_or(*masks))
    white_background = np.full_like(image_hsv, 255)
    result = cv.bitwise_and(white_background, white_background, mask = mask)

    # cv.imshow('input', image_array)
    # cv.imshow('output', result)

    return result, mask