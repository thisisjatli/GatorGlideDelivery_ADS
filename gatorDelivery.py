from avlTree import treeNode, avlTree

myTree = avlTree()
nodes = {}                  # {orderId: node}
outForDelivery = []

def getPriority(orderValue, createTime, valueWeight=0.3, timeWeight=0.7):
    return valueWeight*orderValue/50-timeWeight*createTime

''' print(orderId) '''
def printByOrder(orderId):
    orderString = f"{orderId}"
    orderString += f", {nodes[orderId].createTime}"
    orderString += f", {nodes[orderId].value}"
    orderString += f", {nodes[orderId].deliveryTime}"
    orderString += f", {nodes[orderId].eta}"
    return "["+orderString+"]\n"

''' print(time1, time2) '''
def printByTime(time1, time2):
    
    allOrders = myTree.findOrdersTimeInterval(myTree.root, time1, time2)
    if len(allOrders) == 0 and len(outForDelivery) == 0:
        return "There are no orders in that time period\n"
    
    outputString = ""
    if len(outForDelivery) > 0 and outForDelivery[0].eta >= time1 and outForDelivery[0].eta <= time2:
        outputString += f"{outForDelivery[0].id}, "
    for order in allOrders:
        outputString += f"{order}, "
    
    if len(outputString) > 0:
        return "["+outputString[:-2]+"]\n"

    return "There are no orders in that time period\n"

''' getRankOfOrder(orderId) '''
def getRankOfOrder(orderId):
    num = myTree.findOrderRank(myTree.root, orderId)
    if orderId not in nodes:
        return ""
    
    theETA = nodes[orderId].eta
    num = myTree.findOrderRank(myTree.root, theETA) + len(outForDelivery)
    
    return f"Order {orderId} will be delivered after {num} orders.\n"

''' createOrder(orderId, currentSystemTime, orderValue, deliveryTime) '''
def createOrder(orderId, currentSystemTime, orderValue, deliveryTime):
    global outForDelivery
    # test - check delivered
    deliveredString = ""
    insertTimetmp = 0
    if len(outForDelivery) > 0 and outForDelivery[0].eta <= currentSystemTime:
        insertTimetmp = outForDelivery[0].eta + outForDelivery[0].deliveryTime
        deliveredString += f"Order {outForDelivery[0].id} has been delivered at time {outForDelivery[0].eta}\n"
        del nodes[outForDelivery[0].id]              # remove from dict
        outForDelivery.clear()

    insertTime, deliveredTest = myTree.findDelivered(myTree.root, currentSystemTime, outForDelivery)
    insertTime = max(insertTime, insertTimetmp)
    
    for id, eta in deliveredTest:
        deliveredString += f"Order {id} has been delivered at time {eta}\n"
        removeKey = nodes[id].priority
        myTree.delete(myTree.root, removeKey, id)   # remove from tree
        nodes[id] = outForDelivery # destroy node

    if len(outForDelivery) > 0:
        removeKey = outForDelivery[0].priority
        myTree.delete(myTree.root, removeKey, outForDelivery[0].id)   # remove from tree
        nodes[outForDelivery[0].id] = outForDelivery[0]          # destroy node

    orderETA = insertTime + deliveryTime
    # orderETA = currentSystemTime + deliveryTime
    priority = getPriority(orderValue, currentSystemTime)
    newOrderNode = treeNode(orderId, currentSystemTime, orderValue, deliveryTime, orderETA, priority)
    updatedTest = myTree.insert(myTree.root, newOrderNode)
    nodes[orderId] = newOrderNode

    updatedTuple = []
    prevEndTime = newOrderNode.eta + newOrderNode.deliveryTime
    for id in updatedTest:
        currStartTime = nodes[id].eta - nodes[id].deliveryTime
        if currStartTime < prevEndTime:
            offset = abs(prevEndTime-currStartTime)
            nodes[id].eta += offset
            updatedTuple.append((id, nodes[id].eta))
        prevEndTime = nodes[id].eta+nodes[id].deliveryTime

    updatedString = ""
    if len(updatedTuple) > 0:
        updatedString = "Updated ETAs: ["
        for id, eta in updatedTuple:
            updatedString += f"{id}: {eta}, "
        updatedString = updatedString[:-2] + "]\n"
    return f"Order {orderId} has been created - ETA: {nodes[orderId].eta}\n" + updatedString + deliveredString

''' cancelOrder(orderId, currentSystemTime) '''
def cancelOrder(orderId, currentSystemTime):
    global outForDelivery
    deliveredString = ""
    if len(outForDelivery) > 0 and outForDelivery[0].eta <= currentSystemTime:
        deliveredString += f"Order {outForDelivery[0].id} has been delivered at time {outForDelivery[0].eta}\n"
        del nodes[outForDelivery[0].id]              # remove from dict
        outForDelivery.clear()

    _, deliveredTest = myTree.findDelivered(myTree.root, currentSystemTime, outForDelivery)

    for id, eta in deliveredTest:
        deliveredString += f"Order {id} has been delivered at time {eta}\n"
        removeKey = nodes[id].priority
        myTree.delete(myTree.root, removeKey, id)   # remove from tree
        nodes[id] = None           # destroy node
        del nodes[id]              # remove from dict

    if len(outForDelivery) > 0:
        removeKey = outForDelivery[0].priority
        myTree.delete(myTree.root, removeKey, outForDelivery[0].id)   # remove from tree
        nodes[outForDelivery[0].id] = outForDelivery[0]          # destroy node

    if orderId not in nodes or currentSystemTime >= nodes[orderId].eta - nodes[orderId].deliveryTime:
        return f"Cannot cancel. Order {orderId} has already been delivered.\n" + deliveredString
    
    keyPrio = nodes[orderId].priority
    prevEndTime = nodes[orderId].eta - nodes[orderId].deliveryTime
    newPrevEndTime, deleteTest = myTree.delete(myTree.root, keyPrio, orderId)
    nodes[orderId] = None
    del nodes[orderId]

    updatedTuple = []
    prevEndTime = min(prevEndTime, newPrevEndTime)
    for id in deleteTest:
        currStartTime = nodes[id].eta - nodes[id].deliveryTime
        if currStartTime > prevEndTime:
            offset = abs(currStartTime-prevEndTime)
            nodes[id].eta -= offset
            updatedTuple.append((id, nodes[id].eta))
        prevEndTime =nodes[id].eta + nodes[id].deliveryTime

    updateString = "" if len(updatedTuple) == 0 else "Updated ETAs: ["
    for id, eta in updatedTuple:
        updateString += f"{id}: {eta}, "
    updateString = updateString[:-2] + "]\n" if len(updatedTuple) > 0 else ""

    return f"Order {orderId} has been canceled\n" + updateString + deliveredString
    

