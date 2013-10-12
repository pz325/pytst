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
        return an iterator of obj_list
        '''
        if self.root == None:
            yield []
        else:
            for obj_list in self.__traverse(self.root):
                yield obj_list
    
    def search(self, key):
        '''
        return the obj_list
        '''
        if len(key) == 0:
            return None

        node = self.root
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
                    return node.obj_list
                else:
                    logger.debug('search mid')
                    node = node.mid
                    key = key[1:]
        return None

    def prefix_search(self, prefix):
        '''
        return an iterator
        '''
        pass
    def wildcard_search(self, key):
        '''
        return an iterator
        '''
        pass
    def near_search(self, key):
        '''
        return an iterator
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
        if root.left != None:
            for obj_list in self.__traverse(root.left):
                yield obj_list
        if root.right != None:
            for obj_list in self.__traverse(root.right):
                yield obj_list
        if root.mid != None:
            for obj_list in self.__traverse(root.mid):
                yield obj_list
        if len(root.obj_list) > 0:
            yield root.obj_list

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
    print(tst.search('TV'))
    print(tst.search("z's"))
    print(tst.search('abase'))
    print(tst.search('bellman'))


def small_data_test():
    tst = PyTST()
    # build tree
    tst.insert('abcd', 1)
    tst.insert('aa', 2)
    tst.insert('abdd', 3)

    # search
    obj_list = tst.search('aa')
    print('aa: {0}'.format(obj_list))

    # traverse
    for obj_list in tst.traverse():
        print obj_list
    

def main():
    # import pdb; pdb.set_trace()
    small_data_test()

    

if __name__ == '__main__':
    main()