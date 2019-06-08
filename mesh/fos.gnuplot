set yrange [0:1]
set xlabel "Time Step"
set ylabel "System Utilization (%)"
#set key top right
unset key
set title "wired vs. FSO"

plot [0:300] 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-19-15-38-41-005000' using 1:($4) title "FSO"  with impulses, 'C:\Users\smallcat\workspace\HPCSim\stat_su_2015-08-19-15-34-24-858000' using 1:($4) title "wired" with impulses

set terminal png         # gnuplot recommends setting terminal before output
set output 'C:\Users\smallcat\workspace\HPCSim\result1.png'  

#set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
#set output 'C:\google drive\Google ドライブ\journal\cdf_rev.eps'  
replot
