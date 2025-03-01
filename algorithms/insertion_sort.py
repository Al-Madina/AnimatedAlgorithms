"""
Animated insertion sort
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

screen_width, screen_height = 1200, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Insertion Sort Animation")

# Font
font = pygame.font.Font(None, 36)

BLACK = (0, 0, 0)
BLUE = (58, 148, 255)
LIGHT_BLUE = (170, 214, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLDEN_YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)


# The number of array elements
num_elements = 10
array = [random.randint(1, 99) for _ in range(num_elements)]

# Uncomment the line below to see the best-case scenario (when the array is already sorted)
# array = sorted(array)

# Uncomment the line below to see the worst-case scenario (when the array is sorted in descending order)
# array = sorted(array, reverse=True)

sorted_array = []
rect_width = screen_width // num_elements
rect_height = 100

y = (screen_height - rect_height) // 2

# Control animation speed
clock = pygame.time.Clock()
speed = 720  # frame rate
delay = 0.5  # seconds


def insertion_sort(array):
    draw_array(
        array,
        screen,
        y,
        rect_width,
        rect_height,
        clock,
        speed,
        font,
        highlight_indexes=[0],
    )
    time.sleep(delay)
    for j in range(1, len(array)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key = array[j]
        draw_array(
            array,
            screen,
            y,
            rect_width,
            rect_height,
            clock,
            speed,
            font,
            highlight_indexes=list(range(j)),
            highlight_color=GREEN,
        )
        time.sleep(delay)

        draw_array(
            array,
            screen,
            y,
            rect_width,
            rect_height,
            clock,
            speed,
            font,
            highlight_indexes=[j],
        )
        time.sleep(delay)
        i = j - 1
        while i >= 0 and array[i] > key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            animate_swap(
                array,
                i,
                i + 1,
                y,
                screen,
                rect_width,
                rect_height,
                clock,
                speed,
                font,
            )
            time.sleep(0.5 * delay)
            i -= 1
        array[i + 1] = key

    draw_array(
        array,
        screen,
        y,
        rect_width,
        rect_height,
        clock,
        speed,
        font,
        highlight_indexes=list(range(len(array))),
        highlight_color=GREEN,
    )


def main():
    running = True
    insertion_sort(array)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":

    main()
