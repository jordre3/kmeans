import sys
import math


trainFile = open("SigGene.csv", 'r')

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

#print(trainData)
#print(labels)

numLabels = len(labels)

"""
onexkCentroids = []
for k in range(numLabels):
    onexkCentroids.append([trainData[k], []])
twoxkCentroids = []
for k in range(numLabels * 2):
    twoxkCentroids.append([trainData[k], []])
threexkCentroids = []
for k in range(numLabels * 3):
    threexkCentroids.append([trainData[k], []])
"""

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
                    minIndexM = c
            kCentroids[minIndexM][1].append(point)
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
    print("----manhattan clusters for: k=" + str(k) + " ----")
    for num in range(k):
        print("centroid of cluster " + str(num + 1) + ":")
        print(kCentroids[num][0])
        print("points in cluster " + str(num + 1) + ":")
        print(currentClusters[num])
    print("Algorithm converged after " + str(numIterations) + " iterations")

# def kmeansM(k):
#     previousClustersE = []
#     kCentroidsE = []
#     for ind in range(k):
#         kCentroidsE.append([trainData[ind], []])
#     for point in range(len(trainData)):
#         minDistE = sys.float_info.max
#         minIndexE = numLabels * 4
#         for c in range(len(kCentroidsE)):
#             eucDistSq = 0
#             for i in range(len(trainData[point]) - 1):
#                 eucDistSq += (float(trainData[point][i]) - float(kCentroidsE[c][0][i]))**2
#                 i += 1
#             if math.sqrt(eucDistSq) < minDistE:
#                 minDistE = math.sqrt(eucDistSq)
#                 minIndexE = c
#         kCentroidsE[minIndexE][1].append(point)
#     print("----euclidean clusters for: k=" + str(k) + " ----")
#     for num in range(k):
#         print(kCentroidsE[num][1])

kmeans(numLabels, "Euclidean")
kmeans(numLabels, "Manhattan")
#kmeans(numLabels*3)
