#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 18"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime.eps'  

set size 1,1
set origin 0,0
set multiplot

set size 0.5,1
set origin 0,0
set yrange [2000:3200]
set key top left
set grid
set style data histograms
#set style fill solid 1.00 border -1
set style fill pattern 3 border -1
#set title "Average Queuing Time (16 nodes per cabinet)"
set xtics rotate by -30 font "GothicBBB-Medium-RKSJ-H, 16"
#set xtics font "GothicBBB-Medium-RKSJ-H, 10"
set xlabel "Inter-cabinet Topology (16 Nodes/Cab)" font "GothicBBB-Medium-RKSJ-H, 13"
set ylabel "Average Queuing Time (ms)"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-16-24exchange.txt' using ($2*1000):xtic(1) title "FSO-NONE", '' using ($3*1000) title "FSO-MINOR", '' using ($4*1000) title "FSO-HALF", '' using ($5*1000) title "FSO-ALL"

set size 0.5,1
set origin 0.5,0
set yrange [4000:4800]
set key top left
set grid
set style data histograms
#set style fill solid 1.00 border -1
set style fill pattern 3 border -1
#set title "Average Queuing Time (32 nodes per cabinet)"
set xtics rotate by -30 font "GothicBBB-Medium-RKSJ-H, 16"
#set xtics font "GothicBBB-Medium-RKSJ-H, 10"
set xlabel "Inter-cabinet Topology (32 Nodes/Cab)" font "GothicBBB-Medium-RKSJ-H, 13"
set ylabel "Average Queuing Time (ms)"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-32.txt' using ($2*1000):xtic(1) title "FSO-NONE", '' using ($3*1000) title "FSO-MINOR", '' using ($4*1000) title "FSO-HALF", '' using ($5*1000) title "FSO-ALL"

unset multiplot
reset
