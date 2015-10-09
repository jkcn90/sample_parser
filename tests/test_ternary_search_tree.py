import unittest
from ternary_search_tree import Node, TernarySearchTree

class TestNode(unittest.TestCase):

    def test_initialization(self):
        node = Node('a', False)
        self.assertEqual(node.token, 'a')
        self.assertFalse(node.is_end_of_word)

        node = Node('b', True)
        self.assertEqual(node.token, 'b')
        self.assertTrue(node.is_end_of_word)

    def test_default_initialization(self):
        node = Node('c')
        self.assertEqual(node.token, 'c')
        self.assertFalse(node.is_end_of_word)

class TestTernarySearchTree(unittest.TestCase):

    def test_initialization(self):
        tree = TernarySearchTree()
        self.assertEqual(tree.token, None)
        self.assertEqual(tree.left, None)
        self.assertEqual(tree.right, None)
        self.assertEqual(tree.center, None)

    def test_add_one_token(self):
        tree = TernarySearchTree()
        tree.add('a')
        self.assertEqual(tree.token, 'a')

    def test_add_one_word(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        self.assertEqual(tree.token, 'A')
        self.assertEqual(tree.right.token, 'n')
        self.assertEqual(tree.right.left.token, ' ')
        self.assertEqual(tree.right.left.right.token, 'a')
        self.assertEqual(tree.right.left.right.center.token, 'a')

    def test_add_two_words(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        tree.add('An aardvark fell off the tree')
        node = tree.right.left.right.center
        self.assertEqual(node.right.token, 'p')
        self.assertEqual(node.right.right.token, 'r')
        self.assertEqual(node.right.right.token, 'r')
        self.assertEqual(node.right.center.token, 'p')
        self.assertEqual(node.right.center.left.token, 'l')

    def test_search_single_token(self):
        tree = TernarySearchTree()
        tree.add('a')
        node = tree.search('a')
        self.assertEqual(node.token, 'a')

    def test_search_not_in_tree(self):
        tree = TernarySearchTree()
        tree.add('a')
        node = tree.search('b')
        self.assertEqual(node, None)

    def test_search(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        tree.add('An aardvark fell off the tree')

        node = tree.search('An aa')
        self.assertEqual(node.token, 'a')
        self.assertFalse(node.is_end_of_word)

        node = tree.search('An aardvark')
        self.assertEqual(node.token, 'k')
        self.assertFalse(node.is_end_of_word)

        node = tree.search('An aaple fell off the tree')
        self.assertEqual(node.token, 'e')
        self.assertTrue(node.is_end_of_word)

    def test_contains(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        tree.add('An aardvark fell off the tree')

        result = tree.contains('An aaple fell off the tree')
        self.assertTrue(result)

        result = tree.contains('An aardvark fell off the tree')
        self.assertTrue(result)

    def test_does_not_contains(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        tree.add('An aardvark fell off the tree')
        result = tree.contains('An penguin fell off the tree')
        self.assertFalse(result)

    def test_get_completions(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        tree.add('An aardvark fell off the tree')
        completions = tree.get_completions('An aa')
        expected = set(['An aapple fell off the tree',
                    'An aardvark fell off the tree'])
        self.assertEqual(set(completions), expected)


if __name__ == '__main__':
    unittest.main()
