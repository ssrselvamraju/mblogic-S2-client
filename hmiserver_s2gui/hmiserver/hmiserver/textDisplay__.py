##############################################################################
# Project: 	SeegridS2Client
# Module: 	textDisplay__.py
# Purpose: 	Displays text instructions on the AutoMode screen of the Client HMI.
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
_SOFTNAME = 'textDisplay'

# Version of this server.
_VERSION = '15-November-2013'

_HelpStr = """
%s, %s
This module diplays Text Instructions on the HMI screen based on different states of the robot. Text is written to holding resiter 100 to 100+lenght of string storing 1 character in each register.
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


textDisplayClient1 = ModbusClient.DataTableAccess('10.0.0.100', 1502, 5.0, 1)

ExtData6 = ModbusExtData.ExtendedDataTypes(textDisplayClient1)

############################################################


#record_mode = int(raw_input("Enter 0 to record Train, and 1 to record Replay: "))

while True:

	ExtData6.SetHRegStr16(100,30,"Welcome to S2!")
	
	time.sleep(5)

	train_mode = textDisplayClient1.GetCoilsBool(31) #1 for train start, 0 for train stop

	replay_mode =  textDisplayClient1.GetCoilsBool(32)

	if train_mode == 0 and replay_mode == 0:
		state = "Training not started" #Conditions train_mode = 0, replay_mode = 0, coils have never changed before, start state, or end of loop reached and comes back here.
		ExtData6.SetHRegStr16(100,30,"Press Start to Train Route")
	
	while train_mode == 0 and replay_mode == 0:
		train_mode = textDisplayClient1.GetCoilsBool(31) #1 for train start, 0 for train stop
		replay_mode =  textDisplayClient1.GetCoilsBool(32)

	if train_mode == 1 and replay_mode == 0:
		state = "Training started" #Contions: train_mode = 1 (ensure replay is 0, have a lock on replay_mode), next state cannot be "Replay in Action" 
		ExtData6.SetHRegStr16(100,30,"Training Started")
		
		time.sleep(3)

		while train_mode:
			train_mode = textDisplayClient1.GetCoilsBool(31)
			ExtData6.SetHRegStr16(100,30,"Training in Progress")
			time.sleep(3)
			ExtData6.SetHRegStr16(100,30,"Move truck at a slow const speed")
			time.sleep(3)
		state = "Training complete" #Conditions: train_mode changes from 1 to 0, replay_mode still held at zero, this is next state of "Training started", cannot have any other previous state.
		ExtData6.SetHRegStr16(100,30,"Training Complete. Please wait.")

	time.sleep(5)
		
	train_mode = textDisplayClient1.GetCoilsBool(31)
	replay_mode =  textDisplayClient1.GetCoilsBool(32)

	while train_mode == 0 and train_mode == 0:
		train_mode = textDisplayClient1.GetCoilsBool(31)
		replay_mode =  textDisplayClient1.GetCoilsBool(32)
		ExtData6.SetHRegStr16(100,30,"Take truck to start position")
		time.sleep(3)
		ExtData6.SetHRegStr16(100,30,"Press Replay when ready")
		time.sleep(3)

	if train_mode == 0 and replay_mode == 1:
		state = "Replay in Action" # conditions: Previous mode is "Training Complete", or Training not started (in this case, replay of last trained route will occur), replay_mode = 1, (hold train_mode at 0)
		ExtData6.SetHRegStr16(100,30,"Replay Started")
		time.sleep(3)
		while replay_mode:
			replay_mode = textDisplayClient1.GetCoilsBool(32)
			ExtData6.SetHRegStr16(100,30,"Truck in motion")
			time.sleep(3)
			ExtData6.SetHRegStr16(100,30,"Stay away from the robot")
			time.sleep(3)
		
		state = "Replay Complete" #Conditions: Previous mode is "Replay in Action", train_mode = 0 and replay_mode = 0
		ExtData6.SetHRegStr16(100,30,"Replay complete. Truck is at end point")	

	time.sleep(6)
		
		

