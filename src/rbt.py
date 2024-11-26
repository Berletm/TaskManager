class RBNode:
    """ Red-Black tree node implementation """

    def __init__(self, value: int, task: str, color="red"):
        self.value = value
        self.task = task
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        """ returns grandparent of a node if exists """
        if self.parent is None:
            return None
        return self.parent.parent

    def sibling(self):
        """ returns sibling of a node if exists """
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    def uncle(self):
        """ returns uncle of a node if exists """
        if self.parent is None:
            return None
        return self.parent.sibling()

    def __str__(self):
        return f"{self.task}"


class RBTree:
    """ Red-Black tree implementation """
    nil = RBNode(0, "", "black")

    def __init__(self):
        self.root = self.nil

    def search(self, value: int):
        """ searching for node with val == value """
        cur_node = self.root
        while cur_node is not None:
            if cur_node == self.nil or value == cur_node.value:
                return cur_node
            elif value < cur_node.value:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right

    def insert(self, value: int, task: str):
        """ inserting new node into the tree """
        node = RBNode(value, task)
        node.left = self.nil
        node.right = self.nil

        parent = None
        cur_node = self.root

        while cur_node != self.nil:
            parent = cur_node
            if node.value < cur_node.value:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right

        node.parent = parent
        if parent is None:
            self.root = node
        elif node.value < parent.value:
            parent.left = node
        else:
            parent.right = node

        if node.parent is None:
            node.color = "black"
            return

        if node.parent.parent is None:
            return

        self.balance_insert(node)

    def balance_insert(self, new_node: RBNode):
        """ red node can not have a red child """
        while new_node.parent.color == "red":
            if new_node.parent == new_node.parent.parent.right:
                u = new_node.parent.parent.left
                if u.color == "red":
                    u.color = "black"
                    new_node.parent.color = "black"
                    new_node.parent.parent.color = "red"
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.__rotate_right(new_node)
                    new_node.parent.color = "black"
                    new_node.parent.parent.color = "red"
                    self.__rotate_left(new_node.parent.parent)
            else:
                u = new_node.parent.parent.right

                if u.color == "red":
                    u.color = "black"
                    new_node.parent.color = "black"
                    new_node.parent.parent.color = "red"
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.__rotate_left(new_node)
                    new_node.parent.color = "black"
                    new_node.parent.parent.color = "red"
                    self.__rotate_right(new_node.parent.parent)
            if new_node == self.root:
                break
        self.root.color = "black"

    def delete(self, value: int):
        """ deleting node with val == value if node exists """

        node_to_delete = self.search(value)

        if node_to_delete == self.nil:
            return

        y = node_to_delete
        y_original_color = y.color

        if node_to_delete.left == self.nil:
            x = node_to_delete.right
            self.__replace_node(node_to_delete, node_to_delete.right)
        elif node_to_delete.right == self.nil:
            x = node_to_delete.left
            self.__replace_node(node_to_delete, node_to_delete.left)
        else:
            successor = self.__find_min(node_to_delete.right)
            y_original_color = successor.color
            x = successor.right
            if successor.parent == node_to_delete:
                x.parent = successor
            else:
                self.__replace_node(successor, successor.right)
                successor.right = node_to_delete.right
                successor.right.parent = successor

            self.__replace_node(node_to_delete, successor)
            successor.left = node_to_delete.left
            successor.left.parent = successor
            successor.color = node_to_delete.color

        if y_original_color == "black":
            self.__balance_delete(x)

    def __balance_delete(self, node: RBNode):
        while node != self.root and node.color == "black":
            if node == node.parent.left:
                s = node.parent.right
                if s.color == "red":
                    s.color = "black"
                    node.parent.color = "red"
                    self.__rotate_left(node.parent)
                    s = node.parent.right

                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    node = node.parent
                else:
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.__rotate_right(s)
                        s = node.parent.right

                    s.color = node.parent.color
                    node.parent.color = "black"
                    s.right.color = "black"
                    self.__rotate_left(node.parent)
                    node = self.root
            else:
                s = node.parent.left
                if s.color == "red":
                    s.color = "black"
                    node.parent.color = "red"
                    self.__rotate_right(node.parent)
                    s = node.parent.left

                if s.right.color == "black" and s.right.color == "black":
                    s.color = "red"
                    node = node.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.__rotate_left(s)
                        s = node.parent.left

                    s.color = node.parent.color
                    node.parent.color = "black"
                    s.left.color = "black"
                    self.__rotate_right(node.parent)
                    node = self.root
        node.color = "black"

    def __rotate_right(self, node: RBNode):
        # right rotation around node
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    def __rotate_left(self, node: RBNode):
        """ left rotation around node """
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def __replace_node(self, old_node: RBNode, new_node: RBNode):
        """ forgetting about old_node and placing new_node instead """
        if old_node.parent is None:
            self.root = new_node
        elif old_node == old_node.parent.left:
            old_node.parent.left = new_node
        else:
            old_node.parent.right = new_node
        new_node.parent = old_node.parent

    def __find_min(self, node: RBNode) -> RBNode:
        """ finds minimum val node in a tree """
        while node.left != self.nil:
            node = node.left
        return node

    def __pre_order(self, node: RBNode):
        if not node:
            return
        yield node
        yield from self.__pre_order(node.left)
        yield from self.__pre_order(node.right)

    def __in_order(self, node: RBNode):
        if not node or node == self.nil:
            return
        yield from self.__in_order(node.left)
        yield node
        yield from self.__in_order(node.right)

    def __post_order(self, node: RBNode):
        if not node:
            return
        yield from self.__post_order(node.left)
        yield from self.__post_order(node.right)
        yield node

    def __iter__(self):
        return self.__in_order(self.root)
