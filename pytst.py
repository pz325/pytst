import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

class TSTNode(object):
    def __init__(self, c, left=None, right=None, mid=None, obj=None):
        self.splitchar = c
        self.left = left
        self.right = right
        self.mid = mid
        self.obj_list = []
        self.key = ''
        if obj != None:
            self.obj_list.add(obj)
    
    def add(self, obj):
        self.obj_list.append(obj)

    def set_key(self, key):
        self.key = key

    def __str__(self):
        ret = '=======\n'
        ret += 'splitchar: {0}\n'.format(self.splitchar)
        if self.left == None:
            ret += 'left: None\n'
        else: 
            ret += 'left: Node({0})\n'.format(self.left.splitchar)
        if self.right == None:
            ret += 'right: None\n'
        else:
            ret += 'right: Node({0})\n'.format(self.right.splitchar)
        if self.mid == None:
            ret += 'mid: None\n'
        else:
            ret += 'mid: Node({0})\n'.format(self.mid.splitchar)
        ret += 'obj_list: {0}\n'.format(self.obj_list)
        ret += 'key: {0}\n'.format(self.key)
        return ret

class PyTST(object):
    """docstring for PyTST"""
    def __init__(self):
        '''
        init PyTST
        '''
        self.root = None
        self.num_nodes = 0
        self.ref_key = ''

    def insert(self, key, obj):
        '''
        '''
        if len(key) == 0:
            return 0
        self.ref_key = key
        if self.root == None:
            self.root = TSTNode(key[0])
            self.num_nodes += 1
        return self.__insert(self.root, key, obj);

    def traverse(self):
        '''
        @return an iterator of all nodes
        '''
        if self.root == None:
            yield None
        else:
            for node in self.__traverse(self.root):
                yield node
    
    def search(self, key):
        '''
        @return the matched node
        '''
        if len(key) == 0:
            return None
        self.ref_key = key
        return self.__search(self.root, key)

    def prefix_search(self, prefix):
        '''
        @return an iterator of the matched nodes
        '''
        if len(prefix) == 0:
            yield None
        elif self.root == None:
            yield None
        else:
            self.ref_key = prefix
            sub_root = self.__search(self.root, prefix)
            if sub_root == None:
                yield None
            else:
                if len(sub_root.obj_list) > 0:
                    yield sub_root
                for node in self.__traverse(sub_root.mid):
                    yield node

    def suffix_search(self, suffix):
        '''
        @return an iterator of the matched nodes
        '''
        if len(suffix) == 0:
            yield None
        elif self.root == None:
            yield None
        else:
            self.ref_key = suffix
            for node in self.__suffix_search(self.root, suffix):
                if node != None:
                    yield node

    def wildcard_search(self, key):
        '''
        wildcard '*' zero or more
        TODO remove continous *
        @return an iterator of obj_list
        '''
        if len(key) == 0: 
            yield None
        elif self.root == None: 
            yield None
        elif key == '*':
            for node in self.traverse():
                yield node
        else:
            for node in self.__wildcard_search(self.root, key):
                if node != None: 
                    yield node

    def near_search(self, key):
        '''
        @return an iterator
        '''
        pass

    def __insert(self, root, key, obj):
        '''
        '''
        logger.debug('key: {0}'.format(key))
        logger.debug(root)
        if key[0] < root.splitchar:
            logger.debug('go left')
            if root.left == None:
                root.left = TSTNode(key[0])
                self.num_nodes += 1
            return self.__insert(root.left, key, obj)
        elif key[0] > root.splitchar:
            logger.debug('go right')
            if root.right == None:
                root.right = TSTNode(key[0])
                self.num_nodes += 1
            return self.__insert(root.right, key, obj)
        else:
            if len(key) == 1:
                logger.debug('reach key end')
                root.add(obj)
                root.set_key(self.ref_key)
                logger.debug(root)
                return 0
            else:
                logger.debug('go mid')
                if root.mid == None:
                    # attach the rest to middle branches
                    while len(key) > 1:
                        root.mid = TSTNode(key[1])
                        self.num_nodes += 1
                        root = root.mid
                        key = key[1:]
                    root.add(obj)
                    root.set_key(self.ref_key)
                    logger.debug(root)
                    return 0
                else:
                    return self.__insert(root.mid, key[1:], obj)

    def __traverse(self, root):
        '''
        return an iterator of all nodes
        '''
        if root.left != None:
            for node in self.__traverse(root.left):
                yield node
        if root.right != None:
            for node in self.__traverse(root.right):
                yield node
        if root.mid != None:
            for node in self.__traverse(root.mid):
                yield node
        if len(root.obj_list) > 0:
            yield root

    def __search(self, root, key):
        '''
        return the node
        '''
        node = root
        while node != None:
            logger.debug('search key: {0}'.format(key))
            logger.debug('search node: {0}'.format(node))
            if key[0] < node.splitchar:
                logger.debug('search left')
                node = node.left
            elif key[0] > node.splitchar:
                logger.debug('search right')
                node = node.right
            else:
                if len(key) == 1:
                    if len(node.obj_list) > 0:
                        return node
                    else:
                        return None
                else:
                    logger.debug('search mid')
                    node = node.mid
                    key = key[1:]
        return None

    def __wildcard_search(self, root, key):
        '''
        wildcard '*' one and many any char
        '''
        # # '*a' matches current node
        # if len(root.obj_list) > 0 and len(key) == 2 and key[0] == '*' and key[1] == root.splitchar:
        #     yield root
        # print(root)
        # print(key)

        # process wildcard as prefix
        if len(key) > 1 and key[0] == '*':
            for node in self.__wildcard_search(root, key[1:]):
                yield node

        if len(key) == 1 and key[0] != '*':
            if key == root.splitchar and len(root.obj_list) > 0:
                # print('    ===== yield ====')
                # print root
                # print key
                # print('    ================')
                yield root
            else:
                yield None
        else:
            if len(key) == 1 and key[0] == '*' and len(root.obj_list) > 0:
                    # print('    ===== yield ====')
                    # print root
                    # print key
                    # print('    ================')
                    yield root
            if root.left != None:
                if key[0] == '*' or key[0] < root.splitchar:
                    for node in self.__wildcard_search(root.left, key):
                            yield node
            if root.right != None:
                if key[0] == '*' or key[0] > root.splitchar:
                    for node in self.__wildcard_search(root.right, key):
                        yield node
            if root.mid != None:
                if key[0] == '*':
                    for node in self.__wildcard_search(root.mid, key):
                        yield node
                elif key[0] == root.splitchar:
                    for node in self.__wildcard_search(root.mid, key[1:]):
                        yield node
                else:
                    yield None
    
    def __suffix_search(self, root, key):
        '''
        '''
        # further search three branch for whole key
        if root.left != None:
            for node in self.__suffix_search(root.left, key):
                yield node
        if root.right != None:
            for node in self.__suffix_search(root.right, key):
                yield node
        if root.mid != None:
            for node in self.__suffix_search(root.mid, key):
                yield node
        # search whole key from root
        node = root
        whole_key = key
        ret = None
        n = 0
        while node != None:
            if whole_key[0] < node.splitchar:
                node = node.left
            elif whole_key[0] > node.splitchar:
                node = node.right
            else:
                if len(whole_key) == 1:
                    if len(node.obj_list) > 0:
                        ret = node
                    break
                else:
                    node = node.mid
                    whole_key = whole_key[1:]
        yield ret

def large_data_test():
    tst = PyTST()
    # load data
    print('======= building tree ========')
    lineNum = 1
    for l in open('data/dic.txt'):
        print('indexing {0} -- {1}'.format(l.strip(), lineNum))
        tst.insert(l.strip(), lineNum)
        lineNum += 1

    print('======= searching ========')
    # import pdb; pdb.set_trace()
    # TV = 23872
    # z's = 25477
    # abase = 13
    # bellman = 2267
    print(tst.search('TV').obj_list)
    print(tst.search("z's").obj_list)
    print(tst.search('abase').obj_list)
    print(tst.search('bellman').obj_list)


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
        for node in nodes:
            print node
        obj_list = [node.obj_list for node in nodes]
        results = [[1], [5], [6]]
        self.assertEqual(3, len(nodes))
        for element in results:
            self.assert_(element in obj_list)


def main():
    # import pdb; pdb.set_trace()
    pass

if __name__ == '__main__':
     unittest.main()