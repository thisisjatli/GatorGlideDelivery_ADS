class treeNode(object):
    def __init__(self, orderId, currentSystemTime, orderValue, deliveryTime, ETA, priority) -> None:
        self.id = orderId
        self.createTime = currentSystemTime
        self.value = orderValue
        self.deliveryTime = deliveryTime
        self.eta = ETA
        self.priority = priority

        # for tree
        self.leftChild = None
        self.rightChild = None
        self.parent = None
        self.height = 1
    
    def updateHeight(self):
        leftHeight = 0 if not self.leftChild else self.leftChild.height
        rightheight = 0 if not self.rightChild else self.rightChild.height
        self.height = max(leftHeight, rightheight) + 1

    # @classmethod
    # def createOrder(cls, orderId, curSystemTime, orderVal, deliveryTime):
    #     eta = curSystemTime + deliveryTime
    #     return cls(orderId, orderVal, deliveryTime, eta)

class avlTree(object):
    def __init__(self) -> None:
        self.root = None
        # self.type = "priority"
        
    def insert(self, curr, node):
        if not curr:
            self.root = node
            curr = self.root
        elif node.priority > curr.priority:
            if node.rightChild:
                self.insert(curr.rightChild, node)
            else:
                curr.rightChild = node
                node.parent = curr
        else:
            if node.leftChild:
                self.insert(curr.leftChild, node)
            else:
                curr.leftChild = node
                node.parent = curr
        
        curr.updateHeight()

        # if self.getBf(curr) < -1:
        #     if self.getBf(curr.rightChild) == 1:
        #         self.rlRotate(curr, curr.rightChild, curr.rightChild.leftChild)
        #     else:
        #         self.rRotate(curr, curr.rightChild)

        # elif self.getBf(curr) > 1:
        #     if self.getBf(curr.leftChild) == -1:
        #         self.lrRotate(curr, curr.leftChild, curr.leftChild.rightChild)
        #     else:
        #         self.lRotate(curr, curr.leftChild)

        # balance tree
        self.balanceTree(curr)

    def delete(self, curr, key):
        if not curr:
            # fell off
            return
        elif key > curr.priority:
            self.delete(curr.rightChild, key)
        elif key < curr.priority:
            self.delete(curr.leftChild, key)
        else:
            # found key
            # order of node is less than two, simple
            if not curr.leftChild:
                # it either only has a right child or has none
                curr = curr.rightChild
            elif not curr.rightChild:
                # it only has a left child
                curr = curr.leftChild

            # order of node is two (has both children)
            else:
                # find min in right subtree
                # swap and delete
                minNode = self.getMin(curr.rightChild)
                self.swap(curr, minNode)
                self.delete(curr, key)
        
        if curr:
            # update height
            curr.updateHeight()

            # balance tree
            self.balanceTree(curr)

    def rRotate(self, A, B):
        parent = A.parent

        Br = B.rightChild
        B.rightChild = A
        A.parent = B
        A.leftChild = Br
        if Br:
            Br.parent = A
        B.parent = parent

        A.updateHeight()
        B.updateHeight()

        if not parent:
            self.root = B
        elif parent.leftChild == A:
            parent.leftChild = B
            parent.updateHeight()
        elif parent.rightChild == A:
            parent.rightChild = B
            parent.updateHeight()

    def lRotate(self, A, B):
        parent = A.parent

        Bl = B.leftChild
        B.leftChild = A
        A.parent = B
        A.rightChild = Bl
        if Bl:
            Bl.parent = A
        B.parent = parent

        A.updateHeight()
        B.updateHeight()

        if not parent:
            self.root = B
        elif parent.leftChild == A:
            parent.leftChild = B
            parent.updateHeight()
        elif parent.rightChild == A:
            parent.rightChild = B
            parent.updateHeight()

    def rlRotate(self, A, B, C):
        self.lRotate(B, C)
        self.rRotate(A, C)

    def lrRotate(self, A, B, C):
        self.rRotate(B, C)
        self.lRotate(A, C)
    
    def balanceTree(self, curr):
        if self.getBf(curr) < -1:
            if self.getBf(curr.rightChild) == 1:
                self.rlRotate(curr, curr.rightChild, curr.rightChild.leftChild)
            else:
                self.rRotate(curr, curr.rightChild)

        elif self.getBf(curr) > 1:
            if self.getBf(curr.leftChild) == -1:
                self.lrRotate(curr, curr.leftChild, curr.leftChild.rightChild)
            else:
                self.lRotate(curr, curr.leftChild)

    @staticmethod
    def getBf(node):
        if not node.leftChild and not node.rightChild:
            return 0
        elif not node.leftChild:
            return -node.rightChild.height
        elif not node.rightChild:
            return node.leftChild.height
        else:
            return node.leftChild.height - node.rightChild.height
        
    @staticmethod
    def getMin(node):
        while not node.leftChild:
            node = node.leftChild
        return node
    
    @staticmethod
    def nodeSwap(A, B):
        # id, createTime, value, deliveryTime, eta, priority
        tmp = [A.id, A.createTime, A.value, A.deliveryTime, A.eta, A.priority]

        A.id = B.id
        A.createTime = B.createTime
        A.value = B.value
        A.deliveryTime = B.deliveryTime
        A.eta = B.eta
        A.priority = B.priority

        B.id = tmp[0]
        B.createTime = tmp[1]
        B.value = tmp[2]
        B.deliveryTime = tmp[3]
        B.eta = tmp[4]
        B.priority = tmp[5]
