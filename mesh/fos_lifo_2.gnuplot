set yrange [0:1]
set xlabel "Time Step (20s)"
set ylabel "System Utilization"
#set key box
#set key outside
set key c tm horizontal box
#unset key
#set title "wired vs. FSO"

#timestep=20s
plot [0:3610*10/2/10/2] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-25-15-03-38-461000_4096_LIFO_normal_LLNL-Thunder-2007-1-1-cln-swf' using ($1*10/2/10/2):($4) every 4 title "Wired" with linespoints, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-25-13-38-44-070000_4096_LIFO_FSO_LLNL-Thunder-2007-1-1-cln-swf' using ($1*10/2/10/2):($4) every 4 title "Wireless" with linespoints

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\workspace\HPCSim\result_lifo_2.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\result_lifo_2.eps'  
replot
