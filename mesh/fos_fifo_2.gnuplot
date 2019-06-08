set yrange [0:1]
set xlabel "Time Step (20s)"
set ylabel "System Utilization"
#set key box
#set key outside
set key c tm horizontal box
#unset key
#set title "wired vs. FSO"

#timestep=20s
plot [0:3580*10/2/10/2] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-21-12-39-48-647000_4096_FIFO_normal_LLNL-Thunder-2007-1-1-cln-swf-2' using ($1*10/2/10/2):($4) every 4 title "Wired" with linespoints, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-21-13-43-52-481000_4096_FIFO_FSO_LLNL-Thunder-2007-1-1-cln-swf-2' using ($1*10/2/10/2):($4) every 4 title "Wireless" with linespoints

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_2.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_2.eps'  
replot
