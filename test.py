from pytst import PyTST

import unittest
class TestPyTST(unittest.TestCase):
    def setUp(self):
        self.tst = PyTST()
        # build tree
        self.tst.insert('a', 1)
        self.tst.insert('ab', 2)
        self.tst.insert('abab', 3)
        self.tst.insert('cab', 4)
        self.tst.insert('ca', 5)
        self.tst.insert('aa', 6)

    def test_search(self):
        node = self.tst.search('a')
        self.assertEqual(1, node.obj_list[0])
        self.assertEqual('a', node.key)
        node = self.tst.search('ab')
        self.assertEqual(2, node.obj_list[0])
        self.assertEqual('ab', node.key)
        node = self.tst.search('abab')
        self.assertEqual(3, node.obj_list[0])
        self.assertEqual('abab', node.key)
        node = self.tst.search('cab')
        self.assertEqual(4, node.obj_list[0])
        self.assertEqual('cab', node.key)
        node = self.tst.search('ca')
        self.assertEqual(5, node.obj_list[0])
        self.assertEqual('ca', node.key)
        node = self.tst.search('aa')
        self.assertEqual(6, node.obj_list[0])
        self.assertEqual('aa', node.key)
        node = self.tst.search('ax')
        self.assertEqual(None, node)

    def test_traverse(self):
        nodes = list(self.tst.traverse())
        self.assertEqual(6, len(nodes))

    def test_prefix_search(self):
        # 'ab'
        nodes = list(self.tst.prefix_search('ab'))
        obj_list = [node.obj_list for node in nodes]
        results = [[2], [3]]
        self.assertEqual(2, len(nodes))
        for element in results:
            self.assert_(element in obj_list)

        # 'a'
        nodes = list(self.tst.prefix_search('a'))
        obj_list = [node.obj_list for node in nodes]
        results = [[1], [2], [3], [6]]
        self.assertEqual(4, len(nodes))
        for element in results:
            self.assert_(element in obj_list)

    def test_suffix_search(self):
        # 'ab'
        # import pdb; pdb.set_trace()
        nodes = list(self.tst.suffix_search('ab'))
        obj_list = [node.obj_list for node in nodes]
        results = [[2], [3], [4]]
        self.assertEqual(3, len(nodes))
        for element in results:
            self.assert_(element in obj_list)

        # 'a'
        nodes = list(self.tst.suffix_search('a'))
        obj_list = [node.obj_list for node in nodes]
        results = [[1], [5], [6]]
        self.assertEqual(3, len(nodes))
        for element in results:
            self.assert_(element in obj_list)


if __name__ == '__main__':
     unittest.main()