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

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bubble Sort Animation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLDEN_YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)

font = pygame.font.Font(None, 36)

# Input array
NUM_ELEMENTS = 10
array = [random.randint(1, 100) for _ in range(NUM_ELEMENTS)]
RECT_WIDTH = SCREEN_WIDTH // NUM_ELEMENTS
RECT_HEIGHT = 100

# Uncomment the line below to see the best-case scenario (when the array is already sorted)
# array = sorted(array)

# Uncomment the line below to see the worst-case scenario (when the array is sorted in descending order)
# array = sorted(array, reverse=True)

# Control how fast the animation will play
clock = pygame.time.Clock()
SPEED = 360  # frame rate
DELAY = 0.2  # seconds


# Draw the array and highlight the two elements under focus
def draw_array(array, highlight_indexes=None, correct_position=False, final_color=None):
    # highlight_indexes: are the two element under focus

    SCREEN.fill(BLACK)

    for i, val in enumerate(array):
        # (x, y) coordinate of the current element
        x = i * RECT_WIDTH
        y = (SCREEN_HEIGHT - RECT_HEIGHT) // 2

        # Highlight the elements
        if highlight_indexes and i in highlight_indexes and correct_position:
            color = GREEN
        elif highlight_indexes and i in highlight_indexes and not correct_position:
            color = GOLDEN_YELLOW
        else:
            color = final_color or WHITE

        pygame.draw.rect(SCREEN, color, (x, y, RECT_WIDTH, RECT_HEIGHT))

        # Display the value in the middle of each square
        text = font.render(str(val), True, BLACK)
        text_rect = text.get_rect(center=(x + RECT_WIDTH // 2, y + RECT_HEIGHT // 2))
        SCREEN.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(SPEED)


def animate_swap(array, idx1, idx2):
    # Initial positions of the two squares
    x1, y1 = idx1 * RECT_WIDTH, (SCREEN_HEIGHT - RECT_HEIGHT) // 2
    x2, y2 = idx2 * RECT_WIDTH, (SCREEN_HEIGHT - RECT_HEIGHT) // 2

    # Define target positions for the animation
    target_x1, target_y1 = x2, (SCREEN_HEIGHT - RECT_HEIGHT) // 2
    target_x2, target_y2 = x1, (SCREEN_HEIGHT - RECT_HEIGHT) // 2

    # Move the larger number up and smaller number down
    while (
        y1 > (SCREEN_HEIGHT - RECT_HEIGHT) // 2 - RECT_HEIGHT
        and y2 < (SCREEN_HEIGHT - RECT_HEIGHT) // 2 + RECT_HEIGHT
    ):

        SCREEN.fill(BLACK)

        # Move the larger element up
        if y1 > (SCREEN_HEIGHT - RECT_HEIGHT) // 2 - RECT_HEIGHT:
            y1 -= 1

        # Move the smaller element down
        if y2 < (SCREEN_HEIGHT - RECT_HEIGHT) // 2 + RECT_HEIGHT:
            y2 += 1

        # Draw the elements
        for i, val in enumerate(array):
            x = i * RECT_WIDTH
            y = (SCREEN_HEIGHT - RECT_HEIGHT) // 2
            if i == idx1:
                pygame.draw.rect(SCREEN, RED, (x1, y1, RECT_WIDTH, RECT_HEIGHT))
                text = font.render(str(array[i]), True, BLACK)
                text_rect = text.get_rect(
                    center=(x1 + RECT_WIDTH // 2, y1 + RECT_HEIGHT // 2)
                )
            elif i == idx2:
                pygame.draw.rect(SCREEN, RED, (x2, y2, RECT_WIDTH, RECT_HEIGHT))
                text = font.render(str(array[i]), True, BLACK)
                text_rect = text.get_rect(
                    center=(x2 + RECT_WIDTH // 2, y2 + RECT_HEIGHT // 2)
                )
            else:
                pygame.draw.rect(SCREEN, WHITE, (x, y, RECT_WIDTH, RECT_HEIGHT))
                text = font.render(str(val), True, BLACK)
                text_rect = text.get_rect(
                    center=(x + RECT_WIDTH // 2, y + RECT_HEIGHT // 2)
                )
            SCREEN.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(SPEED)

    # Move the elements horizontally towards their target x positions
    while x1 != target_x1 or x2 != target_x2:
        SCREEN.fill(BLACK)

        if x1 < target_x1:
            x1 += 1
        elif x1 > target_x1:
            x1 -= 1

        if x2 < target_x2:
            x2 += 1
        elif x2 > target_x2:
            x2 -= 1

        for i, val in enumerate(array):
            x = i * RECT_WIDTH
            y = (SCREEN_HEIGHT - RECT_HEIGHT) // 2
            if i == idx1:
                pygame.draw.rect(SCREEN, RED, (x1, y1, RECT_WIDTH, RECT_HEIGHT))
                text = font.render(str(array[i]), True, BLACK)
                text_rect = text.get_rect(
                    center=(x1 + RECT_WIDTH // 2, y1 + RECT_HEIGHT // 2)
                )
            elif i == idx2:
                pygame.draw.rect(SCREEN, RED, (x2, y2, RECT_WIDTH, RECT_HEIGHT))
                text = font.render(str(array[i]), True, BLACK)
                text_rect = text.get_rect(
                    center=(x2 + RECT_WIDTH // 2, y2 + RECT_HEIGHT // 2)
                )
            else:
                pygame.draw.rect(SCREEN, WHITE, (x, y, RECT_WIDTH, RECT_HEIGHT))
                text = font.render(str(val), True, BLACK)
                text_rect = text.get_rect(
                    center=(x + RECT_WIDTH // 2, y + RECT_HEIGHT // 2)
                )
            SCREEN.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(SPEED)

    # After reaching target x, move back vertically to their final positions
    while y1 < target_y1 or y2 > target_y2:
        SCREEN.fill(BLACK)

        if y1 < target_y1:
            y1 += 1
        if y2 > target_y2:
            y2 -= 1

        for i, val in enumerate(array):
            x = i * RECT_WIDTH
            y = (SCREEN_HEIGHT - RECT_HEIGHT) // 2
            if i == idx1:
                pygame.draw.rect(SCREEN, RED, (x1, y1, RECT_WIDTH, RECT_HEIGHT))
                text = font.render(str(array[i]), True, BLACK)
                text_rect = text.get_rect(
                    center=(x1 + RECT_WIDTH // 2, y1 + RECT_HEIGHT // 2)
                )
            elif i == idx2:
                pygame.draw.rect(SCREEN, RED, (x2, y2, RECT_WIDTH, RECT_HEIGHT))
                text = font.render(str(array[i]), True, BLACK)
                text_rect = text.get_rect(
                    center=(x2 + RECT_WIDTH // 2, y2 + RECT_HEIGHT // 2)
                )
            else:
                pygame.draw.rect(SCREEN, WHITE, (x, y, RECT_WIDTH, RECT_HEIGHT))
                text = font.render(str(val), True, BLACK)
                text_rect = text.get_rect(
                    center=(x + RECT_WIDTH // 2, y + RECT_HEIGHT // 2)
                )
            SCREEN.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(SPEED)

    # Finalize the swap in the array
    array[idx1], array[idx2] = array[idx2], array[idx1]


def bubble_sort(array):
    n = len(array)
    while n >= 1:
        k = 0
        for i in range(1, n):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return

            draw_array(array, highlight_indexes=[i - 1, i])
            time.sleep(DELAY)
            if array[i - 1] > array[i]:
                animate_swap(array, i - 1, i)
                draw_array(array, highlight_indexes=[i - 1, i], correct_position=True)
                time.sleep(DELAY)
                k = i
        n = k
    draw_array(array, final_color=GREEN)


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
