from __future__ import annotations

from collections import namedtuple
from collections.abc import Callable
from pprint import pprint
from typing import TypeAlias, TypedDict


Number: TypeAlias = int | float

LeafAlgorithm: TypeAlias = Callable[[Number], Number]


class BinaryTree(TypedDict):

    value: Number
    left: BinaryTree | None
    right: BinaryTree | None


# Значения по умолчанию (вариант с root=11, height=3).
DEFAULT_ROOT: Number = 11
DEFAULT_HEIGHT = 3
DEFAULT_LEFT_LEAF: LeafAlgorithm = lambda root: root ** 2
DEFAULT_RIGHT_LEAF: LeafAlgorithm = lambda root: 2 + root ** 2


_BinaryNodeBase = namedtuple(
    "_BinaryNodeBase",
    ("value", "left", "right"),
    defaults=(None, None),
)


class BinaryNode(_BinaryNodeBase):

    __slots__ = ()
    value: Number
    left: BinaryNode | None
    right: BinaryNode | None


def gen_bin_tree(
    height: int = DEFAULT_HEIGHT,
    root: Number = DEFAULT_ROOT,
    left_leaf: LeafAlgorithm = DEFAULT_LEFT_LEAF,
    right_leaf: LeafAlgorithm = DEFAULT_RIGHT_LEAF,
) -> BinaryTree:

    _validate_height(height)
    _validate_algorithm(left_leaf, "left_leaf")
    _validate_algorithm(right_leaf, "right_leaf")

    tree: BinaryTree = {"value": root, "left": None, "right": None}
    if height == 0:
        return tree

    tree["left"] = gen_bin_tree(
        height - 1,
        left_leaf(root),
        left_leaf,
        right_leaf,
    )
    tree["right"] = gen_bin_tree(
        height - 1,
        right_leaf(root),
        left_leaf,
        right_leaf,
    )
    return tree


def to_namedtuple(tree: BinaryTree | None) -> BinaryNode | None:
    if tree is None:
        return None

    return BinaryNode(
        tree["value"],
        to_namedtuple(tree["left"]),
        to_namedtuple(tree["right"]),
    )


def _validate_height(height: int) -> None:
    if isinstance(height, bool) or not isinstance(height, int):
        raise TypeError("height должен быть целым числом")
    if height < 0:
        raise ValueError("height не может быть отрицательным")


def _validate_algorithm(algorithm: object, parameter_name: str) -> None:
    if not callable(algorithm):
        raise TypeError(f"{parameter_name} должен быть вызываемым объектом")


if __name__ == "__main__":
    pprint(gen_bin_tree(), sort_dicts=False)