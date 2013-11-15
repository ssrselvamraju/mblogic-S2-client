##############################################################################
# Project: 	SeegridS2Client
# Module: 	recordData__.py
# Purpose: 	Record data from the truck's modbus server to be able to feed the playback program.
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
_SOFTNAME = 'ModbusRecordRouteData'

# Version of this server.
_VERSION = '06-November-2013'

_HelpStr = """
%s, %s
This module logs the valVF,	valVL, truckHeading, tractionEncoder, tillerAngle information which is calculated at the Server and stored in allocated InputRegisters. The data is logged into a .dat file which is in a format that can be used by the REPLAY program to generate a planned path for the robot to follow. Data in this format can also be used by GNUplot for visualizing any data.
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

import ModbusClient
import HMIServerCommon
from mbprotocols import ModbusExtData


############################################################

# Get the command line parameter options.
#CmdOpts = HMIServerCommon.GetOptionsClient(502, _HelpStr)


############################################################


# Initialise the client. First get the remote host parameters.
#hbhost, hbport, hbtimeout, hbunitid = CmdOpts.GetRemoteParams()


#Initialize an instance of the ModbusClient.DataTableAccess to initialize this client.

#HBClient = ModbusClient.DataTableAccess(hbhost, hbport, hbtimeout, hbunitid)
#HBClient1 = ModbusClient.DataTableAccess('192.168.10.237', 1502, 5.0, 1)


recDataClient1 = ModbusClient.DataTableAccess('10.0.0.100', 1502, 5.0, 1)

ExtData3 = ModbusExtData.ExtendedDataTypes(recDataClient1)

############################################################


#record_mode = int(raw_input("Enter 0 to record Train, and 1 to record Replay: "))

while True:

	#ExtData3.SetHRegStr16(100,30,"Press Start to Train Route")

	train_mode = recDataClient1.GetCoilsBool(31) #1 for train start, 0 for train stop

	

	while not train_mode:
		train_mode = recDataClient1.GetCoilsBool(31)

	#ExtData3.SetHRegStr16(100,30,"Training Route")


	recDataClient1.SetCoilsBool(40,1)
	
	file = open("truckData.dat", "w")

	file.write( "###Truck route record\n" )
	file.write( "###S.No.\tVF\tVL\tHeading\tEncoder-Raw\tTiller-Angle\n" )

	i = 0

	while train_mode:
		train_mode = recDataClient1.GetCoilsBool(31)
		i = i+1
		valVF = ExtData3.GetInpRegFloat32(20)
		valVL = ExtData3.GetInpRegFloat32(22)
		truckHeading = recDataClient1.GetInputRegistersInt(18)
		tractionEncoder = ExtData3.GetInpRegInt32(12)
		tillerAngle = ExtData3.GetInpRegFloat32(44)

		print str(tractionEncoder) + "\t" + str(tillerAngle)

		file.write( str(i) + '\t' + str(valVF) + '\t' + str(valVL) + '\t' + str(truckHeading) + '\t' + str(tractionEncoder) + '\t' + str(tillerAngle) + '\n' )
		time.sleep(0.5)

		file.close()		

		file = open("truckData.dat", "a")

	file.close()
	print "Training complete"
	#ExtData3.SetHRegStr16(100,30,"Training Route Complete")
	time.sleep(10)

	#		print "Here"
	#print "Here2"
	#Loop exits when program is terminated 
