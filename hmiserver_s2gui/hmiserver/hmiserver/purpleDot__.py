##############################################################################
# Project: 	SeegridS2Client
# Module: 	hmimbclienthearbeat.py
# Purpose: 	Pass a heartbeat value as a client. to turn on and off a coil which is in sync with the MODBUS/TCP server.
# Language:	Python 2.5
# Date:		13-Sep-2013.
# Ver.:		13-Sep-2013.
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
_SOFTNAME = 'ModbusLogVehicleXYData'

# Version of this server.
_VERSION = '30-Aug-2013'

_HelpStr = """
%s, %s
This module logs the Vehicle Forward and Vehicle Lateral information which is calculated at the Server and stored in allocated InputRegisters as a Float Value. The data is logged into a .dat file which is in a format used by gnuplot, to give a plot of the path navigated by the truck.
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
PDClient1 = ModbusClient.DataTableAccess('10.0.0.100', 1502, 5.0, 1)

ExtData2 = ModbusExtData.ExtendedDataTypes(PDClient1)

############################################################



#file2 = open("truckHeading.dat","w")
#file2.write( "0" + '\t' + "0" + '\t' + "0" + '\t' + "0" + '\n' )
#file2.close()
choice = int(raw_input("\nEnter start position code: "))

file = open("truckPurple.dat","w")

while True:


	valVF = ExtData2.GetInpRegFloat32(20)
	valVL = ExtData2.GetInpRegFloat32(22)
	
	if choice is 1:		#bottom left corner and left turns >> VF is along graph x
		start_x = 780
		start_y = 625
		direction = 'xy'
	elif choice is 2:	#bottom left corner and right turns >> VF is along graph y
		#xy axis switched
		start_x = 625
		start_y = 780
		direction = 'yx'

	if direction is 'xy':
		x_map = (((valVF/228)*37)/10) + start_x
		y_map = -(((valVL/228)*37)/10) + start_y
	elif direction is 'yx':
		x_map = (((valVL/228)*37)/10) + start_y
		y_map = (((valVF/228)*37)/10) + start_x

	file.write( str(x_map) + '\t' + str(y_map) + '\n' )
	time.sleep(0.5)

	file.close()		

	os.system('cp truckPurple.dat purplePlot.dat')
	file = open("truckPurple.dat","a")			

#		print "Here"
#print "Here2"
#Loop exits when program is terminated 
