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
        if obj != None:
            self.obj_list.add(obj)
    
    def add(self, obj):
        self.obj_list.append(obj)

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
        return ret

class PyTST(object):
    """docstring for PyTST"""
    def __init__(self):
        '''
        init PyTST
        '''
        self.root = None
        self.num_nodes = 0

    def insert(self, key, obj):
        '''
        '''
        if len(key) == 0:
            return 0
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

        return self.__search(self.root, key)

    def prefix_search(self, prefix):
        '''
        @return an iterator of the matched nodes
        '''
        sub_root = self.__search(self.root, prefix)
        if sub_root == None:
            yield None
        else:
            if len(sub_root.obj_list) > 0:
                yield sub_root
            for node in self.__traverse(sub_root.mid):
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
        else:
            for node in self.__wildcard_search(self.root, key):
                if node != None:
                    yield node.obj_list

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
                    return 0
                else:
                    return self.__insert(root.mid, key[1:], obj)
                # return self.__insert(root.mid, key[1:], obj)

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
        print(root)
        print(key)
        if len(key) == 1:
            if key == root.splitchar:
                yield root
            else:
                yield None
        else:
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
                    for node in self.__wildcard_search(root.mid, key[1:]):
                        yield node
                elif key[0] == root.splitchar:
                    for node in self.__wildcard_search(root.mid, key[1:]):
                        yield node
                else:
                    yield None
            else:
                if len(key) == 1 and key[0] == '*':
                    yield root
                else:
                    yield None
            

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


def small_data_test():
    tst = PyTST()
    # build tree
    print('==== build tree ====')
    tst.insert('a', 1)
    tst.insert('ab', 2)
    tst.insert('abab', 3)
    tst.insert('cab', 4)
    tst.insert('ca', 5)
    tst.insert('aa', 6)


    # search
    print('==== search ====')
    print('aa: [6]')
    print tst.search('aa')
    print('ac: None')
    print tst.search('ac')

    # traverse
    print('==== traverse ====')
    for node in tst.traverse():
        print node
    
    # prefix search
    print('==== prefix search ====')
    print('ab: [2][3]')
    for node in tst.prefix_search('ab'):
        print node

    # wildcard search
    print('==== wildcard search ====')
    print('*a: [1][5][6]')
    # import pdb; pdb.set_trace()
    for node in tst.wildcard_search('*a'):
        print node
    # print('a*: [2][3][1]')
    # for obj_list in tst.wildcard_search('a*'):
    #     print obj_list
    # print ('*bd*: [3][4]')
    # for obj_list in tst.wildcard_search('*bd*'):
    #     print obj_list

def main():
    # import pdb; pdb.set_trace()
    small_data_test()

    

if __name__ == '__main__':
    main()