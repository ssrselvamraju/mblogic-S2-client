
#In shell do this to copy lines to one file:
paste FileSFC1 FileSFC2 | awk '{print $1 $2 $3 $10 $11 $12}' > newFileSFC


#Gnuplotting for graphs:
1. Normal
plot "truckData.dat" using 5:6 with linespoints, "truckReplayStats1.dat" using 4:6 with linespoints, "truckData_replay1.dat" u 5:6 w lp
2. Stats
plot "routeStats.dat" using 2:4 with linespoints title "Actual", "routeStats.dat" using 2:5 with linespoints title "Set", "routeStats.dat" using 2:6 with linespoints title "Error"

#Datapuller.py sets up the data

