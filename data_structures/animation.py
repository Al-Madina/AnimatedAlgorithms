"""
A module to handle animation logic

NOTE if the codebase grows, consider refactoring this module
"""

import math
import sys
import time
from collections import namedtuple

import pygame
from tree import AVLTree, BinaryTreeNode, Tree

BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (58, 148, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLDEN_YELLOW = (255, 215, 0)
GREEN = (30, 128, 30)

# Represent a point in the xy-plane
Point = namedtuple("Point", ["x", "y"])

# Represent a small incremental step to the current position towards the target
Step = namedtuple("Step", ["stepx", "stepy"])


class Setting:

    def __init__(self):
        # Screen
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = BLACK

        # Font
        self.font_color = WHITE
        self.font_size = 36
        self.font = pygame.font.Font(None, self.font_size)

        # Animation speed
        self.fps = 30
        self.delay = 0.2  # seconds
        self.anim_step_duration = 0.5  # seconds
        self.clock = pygame.time.Clock()

        # Small margins: horizontal and vertical
        self.hspace = self.screen_width // 12
        self.vspace = self.screen_height // 8


class TreeSetting(Setting):

    def __init__(self):
        super().__init__()
        self.node_radius = 25
        self.node_color = RED
        self.edge_color = WHITE
        self.edge_width = 3


class DataStrucAnimator:
    """
    A generic class for animating data structures.

    The class animate three basic operations shared by most data structures:
        1. Insert
        2. Delete
        3. Query: looking for specific element in the data structure

    Concrete classes should extend this class by implementating these methods
    """

    def __init__(self, setting=None, title=None):
        pygame.init()

        self.setting = Setting() if not setting else setting
        self.screen = pygame.display.set_mode(
            (self.setting.screen_width, self.setting.screen_height)
        )
        self.screen.fill(self.setting.bg_color)

        # Change title in subclasses
        if title:
            pygame.display.set_caption(title)

    def check_events(self):
        # Quit animation by clicking the exit button or pressing 'q' in keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_q
            ):
                pygame.quit()
                sys.exit()

    # def _update_screen(self):
    #     raise NotImplemented("Implement this method in your subclass")

    def animate_insert(self, value):
        raise NotImplemented("Implement this method in your subclass")

    def animate_delete(self, value):
        raise NotImplemented("Implement this method in your subclass")

    def animate_query(self, value):
        raise NotImplemented("Implement this method in your subclass")

    def step_size(self, start: Point, end: Point):
        dx = end.x - start.x
        dy = end.y - start.y
        # distance = math.sqrt(dx**2 + dy**2)
        steps = self.setting.fps * self.setting.anim_step_duration
        stepx = dx / steps
        stepy = dy / steps
        # delta = distance / steps
        # stepx = delta if dx > 0 else -delta
        # stepy = delta if dy > 0 else -delta
        return Step(stepx, stepy)


