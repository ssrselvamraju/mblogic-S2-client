#set xrange [-1000:100000]
#set yrange [-10000:10000]
plot "truckplot.dat" using 1:2 with linespoints
pause 1
reread
