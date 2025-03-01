import enum


# Python >= 3.4: https://docs.python.org/3/library/enum.html
class NodeStatus(enum.Enum):
    UNVISITED = 0
    VISITED = 1
    ACCESSED = 2


class TreeNode:
    def __init__(self, value, parent=None):
        self.value: float = value
        self.parent: TreeNode = parent

        # NOTE status is not necessary for BST. Included to viz tree traversal
        self.status: NodeStatus = None

        # NOTE only needed for viz
        self.x = 100
        self.y = 100
        self.radius = 25

    def __eq__(self, other):
        # NOTE comparing parents directly `self.parent == other.parent` will result in indefinite recursion

        if not isinstance(other, TreeNode):
            return False
        return self.value == other.value and self.parent.value == other.parent.value

    def __hash__(self):
        return hash((self.value, self.parent.value))

    def __str__(self):
        return str(self.value)


# TODO move to bst module
class BinaryTreeNode(TreeNode):

    def __init__(self, value, parent=None, left=None, right=None):
        super().__init__(value, parent)
        self.left: BinaryTreeNode = left
        self.right: BinaryTreeNode = right

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False

        parent_value = self.parent.value if self.parent else 0
        left_value = self.left.value if self.left else 0
        right_value = self.right.value if self.right else 0

        other_parent_value = other.parent.value if other.parent else 0
        other_left_value = other.left.value if other.left else 0
        other_right_value = other.right.value if other.right else 0

        return (
            self.value == other.value
            and parent_value == other_parent_value
            and left_value == other_left_value
            and right_value == other_right_value
        )

    def __hash__(self):
        parent_value = self.parent.value if self.parent else 0
        left_value = self.left.value if self.left else 0
        right_value = self.right.value if self.right else 0
        return hash((self.value, parent_value, left_value, right_value))


class AVLNode(BinaryTreeNode):
    def __init__(self, value):
        super().__init__(value)
        self.height = 0

    @classmethod
    def fromBinaryTreeNode(cls, bst_node):
        avl_node = cls(bst_node.value)
        avl_node.parent = bst_node.parent
        avl_node.left = bst_node.left
        avl_node.right = bst_node.right
        avl_node.status = bst_node.status
        avl_node.x = bst_node.x
        avl_node.y = bst_node.y
        return avl_node


class Tree:
    """
    Generic tree class
    """

    def __init__(self):
        self.root = None

        # track the order by which nodes are inserted for anime later. This not necessary but makes viz easier
        self.nodes = []

    def insert(self, value):
        raise NotImplemented("Implement this method in your subclass")

    def delete(self, value):
        raise NotImplemented("Implement this method in your subclass")

    def get_depth(self, node):
        depth = 0
        while node.parent is not None:
            depth += 1
            node = node.parent

        return depth


class BinarySearchTree(Tree):

    def __init__(self):
        super().__init__()

    def _insert(self, node, value, parent=None):
        # If the tree is empty, create a new node, set its parent, and return it
        if node is None:
            new_node = BinaryTreeNode(value)
            new_node.parent = parent

            if not self.root:
                self.root = new_node

            if parent:
                if value < parent.value:
                    parent.left = new_node
                else:
                    parent.right = new_node

            # NOTE Recall to insert the node in `nodes`
            self.nodes.append(new_node)

            # Terminate func
            return

        # Traverse the tree to find the correct insertion point
        if value < node.value:
            # Insert in the left subtree
            self._insert(node.left, value, node)
        elif value > node.value:
            # Insert in the right subtree
            self._insert(node.right, value, node)
        else:
            # Do not allow duplicated key
            return

    def insert(self, value):

        self._insert(self.root, value)

    def _delete(self, node, value):
        # Step 1: Perform standard BST delete
        if node is None:
            return node

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Node with one child or no child
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self.left_most(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)

        return node

    def delete(self, value):
        self._delete(self.root, value)

    def left_most(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def __str__(self):
        pass


def get_descendants(node):
    """Find node descendants including `node`"""

    if node is None:
        return []

    return [node] + get_descendants(node.left) + get_descendants(node.right)


def get_depth(node):
    depth = 0
    while node.parent is not None:
        depth += 1
        node = node.parent

    return depth


class AVLTree(BinarySearchTree):
    def __init__(self):
        super().__init__()

    # TODO complete ...
