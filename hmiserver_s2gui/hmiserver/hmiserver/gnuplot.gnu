set xrange [-50000:50000]
set yrange [-50000:50000]
plot "truckplot.dat" using 1:2 with lines title "VF vs VL", "truckHeading.dat" using 1:2:3:4 with vectors title "Heading" ls 3
pause 1
reread
