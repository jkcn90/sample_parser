import unittest
from ternary_search_tree import Node, TernarySearchTree

class TestNode(unittest.TestCase):

    def test_initialization(self):
        node = Node('a')
        self.assertEqual(node.token, 'a')
        self.assertEqual(node.child_tokens_dict['A'], set())
        self.assertEqual(node.left, None)
        self.assertEqual(node.right, None)
        self.assertEqual(node.is_end_of_word_dict, {})

class TestTernarySearchTree(unittest.TestCase):

    def test_add_one_token(self):
        tree = TernarySearchTree()
        tree.add('a')
        node = tree.root_map['a']
        self.assertEqual(node.token, 'a')

    def test_add_one_repeating_token(self):
        tree = TernarySearchTree()
        tree.add('aattaa')
        node = tree.root_map['a']
        self.assertEqual(node.token, 'a')
        self.assertEqual(node.right.child_tokens_dict[2], {'a'})
        self.assertEqual(node.right.left.child_tokens_dict[2], {''})

    def test_add_one_sentence(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        node = tree.root_map['A']
        self.assertEqual(node.token, 'A')
        self.assertEqual(node.right.token, 'n')
        self.assertEqual(node.right.left.token, ' ')
        self.assertEqual(node.right.left.right.token, 'a')

    def test_add_two_sentences(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        tree.add('An aardvark fell off the tree')
        node = tree.root_map['A'].right.left.right
        self.assertEqual(node.right.token, 'p')
        self.assertEqual(node.right.right.token, 'r')
        self.assertEqual(node.right.right.token, 'r')
        self.assertEqual(node.right.token, 'p')
        self.assertEqual(node.right.left.token, 'l')

    def test_search_single_token(self):
        tree = TernarySearchTree()
        tree.add('a')
        node, count = tree.search('a')
        self.assertEqual(node.token, 'a')
        self.assertEqual(count, 1)

    def test_search_repeated_token(self):
        tree = TernarySearchTree()
        tree.add('aaaa')
        node, count = tree.search('aaa')
        self.assertEqual(node.token, 'a')
        self.assertEqual(count, 3)

    def test_search_not_in_tree(self):
        tree = TernarySearchTree()
        tree.add('a')
        node, count = tree.search('b')
        self.assertEqual(node, None)
        self.assertEqual(count, 0)

    def test_search(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        tree.add('An aardvark fell off the tree')

        (node, count) = tree.search('An aa')
        self.assertEqual(node.token, 'a')
        self.assertEqual(count, 2)

        (node, count) = tree.search('An aardvark')
        self.assertEqual(node.token, 'k')
        self.assertEqual(count, 1)

        (node, count) = tree.search('An aapple fell off the tree')
        self.assertEqual(node.token, 'e')
        self.assertEqual(count, 2)

    def test_contains(self):
        tree = TernarySearchTree()
        tree.add('An aapple fell off the tree')
        tree.add('An aardvark fell off the tree')

        result = tree.contains('An aapple fell off the tree')
        self.assertTrue(result)

        result = tree.contains('An aaple fell off the tree')
        self.assertFalse(result)

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

    def test_get_completions_words(self):
        tree = TernarySearchTree()
        sentences = ['An aapple fell off the tree',
                     'An aardvark fell off the tree',
                     'asdf',
                     'asdf airplane asdfpppwpi gjas',
                    ]
        for sentence in sentences:
            for word in sentence.split():
                tree.add(word)
        completions = tree.get_completions('a')
        expected = set(['aapple', 'aardvark', 'asdfpppwpi', 'airplane', 'asdf'])
        self.assertEqual(set(completions), expected)

    def test_get_repeated_completions(self):
        tree = TernarySearchTree()
        tree.add('An aaaaaaaaa')
        tree.add('An aaaaaaaab')
        completions = tree.get_completions('An aa')
        expected = set(['An aaaaaaaaa',
                        'An aaaaaaaab'])
        self.assertEqual(set(completions), expected)


if __name__ == '__main__':
    unittest.main()
