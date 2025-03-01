"""
Animated quicksort.

NOTE Quicksort is the sorting algorithm used in practice, often with additional improvements, due to O(n log(n)) average running time.
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

screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Quicksort Animation")

BLACK = (0, 0, 0)
BLUE = (58, 148, 255)
ORGANGE = (255, 151, 33)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLDEN_YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)

font = pygame.font.Font(None, 36)

# Number of array elements
num_elements = 10

# Best case: uncomment the line below
array = [10, 15, 40, 30, 20, 75, 70, 95, 90, 50]
num_elements = len(array)

# Uncomment the line below to see the worst-case scenario (when the array is sorted in descending order)
# array = sorted(array)

rect_width = screen_width // num_elements
rect_height = 100
# Place the array in the middle of the screen (roughly)
y = screen_height // 2


# Control how fast the animation will play
clock = pygame.time.Clock()
speed = 720  # cap the frame rate
delay = 0.5  # seconds


def partition(array, low, high):

    # The pivot is chosen as the last element
    pivot = array[high]
    pivot_index = low - 1

    # Indexes of the current partition. To lift the elements slighly higher
    # than rest of the array
    lift_indexes = list(range(low, high + 1))

    draw_array(
        array,
        screen,
        y,
        rect_width,
        rect_height,
        clock,
        speed,
        font,
        highlight_indexes=list(range(low, high + 1)),
        highlight_color=RED,
        lift_indexes=lift_indexes,
    )
    time.sleep(2 * delay)

    for idx in range(low, high):
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
            highlight_indexes=[idx],
            pivot_index=high,
            connect_indexes=[idx, high],
            lift_indexes=lift_indexes,
        )
        time.sleep(delay)

        # Element left to the pivot must be smaller and elements right to the
        # pivot must be larger
        if array[idx] < pivot:
            # If the current element is less than the pivot, move the pivot index forward
            pivot_index += 1
            if pivot_index != idx:
                draw_array(
                    array,
                    screen,
                    y,
                    rect_width,
                    rect_height,
                    clock,
                    speed,
                    font,
                    highlight_color=ORGANGE,
                    pivot_index=high,
                    connect_indexes=[pivot_index, idx],
                    lift_indexes=lift_indexes,
                )
                time.sleep(delay)
                animate_swap(
                    array,
                    pivot_index,
                    idx,
                    y,
                    screen,
                    rect_width,
                    rect_height,
                    clock,
                    speed,
                    font,
                    lift_indexes=lift_indexes,
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
            # Pivot index to highlight depending on the initial pivot index
            highlight_indexes=[pivot_index + 1 if pivot_index > low - 1 else low],
            highlight_color=ORGANGE,
            pivot_index=high,
            lift_indexes=lift_indexes,
        )
        time.sleep(delay)

    pivot_index += 1
    if pivot_index != high and array[pivot_index] != array[high]:
        draw_array(
            array,
            screen,
            y,
            rect_width,
            rect_height,
            clock,
            speed,
            font,
            highlight_color=BLUE,
            pivot_index=high,
            connect_indexes=[pivot_index, high],
            lift_indexes=lift_indexes,
        )
        time.sleep(delay)
        animate_swap(
            array,
            pivot_index,
            high,
            y,
            screen,
            rect_width,
            rect_height,
            clock,
            speed,
            font,
            highlight_color=BLUE,
            lift_indexes=lift_indexes,
        )

    return pivot_index


def quicksort(array, low, high):
    if low < high:
        pivot_index = partition(array, low, high)
        time.sleep(delay)
        quicksort(array, low, pivot_index - 1)
        quicksort(array, pivot_index + 1, high)


def main():
    running = True
    quicksort(array, 0, len(array) - 1)

    Y = (screen_height - rect_height) // 2
    draw_array(
        array,
        screen,
        Y,
        rect_width,
        rect_height,
        clock,
        speed,
        font,
        list(range(len(array))),
        highlight_color=GREEN,
    )

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    array = [random.randint(1, 99) for _ in range(num_elements)]

    main()
