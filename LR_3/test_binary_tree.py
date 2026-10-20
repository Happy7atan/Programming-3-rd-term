import ast
import inspect
import unittest

from binary_tree import (
    BinaryNode,
    BinaryTree,
    DEFAULT_HEIGHT,
    DEFAULT_LEFT_LEAF,
    DEFAULT_RIGHT_LEAF,
    DEFAULT_ROOT,
    gen_bin_tree,
    to_namedtuple,
)


class GenBinTreeTests(unittest.TestCase):

    def test_height_zero_contains_only_root(self) -> None:
        self.assertEqual(
            gen_bin_tree(height=0, root=42),
            {"value": 42, "left": None, "right": None},
        )

    def test_custom_algorithms_are_used_on_every_level(self) -> None:
        tree = gen_bin_tree(
            height=2,
            root=10,
            left_leaf=lambda value: value - 1,
            right_leaf=lambda value: value + 1,
        )

        self.assertEqual(tree["left"]["value"], 9)
        self.assertEqual(tree["right"]["value"], 11)
        self.assertEqual(tree["left"]["left"]["value"], 8)
        self.assertEqual(tree["left"]["right"]["value"], 10)
        self.assertEqual(tree["right"]["left"]["value"], 10)
        self.assertEqual(tree["right"]["right"]["value"], 12)

    def test_default_parameters_match_selected_variant(self) -> None:
        tree = gen_bin_tree()

        self.assertEqual((DEFAULT_ROOT, DEFAULT_HEIGHT), (11, 3))
        # left_leaf: root ** 2
        self.assertEqual(DEFAULT_LEFT_LEAF(10), 100)
        # right_leaf: 2 + root ** 2
        self.assertEqual(DEFAULT_RIGHT_LEAF(10), 102)

        self.assertEqual(tree["value"], 11)
        # left = 11 ** 2 = 121
        self.assertEqual(tree["left"]["value"], 121)
        # right = 2 + 11 ** 2 = 123
        self.assertEqual(tree["right"]["value"], 123)

        self.assertEqual(self._height(tree), 3)
        # Дерево высоты 3 -> 2^(3+1) - 1 = 15 узлов
        self.assertEqual(self._node_count(tree), 15)

    def test_parameters_can_be_overridden_independently(self) -> None:
        tree = gen_bin_tree(height=1, root=10)

        self.assertEqual(tree["value"], 10)
        # left = 10 ** 2 = 100
        self.assertEqual(tree["left"]["value"], 100)
        # right = 2 + 10 ** 2 = 102
        self.assertEqual(tree["right"]["value"], 102)

    def test_result_has_required_keys_in_every_node(self) -> None:
        tree = gen_bin_tree(height=2)
        self._assert_required_keys(tree)

    def test_function_is_recursive(self) -> None:
        syntax_tree = ast.parse(inspect.getsource(gen_bin_tree))
        recursive_calls = [
            node
            for node in ast.walk(syntax_tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "gen_bin_tree"
        ]
        self.assertEqual(len(recursive_calls), 2)

    def test_negative_height_is_rejected(self) -> None:
        for height in (-1, -10):
            with self.subTest(height=height):
                with self.assertRaises(ValueError):
                    gen_bin_tree(height=height)

    def test_non_integer_height_is_rejected(self) -> None:
        for height in (2.5, "3", True):
            with self.subTest(height=height):
                with self.assertRaises(TypeError):
                    gen_bin_tree(height=height)

    def test_non_callable_algorithm_is_rejected(self) -> None:
        with self.assertRaisesRegex(TypeError, "left_leaf"):
            gen_bin_tree(left_leaf=2)
        with self.assertRaisesRegex(TypeError, "right_leaf"):
            gen_bin_tree(right_leaf=None)

    def _assert_required_keys(self, tree: BinaryTree | None) -> None:
        if tree is None:
            return
        self.assertEqual(set(tree), {"value", "left", "right"})
        self._assert_required_keys(tree["left"])
        self._assert_required_keys(tree["right"])

    def _height(self, tree: BinaryTree | None) -> int:
        if tree is None:
            return -1
        return 1 + max(self._height(tree["left"]), self._height(tree["right"]))

    def _node_count(self, tree: BinaryTree | None) -> int:
        if tree is None:
            return 0
        return 1 + self._node_count(tree["left"]) + self._node_count(tree["right"])


class NamedTupleTreeTests(unittest.TestCase):

    def test_conversion_preserves_values_and_shape(self) -> None:
        tree = gen_bin_tree(
            height=1,
            root=5,
            left_leaf=lambda value: value * 2,
            right_leaf=lambda value: value + 2,
        )

        converted = to_namedtuple(tree)

        self.assertIsInstance(converted, BinaryNode)
        self.assertEqual(converted.value, 5)
        self.assertEqual(converted.left.value, 10)
        self.assertEqual(converted.right.value, 7)
        self.assertIsNone(converted.left.left)
        self.assertIsNone(converted.right.right)

    def test_none_is_preserved(self) -> None:
        self.assertIsNone(to_namedtuple(None))

    def test_namedtuple_nodes_are_immutable(self) -> None:
        node = BinaryNode(1)
        with self.assertRaises(AttributeError):
            node.value = 2


if __name__ == "__main__":
    unittest.main(verbosity=2)