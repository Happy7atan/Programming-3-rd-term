"""
Модуль для нерекурсивной генерации бинарного дерева и исследования
различных структур данных (контейнеров) для его хранения.
Вариант 11.
"""

import collections
from dataclasses import dataclass
import pprint
import sys
import timeit
from typing import Any, Callable, Optional, Union

# Псевдонимы типов
Number = Union[int, float]
LeafFunc = Callable[[Number], Number]
TreeNodeDict = dict[str, Any]


def gen_bin_tree(
    root: Number = 11,
    height: int = 3,
    left_leaf: LeafFunc = lambda x: x ** 2,
    right_leaf: LeafFunc = lambda x: 2 + x ** 2,
) -> TreeNodeDict:
    """
    Строит бинарное дерево нерекурсивным способом (в виде словаря).

    Алгоритм использует итеративный обход в ширину (BFS) на базе очереди
    collections.deque. Значения по умолчанию соответствуют Варианту 11.

    Args:
        root (int | float): Значение в корне дерева. По умолчанию 11.
        height (int): Высота дерева (количество уровней). По умолчанию 3.
        left_leaf (Callable): Функция вычисления левого потомка.
                              По умолчанию lambda x: x ** 2.
        right_leaf (Callable): Функция вычисления правого потомка.
                               По умолчанию lambda x: 2 + x ** 2.

    Returns:
        dict[str, Any]: Вложенный словарь с ключами 'value', 'left', 'right'.
                        Если height <= 0, возвращает пустой словарь {}.
    """
    if height <= 0:
        return {}

    tree_root: TreeNodeDict = {"value": root, "left": None, "right": None}
    queue: collections.deque[tuple[TreeNodeDict, int]] = collections.deque(
        [(tree_root, 1)]
    )

    while queue:
        current_node, current_level = queue.popleft()

        if current_level < height:
            val = current_node["value"]

            left_node: TreeNodeDict = {
                "value": left_leaf(val),
                "left": None,
                "right": None,
            }
            right_node: TreeNodeDict = {
                "value": right_leaf(val),
                "left": None,
                "right": None,
            }

            current_node["left"] = left_node
            current_node["right"] = right_node

            queue.append((left_node, current_level + 1))
            queue.append((right_node, current_level + 1))

    return tree_root


# ==============================================================================
# ИССЛЕДОВАНИЕ ДРУГИХ СТРУКТУР ДАННЫХ
# ==============================================================================

# 1. collections.namedtuple
TreeNodeNT = collections.namedtuple("TreeNodeNT", ["value", "left", "right"])


def gen_bin_tree_namedtuple(
    root: Number = 11,
    height: int = 3,
    left_leaf: LeafFunc = lambda x: x ** 2,
    right_leaf: LeafFunc = lambda x: 2 + x ** 2,
) -> Optional[TreeNodeNT]:
    """Строит бинарное дерево с использованием collections.namedtuple."""
    if height <= 0:
        return None

    levels: list[list[Number]] = [[root]]
    for _ in range(1, height):
        next_level = []
        for val in levels[-1]:
            next_level.append(left_leaf(val))
            next_level.append(right_leaf(val))
        levels.append(next_level)

    nodes = [TreeNodeNT(v, None, None) for v in levels[-1]]
    for h in range(height - 2, -1, -1):
        nodes = [
            TreeNodeNT(val, nodes[i * 2], nodes[i * 2 + 1])
            for i, val in enumerate(levels[h])
        ]
    return nodes[0]


# 2. collections.defaultdict
def gen_bin_tree_defaultdict(
    root: Number = 11,
    height: int = 3,
    left_leaf: LeafFunc = lambda x: x ** 2,
    right_leaf: LeafFunc = lambda x: 2 + x ** 2,
) -> collections.defaultdict:
    """Строит бинарное дерево на базе контейнера collections.defaultdict."""
    if height <= 0:
        return collections.defaultdict(lambda: None)

    def make_node(val: Number) -> collections.defaultdict:
        node: collections.defaultdict = collections.defaultdict(lambda: None)
        node["value"] = val
        return node

    tree_root = make_node(root)
    queue = collections.deque([(tree_root, 1)])

    while queue:
        curr, level = queue.popleft()
        if level < height:
            val = curr["value"]
            curr["left"] = make_node(left_leaf(val))
            curr["right"] = make_node(right_leaf(val))
            queue.append((curr["left"], level + 1))
            queue.append((curr["right"], level + 1))

    return tree_root


