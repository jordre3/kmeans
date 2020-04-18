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

def kmeans(k):
    kCentroidsM = []
    kCentroidsE = []
    for ind in range(k):
        kCentroidsM.append([trainData[ind], []])
        kCentroidsE.append([trainData[ind], []])
    for point in range(len(trainData)):
        minDistM = sys.float_info.max
        minDistE = sys.float_info.max
        minIndexM = numLabels * 4
        minIndexE = numLabels * 4
        for c in range(len(kCentroidsM)):
            manDist = 0
            eucDistSq = 0
            for i in range(len(trainData[point]) - 1):
                manDist += abs(float(trainData[point][i]) - float(kCentroidsM[c][0][i]))
                eucDistSq += (float(trainData[point][i]) - float(kCentroidsM[c][0][i]))**2
                i += 1
            if manDist < minDistM:
                minDistM = manDist
                minIndexM = c
            if math.sqrt(eucDistSq) < minDistE:
                minDistE = math.sqrt(eucDistSq)
                minIndexE = c
        kCentroidsM[minIndexM][1].append(point)
        kCentroidsE[minIndexE][1].append(point)
    print("----manhattan clusters for: k=" + str(k) + " ----")
    for num in range(k):
        print(kCentroidsM[num][1])
    print("----euclidean clusters for: k=" + str(k) + " ----")
    for num in range(k):
        print(kCentroidsE[num][1])

kmeans(numLabels)
kmeans(numLabels*2)
#kmeans(numLabels*3)
