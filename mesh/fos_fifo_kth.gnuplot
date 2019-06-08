set yrange [0:1]
set xlabel "Time Step (20s)"
set ylabel "System Utilization"
#set key box
#set key outside
#set key top right
set key c tm horizontal box
#unset key
#set title "wired vs. FSO"


#timestep=20s
plot [0:3855/2] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-28-18-48-47-964000_100_FIFO_normal_KTH-SP2-1996-2-1-cln-swf' using ($1/2):($4) every 2 title "Wired" with linespoints, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-28-20-37-14-120000_100_FIFO_FSO_KTH-SP2-1996-2-1-cln-swf' using ($1/2):($4) every 2 title "Wireless" with linespoints

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_kth.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_kth.eps'  
replot
