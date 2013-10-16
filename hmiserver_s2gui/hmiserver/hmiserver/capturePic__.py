##############################################################################
# Project: 	SeegridS2Client
# Module: 	capturePic.py
# Purpose: 	Capture an image of everything in front of the truck when a truck stops.
# Language:	Python 2.5
# Date:		15-Oct-2013.
# Ver.:		15-Oct-2013.
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
_SOFTNAME = 'ModbuscapturePic'

# Version of this server.
_VERSION = '30-Aug-2013'

_HelpStr = """
%s, %s
This module, when a truck stops, captures an image of the view in front of the truck from the axis camera at the IP 10.0.0.111 and saves it to a local folder. This is used to identify the reson for a truck stop.


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


PicClient = ModbusClient.DataTableAccess('10.0.0.100', 1502, 5.0, 1)


############################################################

while True:
	truckSpeed = PicClient.GetInputRegistersInt(16);
	 #Moniter speed, if it comes down to zero take a pic once and save, then start monitoring again when truck speed changes...

	while truckSpeed is not 0:
		#State1: Truck in Motion (Non-zero speed, except reverse)
		truckSpeed = PicClient.GetInputRegistersInt(16);

	os.system('wget -P ./StopPicCapture --user=root --password=root http://10.0.0.111/axis-cgi/jpg/image.cgi')
	#State2: First occurance of truck speed 0, after start up or after truck is at a non-zero speed. [Doesn't work for reverse, for now]
	time.sleep(0.5)

	while truckSpeed is 0:
		#State3: Truck speed still 0 and has not entered a non-zero speed state.
		truckSpeed = PicClient.GetInputRegistersInt(16);


#	if x % 7 is 0:


	
#Loop exits when program is terminated 
