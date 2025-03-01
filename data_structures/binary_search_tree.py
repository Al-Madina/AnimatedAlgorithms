"""
Animated binary search tree

NOTE THIS IS A LEGACY APPROACH USED BEFORE MOVING TO THE OOP APPROACH. See `tree.py` and `animation.py`
"""

__author__ = "Ahmed Hassan"
__license__ = "MIT"
__email__ = "ahmedhassan@aims.ac.za"


import enum
import math
import random
import sys
import time

import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1200, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Binary Search Tree")

# Colors
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (58, 148, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLDEN_YELLOW = (255, 215, 0)
GREEN = (30, 128, 30)

# Calculate node radius and vertical spacing
radius = 25  # max(20, min(SCREEN_WIDTH, SCREEN_HEIGHT) // 30)
# Vertical spacing between tree  levels
vspace = screen_height // 8
delta_width = screen_width // 12

# Number of nodes
num_nodes = 15
# Generate a random list of numbers
array = [random.randint(1, 99) for _ in range(num_nodes)]


def balance_array_for_bst(array):
    """
    Reorders the array for balanced BST creation.
    """

    def _create_balanced_bst_from_tree(arr):
        if not arr:
            return []

        middle_index = len(arr) // 2
        root = arr[middle_index]
        left_subtree = _create_balanced_bst_from_tree(arr[:middle_index])
        right_subtree = _create_balanced_bst_from_tree(arr[middle_index + 1 :])

        return [root] + left_subtree + right_subtree

    return _create_balanced_bst_from_tree(sorted(array))


# NOTE Most efficient BST (balanced BST). Uncomment the line below
array = balance_array_for_bst(array)

# NOTE Least efficient BST
# array = sorted(array)

# Storing the nodes in the order by which they are inserted.
# NOTE this is not necessary but simplifies working with viz
node_sequence = []

# Control animation speed
clock = pygame.time.Clock()
speed = 360  # frame rate
delay = 0.3  # seconds


# NOTE Enum are useful to define enumerated constants.
# Enum are not normal Python classes (Python >= 3.4)
# https://docs.python.org/3/library/enum.html
class NodeStatus(enum.Enum):
    UNVISITED = 0
    VISITED = 1
    ACCESSED = 2


# Binary Tree Node
class BSTNode:
    def __init__(self, value):
        self.value: float = value
        self.parent: BSTNode = None
        self.left: BSTNode = None
        self.right: BSTNode = None

        # NOTE status is not necessary for BST. Included to viz tree traversal
        self.status: NodeStatus = None

        # NOTE (x, y) are not necessary for BST. Included for viz only.
        self.x: int = None
        self.y: int = None

    def __eq__(self, other):
        if not isinstance(other, BSTNode):
            return False

        return (
            self.value == other.value
            and self.parent == other.parent
            and self.left == other.left
            and self.right == other.right
        )

    def __hash__(self):
        return hash((self.value, self.parent, self.left, self.right))


# NOTE BSTNode is basically a dataclass. If your Python >= 3.7 consider using
# `dataclass` as it comes with the default implementation for `eq` and `hash`
# https://docs.python.org/3/library/dataclasses.html


def insert_node(root: BSTNode, value: float, node_status=None):
    """
    Insert a new node into the tree rooted at `root`
    """

    # The node to be inserted
    new_node = BSTNode(value)
    new_node.status = node_status

    # The parent of the new node
    current_parent = None

    current_node = root

    # Info for calculating the new node's position (x, y)
    x_min, x_max = 0, screen_width
    x, y = 0, 0

    # While a position for `new_node` is not found (while `current_node` is not a leave)
    while current_node is not None:
        x = (x_max + x_min) // 2
        current_parent = current_node
        if new_node.value < current_node.value:
            current_node = current_node.left
            x_max = x
            y += vspace
        else:
            current_node = current_node.right
            x_min = x
            y += vspace

    # At this point, a valid position is found
    x = (x_max + x_min) // 2
    y += vspace
    new_node.parent = current_parent
    new_node.x = x
    new_node.y = y

    # If current_parent is None, this node is the root.  No further action.
    if current_parent and new_node.value < current_parent.value:
        current_parent.left = new_node
    elif current_parent and new_node.value >= current_parent.value:
        current_parent.right = new_node
    else:
        pass

    # Storing the nodes in the order of their insertion.
    # NOTE this is NOT necessary but simplifies the viz
    node_sequence.append(new_node)

    root = root or new_node

    # Returning the root suffices for tree operations
    return root


def draw_node(node, screen, xy=None, node_color=RED, border_color=WHITE, font=None):

    # Override node colors if `node.status` is not None. Useful for tree traversal
    if node.status == NodeStatus.UNVISITED:
        node_color = GRAY
    elif node.status == NodeStatus.VISITED:
        node_color = RED
    elif node.status == NodeStatus.ACCESSED:
        node_color = GREEN
    else:
        pass

    x = node.x if xy is None else xy[0]
    y = node.y if xy is None else xy[1]
    pygame.draw.circle(screen, node_color, (x, y), radius)
    pygame.draw.circle(screen, border_color, (x, y), radius, 3)  # Border
    font = font or pygame.font.Font(None, int(radius * 1.5))
    text = font.render(str(node.value), True, WHITE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def draw_tree(screen, sequence=None, node_color=RED, border_color=WHITE, font=None):
    """
    Draw tree. If sequence is provided, it draws the tree from this sequence.
    NOTE `sequence` allows for drawing 'subtrees' or 'partial trees'. Useful for viz
    """

    # If sequence is not provided, draw all nodes
    sequence = sequence or node_sequence

    for node in sequence:
        x, y = node.x, node.y

        draw_node(
            node, screen, node_color=node_color, border_color=border_color, font=font
        )

        if node.parent:
            parent_x, parent_y = node.parent.x, node.parent.y  # positions[node.left]
            pygame.draw.line(
                screen, border_color, (x, y - radius), (parent_x, parent_y + radius), 3
            )


def animate_node_insertion(new_node, sequence, screen, anim_steps=2):
    screen.fill(BLACK)
    # NOTE Use static surface to avoid redrawing the tree unnecessarily.
    # Otherwise, the animation will slow as the tree grows larger.
    static_surface = pygame.Surface(screen.get_size())
    static_surface.fill(BLACK)

    # Draw the partially complete tree
    draw_tree(static_surface, sequence)

    # Draw the new node
    current_node = sequence[0]
    x = (
        current_node.x + delta_width
        if new_node.value >= current_node.value
        else current_node.x - delta_width
    )
    y = current_node.y
    xy = (x, y)

    draw_node(new_node, screen, xy=xy)

    # Final node position
    destination_reached = False
    while not destination_reached:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Next node in the current path to a leave
        next_node = (
            current_node.left
            if new_node.value < current_node.value
            else current_node.right
        )

        # Path from current node to next node
        dx = next_node.x - current_node.x
        dy = next_node.y - current_node.y
        distance = math.sqrt(dx**2 + dy**2)
        steps = int(distance / anim_steps)
        step_x = dx / steps
        step_y = dy / steps

        # Current position of the new node
        current_x, current_y = current_node.x, current_node.y

        # Move along the path until a new next node is found
        next_node_reached = False
        while not next_node_reached:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            if current_x == current_node.x and current_y == current_node.y:
                screen.blit(static_surface, (0, 0))
                x = (
                    current_node.x + delta_width
                    if new_node.value >= current_node.value
                    else current_node.x - delta_width
                )
                y = current_node.y
                xy = (x, y)

                draw_node(new_node, screen, xy=xy, node_color=BLUE)

                # Show the inequality symbo next to the node
                ineq_symbol = "<" if new_node.value < current_node.value else ">="
                font = pygame.font.Font(None, int(radius * 2.5))  ### Global font
                text = font.render(ineq_symbol, True, WHITE)
                text_rect = text.get_rect(
                    center=((x + current_node.x) // 2, (y + current_node.y) // 2)
                )
                screen.blit(text, text_rect)
                pygame.display.flip()

                # More patience here!
                time.sleep(2 * delay)

            # Just blit! No redrawing
            screen.blit(static_surface, (0, 0))

            draw_node(new_node, screen, xy=(current_x, current_y), node_color=BLUE)

            # Update the display
            pygame.display.flip()

            # Move closer to the target position
            if abs(current_x - next_node.x) > abs(step_x) or abs(
                current_y - next_node.y
            ) > abs(step_y):
                current_x += step_x
                current_y += step_y
            else:
                # Snap to the final position if close enough
                current_x, current_y = next_node.x, next_node.y
                next_node_reached = True

            # Frame rate
            clock.tick(speed)

        if current_x == new_node.x and current_y == new_node.y:
            destination_reached = True
        else:
            current_node = next_node


# Main loop for dynamic construction
def create_bst_tree(random_numbers):
    root = None
    for value in random_numbers:

        root = insert_node(root, value)

    for i, node in enumerate(node_sequence):
        if i == 0:
            continue
        animate_node_insertion(node, node_sequence[:i], screen)
        draw_tree(screen, node_sequence[: i + 1])
        pygame.display.flip()

    draw_tree(screen)
    pygame.display.flip()


def main():
    running = True
    constructed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Construct and display the BST dynamically only once
        if not constructed:
            create_bst_tree(array)
            constructed = True

        clock.tick(speed)


if __name__ == "__main__":

    main()
