"""
Animated RRT 
"""

__author__ = "Ahmed Hassan"
__license__ = " MIT"
__email__ = "ahmedhassan@aims.ac.za"

import pyglet
import random
import math

# Screen dimensions
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

# Start at the center.
INIT_VERTEX = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# Step size to extend the tree
DELTA = 30

# If a node is within this distance to the target, we are done!
THRESHOLD = 10

# Target radius
RADIUS = 30

# Randomly place the target
TARGET_COORD = (
    random.random() * (SCREEN_WIDTH - RADIUS / 2),
    random.random() * (SCREEN_HEIGHT - RADIUS / 2),
)

# Number of obstacles.
NUM_OBSTACLES = 30

vertices = [INIT_VERTEX]

WINDOW = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
batch = pyglet.graphics.Batch()
pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()
OBSTACLE_IMAGE = pyglet.resource.image("square.png")
OBSTACLE_IMAGE.anchor_x = OBSTACLE_IMAGE.width / 2
OBSTACLE_IMAGE.anchor_y = OBSTACLE_IMAGE.height / 2


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Extend the tree
def extension(nearest_vertex, rand_vertex, delta):
    theta = math.atan2(
        rand_vertex[1] - nearest_vertex[1], rand_vertex[0] - nearest_vertex[0]
    )
    return nearest_vertex[0] + delta * math.cos(theta), nearest_vertex[
        1
    ] + delta * math.sin(theta)


# obstracles will be scaled by this factor; see below
obstacle_size = 0.3 * OBSTACLE_IMAGE.width / 2
obstacle_radius = math.sqrt(2) * obstacle_size
obstacles_coord = []  # Coordinates of the obstacles


# Calc the coordinates of the obstacles while considering the initial vertex, target, and existing obstacles
for _ in range(NUM_OBSTACLES):
    # If the current obstacle collide with an existing object, keep looking for a new position
    while True:
        x = random.random() * (SCREEN_WIDTH - obstacle_radius)
        y = random.random() * (SCREEN_HEIGHT - obstacle_radius)
        # Check if the current position is available
        if (
            distance((x, y), TARGET_COORD) >= obstacle_radius
            and distance((x, y), INIT_VERTEX) >= obstacle_radius
            and all(
                distance((x, y), obs) >= 2 * obstacle_radius for obs in obstacles_coord
            )
        ):
            obstacles_coord.append((x, y))
            break


# Create obstacles
obstacle_sprites = [
    pyglet.sprite.Sprite(OBSTACLE_IMAGE, x, y, batch=batch) for x, y in obstacles_coord
]
for sprite in obstacle_sprites:
    sprite.scale = 0.3

# Draw target
target_circle = pyglet.shapes.Circle(
    TARGET_COORD[0], TARGET_COORD[1], RADIUS, color=(250, 0, 0), batch=batch
)


# Tree
lines = []

# Store the parent for backtracking the path once the target is found
parent_map = {}


# Update function to grow RRT
def update(dt):
    global lines

    # Goal checking: keep growing the tree if the target is not reached
    if distance(vertices[-1], TARGET_COORD) > RADIUS:
        # Random point in the config space
        rand_vertex = random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT

        # Find the nearest point to the random point
        nearest_vertex = min(vertices, key=lambda v: distance(v, rand_vertex))

        # Extend the nearest point in the direction of the random point to create the new point
        new_vertex = extension(nearest_vertex, rand_vertex, DELTA)

        # Collision checking
        if all(
            distance(new_vertex, (obs[0], obs[1])) >= obstacle_radius
            for obs in obstacles_coord
        ):
            parent_map[new_vertex] = nearest_vertex
            vertices.append(new_vertex)
            line = pyglet.shapes.Line(
                nearest_vertex[0],
                nearest_vertex[1],
                new_vertex[0],
                new_vertex[1],
                width=3,
                color=(255, 255, 255),
                batch=batch,
            )
            lines.append(line)
    else:  # The new point is within the target
        current_node = vertices[-1]
        # Backtrack to the root to find the obstacle-free path from the root to the target
        while current_node in parent_map:
            parent_node = parent_map[current_node]
            line = pyglet.shapes.Line(
                current_node[0],
                current_node[1],
                parent_node[0],
                parent_node[1],
                width=3,
                color=(255, 0, 0),
                batch=batch,
            )
            lines.append(line)
            current_node = parent_node


@WINDOW.event
def on_draw():
    WINDOW.clear()
    batch.draw()


# Schedule the update function
if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 20.0)
    pyglet.app.run()
