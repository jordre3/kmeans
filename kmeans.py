import sys


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

print(trainData)
print(labels)

numLabels = len(labels)

onexkCentroids = []
for k in range(numLabels):
    onexkCentroids.append([trainData[k], []])
twoxkCentroids = []
for k in range(numLabels * 2):
    twoxkCentroids.append([trainData[k], []])
threexkCentroids = []
for k in range(numLabels * 3):
    threexkCentroids.append([trainData[k], []])


for point in range(len(trainData)):
    minDist = sys.float_info.max
    minIndex = numLabels * 4
    for c in range(len(onexkCentroids)):
        manDist = 0
        for i in range(len(trainData[point]) - 1):
            manDist += abs(float(trainData[point][i]) - float(threexkCentroids[c][0][i]))
            i += 1
        if manDist < minDist:
            minDist = manDist
            minIndex = c
    onexkCentroids[minIndex][1].append(point)

print(onexkCentroids[0][1])
print(onexkCentroids[1][1])