#Repo for exclusively running a S2 Modbus client

#Used for running on Truck's GOI

1. This repo has the required files to run a MODBUS client for the S2 HMI, which would connect to the Server on the Flagship truck's BeagleBone over the S2FlagshipWiFi.

2. This repo also has the necessary executables for the purple dot plotting and Train, Build, Follow. 

3. More details about these files and development notes are available in the developer's repo (which also includes this repo as a sub directory).


#Other notes

>>>>Be sure to check the mbhmi.config file while working with different servers.



#Steps to follow for client start up

1. Make sure you're in the "hmiserver" directory. (There are sub directories with the same name, to avoid confusion, the "hmiserver" directory mentioned here contains ".sh" files and ".config" files and will have no ".py" files.)
2. Start the hmiservermbc_custom_beaglewifi.sh (by either Double Click, or type "./hmiservermbc_custom_beaglewifi.sh" in the terminal, to start the client software. Before this step, the laptop/computer/GOI should be connected to the S2FlagshipWiFi (or be on the same network connected to the LAN switch via ethernet).
2. On the browser go to http://localhost:8084???????????????/s2o??build.xhtml to open the client HMI on the browser (fill ?? with latest build number).
3. Go into the hmiserver directory and and run " python hmiMBheartbeatclient.py " in terminal to start the heartbeat.
4. In the same directory run " python logXYdata.py " in the terminal to start logging the truck's xy position to file.
5. In the terminal run " gnuplot gnuplot.gnu " to start graphing the data which is updated every 1/2 second.
