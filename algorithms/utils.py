"""
Utility module for algorithms.
"""

__author__ = "Ahmed Hassan"
__license__ = "MIT"
__email__ = "ahmedhassan@aims.ac.za"


import pygame

BLACK = (0, 0, 0)
BLUE = (58, 148, 255)
LIGHT_BLUE = (170, 214, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLDEN_YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)


def connect_two_array_elments(
    idx1, idx2, y, screen, rect_width, rect_height, color=GOLDEN_YELLOW
):
    """
    Connect the elements at index `idx1` and `idx2` with an inverted U-shape-like lines
    """
    x1 = idx1 * rect_width
    x2 = idx2 * rect_width

    pygame.draw.line(
        screen,
        color,
        (x1 + rect_width // 2, y),
        (x1 + rect_width // 2, y - rect_height // 2),
        2,
    )
    pygame.draw.line(
        screen,
        color,
        (x1 + rect_width // 2, y - rect_height // 2),
        (x2 + rect_width // 2, y - rect_height // 2),
        2,
    )
    pygame.draw.line(
        screen,
        color,
        (x2 + rect_width // 2, y - rect_height // 2),
        (x2 + rect_width // 2, y),
        2,
    )


def _animate_swap(
    array,
    idx1,
    idx2,
    coord,
    y,
    screen,
    rect_width,
    rect_height,
    clock,
    speed,
    font,
    highlight_color=RED,
    lift_indexes=None,
):
    """
    Perform the swapping move of the two elements at index `idx1` and `idx2` in `array`
    """
    screen.fill(BLACK)
    x1, x2, y1, y2 = coord
    y_orig = y
    y_lift = y - rect_height
    for i, val in enumerate(array):
        x = i * rect_width
        y = y_lift if lift_indexes and i in lift_indexes else y_orig
        if i == idx1:
            pygame.draw.rect(screen, highlight_color, (x1, y1, rect_width, rect_height))
            text = font.render(str(array[i]), True, BLACK)
            text_rect = text.get_rect(
                center=(x1 + rect_width // 2, y1 + rect_height // 2)
            )
        elif i == idx2:
            pygame.draw.rect(screen, highlight_color, (x2, y2, rect_width, rect_height))
            text = font.render(str(array[i]), True, BLACK)
            text_rect = text.get_rect(
                center=(x2 + rect_width // 2, y2 + rect_height // 2)
            )
        else:
            pygame.draw.rect(screen, WHITE, (x, y, rect_width, rect_height))
            text = font.render(str(val), True, BLACK)
            text_rect = text.get_rect(
                center=(x + rect_width // 2, y + rect_height // 2)
            )
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(speed)


def animate_swap(
    array,
    idx1,
    idx2,
    y,
    screen,
    rect_width,
    rect_height,
    clock,
    speed,
    font,
    highlight_color=RED,
    lift_indexes=None,
):
    """
    Animate swaping the two elments at position `idx1` and `idx2` in `array`
    """
    # Initial positions of the two squares
    target_y = y - rect_height if lift_indexes else y
    x1, y1 = idx1 * rect_width, target_y
    x2, y2 = idx2 * rect_width, target_y

    # Define target positions for the animation
    target_x1, target_y1 = x2, target_y
    target_x2, target_y2 = x1, target_y

    # Move the larger number up and smaller number down
    while y1 > target_y - rect_height and y2 < target_y + rect_height:

        # Move the larger element up
        if y1 > target_y - rect_height:
            y1 -= 1

        # Move the smaller element down
        if y2 < target_y + rect_height:
            y2 += 1

        # Draw the elements
        _animate_swap(
            array,
            idx1,
            idx2,
            (x1, x2, y1, y2),
            y,
            screen,
            rect_width,
            rect_height,
            clock,
            speed,
            font,
            highlight_color,
            lift_indexes,
        )

    # Move the elements horizontally towards their target x positions
    while x1 != target_x1 or x2 != target_x2:
        if x1 < target_x1:
            x1 += 1
        elif x1 > target_x1:
            x1 -= 1

        if x2 < target_x2:
            x2 += 1
        elif x2 > target_x2:
            x2 -= 1

        _animate_swap(
            array,
            idx1,
            idx2,
            (x1, x2, y1, y2),
            y,
            screen,
            rect_width,
            rect_height,
            clock,
            speed,
            font,
            highlight_color,
            lift_indexes,
        )

    # After reaching target x, move back vertically to their target positions
    while y1 < target_y1 or y2 > target_y2:

        if y1 < target_y1:
            y1 += 1
        if y2 > target_y2:
            y2 -= 1

        _animate_swap(
            array,
            idx1,
            idx2,
            (x1, x2, y1, y2),
            y,
            screen,
            rect_width,
            rect_height,
            clock,
            speed,
            font,
            highlight_color,
            lift_indexes,
        )

    # Finalize the swap in the array
    array[idx1], array[idx2] = array[idx2], array[idx1]


def draw_array(
    array,
    screen,
    y,
    rect_width,
    rect_height,
    clock,
    speed,
    font,
    highlight_indexes=None,
    highlight_color=GOLDEN_YELLOW,
    pivot_index=None,
    pivot_color=BLUE,
    lift_indexes=None,
    connect_indexes=None,
    erase=True,
):
    """
    Draw an array.

    Parameter
    ---------
    highlight_indexes: List[int]
        The indexes of the elements to highlight with `highlight_color`
    highlight_color: Tuple(int, int, int)
        RGB color
    pivot_index: int
        The index of the pivot (i.e. the partition index).
    lift_indexes: List[int]
        The indexes in the current sub-array (partition) that should be lifted
        slightly above of the rest of the array

    NOTE
    `pivot_index` and `lift_indexes` are only relevant for divide and conquer
    sorting algorithms such as quicksort.
    """

    if erase:
        screen.fill(BLACK)

    y_orig = y
    y_lift = y - rect_height

    for i, val in enumerate(array):
        # (x, y) coordinate of the current element
        x = i * rect_width

        y = y_lift if lift_indexes and i in lift_indexes else y_orig

        # Highlight the elements
        if highlight_indexes and i in highlight_indexes:
            color = highlight_color  # or GOLDEN_YELLOW
        elif pivot_index and i == pivot_index:
            color = pivot_color  # or BLUE
        else:
            color = WHITE

        # Draw currnet element
        pygame.draw.rect(screen, color, (x, y, rect_width, rect_height))

        # Display the value in the middle of each square
        text = font.render(str(val), True, BLACK)
        text_rect = text.get_rect(center=(x + rect_width // 2, y + rect_height // 2))
        screen.blit(text, text_rect)

    if connect_indexes:
        connect_two_array_elments(
            connect_indexes[0],
            connect_indexes[1],
            y_lift if lift_indexes else y_orig,
            screen,
            rect_width,
            rect_height,
            color=highlight_color,
        )

    pygame.display.flip()
    clock.tick(speed)
