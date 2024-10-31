import math
import config
import cv2 as cv
import numpy as np

def get_color_interval_from_rgb(rgb: tuple[int, int, int], treshold = 80) -> tuple:
    r, g, b = rgb
    hsv = cv.cvtColor(np.uint8([[[r, g, b]]]), cv.COLOR_RGB2HSV)[0][0]
    min = np.array([hsv[0] - treshold, 110, 100])
    max = np.array([hsv[0] + treshold, 255, 255])
    return min, max

def create_masks_by_colors(image_hsv, *colors) -> tuple:
    masks = []
    for color in colors:
        lower, upper = get_color_interval_from_rgb(color)
        masks.append(cv.inRange(image_hsv, lower, upper))
    return tuple(masks)

def enhance_image(image, target_height = 100):
    image_array = np.array(image)

    height, width = image_array.shape[:2]
    ratio = target_height / height
    image_array = cv.resize(image_array, (math.trunc(ratio * width), math.trunc(ratio * height)), interpolation = cv.INTER_CUBIC)

    image_hsv = cv.cvtColor(image_array, cv.COLOR_RGB2HSV)

    masks = create_masks_by_colors(image_hsv, config.ally_color, config.enemy_color)

    mask = cv.bitwise_not(cv.bitwise_or(*masks))
    white_background = np.full_like(image_hsv, 255)
    result = cv.bitwise_and(white_background, white_background, mask = mask)

    # cv.imshow('input', image_array)
    # cv.imshow('output', result)

    return result, mask

def enhance_weapon_image(image, target_height = 100):
    image_array = np.array(image)

    image_gray = cv.cvtColor(image_array, cv.COLOR_RGB2GRAY)

    # binary_image = cv.adaptiveThreshold(image_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 3, 1)

    # scale_factor = 1.25

    # # Calculate the new dimensions
    # new_width = int(binary_image.shape[1] * scale_factor)
    # new_height = int(binary_image.shape[0] * scale_factor)

    # result = cv.resize(binary_image, (new_width, new_height), interpolation=cv.INTER_CUBIC)

    return image_gray, image_array