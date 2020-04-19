import sys


trainFile = open("smallTest.csv", 'r')

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

#call would be wss(k, kCentroids, currentClusters)
def wss(k, centroid, cluster):
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
def bss(k,centroids, cluster):
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

def kmeans(k, distMeasure):
    previousClusters = []
    currentClusters = []
    currentClusters.append('x')
    kCentroids = []
    numIterations = 0
    for ind in range(k):
        kCentroids.append([trainData[ind], []])
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
    print("The WSS measure is : " + str(wss(k, kCentroids, currentClusters)))
    print("The BSS measure is : " + str(bss(k, kCentroids, currentClusters)))
    print("Algorithm converged after " + str(numIterations) + " iterations")


#kmeans(numLabels, "Euclidean")
kmeans(numLabels, "Manhattan")
#kmeans(numLabels*3, "Euclidean")
