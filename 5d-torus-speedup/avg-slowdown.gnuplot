set yrange [0:0.5]
set xlabel "FSO Links per Node"
set ylabel "Average Slowdown"
set key top right
#unset key
#set title "Average Slowdown"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\5d-torus-speedup\avg-slowdown.txt' using 2:xtic(1) title "without speedup"with linespoints pointtype 4 linewidth 2 pointsize 2, '' using 3 title "with speedup"with linespoints linewidth 2 pointsize 2

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\5d-torus-speedup\avg-slowdown.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\5d-torus-speedup\avg-slowdown.eps'  
replot
