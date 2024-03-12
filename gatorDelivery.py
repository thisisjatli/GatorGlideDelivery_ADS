def printByOrder(orderId):
    return

def printByTime(time1, time2):
    return

def getRankOfOrder(orderId):
    return

def createOrder(orderId, currentSystemTime, orderValue, deliveryTime):
    return

def cancelOrder(orderId, currentSystemTime):
    return

def updateTime(orderId, currentSystemTime, newDeliveryTime):
    return

def processCommand(cmd):
    cmd = cmd.split('(')
    cmdType = cmd[0]
    args = cmd[1][:-1].split(", ")
    
    if cmdType == "print" and len(args) == 1:
        orderId = int(args[0])
        printByOrder(orderId)
    
    elif cmdType == "print" and len(args) == 2:
        time1 = int(args[0])
        time2 = int(args[1])
        printByTime(time1, time2)
    
    elif cmdType == "getRankOfOrder" and len(args) == 1:
        orderId = int(args[0])
        getRankOfOrder(orderId)
    
    elif cmdType == "createOrder" and len(args) == 4:
        orderId = int(args[0])
        currentSystemTime = int(args[1])
        orderValue = int(args[2])
        deliveryTime = int(args[3])
        createOrder(orderId, currentSystemTime, orderValue, deliveryTime)
    
    elif cmdType == "cancelOrder" and len(args) == 2:
        orderId = int(args[0])
        currentSystemTime = int(args[1])
        cancelOrder(orderId, currentSystemTime)
    
    elif cmdType == "updateTime" and len(args) == 3:
        orderId = int(args[0])
        currentSystemTime = int(args[1])
        newDeliveryTime = int(args[2])
        updateTime(orderId, currentSystemTime, newDeliveryTime)

    else:
        print("Please enter a valid command.")
        return

if __name__ == "__main__":
    # inputfile, readlines
    
    cmd = input()
    while cmd != "Quit()":
        processCommand(cmd)
        cmd = input()

    exit()