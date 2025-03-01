import random
import warnings

from animation import BinarySearchTreeAnimator
from tree import BinarySearchTree


def generate_unique_random_number(n, low=0, high=99):
    numbers = set()
    if n > high:
        warnings.warn("`n` is greater than `high`. Setting `n` to `high`")
        n = high

    while len(numbers) < n:
        x = random.randint(low, high)
        if x not in numbers:
            numbers.add(x)
    numbers = list(numbers)
    random.shuffle(numbers)
    return numbers


def animate_binary_tree_insert(num_nodes):
    tree = BinarySearchTree()
    bst_animator = BinarySearchTreeAnimator(tree)
    values = generate_unique_random_number(num_nodes)

    anim_done = False
    while True:
        # Terminate on user request
        bst_animator.check_events()
        if not anim_done:
            for value in values:
                print("inserting ", value)
                bst_animator.animate_insert(value)

        anim_done = True


if __name__ == "__main__":
    animate_binary_tree_insert(10)
