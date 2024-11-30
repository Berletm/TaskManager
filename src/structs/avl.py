class Node:
    def __init__(self, priority: int, task: str, left=None, right=None):
        self.height = 1
        self.priority = priority
        self.task = task
        self.left = left
        self.right = right

    def __str__(self):
        return f"Task {self.priority} priority is: {self.task}"


class AVLTree:
    def __init__(self):
        self.root = None

    @staticmethod
    def height(node):
        if not node:
            return 0
        return node.height

    def __update_height(self, node: Node):
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def __get_balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def __left_rotation(self, node_a):
        node_b = node_a.right
        node_a.right = node_b.left
        node_b.left = node_a

        self.__update_height(node_a)
        self.__update_height(node_b)

        return node_b

    def __right_rotation(self, node_a):
        node_b = node_a.left
        node_a.left = node_b.right
        node_b.right = node_a

        self.__update_height(node_a)
        self.__update_height(node_b)

        return node_b

    def __balance(self, node):
        if self.__get_balance(node) > 1:
            if self.__get_balance(node.left) < 0:
                node.left = self.__left_rotation(node.left)
            return self.__right_rotation(node)

        elif self.__get_balance(node) < -1:
            if self.__get_balance(node.right) > 0:
                node.right = self.__right_rotation(node.right)
            return self.__left_rotation(node)

        return node

    def __insert(self, node: Node, priority: int, task: str):
        if not node:
            return Node(priority, task)
        elif priority < node.priority:
            node.left = self.__insert(node.left, priority, task)
        elif priority > node.priority:
            node.right = self.__insert(node.right, priority, task)
        else:
            node.task = task

        self.__update_height(node)

        return self.__balance(node)

    def __pre_order(self, node: Node):
        if not node:
            return
        print(node)
        self.__pre_order(node.left)
        self.__pre_order(node.right)

    def __in_order(self, node: Node):
        if not node:
            return
        yield from self.__in_order(node.left)
        yield node
        yield from self.__in_order(node.right)

    def __post_order(self, node: Node):
        if not node:
            return
        self.__post_order(node.left)
        self.__post_order(node.right)
        print(node)

    def __iter__(self):
        return self.__in_order(self.root)

    def rebalance_root(self):
        return self.__balance(self.root)

    def insert(self, priority: int, task: str):
        self.root = self.__insert(self.root, priority, task)

    def __find(self, node: Node, priority: int):
        if not node or node.priority == priority:
            return node
        if node.priority > priority:
            return self.__find(node.left, priority)
        elif node.priority < priority:
            return self.__find(node.right, priority)

    def find_root(self, priority: int):
        return self.__find(self.root, priority)

    def __find_min(self, node):
        if node is None:
            return None
        return self.__find_min(node.left) if node.left is not None else node

    def __remove_element(self, node, element):
        if node is None:
            return None
        if element < node.priority:
            node.left = self.__remove_element(node.left, element)
        elif element > node.priority:
            node.right = self.__remove_element(node.right, element)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            node.priority = self.__find_min(node.right).val
            node.right = self.__remove_element(node.right, node.priority)
        if not node:
            return node
        return self.__balance(node)

    def remove_root(self, element):
        self.__remove_element(self.root, element)
