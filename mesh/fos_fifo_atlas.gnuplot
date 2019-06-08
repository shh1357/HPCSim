set yrange [0:1]
set xlabel "Time Step (20s)"
set ylabel "System Utilization"
#set key box
#set key outside
set key c tm horizontal box
#unset key
#set title "wired vs. FSO"

#timestep=20s
plot [0:2122/2] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-28-11-17-16-492000_9216_FIFO_normal_LLNL-Atlas-2006-2-1-cln-swf' using ($1/2):($4) every 2 title "Wired" with linespoints, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-28-11-58-59-850000_9216_FIFO_FSO_LLNL-Atlas-2006-2-1-cln-swf' using ($1/2):($4) every 2 title "Wireless" with linespoints

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_atlas.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_atlas.eps'  
replot
