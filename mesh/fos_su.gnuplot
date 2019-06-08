set yrange [0:1]
set key top right
set grid
set style data histograms
set style fill solid 1.00 border -1
#set title "System Utilization"
set xlabel "Scheduling"
set ylabel "System Utilization"
plot  'C:\Users\smallcat\workspace\HPCSim\su.txt' using 2:xtic(1)  title "Wired", '' using 3 title "Wireless"

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\workspace\HPCSim\su.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\result_su.eps'  

replot
