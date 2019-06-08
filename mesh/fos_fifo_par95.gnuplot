set yrange [0:1]
set xlabel "Time Step (20s)"
set ylabel "System Utilization"
#set key box
#set key outside
set key c tm horizontal box
#unset key
#set title "wired vs. FSO"

#timestep=20s
plot [0:3347/2] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-30-15-36-08-555000_400_FIFO_normal_SDSC-Par-1995-3-1-cln-swf' using ($1/2):($4) every 2 title "Wired" with linespoints, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-30-16-33-48-216000_400_FIFO_FSO_SDSC-Par-1995-3-1-cln-swf' using ($1/2):($4) every 2 title "Wireless" with linespoints

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_par95.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\result_fifo_par95.eps'  
replot
