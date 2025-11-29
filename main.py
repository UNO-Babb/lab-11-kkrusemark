#GroceryStoreSim.py
#Name: Kylie Krusemark
#Date: 11/29/25
#Assignment: Lab 11

import simpy
import random
eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(2, 20)
    shoppingTime = items * 1.25 # shopping takes 1.25 minutes (1 min and 15s) per item.
    yield env.timeout(shoppingTime)
    # join the queue of waiting shoppers
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1) # wait a minute and check again

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(1) #New shopper every two minutes

def processResults():
    totalWait = 0
    totalShoppers = 0
    totalItems = 0
    maxWait = 0 

    for e in eventLog:
        items = e[1]

        waitTime = e[4] - e[3] #depart time - done shopping time
        totalWait += waitTime
        totalItems += items
        totalShoppers += 1

        if waitTime > maxWait:
            maxWait = waitTime

    avgWait = totalWait / totalShoppers
    avgItems = totalItems / totalShoppers
    
    print("Total Shoppers:", totalShoppers)
    print("Total idle time: %d minutes" % idleTime)
    print("Average wait time: %.2f minutes." % avgWait)
    print("Max wait time: %.2f minutes" % maxWait)
    print("Average items bought: %.2f" % avgItems)


def main():
    numberCheckers = 3

    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180 )

    print("Shoppers still waiting at end:", len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()