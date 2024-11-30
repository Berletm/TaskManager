class RBNode:
    """ Red-Black tree node implementation """

    def __init__(self, value: int, task: str, color="red"):
        # new nodes by default has to be red
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

    # nil node for tree
    nil = RBNode(0, "", "black")

    def __init__(self):
        # by default tree root is black
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

        # leaves always has to be black
        node.left = self.nil
        node.right = self.nil

        parent = None
        cur_node = self.root

        # looking for place to insert
        while cur_node != self.nil:
            parent = cur_node
            if node.value < cur_node.value:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right

        node.parent = parent

        # no elements in tree
        if parent is None:
            self.root = node
        # changing parent ref according to parent value
        elif node.value < parent.value:
            parent.left = node
        else:
            parent.right = node

        if node.parent is None:
            node.color = "black"
            return

        # in total 3 elements -> no need to balance
        if node.grandparent() is None:
            return

        self.balance_insert(node)

    def balance_insert(self, new_node: RBNode):
        """ fixing violations after inserting a node """

        # red node can not have a red child
        while new_node.parent.color == "red":
            if new_node.parent == new_node.grandparent().right:
                u = new_node.uncle()  # parent parent left
                if u.color == "red":
                    u.color = "black"
                    new_node.parent.color = "black"
                    new_node.grandparent().color = "red"  # parent parent
                    new_node = new_node.grandparent()  # parent parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.__rotate_right(new_node)
                    new_node.parent.color = "black"
                    new_node.grandparent().color = "red"  # parent parent
                    self.__rotate_left(new_node.grandparent())  # parent parent
            else:
                u = new_node.uncle()  # parent parent right

                if u.color == "red":
                    u.color = "black"
                    new_node.parent.color = "black"
                    new_node.grandparent().color = "red"  # parent parent
                    new_node = new_node.grandparent()  # parent parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.__rotate_left(new_node)
                    new_node.parent.color = "black"
                    new_node.grandparent().color = "red"  # parent parent
                    self.__rotate_right(new_node.grandparent())  # parent parent
            if new_node == self.root:
                break
        # root always has to be black
        self.root.color = "black"

    def delete(self, value: int):
        """Deleting node with val == value if node exists"""

        # looking for node to delete
        node_to_delete = self.search(value)

        # node to delete not found
        if node_to_delete == self.nil:
            return

        # save original color of node to delete
        original_color = node_to_delete.color

        # Case 1: node has no left child -> replace with right child
        if node_to_delete.left == self.nil:
            x = node_to_delete.right
            self.__replace_node(node_to_delete, x)

        # Case 2: node has no right child -> replace with left child
        elif node_to_delete.right == self.nil:
            x = node_to_delete.left
            self.__replace_node(node_to_delete, x)

        # Case 3: node has two children -> replace with successor
        else:
            # finding min element in right subtree
            successor = self.__find_min(node_to_delete.right)

            # saving its color
            original_color = successor.color

            # saving its right child
            x = successor.right

            # if the successor has right child we'll lose him -> do not forget to swap successor with its right child
            if successor.parent != node_to_delete:
                self.__replace_node(successor, x)
                successor.right = node_to_delete.right
                successor.right.parent = successor

            # now replace the successor with node to delete
            self.__replace_node(node_to_delete, successor)
            successor.left = node_to_delete.left
            successor.left.parent = successor
            successor.color = node_to_delete.color

        # if original node was black -> we need to balance the tree
        if original_color == "black":
            self.__balance_delete(x)

    def __balance_delete(self, node: RBNode):
        """ fixing violations after removing a node """

        while node != self.root and node.color == "black":
            # Case 1: we are on the left side
            if node == node.parent.left:
                s = node.sibling()  # parent right

                # by the default our node color is black then our sibling has to be black too
                if s.color == "red":
                    # making sibling black too
                    s.color = "black"

                    # our common parent has to be red then
                    node.parent.color = "red"

                    # do the left rotation to make root become black
                    self.__rotate_left(node.parent)

                    # now our sibling has changed so look at our new sibling
                    s = node.sibling()  # parent right

                # black children has to have red parent
                if s.left.color == "black" and s.right.color == "black":
                    # parent color
                    s.color = "red"

                    # going upwards to in the root direction
                    node = node.parent

                else:
                    # parent is black and left children is red -> look at the right children
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.__rotate_right(s)
                        s = node.sibling()  # parent right

                    s.color = node.parent.color
                    node.parent.color = "black"
                    s.right.color = "black"
                    self.__rotate_left(node.parent)

                    # ending while loop
                    node = self.root
            else:
                s = node.sibling()  # parent left
                if s.color == "red":
                    s.color = "black"
                    node.parent.color = "red"
                    self.__rotate_right(node.parent)
                    s = node.sibling()  # parent left

                # red node has to have black children
                if s.right.color == "black" and s.right.color == "black":
                    s.color = "red"
                    node = node.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.__rotate_left(s)
                        s = node.sibling()  # parent left

                    s.color = node.parent.color
                    node.parent.color = "black"
                    s.left.color = "black"
                    self.__rotate_right(node.parent)
                    # ending while loop
                    node = self.root
        # root always has to be black
        node.color = "black"

    def __rotate_right(self, node: RBNode):
        """ right rotation around node """

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

    def __len__(self):
        return sum(1 for _ in self.__in_order(self.root))