# 3. collections.UserDict
class TreeNodeUserDict(collections.UserDict):
    """Пользовательский контейнер узла дерева на базе collections.UserDict."""

    def __init__(self, value: Number) -> None:
        """Инициализирует узел со значением и пустыми потомками."""
        super().__init__({"value": value, "left": None, "right": None})


def gen_bin_tree_userdict(
    root: Number = 11,
    height: int = 3,
    left_leaf: LeafFunc = lambda x: x ** 2,
    right_leaf: LeafFunc = lambda x: 2 + x ** 2,
) -> Optional[TreeNodeUserDict]:
    """Строит бинарное дерево с использованием collections.UserDict."""
    if height <= 0:
        return None

    tree_root = TreeNodeUserDict(root)
    queue = collections.deque([(tree_root, 1)])

    while queue:
        curr, level = queue.popleft()
        if level < height:
            val = curr["value"]
            curr["left"] = TreeNodeUserDict(left_leaf(val))
            curr["right"] = TreeNodeUserDict(right_leaf(val))
            queue.append((curr["left"], level + 1))
            queue.append((curr["right"], level + 1))

    return tree_root


# 4. dataclass
@dataclass(slots=True)
class TreeNodeDataClass:
    """Контейнер узла бинарного дерева на базе dataclass со слотами."""

    value: Number
    left: Optional["TreeNodeDataClass"] = None
    right: Optional["TreeNodeDataClass"] = None


def gen_bin_tree_dataclass(
    root: Number = 11,
    height: int = 3,
    left_leaf: LeafFunc = lambda x: x ** 2,
    right_leaf: LeafFunc = lambda x: 2 + x ** 2,
) -> Optional[TreeNodeDataClass]:
    """Строит бинарное дерево с использованием dataclass."""
    if height <= 0:
        return None

    tree_root = TreeNodeDataClass(root)
    queue = collections.deque([(tree_root, 1)])

    while queue:
        curr, level = queue.popleft()
        if level < height:
            curr.left = TreeNodeDataClass(left_leaf(curr.value))
            curr.right = TreeNodeDataClass(right_leaf(curr.value))
            queue.append((curr.left, level + 1))
            queue.append((curr.right, level + 1))

    return tree_root


def benchmark_structures() -> None:
    """
    Сравнивает время построения и размер одного узла в памяти
    для различных контейнеров (исследование структур).
    """
    sample_dict = {"value": 1, "left": None, "right": None}
    sample_nt = TreeNodeNT(1, None, None)
    sample_dd = gen_bin_tree_defaultdict(height=1)
    sample_ud = TreeNodeUserDict(1)
    sample_dc = TreeNodeDataClass(1)

    print("\nСравнение контейнеров (высота дерева = 10, 1000 запусков):")
    print("-" * 65)
    print(f"{'Структура':<25} | {'Память (1 узел)':<17} | {'Время (сек)':<12}")
    print("-" * 65)

    tests = [
        ("dict (базовый)", sample_dict, lambda: gen_bin_tree(height=10)),
        ("collections.namedtuple", sample_nt, lambda: gen_bin_tree_namedtuple(height=10)),
        ("collections.defaultdict", sample_dd, lambda: gen_bin_tree_defaultdict(height=10)),
        ("collections.UserDict", sample_ud, lambda: gen_bin_tree_userdict(height=10)),
        ("dataclass (slots=True)", sample_dc, lambda: gen_bin_tree_dataclass(height=10)),
    ]

    for name, node_obj, func in tests:
        mem = sys.getsizeof(node_obj)
        elapsed = timeit.timeit(func, number=1000)
        print(f"{name:<25} | {mem:<12} байт | {elapsed:.4f} с")
    print("-" * 65)


if __name__ == "__main__":
    # Для наглядного вывода используем высоту 3 (как в задании)
    print("Пример дерева по умолчанию (высота 3):")
    pprint.pprint(gen_bin_tree())
    
    # Бенчмарк запускаем на высоте 10, чтобы разница во времени была заметнее
    benchmark_structures()