''' updateTime(orderId, currentSystemTime, newDeliveryTime) '''
def updateTime(orderId, currentSystemTime, newDeliveryTime):
    global outForDelivery
    deliveredString = ""
    if len(outForDelivery) > 0 and outForDelivery[0].eta <= currentSystemTime:
        deliveredString += f"Order {outForDelivery[0].id} has been delivered at time {outForDelivery[0].eta}\n"
        del nodes[outForDelivery[0].id]              # remove from dict
        outForDelivery.clear()

    _, deliveredTest = myTree.findDelivered(myTree.root, currentSystemTime, outForDelivery)

    for id, eta in deliveredTest:
        deliveredString += f"Order {id} has been delivered at time {eta}\n"
        removeKey = nodes[id].priority
        myTree.delete(myTree.root, removeKey, id)   # remove from tree
        nodes[id] = None           # destroy node
        del nodes[id]              # remove from dict

    if len(outForDelivery) > 0:
        removeKey = outForDelivery[0].priority
        myTree.delete(myTree.root, removeKey, outForDelivery[0].id)   # remove from tree
        nodes[outForDelivery[0].id] = outForDelivery[0]          # destroy node

    if orderId not in nodes or currentSystemTime >= nodes[orderId].eta - nodes[orderId].deliveryTime:
        return f"Cannot update. Order {orderId} has already been delivered.\n" + deliveredString
    
    updateTest = myTree.updateOrderTime(myTree.root, orderId, nodes[orderId].priority)

    offset = newDeliveryTime-nodes[orderId].deliveryTime
    nodes[orderId].eta = nodes[orderId].eta + offset
    nodes[orderId].deliveryTime = newDeliveryTime
    updateTuple = [(orderId, nodes[orderId].eta)]

    prevEndTime = nodes[orderId].eta + newDeliveryTime
    for id in updateTest:
        currStartTime = nodes[id].eta - nodes[id].deliveryTime
        offset = prevEndTime - currStartTime
        nodes[id].eta += offset    # update nodes
        updateTuple.append((id, nodes[id].eta))
        prevEndTime = nodes[id].eta + nodes[id].deliveryTime

    updateString = "Updated ETAs: ["
    for id, eta in updateTuple:
        updateString += f"{id}: {eta}, "
    updateString = updateString[:-2] + "]\n"

    return updateString + deliveredString


''' Output the remaining orders when Quit() '''
def outputRemaining():
    remainList = myTree.outputRemaining(myTree.root)

    outputStr = ""
    if len(outForDelivery) > 0:
        outputStr += f"Order {outForDelivery[0].id} has been delivered at time {outForDelivery[0].eta}\n"
    for id, eta in remainList:
        outputStr += f"Order {id} has been delivered at time {eta}\n"

    return outputStr

def processCommand(cmd):
    cmd = cmd.strip().split('(')
    cmdType = cmd[0]
    argStr = cmd[1][:-1]
    args = argStr.split(",")
    args = [arg.strip() for arg in args]
    
    if cmdType == "print" and len(args) == 1:
        orderId = int(args[0])
        return printByOrder(orderId)
    
    elif cmdType == "print" and len(args) == 2:
        time1, time2 = map(int, args)
        return printByTime(time1, time2)
    
    elif cmdType == "getRankOfOrder" and len(args) == 1:
        orderId = int(args[0])
        return getRankOfOrder(orderId)
    
    elif cmdType == "createOrder" and len(args) == 4:
        orderId, currentSystemTime, orderValue, deliveryTime = map(int, args)
        return createOrder(orderId, currentSystemTime, orderValue, deliveryTime)
    
    elif cmdType == "cancelOrder" and len(args) == 2:
        orderId, currentSystemTime = map(int, args)
        return cancelOrder(orderId, currentSystemTime)
    
    elif cmdType == "updateTime" and len(args) == 3:
        orderId, currentSystemTime, newDeliveryTime = map(int, args)
        return updateTime(orderId, currentSystemTime, newDeliveryTime)

    else:
        print("Please enter a valid command.")
        return ""

if __name__ == "__main__":
    import sys

    inputFile = sys.argv[1]
    fileName = inputFile[:-4]

    outputStr = ""

    with open(inputFile, 'r') as f:
        cmd = f.readline()
        while not cmd.startswith("Quit()"):
            outputStr += processCommand(cmd[:-1])
            cmd = f.readline()

    if cmd.startswith("Quit()"):
        # print out all remaining orders
        outputStr += outputRemaining()

    with open(f"{fileName}_output_file.txt", 'w') as f:
        f.writelines(outputStr)
