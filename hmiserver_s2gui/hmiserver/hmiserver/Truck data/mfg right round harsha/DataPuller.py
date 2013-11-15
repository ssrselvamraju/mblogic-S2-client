import time
import sys
import os
import math
from operator import itemgetter
import numpy as np


def buildData1(full_data):
	for ln in full_data:
		if ln[4] > 0:
			break
	built_data = [[full_data[full_data.index(ln)-1][4], full_data[full_data.index(ln)-1][5]]]
	max_enc = max(map(itemgetter(4),full_data))
	#print max_enc
	for ln in full_data[full_data.index(ln):]:
		if abs(ln[4]) <= max_enc:
			built_data.append([abs(ln[4]), ln[5]])
		if abs(ln[4]) == max_enc:
			return built_data

def buildData2(full_data):
	for ln in full_data:
		if ln[0] > 0:
			break
	built_data = [[full_data[full_data.index(ln)-1][0], full_data[full_data.index(ln)-1][1]]]
	max_enc = max(map(itemgetter(0),full_data))
	#print max_enc
	for ln in full_data[full_data.index(ln):]:
		if abs(ln[0]) <= max_enc:
			built_data.append([abs(ln[0]), ln[1]])
		if abs(ln[0]) == max_enc:
			return built_data


def sliceData2(followed_data, commanded_data):
	commanded_sliced = []
	follow_sliced = []
	for follow_sub in followed_data:
		for command_sub in commanded_data:
			if command_sub[0] == follow_sub[0]:
				commanded_sliced.append(command_sub)
				follow_sliced.append(follow_sub)
				break
	return commanded_sliced, follow_sliced





file = open("truckData_replay1.dat","r")
file.readline()
file.readline()

data = [map(float, line.split()) for line in file]
data_end = len(data)-1

file.close()

data_followed_by_truck = buildData1(data)

#print data_to_follow

file2 = open("truckReplayStatsExtr.dat","r")

data2 = [map(float, line.split()) for line in file2]

file2.close()

data_commanded = buildData2(data2)

data_commanded_sliced, data_followed_by_truck_sliced = sliceData2(data_followed_by_truck, data_commanded)

file3 = open("routeStats.dat","w")

max_len = len(data_commanded_sliced)

iter = 0
diff = []
while iter < max_len:
	file3.write(str(iter) + '\t'+ str(data_followed_by_truck_sliced[iter][0]) + '\t'+ str(data_commanded_sliced[iter][0]) +'\t'+ str(data_followed_by_truck_sliced[iter][1]) +'\t'+ str(data_commanded_sliced[iter][1]) + '\t' + str(data_commanded_sliced[iter][1]-data_followed_by_truck_sliced[iter][1]) +'\n')
	diff.append(abs(data_commanded_sliced[iter][1]- data_followed_by_truck_sliced[iter][1]))
	iter = iter+1
	

std_dev = np.std(diff)
average = np.average(diff)
min_diff = np.amin(diff)
max_diff = np.amax(diff)
range_diff = np.ptp(diff)


print "Standard Deviation: " + str(std_dev)
print "Average: " + str(average)
print "Min Difference: " + str(min_diff)
print "Max Difference: " + str(max_diff)
print "Range: " + str(range_diff)



#print data_commanded
