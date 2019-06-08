set yrange [0:1]
set xlabel "Time Step (10s)"
set ylabel "System Utilization"
#set key box
#set key outside
#set key top right
unset key
#set title "Supercomputer Utilization"

plot [0:3580*10/2/10] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-21-12-39-48-647000_4096_FIFO_normal_LLNL-Thunder-2007-1-1-cln-swf-2' using ($1*10/2/10):($4) every 2 title "wired" with linespoints

set terminal png         # gnuplot recommends setting terminal before output
set output 'C:\Users\smallcat\workspace\HPCSim\fos_u.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\fos_u.eps'  
replot
