# Animated Algorithms

The objective of this repository is to **animate foundational algorithms in computer science**. By looking into the code alongside the visual demo, learners can develop deeper and more intuitive understanding of these algorithms.

We warmly invite contributions from the community to expand and improve this resource—whether by adding new algorithm visualizations, improving existing code, suggesting enhancements, or making other educators/learners aware of this repository. **Together, we can make this a valuable tool for learners and educators alike.**

# Table of Content

- [Getting Started](#getting-started)
- [Algorithms](#algorithms)
  - [Sort Algorithms](#sort-algorithms)
    - [Bubble Sort](#bubble-sort)
    - [Quick Sort](#quick-sort)
  - [Backtracking Algorithm](#backtracking-algorithm)
  - [RRT Algorithm](#rrt-algorithm)
- [Data Structures](#data-structures)
  - [Binary Search Tree](#binary-search-tree)
- [Contribution](#contribution)

# Getting Started

To get started, you need to follow the steps below

- Clone the repository

```bash
git clone <repository-url>
```

- Navigate to the root directory of the project (the directory which contains `README.md`) and create a virtual environment (`.env`)

```python
python -m venv .env
```

- Activate the environment

```bash
source .env/bin/activate
```

- Install the requirements

```bash
pip install -r requirements.txt
```

Now, you can run any example in the repo. For example, to run the example for the backtracking algorithm, you execute

```bash
python3 backtracking.py
```

# Algorithms

## Sort Algorithms

### Bubble Sort

Bubble Sort is a comparison-based sorting algorithm. It works by repeatedly stepping through the array to be sorted, comparing each pair of adjacent items, and swapping them if they are in the wrong order. This process is repeated until the array is sorted.

You can find the code for the animated the bubble sort algorithm [here](bubble_sort.py).

![Bubble Sort](https://github.com/Al-Madina/dummyrepo/blob/master/gif/bubble_sort.gif)

#### Best-Case Scenario

The best case scenario occurs when the array is already sorted.

![Best-Case](gif/bubble_best_case.gif)

#### Wors-Case Scenario

The worst case scenario occurs when the array is sorted in a descending order (reverse).

![Worst-Case](gif/bubble_worst_case.gif)

### Quick Sort

To be completed ...

## Backtracking Algorithm

Backtracking is a general problem solving technique that builds a solution incrementally and abandons "backtracks" a candidate move if it will lead to invalid solution. Please read more on backtracking [here](https://en.wikipedia.org/wiki/Backtracking). In the case of the eight aueens puzzle, assume we placed <img src="https://latex.codecogs.com/svg.image?k-1" title="https://latex.codecogs.com/svg.image?k-1" /> queens in the first <img src="https://latex.codecogs.com/svg.image?k-1" title="https://latex.codecogs.com/svg.image?k-1" /> rows. The algorithm places a queen in the <img src="https://latex.codecogs.com/svg.image?k^{th}" title="https://latex.codecogs.com/svg.image?k^{th}" /> row as long as it does not threaten a previously placed queen in any of the previous rows. If that is not possible, the algorithm removes the queen in the <img src="https://latex.codecogs.com/svg.image?(k-1)^{th}" title="https://latex.codecogs.com/svg.image?(k-1)^{th}" /> row and try to find a new position for it. If it succeeds, it proceeds forward. Otherwise, it goes backward again to the <img src="https://latex.codecogs.com/svg.image?(k-2)^{th}" title="https://latex.codecogs.com/svg.image?(k-2)^{th}" /> row and so on.

You can find the code for the animated backtracking algorithm [here](backtracking.py).

### Eight Queens Puzzle

The 8 queens puzzle is concerned with placing 8 queens in an <img src="https://latex.codecogs.com/svg.image?8\times8" title="https://latex.codecogs.com/svg.image?8\times8" /> chess board such that no queen threatens any other queen. Please read more on the eight queens puzzle [here](https://en.wikipedia.org/wiki/Eight_queens_puzzle). In this repo we present a solution to the general N queens puzzle in <img src="https://latex.codecogs.com/svg.image?N\times&space;N" title="https://latex.codecogs.com/svg.image?N\times N" /> chess board.

### Animation

In the animation, the forward move is hightlighted in yellow, the backward move is highlighted in red, and a solid red line is drawn to connect the two queens that threaten each other.

#### 4 Queens

<p align="center">
<img src="gif/4_queens.gif" width="600" height="600">
</p>

#### 8 Queens

<p align="center">
<img src="gif/8_queens.gif" width="600" height="600">
</p>

## RRT Algorithm

The Rapidly-exploring Random Tree (RRT) algorithm is a popular path planning algorithm used in robotics and artificial intelligence. It's designed to find a path from a starting point to a goal point in a space with obstacles. Read more about RRT [here](https://en.wikipedia.org/wiki/Rapidly_exploring_random_tree). The version that is implemented in this repository is described below.

You can find the code for the animated RRT [here](RRT.py).

Initialization:

- Start with an empty tree.
- Add the starting point as the root of the tree.

Random Sampling:

- Randomly sample a point in the space. This point is called the _random point_.

Nearest Neighbor Search:

- Find the point in the existing tree that is closest to the random point. This point is called the _nearest point_.

Extension:

- Extend the tree from the nearest point towards the random point by a small step size to create a _new point_.

Collision Checking:

- Check if the path from the nearest point to the new point collides with any obstacles.
  - If there is a collision, discard the new point and repeat the process from step 2.
  - Otherwise, accept the new point and add it to the tree

Goal Checking:

- Check if the new point is close enough to the target.
  - If it is, backtrack the path from the new point to the root to establish the obstacle-free path.
  - Otherwise, repeat the process from step 2.

Termination:

- Repeat steps 2 to 5 until a path to the goal is found or a maximum number of iterations is reached.

### Animation

In the animation, blue rectangles represent obstacles, a red circle indicates the target, and the tree grows from the screen's center.

#### Small Tree

<p align="center">
<img src="gif/rrt_small.gif" width="600" height="600">
</p>

#### Large Tree

<p align="center">
<img src="gif/rrt_large.gif" width="600" height="600">
</p>

# Data Structures

## Binary Search Tree

To be completed ...

# Contribution

If you would like to contribute, whether by adding new features, improving the codebase, bug fixing, or providing feedback, your input is greatly appreciated. **Please feel free to open issues, submit pull requests, or suggest improvements.** If you would like to **become a collaborator**, please drop me an email at <a href="mailto:ahmedhassan@aims.ac.za">ahmedhassan@aims.ac.za</a>.

The animated algorithms are created in Python. You can use any Python library to create your animated algorithms. Currently, both [Pygame](https://pypi.org/project/pygame/) and [Pyglet](https://pypi.org/project/pyglet/) are used. If you use something else, please remember to add it to the `requirements.txt` if it is not already there.
