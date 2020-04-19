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
    print("Algorithm converged after " + str(numIterations) + " iterations")


kmeans(numLabels, "Euclidean")
kmeans(numLabels, "Manhattan")
#kmeans(numLabels*3, "Euclidean")
