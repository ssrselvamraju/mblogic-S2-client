##############################################################################
# Project: 	SeegridS2Client
# Module: 	hmimbclienthearbeat.py
# Purpose: 	Pass a heartbeat value as a client. to turn on and off a coil which is in sync with the MODBUS/TCP server.
# Language:	Python 2.5
# Date:		30-Aug-2013.
# Ver.:		30-Aug-2013.
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
_SOFTNAME = 'ModbusLogEncoderData'

# Version of this server.
_VERSION = '30-Aug-2013'

_HelpStr = """
%s, %s
This module passes a heartbeat value as a client to turn on and off a coil which should be sync with the MODBUS/TCP server heartbeat monitor. In case of powerloss or wifi disconnect the heartbeat is lost and the server terminates any critical functions to ensure safety.
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

import ModbusClient
import HMIServerCommon


############################################################

# Get the command line parameter options.
#CmdOpts = HMIServerCommon.GetOptionsClient(502, _HelpStr)


############################################################


# Initialise the client. First get the remote host parameters.
#hbhost, hbport, hbtimeout, hbunitid = CmdOpts.GetRemoteParams()


#Initialize an instance of the ModbusClient.DataTableAccess to initialize this client.

#HBClient = ModbusClient.DataTableAccess(hbhost, hbport, hbtimeout, hbunitid)

HBClient1 = ModbusClient.DataTableAccess('192.168.10.237', 1502, 5.0, 1)

############################################################

#Loop to keep the heartbeat alive

file = open("truckxy.dat","w")
with open("truckxy.dat","w") as file:
	while True:
		valX = HBClient1.GetInputRegistersInt(14)
		valY = HBClient1.GetInputRegistersInt(15)	
		file.write( str(valX) + '\t' + str(valY) + '\n' )
		time.sleep(0.5)
#		print "Here"
#print "Here2"
#Loop exits when program is terminated 
