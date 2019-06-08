set yrange [0.3:0.7]
set xlabel "FSO Links per Node"
set ylabel "Overall System Utilization"
set key top right
#unset key
#set title "Overall System Utilization"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-speedup\overall-uti.txt' using 2:xtic(1) title "without speedup"with linespoints pointtype 4 linewidth 2 pointsize 2, '' using 3 title "with speedup"with linespoints linewidth 2 pointsize 2 

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-speedup\overall-uti.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-speedup\overall-uti.eps'  
replot
