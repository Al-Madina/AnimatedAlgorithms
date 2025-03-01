"""
Animated tree traversal
"""

__author__ = "Ahmed Hassan"
__license__ = "MIT"
__email__ = "ahmedhassan@aims.ac.za"

import random
import sys
import time
from collections import deque

import pygame
from binary_search_tree import NodeStatus, draw_tree, insert_node, balance_array_for_bst

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tree Traversal Algorithms")


# # Number of nodes
NUM_NODES = 15

# Storing the nodes in the order by which they are inserted.
# NOTE: this is not necessary but simplifies working with viz
node_sequence = []

# Control how fast the animation will play
clock = pygame.time.Clock()
SPEED = 360  # frame rate
DELAY = 0.9  # seconds


def create_bst_tree_from_array(array):
    root = None
    for value in array:
        root = insert_node(root, value, node_status=NodeStatus.UNVISITED)

    return root


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def inorder(node):

    if node is None:
        return

    draw_tree(screen)
    pygame.display.flip()
    clock.tick(SPEED)
    time.sleep(DELAY)

    if node.left:
        node.left.status = NodeStatus.VISITED
        draw_tree(screen)
        pygame.display.flip()
        clock.tick(SPEED)
        time.sleep(DELAY)

    inorder(node.left)

    node.status = NodeStatus.ACCESSED

    if node.right:
        node.right.status = NodeStatus.VISITED
        draw_tree(screen)
        pygame.display.flip()
        clock.tick(SPEED)
        time.sleep(DELAY)

    inorder(node.right)


def inorder(node):
    """
    Perform an inorder traversal while animating the process.
    Each node's status is updated and the tree is redrawn at each step.
    """
    if node is None:
        return

    # Mark node as visiting (start of left subtree traversal)
    node.status = NodeStatus.VISITED
    draw_tree(screen)
    pygame.display.flip()
    time.sleep(DELAY)
    # pygame.time.delay(DELAY)
    handle_events()

    # Recur on left subtree
    inorder(node.left)

    # Mark node as visited (processing current node)
    node.status = NodeStatus.ACCESSED
    draw_tree(screen)
    pygame.display.flip()
    time.sleep(DELAY)
    # pygame.time.delay(DELAY)
    handle_events()

    # Recur on right subtree
    inorder(node.right)


def preorder(node):
    """
    Perform a preorder traversal while animating the process.
    Each node's status is updated and the tree is redrawn at each step.
    """
    if node is None:
        return

    # Mark node as visiting (processing current node)
    node.status = NodeStatus.VISITED
    draw_tree(screen)
    pygame.display.flip()
    time.sleep(DELAY)
    handle_events()

    # Mark node as visited
    node.status = NodeStatus.ACCESSED
    draw_tree(screen)
    pygame.display.flip()
    time.sleep(DELAY)
    handle_events()

    # Recur on left subtree
    preorder(node.left)

    # Recur on right subtree
    preorder(node.right)


def postorder(node):
    """
    Perform a postorder traversal while animating the process.
    Each node's status is updated and the tree is redrawn at each step.
    """
    if node is None:
        return

    # Recur on left subtree
    postorder(node.left)

    # Recur on right subtree
    postorder(node.right)

    # Mark node as visiting (processing current node)
    node.status = NodeStatus.VISITED
    draw_tree(screen)
    pygame.display.flip()
    time.sleep(DELAY)
    handle_events()

    # Mark node as visited
    node.status = NodeStatus.ACCESSED
    draw_tree(screen)
    pygame.display.flip()
    time.sleep(DELAY)
    handle_events()


def level_order(node):
    """
    Perform a level-order traversal (breadth-first search) while animating the process.
    Each node's status is updated, and the tree is redrawn at each step.
    """
    if node is None:
        return

    # Initialize a queue for level-order traversal
    queue = deque([node])

    while queue:
        current = queue.popleft()  # Get the next node in the queue

        # Mark the current node as visiting
        current.status = NodeStatus.VISITED
        draw_tree(screen)
        pygame.display.flip()
        time.sleep(DELAY)
        handle_events()

        # Mark the current node as visited
        current.status = NodeStatus.ACCESSED
        draw_tree(screen)
        pygame.display.flip()
        time.sleep(DELAY)
        handle_events()

        # Enqueue left child if it exists
        if current.left:
            queue.append(current.left)

        # Enqueue right child if it exists
        if current.right:
            queue.append(current.right)


def main(root, tree_traveral):
    running = True
    constructed = False

    draw_tree(screen)
    pygame.display.flip()
    clock.tick(SPEED)
    time.sleep(DELAY)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        if not constructed:
            tree_traveral(root)
            constructed = True

        draw_tree(screen)
        pygame.display.flip()
        clock.tick(SPEED)


if __name__ == "__main__":

    # Generate a random list of numbers
    array = [random.randint(1, 99) for _ in range(NUM_NODES)]
    array = balance_array_for_bst(array)

    root = create_bst_tree_from_array(array)

    main(root, inorder)
