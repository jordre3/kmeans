import sys
import random
import math
import pandas as pd


def loadData(file):
    #trainFile = open("smallTest.csv", 'r')
    trainFile = open(file, 'r')
    dataLine = trainFile.readline()

    trainData = []
    labels = []
    dataLine = trainFile.readline()
    i = 0
    while dataLine is not "":
        dataLine = dataLine.strip('\n').split(',')
        for i in range(len(dataLine) - 1):
            dataLine[i] = float(dataLine[i])
        if dataLine[len(dataLine) - 1] not in labels:
            labels.append(dataLine[len(dataLine) - 1])
        trainData.append(dataLine)
        dataLine = trainFile.readline()
        i += 1

    numLabels = len(labels)
    return (trainData, labels)

#call would be wss(k, kCentroids, currentClusters)
def wss(k, centroid, cluster, trainData):
    wss = 0
    # sum of (point value minus its cluster center)^2
    for num in range(k):
        for item in cluster[num]:
            add = 0
            for d in range(len(trainData[0]) - 1):
                add += abs(centroid[num][0][d] - trainData[item][d])
            wss += (add**2)
    return wss

#call would be bss(k, kCentroids, currentClusters)
def bss(k,centroids, cluster, trainData):
    dimensions = len(trainData[0]) - 1
    averageList = []
    for d in range(dimensions):
        sum = 0
        for i in range(len(trainData)):
            sum += trainData[i][d]
        average = sum / (len(trainData))
        averageList.append(average)
    total = 0
    for num in range(k):
        bss = 0
        for d in range(dimensions):
            bss += abs(averageList[d] - centroids[num][0][d])
        numInCluster = len(cluster[num])
        finalB = numInCluster * (bss ** 2)
        total += finalB
    return total


def infoGain(currentClusters, trainData, labels):
    parentEntropy = 0.00
    lCount = []
    for x in range(len(labels)):
        lCount.append(0)
    for point in trainData:
        index = labels.index(point[len(point) - 1])
        lCount[index] += 1
    for j in range(len(lCount)):
        if lCount[j] != 0:
            parentEntropy += (-lCount[j] / len(trainData) * math.log((lCount[j] / len(trainData)), 2))
    infoGain = parentEntropy
    for num in range(len(currentClusters)):
        lCount = []
        for x in range(len(labels)):
            lCount.append(0)
        for i in currentClusters[num]:
            # print(num, i)
            # print(trainData[i])
            # print(trainData[i][len(trainData[0]) - 1])
            index = labels.index(trainData[i][len(trainData[0]) - 1])
            lCount[index] = lCount[index] + 1
        # fPIC means points in cluster
        fPIC = len(currentClusters[num])
        fAllPoints = len(trainData)
        entropy = 0.0
        for j in range(len(lCount)):
            if lCount[j] != 0:
                entropy += (-lCount[j] / fPIC * math.log((lCount[j] / fPIC), 2))

        infoGain -= entropy * (fPIC / fAllPoints)
    return infoGain

def kmeans(k, distMeasure, trainData, labels):
    numLabels = len(labels)
    previousClusters = []
    currentClusters = []
    currentClusters.append('x')
    kCentroids = []
    numIterations = 0
    
    ##################################

    #################################
    
    centroids = random.sample(trainData, k)
    for ind in centroids:
        kCentroids.append([ind, []])
    while previousClusters != currentClusters and numIterations < 100:
        for point in range(len(trainData)):
            minDist = sys.float_info.max
            minIndex = numLabels * 4
            for c in range(len(kCentroids)):
                dist = 0
                for i in range(len(trainData[point]) - 1):
                    if(distMeasure == 'Manhattan'):
                        dist += abs(float(trainData[point][i]) - float(kCentroids[c][0][i]))
                    else:
                        dist += (float(trainData[point][i]) - float(kCentroids[c][0][i]))**2
                if dist < minDist:
                    minDist = dist
                    minIndex = c
            kCentroids[minIndex][1].append(point)
        previousClusters = currentClusters
        currentClusters = []
        for num in range(k):
            currentClusters.append(kCentroids[num][1])
        kCentroids.clear()
        for cluster in currentClusters:
            newCentroid = []
            for i in range(len(trainData[0]) - 1):
                sum = 0
                for point in cluster:
                    sum += float(trainData[int(point)][i])
                if(len(cluster) == 0):
                    avg = 0
                else:
                    avg = sum / len(cluster)
                newCentroid.append(avg)
            kCentroids.append([newCentroid, []])
        numIterations += 1

    
    print("----" + distMeasure + " clusters for: k=" + str(k) + " ----")
    for num in range(k):
        print("centroid of cluster " + str(num + 1) + ":")
        print(kCentroids[num][0])
        print("points in cluster " + str(num + 1) + ":")
        print(currentClusters[num])
    print("The WSS measure is : " + str(wss(k, kCentroids, currentClusters, trainData)))
    print("The BSS measure is : " + str(bss(k, kCentroids, currentClusters, trainData)))
    print("The infoGain measure is : " + str(infoGain(currentClusters, trainData, labels)))
    print("Algorithm converged after " + str(numIterations) + " iterations")
    return ((wss(k, kCentroids, currentClusters, trainData)), (bss(k, kCentroids, currentClusters, trainData)), (infoGain(currentClusters, trainData, labels)))

def visualize(file):
    trainData, labels = loadData(file)
    numL = len(labels)
    m1 = kmeans(numL, "Manhattan", trainData, labels)
    e1 = kmeans(numL, "Euclidean", trainData, labels)
    m2 = kmeans(numL*2, "Manhattan", trainData, labels)
    e2 = kmeans(numL*2, "Euclidean", trainData, labels)
    m3 = kmeans(numL*3, "Manhattan", trainData, labels)
    e3 = kmeans(numL*3, "Euclidean", trainData, labels)
    data = {"k-Value": [numL, numL, numL*2, numL*2, numL*3, numL *3],
            "Distance Measure": ["Manhattan", "Euclidean", "Manhattan",
                                 "Euclidean", "Manhattan", "Euclidean"],
            "WSS": [m1[0], e1[0], m2[0], e2[0], m3[0], e3[0]],
            "BSS": [m1[1], e1[1], m2[1], e2[1], m3[1], e3[1]],
            "Info Gain": [m1[2], e1[2], m2[2], e2[2], m3[2], e3[2]]}
    #wss, bss, infoGain
    return pd.DataFrame(data)



print(visualize("smallTest.csv"))
"""
wTotal = 0.0
bTotal = 0.0
infoTotal = 0.0
for i in range(0, 10):
        w, b, infoG = kmeans(numLabels, "Manhattan")
        wTotal = wTotal + w
        bTotal = bTotal + b
        infoTotal = infoTotal + infoG
averageW = wTotal / 10.0
averageB = bTotal / 10.0
averageIG = infoTotal / 10.0
print("\naverage WSS for 10 runs: " + str(averageW) + "\n" + "average BSS for 10 runs: " + str(averageB) + "\n" + "average info gain for 10 runs: " + str(averageIG) + "\n")
"""
