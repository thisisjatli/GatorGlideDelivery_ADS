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

class avlTree(object):
    def __init__(self) -> None:
        self.root = None
        
    def insert(self, curr, node):   # return updated ETAs (highest priority to lowest)
        outputList = []
        if not curr:
            self.root = node
            curr = self.root
        
        elif node.priority > curr.priority:
            if curr.rightChild:
                outputList += self.insert(curr.rightChild, node)
            else:
                curr.rightChild = node
                node.parent = curr
            
            # balance tree
            curr.updateHeight()
            self.balanceTree(curr)

            if node.createTime >= curr.eta - curr.deliveryTime:     # this order is out for delivery even with a lower priority
                outputList += self.appendUpdatedEta(curr.leftChild)
            else:
                outputList += [curr.id] + self.appendUpdatedEta(curr.leftChild)
            
        else:
            if curr.leftChild:
                outputList += self.insert(curr.leftChild, node)
            else:
                curr.leftChild = node
                node.parent = curr

            node.eta = max(node.eta, curr.eta+curr.deliveryTime+node.deliveryTime)
        
        curr.updateHeight()
        # balance tree
        self.balanceTree(curr)

        return outputList

    def delete(self, curr, key, id):
        outputList = []
        prevEndTime = 0
        if not curr:
            # fell off
            return 0, outputList
        
        elif curr.id == id:
            outputList += self.appendUpdatedEta(curr.leftChild)
            parent = curr.parent
            # found key
            # order of node is less than two, simple
            if not curr.leftChild:
                if curr.rightChild:
                    prevEndTime = max(prevEndTime, curr.rightChild.eta+curr.rightChild.deliveryTime)
                else:
                    prevEndTime = max(prevEndTime, curr.eta+curr.deliveryTime)
                # it either only has a right child or has none
                # curr = curr.rightChild
                if parent is None:
                    if curr.rightChild is None:
                        self.root = None
                    else:
                        self.root = curr.rightChild
                        curr.parent = None
                else:
                    if curr.rightChild is None:
                        if parent.leftChild == curr:
                            parent.leftChild = None
                        else:
                            parent.rightChild = None
                    else:
                        if parent.leftChild == curr:
                            parent.leftChild = curr.rightChild
                            curr.rightChild.parent = parent
                        else:
                            parent.rightChild = curr.rightChild
                            curr.rightChild.parent = parent
                curr = curr.rightChild

            elif not curr.rightChild:
                prevEndTime = max(prevEndTime, curr.eta+curr.deliveryTime)
                # it only has a left child
                parent = curr.parent
                if not parent:
                    self.root = curr.leftChild
                    curr.leftChild.parent = None
                else:
                    if parent.leftChild == curr:
                        parent.leftChild = curr.leftChild
                        curr.leftChild.parent = parent
                    else:
                        parent.rightChild = curr.leftChild
                        curr.leftChild.parent = parent
                curr = curr.leftChild

            # order of node is two (has both children)
            else:
                # find min in right subtree
                # swap and delete
                minNode = self.getMin(curr.rightChild)
                prevEndTime = max(prevEndTime, minNode.eta+minNode.deliveryTime)
                self.nodeSwap(curr, minNode)
                self.delete(curr, key, id)
        
        elif key > curr.priority:
            outputList += [curr.id] + self.appendUpdatedEta(curr.leftChild)
            results = self.delete(curr.rightChild, key, id)
            outputList += results[1]
            prevEndTime = max(prevEndTime, results[0])
        
        elif key <= curr.priority:
            minNode = curr if curr.rightChild is None else self.getMin(curr.rightChild)
            prevEndTime = max(prevEndTime, minNode.eta+minNode.deliveryTime)
            results = self.delete(curr.leftChild, key, id)
            outputList += results[1]
            prevEndTime = max(prevEndTime, results[0])
        
        if curr:
            # update height
            curr.updateHeight()

            # balance tree
            self.balanceTree(curr)
        
        return prevEndTime, outputList

    def rRotate(self, A, B):
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

    def lRotate(self, A, B):
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

    def rlRotate(self, A, B, C):
        self.lRotate(B, C)
        self.rRotate(A, C)

    def lrRotate(self, A, B, C):
        self.rRotate(B, C)
        self.lRotate(A, C)
    
    def balanceTree(self, curr):
        if not curr:
            return
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

    def findOrdersTimeInterval(self, curr, time1, time2):
        odrs = []
        if curr.eta < time1:
            if curr.leftChild:
                return self.findOrdersTimeInterval(curr.leftChild, time1, time2)
            else:
                return []
        if curr.eta > time2:
            if curr.rightChild:
                return self.findOrdersTimeInterval(curr.rightChild, time1, time2)
            else:
                return []
        
        if curr.rightChild:
            odrs += self.findOrdersTimeInterval(curr.rightChild, time1, time2)
        odrs += [curr.id]
        if curr.leftChild:
            odrs += self.findOrdersTimeInterval(curr.leftChild, time1, time2)

        return odrs
    
    def countSubtreeNum(self, curr):
        if curr is None:
            return 0
        return 1 + self.countSubtreeNum(curr.leftChild) + self.countSubtreeNum(curr.rightChild)
    
    def findOrderRank(self, curr, theETA):        
        if theETA > curr.eta:
            if curr.leftChild:
                return self.findOrderRank(curr.leftChild, theETA) + self.countSubtreeNum(curr.rightChild) + 1
            else:
                return self.countSubtreeNum(curr.rightChild) + 1
        
        elif theETA < curr.eta:
            if curr.rightChild:
                return self.findOrderRank(curr.rightChild, theETA)
            else:
                return 0
        
        else:
            return self.countSubtreeNum(curr.rightChild)
        
    def appendDelivered(self, curr):
        if curr is None:
            return []
        outputList = []
        outputList += self.appendDelivered(curr.rightChild)
        outputList += [(curr.id, curr.eta)]
        outputList += self.appendDelivered(curr.leftChild)

        return outputList
    
    def findDelivered(self, curr, nowTime, outForDelivery=None):
        if not curr:
            return nowTime, []
        
        outputList = []
        if curr.eta < nowTime:
            insertTime = max(curr.eta + curr.deliveryTime, nowTime)
            outputList += self.appendDelivered(curr.rightChild)
            outputList += [(curr.id, curr.eta)]
            results = self.findDelivered(curr.leftChild, nowTime, outForDelivery)
            outputList += results[1]
            insertTime = max(insertTime, results[0])

        else:
            insertTime = nowTime
            if nowTime >= curr.eta - curr.deliveryTime:
                insertTime = max(curr.eta + curr.deliveryTime, insertTime)
                nodeCopy = treeNode(curr.id, curr.createTime, curr.value, curr.deliveryTime, curr.eta, curr.priority)
                outForDelivery.append(nodeCopy)
            
            results = self.findDelivered(curr.rightChild, nowTime, outForDelivery)
            outputList += results[1]
            insertTime = max(insertTime, results[0])
        
        return insertTime, outputList
    
    def updateOrderTime(self, curr, id, prio):
        if not curr:
            return []
        
        outputList = []
        if curr.id == id:
            outputList += self.appendUpdatedEta(curr.leftChild)

        elif prio > curr.priority:
            outputList += self.updateOrderTime(curr.rightChild, prio, id) + [curr.id] + self.appendUpdatedEta(curr.leftChild)

        else:
            outputList += self.updateOrderTime(curr.leftChild, prio, id)

        return outputList
    
    def appendUpdatedEta(self, curr):
        if not curr:
            return []
        
        outputList = []
        outputList += self.appendUpdatedEta(curr.rightChild)
        outputList += [curr.id]
        outputList += self.appendUpdatedEta(curr.leftChild)

        return outputList
    
    def outputRemaining(self, curr):
        if curr is None:
            return []
        
        return self.outputRemaining(curr.rightChild) + [(curr.id, curr.eta)] + self.outputRemaining(curr.leftChild)
            
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
        # while not node.leftChild:
        while node.leftChild:
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

    def inorderTraverse(self, curr):
        if not curr:
            return
        if curr.leftChild:
            self.inorderTraverse(curr.leftChild)
        print(curr.id, curr.eta, curr.priority)
        if curr.rightChild:
            self.inorderTraverse(curr.rightChild)
