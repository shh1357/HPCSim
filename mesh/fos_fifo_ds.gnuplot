set yrange [0:1]
set xlabel "Time Step (20s)"
set ylabel "System Utilization"
#set key box
#set key outside
set key c tm horizontal box
#unset key
#set title "wired vs. FSO"

plot [0:4810/2] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-28-15-03-37-018000_1681_FIFO_normal_SDSC-DS-2004-2-1-cln-swf' using ($1/2):($4) every 2 title "Wired" with linespoints, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-28-16-26-00-804000_1681_FIFO_FSO_SDSC-DS-2004-2-1-cln-swf' using ($1/2):($4) every 2 title "Wireless" with linespoints

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_ds.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_ds.eps'  
replot
