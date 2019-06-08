set yrange [0.0:30.0]
#set xrange [0:10000]
set xlabel "Hops"
set ylabel "Execution Time Scale"
set key top left
#unset key
#set title "Overall CPU Utilization"

plot 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\time-hops\ssdgpu.txt' using 2:xtic(1) title "SSD Write" with linespoints pointtype 2 linewidth 2 pointsize 3, '' using 3 title "GPU Write"with linespoints pointtype 4 linewidth 2 pointsize 3

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\time-hops\ssdgpu.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
#set term post eps color 
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\time-hops\ssdgpu.eps'  
replot
