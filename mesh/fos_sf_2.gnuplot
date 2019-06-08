set yrange [0:1]
set xlabel "Time Step (20s)"
set ylabel "System Utilization"
set key c tm horizontal box
#unset key
#set title "wired vs. FSO"

#timestep=20s
plot [0:3940*10/2/10/2] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-21-22-13-38-544000_4096_SF_normal_LLNL-Thunder-2007-1-1-cln-swf-2' using ($1*10/2/10/2):($4) every 4 title "Wired"  with linespoints, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-21-23-02-22-572000_4096_SF_FSO_LLNL-Thunder-2007-1-1-cln-swf-2' using ($1*10/2/10/2):($4) every 4 title "Wireless" with linespoints

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\workspace\HPCSim\result_sf_2.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\workspace\HPCSim\result_sf_2.eps'  
replot
