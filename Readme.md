#################################################################
These are the notes for the work being done on the S2HMI
#################################################################


####S2GUI.svg#####

[x] The Digital and Analog inputs are to be included >>> Configure the Str buttons right >>>>>>>>>>Done

[x] Check if speed and angle buttons are configured correctly.>>>>>>>Done

[x] There was no id for the vertical display bar, check that.>>>>>>>>>Done

[x] Adjust graph dimensions!!!!!!!!! >>> Adjust timing and and sizes >>>>>>>>>>Done>>>To be changed after talking to Chun as per requirements later

[ ] Try configuring alarms and events

[X] Fix vertical column issue, if doesn't work, add two columns with different ranges >>>>>>>>>Done

[X] Reconfigure addresses after getting ones from Harsha. Save old file and do this in a new file.

[?] Cleanup unwanted items.

[X] Change graph width (x) to about 100 or 200, as it's very small now.

[X] Issues with communication, look into sourcecode.

[X] Check writing and reading a 32bit input/holding register.... Use the full program and in engg screen use the last address to be a 32 bit int.

[ ] Generalize the start of different py files like heartbeat and logdata to start with server parameters as set in the original client. > Get values from the client, or add everything on a sh file.


##############################################################
##Changes Made###
#############################################################

[ ] Check these and modify in this file.

#Modbusclient.py

>>def SetCoilsBool()

>>added SetCoils()

>>def SetHoldingRegistersInt()


#ModbusDatalib.py

>>def coilvalue()


##Other notes

>>>>>>Be sure to check the mbhmi.config file while working with different servers.



#Steps to follow for client start up

1. Start the hmiservermbc_custom.sh to start the client software.
2. On the browser go to http://localhost:8084/s2o??build.xhtml to open the client HMI on the browser (fill ?? with latest build number).
3. Go into the hmiserver directory and and run " python hmiMBheartbeatclient.py " in terminal to start the heartbeat.
4. In the same directory run " python logXYdata.py " in the terminal to start logging the truck's xy position to file.
5. In the terminal run " gnuplot gnuplot.gnu " to start graphing the data which is updated every 1/2 second.
