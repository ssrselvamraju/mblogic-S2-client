##############################################################################
# Project: 	SeegridS2Client
# Module: 	replayData__.py
# Purpose: 	Playsback recorded data from the truck's modbus server to be able to drive the truck through this recorded path through calculated speeds.
# Language:	Python 2.5
# Date:		06-Nov-2013.
# Ver.:		06-Nov-2013.
# Copyright:	2013 - 2014 - S. Selvam Raju @SEEGRID corp.       <sraju@seegrid.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Important:	WHEN EDITING THIS FILE, USE TABS TO INDENT - NOT SPACES!
##############################################################################

# Name of this program.
_SOFTNAME = 'ModbusReplayRouteData'

# Version of this server.
_VERSION = '06-November-2013'

_HelpStr = """
%s, %s
This module takes the truck through a route recorded previously in the truckData.dat file by calculating speeds and following steering turns at corresponding encoder values. The calculated speeds and tiller angles are written to the modbus registers and the modbus server takes necessary action to run the truck.
Just like the standard clients this client has to be started with the command line parameters (which are supposed to be the same as those in the MBClient and this program should run on the same computer that runs the standard client.

Any parameters which are not specified will use their default values. 
These include:

-p Port number of HMI web server. The default is 8082.
-h Name or address of remote server. The default is localhost.
-r Port number of remote server. The default is 502.
-u Unit ID of remote server. The default is 1. (This is Modbus specific).
-t Timeout for communications. The default is 5.0 seconds.
-e hElp. (this screen).

This program is automatically setup to get the command line parameters sent to the standard MBClient and none of the above parameters need to be passed to this program seperately.
""" % (_SOFTNAME, _VERSION)

############################################################

import time
import sys
import os
import math
from operator import itemgetter

import ModbusClient
import HMIServerCommon
from mbprotocols import ModbusExtData


############################################################

# Get the command line parameter options.
#CmdOpts = HMIServerCommon.GetOptionsClient(502, _HelpStr)


############################################################

#Function Defenitions

def buildData(full_data):
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
	#return built_data
'''
def read_encoder(a):
	return a+10

def read_encoder1(a):
	return a
'''
############################################################




# Initialise the client. First get the remote host parameters.
#hbhost, hbport, hbtimeout, hbunitid = CmdOpts.GetRemoteParams()


#Initialize an instance of the ModbusClient.DataTableAccess to initialize this client.

#HBClient = ModbusClient.DataTableAccess(hbhost, hbport, hbtimeout, hbunitid)

#HBClient1 = ModbusClient.DataTableAccess('192.168.10.237', 1502, 5.0, 1)

replayDataClient1 = ModbusClient.DataTableAccess('10.0.0.100', 1502, 5.0, 1)

ExtData4 = ModbusExtData.ExtendedDataTypes(replayDataClient1)

############################################################


while True:


	replay_mode = replayDataClient1.GetCoilsBool(32) #1 for replay start, 0 when done

	while not replay_mode:
		replay_mode = replayDataClient1.GetCoilsBool(32)

	replayDataClient1.SetCoilsBool(40,0)
	
	replayDataClient1.SetCoilsBool(12,1)
	time.sleep(10)

	replayDataClient1.SetCoilsBool(14,1)

	
	file = open("truckData.dat","r")
	file2 = open("truckReplayStats.dat", "w")


	file.readline()
	file.readline()
	truck_const_speed = 500 #mm/s





	data = [map(float, line.split()) for line in file]
	data_end = len(data)-1

	file.close()

	data_to_follow = buildData(data)

	#print data_to_follow

	file2.write("Index\tEnc\tAng\n\n")



	ExtData4.SetHRegFloat32(44, data_to_follow[0][1]) #Truck's start angle at 0 speed

#	dummy = raw_input("Enter something and press Return to get the truck moving: ") #Wait until user input

	print "Moving truck"
	replayDataClient1.SetHoldingRegistersInt(10,truck_const_speed) #Set truck to move at a constant speed
	
	replayDataClient1.SetCoilsBool(8,1) #Setting deadman switch to 1 to make truck move


	index = 1

	#print "Here"
	#print data_to_follow[len(data_to_follow)-3][0]
	while abs(ExtData4.GetInpRegInt32(12)) < data_to_follow[len(data_to_follow)-1][0]:  #Getting current encoder and checking if lesser than (last but third) end point encoder value
		#print str(a) + " " + str(data_to_follow[index][0]) +" " + str(data_to_follow[index-1][0])
		while abs(ExtData4.GetInpRegInt32(12)) < data_to_follow[index][0] and abs(ExtData4.GetInpRegInt32(12)) >= data_to_follow[index-1][0]:
			truck_angle = data_to_follow[index-1][1]
			ExtData4.SetHRegFloat32(44,truck_angle)
			file2.write(str(index) + '\t' + str(ExtData4.GetInpRegInt32(12)) + '\t' + str(truck_angle) + '\n')
			#print "\n   Move in Progress...\n"
			print "Enc:\t" + str(ExtData4.GetInpRegInt32(12)) + "\tAng:\t" + str(truck_angle) + '\n'

			print "Home Coil:" + str(replayDataClient1.GetCoilsBool(12))
		index = index+1

	replayDataClient1.SetHoldingRegistersInt(10,0) #Set truck speed to 0 to stop truck
	replayDataClient1.SetCoilsBool(8,0) #Setting deadman switch to 0, this switches steering to analog

	print "\nRun successful. Truck at the trained endpoint.\n"
	
	file2.close()
	replayDataClient1.SetCoilsBool(32,0) #Pulling down the Replay mode swtich back to 0




####ALGO

#read all encoder values and clean them up and store in another register ######start with making only forward motion work, if reverse motion throw error during this step
#set angle at data[1]
#give cont speed to truck
#read truck encoders
#while truck encoder near end stop
#while truck encoder is > data[i] and  < data[i+1] truck encoder = enc@data[i]
#when this while breaks, i++ and back to while //Considering linear increments

