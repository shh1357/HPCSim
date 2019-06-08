#set terminal png 18         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d.png'  

set term post eps color 16      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d.eps'  

set size 1,1
set origin 0,0
set multiplot

set size 0.5,1
set origin 0,0
set yrange [2100:3000]
set xlabel "FSO Links per Cabinet (16 Nodes/Cab)" font "Times-Roman,18"
set ylabel "Average Queuing Time (ms)"
set key top right
#unset key
#set title "Average Queuing Time (16 nodes per cabinet)"
set xtics ("0\%%" 0, "20\%%" 0.2, "25\%%" 0.25, "50\%%" 0.5, "100\%%" 1.0) font "Times-Roman,16"
#set xtics (0, 0.2, 0.25, 0.5, 1.0)
set xtics rotate by -60

#plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d-16.txt' using ($1):($2*1000) title "{/Times=14 GUEST,HOST(3D,4D)}"with linespoints linewidth 2 pointtype 4 pointsize 2, '' using ($1):($3*1000) title "{/Times=14 GUEST,HOST(4D,4D)}"with linespoints linewidth 2 pointtype 2 pointsize 2, '' using ($1):($4*1000) title "{/Times=14 GUEST,HOST(3D,5D)}"with linespoints linewidth 2 pointtype 8 pointsize 2, '' using ($1):($5*1000) title "{/Times=14 GUEST,HOST(5D,5D)}"with linespoints linewidth 2 pointtype 1 pointsize 2

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d-16-host4d.txt' using ($1):($2*1000) title "{/Times=14 GUEST,HOST(3D,4D)}"with linespoints linewidth 2 pointtype 4 pointsize 2, '' using ($1):($3*1000) title "{/Times=14 GUEST,HOST(4D,4D)}"with linespoints linewidth 2 pointtype 2 pointsize 2, 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d-16-host5d.txt' using ($1):($2*1000) title "{/Times=14 GUEST,HOST(3D,5D)}"with linespoints linewidth 2 pointtype 8 pointsize 2, '' using ($1):($3*1000) title "{/Times=14 GUEST,HOST(5D,5D)}"with linespoints linewidth 2 pointtype 1 pointsize 2

set size 0.5,1
set origin 0.5,0
set yrange [4000:4900]
set xlabel "FSO Links per Cabinet (32 Nodes/Cab)" font "Times-Roman,18"
set ylabel "Average Queuing Time (ms)"
set key top right
#unset key
#set title "Average Queuing Time (32 nodes per cabinet)"
set xtics ("0\%%" 0, "20\%%" 0.2, "25\%%" 0.25, "50\%%" 0.5, "100\%%" 1.0) font "Times-Roman,16"
#set xtics (0, 0.2, 0.25, 0.5, 1.0)
set xtics rotate by -60

#plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d-32.txt' using ($1):($2*1000) title "{/Times=14 GUEST,HOST(3D,4D)}"with linespoints linewidth 2 pointtype 4 pointsize 2, '' using ($1):($3*1000) title "{/Times=14 GUEST,HOST(4D,4D)}"with linespoints linewidth 2 pointtype 2 pointsize 2, '' using ($1):($4*1000) title "{/Times=14 GUEST,HOST(3D,5D)}"with linespoints linewidth 2 pointtype 8 pointsize 2, '' using ($1):($5*1000) title "{/Times=14 GUEST,HOST(5D,5D)}"with linespoints linewidth 2 pointtype 1 pointsize 2

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d-32-host4d.txt' using ($1):($2*1000) title "{/Times=14 GUEST,HOST(3D,4D)}"with linespoints linewidth 2 pointtype 4 pointsize 2, '' using ($1):($3*1000) title "{/Times=14 GUEST,HOST(4D,4D)}"with linespoints linewidth 2 pointtype 2 pointsize 2, 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d-32-host5d.txt' using ($1):($2*1000) title "{/Times=14 GUEST,HOST(3D,5D)}"with linespoints linewidth 2 pointtype 8 pointsize 2, '' using ($1):($3*1000) title "{/Times=14 GUEST,HOST(5D,5D)}"with linespoints linewidth 2 pointtype 1 pointsize 2


unset multiplot
reset