#set xrange [-1000:100000]
#set yrange [-10000:10000]
plot "truckplot.dat" using 1:2 with linespoints title "VF vs VL", "truckHeading.dat" using 1:2:3:4 with vectors title "Heading"
pause 1
reread
