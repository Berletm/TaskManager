import pytest
import sys

sys.path.append(r"C:\Users\arafa\PycharmProjects\TaskManager")
from TaskManager.src.rbt import RBTree


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