class TreeAnimator(DataStrucAnimator):
    """
    Generic tree animator providing the logic shared by concrete trees: BST, AVL, etc
    """

    def __init__(self, tree: Tree, setting=None, title="Generic Tree"):
        super().__init__()
        if setting and isinstance(TreeSetting):
            self.setting = setting
        else:
            self.setting = TreeSetting()

        # Change title in subclasses
        pygame.display.set_caption(title)

        # Generic tree
        self.tree = tree

    def _draw_node(
        self,
        node,
        screen=None,
        position: Point = None,
        node_color=RED,
        edge_color=WHITE,
        font=None,
    ):
        x = node.x if position is None else position.x
        y = node.y if position is None else position.y

        # Optionally, provide the screen. This is to support static surfaces which are fast to blit
        screen = screen or self.screen

        pygame.draw.circle(screen, node_color, (x, y), self.setting.node_radius)
        edge_color = edge_color or self.setting.edge_color
        pygame.draw.circle(screen, edge_color, (x, y), self.setting.node_radius, 3)
        font = font or self.setting.font
        text = font.render(str(node.value), True, self.setting.font_color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    def _draw_edge(self, node, parent, screen=None, edge_color=None):
        screen = screen or self.screen
        edge_color = edge_color or self.setting.edge_color
        pygame.draw.line(
            screen,
            edge_color,
            (node.x, node.y - self.setting.node_radius),
            (parent.x, parent.y + self.setting.node_radius),
            self.setting.edge_width,
        )

    def _draw_tree(
        self, screen=None, nodes=None, node_color=RED, edge_color=WHITE, font=None
    ):
        """
        Draw tree.

        If `nodes` is provided, it draws the tree from this list of nodes.

        NOTE `nodes` allows for drawing 'subtrees' or 'partial trees'. Useful for viz
        """

        screen = screen or self.screen

        # If node list is not provided, draw the entire tree
        nodes = nodes or self.tree.nodes

        for node in nodes:

            self._draw_node(
                node,
                screen=screen,
                node_color=node_color,
                edge_color=edge_color,
                font=font,
            )

            if node.parent:
                self._draw_edge(node, node.parent, screen=screen, edge_color=edge_color)

    def animate_insert(self, value):
        raise NotImplemented("Implement this method in your subclass")

    def _update_node_position_on_screen(self, node, start, end):
        raise NotImplemented("Implement this method in your subclass")

    def move_node_collection(self, start, end):
        raise NotImplemented("Implement this method in your subclass")

    def animate_node_insert(self, tree):
        raise NotImplemented("Implement this method in your subclass")

    def animate_node_delete(self, tree):
        raise NotImplemented("Implement this method in your subclass")


# NOTE every data structure should has its own animator class
class BinarySearchTreeAnimator(TreeAnimator):

    def __init__(self, tree, setting=None, title="Binary Search Tree"):
        super().__init__(tree, setting, title)

    def _calc_node_position(self, new_node):

        # For calculating the new node's position (x, y)
        x_min, x_max = 0, self.setting.screen_width
        x, y = 0, 0

        current_node = self.tree.root

        # While a position for `new_node` is not found (`current_node` is not a leave), keep going
        while current_node is not None:
            x = (x_max + x_min) // 2
            if new_node.value < current_node.value:
                current_node = current_node.left
                x_max = x
                y += self.setting.vspace
            elif new_node.value > current_node.value:
                current_node = current_node.right
                x_min = x
                y += self.setting.vspace
            else:
                raise ValueError("Duplicated value are not allowed")

        # At this point, a valid position is found
        x = (x_max + x_min) // 2
        y += self.setting.vspace

        new_node.x = x
        new_node.y = y

    def _update_node_position_on_screen(
        self,
        node,
        current_position,
        step,
        screen=None,
        static_surface=None,
    ):
        # Current position of the node on the screen
        x, y = current_position.x, current_position.y
        stepx, stepy = step.x, step.y

        screen = screen or self.screen

        screen.fill(self.setting.bg_color)
        static_surface.fill(self.setting.bg_color)
        self._draw_tree(static_surface)

        # Just blit! No redrawing
        screen.blit(static_surface, (0, 0))

        pos = Point(x + stepx, y + stepy)
        self._draw_node(node, position=pos, node_color=BLUE)

        return pos

    def _animate_rotate(self):
        # Not applicable
        pass

    def animate_insert(self, value):
        # Create a node
        new_node = BinaryTreeNode(value)

        # Calc node's position on the screen
        self._calc_node_position(new_node)
        # node_position = Point(new_node.x, new_node.y)

        self.screen.fill(self.setting.bg_color)

        #  Use static surface to avoid redrawing parts of the tree that have not changed
        static_surface = pygame.Surface(
            (self.setting.screen_width, self.setting.screen_height)
        )

        if not self.tree.root:
            self.tree.insert(value)
            new_node = self.tree.nodes[-1]
            new_node.x = self.setting.screen_width // 2
            new_node.y = self.setting.vspace
            return

        static_surface.fill(self.setting.bg_color)
        self._draw_tree(static_surface)
        self.screen.blit(static_surface, (0, 0))
        pygame.display.flip()
        time.sleep(self.setting.delay)

        # Start from the root
        current_node = self.tree.root

        # Final node position
        final_position_reached = False
        while not final_position_reached:

            # Listen to events
            self.check_events()

            current_pos = Point(current_node.x, current_node.y)

            # Next node in the current path to a leave
            next_node = (
                current_node.left
                if new_node.value < current_node.value
                else current_node.right
            )

            next_pos = (
                Point(next_node.x, next_node.y)
                if next_node
                else Point(new_node.x, new_node.y)
            )

            # Comparison
            if current_pos.x == current_node.x and current_pos.y == current_node.y:
                self.screen.fill(self.setting.bg_color)
                self.screen.blit(static_surface, (0, 0))

                x = (
                    current_node.x + self.setting.hspace
                    if new_node.value >= current_node.value
                    else current_node.x - self.setting.hspace
                )
                y = current_node.y
                pos = Point(x, y)

                self._draw_node(new_node, position=pos, node_color=BLUE)

                # Show the inequality symbol next to the node
                ineq_symbol = "<" if new_node.value < current_node.value else ">"
                # font = pygame.font.Font(None, int(new_node.radius * 2.5))
                text = self.setting.font.render(ineq_symbol, True, WHITE)
                text_rect = text.get_rect(
                    center=((x + current_node.x) // 2, (y + current_node.y) // 2)
                )
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                self.setting.clock.tick(self.setting.fps)

                # More patience here!
                time.sleep(2 * self.setting.delay)

            # Move from current node to next node
            step = self.step_size(current_pos, next_pos)
            while current_pos != next_pos:
                # current_pos.x != next_pos.x and current_pos.y != next_pos.y:
                self.check_events()

                self.screen.fill(self.setting.bg_color)
                self.screen.blit(static_surface, (0, 0))

                self._draw_node(new_node, position=current_pos)

                pygame.display.flip()
                self.setting.clock.tick(self.setting.fps)

                dx = next_pos.x - current_pos.x
                dy = next_pos.y - current_pos.y
                # distance = math.sqrt(dx**2 + dy**2)
                if abs(dx) < abs(step.stepx) and abs(dy) < abs(step.stepy):
                    current_pos = next_pos
                else:
                    x = current_pos.x + step.stepx
                    x = next_pos.x if abs(dx) < abs(step.stepx) else x
                    y = current_pos.y + step.stepy
                    y = next_pos.y if abs(dy) < abs(step.stepy) else y
                    current_pos = Point(x, y)

            if current_pos.x == new_node.x and current_pos.y == new_node.y:
                final_position_reached = True
            else:
                current_node = next_node

        # NOTE do not forget to actually insert the node into the tree!
        self.tree.insert(value)
        new_tree_node = self.tree.nodes[-1]
        new_tree_node.x = new_node.x
        new_tree_node.y = new_node.y

        self.screen.fill(self.setting.bg_color)
        self._draw_tree()
        pygame.display.flip()
        self.setting.clock.tick(self.setting.fps)


class AVLTreeAnimator(BinarySearchTreeAnimator):

    def __init__(self, tree: AVLTree, setting=None, title="AVL Tree"):
        super().__init__(tree, setting, title)

    # TODO complete ...
