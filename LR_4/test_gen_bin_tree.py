"""
Модуль тестирования функций генерации бинарного дерева из модуля gen_bin_tree.
"""

import unittest
from gen_bin_tree import (
    gen_bin_tree,
    gen_bin_tree_dataclass,
    gen_bin_tree_defaultdict,
    gen_bin_tree_namedtuple,
    gen_bin_tree_userdict,
)


class TestGenBinTree(unittest.TestCase):
    """Набор модульных тестов для проверки генерации бинарного дерева."""

    def test_default_parameters(self) -> None:
        """Проверяет построение дерева с параметрами по умолчанию (Вариант 11)."""
        # По умолчанию: root=11, height=3, left=x**2, right=2+x**2
        tree = gen_bin_tree()
        
        # Корень
        self.assertEqual(tree["value"], 11)
        
        # 2-й уровень (дети корня)
        self.assertEqual(tree["left"]["value"], 11 ** 2)       # 121
        self.assertEqual(tree["right"]["value"], 2 + 11 ** 2)  # 123
        
        # 3-й уровень (дети левого и правого)
        self.assertEqual(tree["left"]["left"]["value"], 121 ** 2)       # 14641
        self.assertEqual(tree["left"]["right"]["value"], 2 + 121 ** 2)  # 14643
        self.assertEqual(tree["right"]["left"]["value"], 123 ** 2)      # 15129
        self.assertEqual(tree["right"]["right"]["value"], 2 + 123 ** 2) # 15131
        
        # Проверка, что на 4-м уровне потомков нет (так как height=3)
        self.assertIsNone(tree["left"]["left"]["left"])

    def test_custom_parameters(self) -> None:
        """Проверяет передачу пользовательских параметров."""
        tree = gen_bin_tree(
            root=3,
            height=2,
            left_leaf=lambda x: x + 2,
            right_leaf=lambda x: x * 3,
        )
        self.assertEqual(tree["value"], 3)
        self.assertEqual(tree["left"]["value"], 5)
        self.assertEqual(tree["right"]["value"], 9)
        self.assertIsNone(tree["left"]["left"])

    def test_edge_cases_height(self) -> None:
        """Проверяет граничные случаи высоты (0, отрицательная, 1)."""
        self.assertEqual(gen_bin_tree(height=0), {})
        self.assertEqual(gen_bin_tree(height=-3), {})

        single = gen_bin_tree(height=1, root=42)
        self.assertEqual(single, {"value": 42, "left": None, "right": None})

    def test_alternative_containers(self) -> None:
        """Проверяет корректность работы альтернативных контейнеров."""
        # 1. namedtuple (тестируем на параметрах варианта)
        nt_tree = gen_bin_tree_namedtuple(height=2)
        self.assertIsNotNone(nt_tree)
        self.assertEqual(nt_tree.value, 11)
        self.assertEqual(nt_tree.left.value, 121)
        self.assertEqual(nt_tree.right.value, 123)
        self.assertIsNone(gen_bin_tree_namedtuple(height=0))

        # 2. defaultdict
        dd_tree = gen_bin_tree_defaultdict(height=2)
        self.assertEqual(dd_tree["left"]["value"], 121)
        self.assertIsNone(dd_tree["left"]["left"])  # Свойство defaultdict

        # 3. UserDict
        ud_tree = gen_bin_tree_userdict(height=2)
        self.assertIsNotNone(ud_tree)
        self.assertEqual(ud_tree["right"]["value"], 123)
        self.assertIsNone(gen_bin_tree_userdict(height=0))

        # 4. dataclass
        dc_tree = gen_bin_tree_dataclass(height=2)
        self.assertIsNotNone(dc_tree)
        self.assertEqual(dc_tree.left.value, 121)
        self.assertIsNone(gen_bin_tree_dataclass(height=0))


if __name__ == "__main__":
    unittest.main()
    