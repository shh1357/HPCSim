set yrange [100:400]
set xlabel "FSO Links per Node"
set ylabel "Average Turnaround Time (s)"
set key top right
#unset key
#set title "Average Turnaround Time"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\5d-torus-speedup\avg-turnaround.txt' using 2:xtic(1) title "without speedup"with linespoints pointtype 4 linewidth 2 pointsize 2, '' using 3 title "with speedup"with linespoints linewidth 2 pointsize 2

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\5d-torus-speedup\avg-turnaround.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\5d-torus-speedup\avg-turnaround.eps'  
replot
