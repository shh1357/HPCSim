set yrange [0:1]
set xlabel "Time Step"
set ylabel "System Utilization (%)"
#set key top right
unset key
set title "wired vs. FSO"

plot [0:800] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-20-14-38-35-111000_4096_FIFO_FSO' using 1:($4) title "FSO"  with linespoints, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-20-14-20-27-267000_4096_FIFO_normal' using 1:($4) title "wired" with linespoints

set terminal png         # gnuplot recommends setting terminal before output
set output 'C:\Users\smallcat\workspace\HPCSim\result_1.png'  

#set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
#set output 'C:\google drive\Google ドライブ\journal\cdf_rev.eps'  
replot
