#set xrange [-20000:20000]
#set yrange [-20000:20000]
plot "truckplot.dat" using 1:2 with lines title "VF vs VL", "truckHeading.dat" using 1:2:3:4 with vectors title "Heading" ls 3
pause -1 "Hit any key to continue"
#reread
