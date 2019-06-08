set yrange [0:1]
set xlabel "Time Step"
set ylabel "System Utilization (%)"
#set key top right
unset key
set title "wired vs. FSO"

plot [0:40000] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-21-14-18-57-437000_4096_BF_normal_LLNL-Thunder-2007-1-1-cln-swf' using ($1*10):($4) title "wired"  with linespoints, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-21-13-14-09-412000_4096_BF_FSO_LLNL-Thunder-2007-1-1-cln-swf' using ($1*10):($4) title "fso" with linespoints

set terminal png         # gnuplot recommends setting terminal before output
set output 'C:\Users\smallcat\workspace\HPCSim\result_bf.png'  

#set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
#set output 'C:\google drive\Google ドライブ\journal\cdf_rev.eps'  
replot
