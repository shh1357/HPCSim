#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-speedup\2d-torus-speedup.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-speedup\2d-torus-speedup.eps'  

set size 1,1.5
set origin 0,0
set multiplot

set size 1,0.5
set origin 0,1
set yrange [0.3:0.7]
set xlabel "FSO Links per Node"
set ylabel "Overall System Uti."
set key top right
#unset key
set title "Overall System Utilization"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-speedup\overall-uti.txt' using 2:xtic(1) title "without speedup"with linespoints pointtype 4 linewidth 2 pointsize 2, '' using 3 title "with speedup"with linespoints linewidth 2 pointsize 2 

set size 1,0.5
set origin 0,0.5
set yrange [200:500]
set xlabel "FSO Links per Node"
set ylabel "Avg. Turnaround (s)"
set key top right
#unset key
set title "Average Turnaround Time"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-speedup\avg-turnaround.txt' using 2:xtic(1) title "without speedup"with linespoints pointtype 4 linewidth 2 pointsize 2, '' using 3 title "with speedup"with linespoints linewidth 2 pointsize 2

set size 1,0.5
set origin 0,0
set yrange [0:1.0]
set xlabel "FSO Links per Node"
set ylabel "Avg. Slowdown"
set key top right
#unset key
set title "Average Slowdown"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-speedup\avg-slowdown.txt' using 2:xtic(1) title "without speedup"with linespoints pointtype 4 linewidth 2 pointsize 2, '' using 3 title "with speedup"with linespoints linewidth 2 pointsize 2


unset multiplot
reset