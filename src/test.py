import pytest
import random
import string
from TaskManager.src.structs.rbt import RBTree


def rand_description_generator(size=3):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


def add_rand_tasks(rbt: RBTree, n_tasks: int):
    for priority in range(n_tasks):
        rbt.insert(len(rbt) + priority + 1, rand_description_generator())


@pytest.mark.parametrize("data, expected", [([(1, "a"), (2, "b"), (3, "c"), (4, "d")],
                                             ["a", "b", "c", "d"]),
                                            ([(333, "a"), (222, "b"), (111, "c"), (444, "d")],
                                             ["c", "b", "a", "d"])])
def test_rbt(data, expected):
    rbt = RBTree()
    for priority, description in data:
        rbt.insert(priority, description)

    for idx, val in enumerate(rbt):
        assert str(val) == expected[idx]
