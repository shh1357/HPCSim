set yrange [0:25000]
set key top right
set grid
set style data histograms
set style fill solid 1.00 border -1
#set title "Simulation Time"
set xlabel "Scheduling"
set ylabel "Service Time (s)"
plot  'C:\Users\smallcat\workspace\HPCSim\time.txt' using 2:xtic(1)  title "Wired", '' using 3 title "Wireless"

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\workspace\HPCSim\time.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\result_time.eps'  

replot
