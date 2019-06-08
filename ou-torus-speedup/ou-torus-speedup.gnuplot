#2<->5
#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\ou-torus-speedup\ou-torus-speedup.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\ou-torus-speedup\ou-torus-speedup.eps'  

set size 1,1.5
set origin 0,0
set multiplot

set size 1,0.5
set origin 0,1
set yrange [0.3:0.7]
set xlabel "FSO Links per Node (2-D Torus)"
set ylabel "Overall Utilization" font "GothicBBB-Medium-RKSJ-H, 18"
set key top right
#unset key
#set title "Overall System Utilization"
set xtics (0, 1, 2, 3, 4)

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\ou-torus-speedup\2d-overall-uti.txt' using 1:2 title "without speedup" with linespoints linewidth 2 pointtype 2 pointsize 2, '' using 1:3 title "with speedup" with linespoints linewidth 2 pointtype 8 pointsize 2 

set size 1,0.5
set origin 0,0.5
set yrange [0.3:0.7]
set xlabel "FSO Links per Node (4-D Torus)"
set ylabel "Overall Utilization" font "GothicBBB-Medium-RKSJ-H, 18"
set key top right
#unset key
#set title "Overall System Utilization"
set xtics (0, 2, 4, 6, 8)

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\ou-torus-speedup\4d-overall-uti.txt' using 1:2 title "without speedup" with linespoints linewidth 2 pointtype 2 pointsize 2, '' using 1:3 title "with speedup" with linespoints linewidth 2 pointtype 8 pointsize 2 

set size 1,0.5
set origin 0,0
set yrange [0.3:0.7]
set xlabel "FSO Links per Node (5-D Torus)"
set ylabel "Overall Utilization" font "GothicBBB-Medium-RKSJ-H, 18"
set key top right
#unset key
#set title "Overall System Utilization"
set xtics (0, 2, 5, 8, 10)

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\ou-torus-speedup\5d-overall-uti.txt' using 1:2 title "without speedup" with linespoints linewidth 2 pointtype 2 pointsize 2, '' using 1:3 title "with speedup" with linespoints linewidth 2 pointtype 8 pointsize 2 


unset multiplot
reset