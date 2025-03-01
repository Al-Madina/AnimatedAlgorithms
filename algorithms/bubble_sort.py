"""
Animated bubble sort
"""

__author__ = "Ahmed Hassan"
__license__ = "MIT"
__email__ = "ahmedhassan@aims.ac.za"

import random
import sys
import time

import pygame
from utils import draw_array, animate_swap

pygame.init()

screen_width, screen_height = 1200, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bubble Sort Animation")

# Font
font = pygame.font.Font(None, 36)


BLACK = (0, 0, 0)
BLUE = (58, 148, 255)
LIGHT_BLUE = (170, 214, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLDEN_YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)


# Input array
num_elements = 10
array = [random.randint(1, 99) for _ in range(num_elements)]

# Best Case: array is already sorted
# Uncomment the line below
# array = sorted(array)

# Worst Case: array is reverse sorted
# Uncomment the line below
# array = sorted(array, reverse=True)

rect_width = screen_width // num_elements
rect_height = 100
# Place the array in the middle of the screen
y = (screen_height - rect_height) // 2

# Control animation speed
clock = pygame.time.Clock()
speed = 360  # frame rate
delay = 0.2  # seconds


def bubble_sort(array):
    n = len(array)
    while n >= 1:
        k = 0
        for i in range(1, n):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            draw_array(
                array,
                screen,
                y,
                rect_width,
                rect_height,
                clock,
                speed,
                font,
                highlight_indexes=[i - 1, i],
            )
            time.sleep(delay)
            if array[i - 1] > array[i]:
                animate_swap(
                    array,
                    i - 1,
                    i,
                    y,
                    screen,
                    rect_width,
                    rect_height,
                    clock,
                    speed,
                    font,
                )
                draw_array(
                    array,
                    screen,
                    y,
                    rect_width,
                    rect_height,
                    clock,
                    speed,
                    font,
                    highlight_indexes=[i - 1, i],
                    highlight_color=GREEN,
                )
                time.sleep(delay)
                k = i
        n = k
    draw_array(
        array,
        screen,
        y,
        rect_width,
        rect_height,
        clock,
        speed,
        font,
        list(range(len(array))),
        highlight_color=GREEN,
    )


def main():
    running = True
    bubble_sort(array)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":

    main()
