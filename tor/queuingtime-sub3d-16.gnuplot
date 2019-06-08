set yrange [2100:3000]
set xlabel "FSO Links per Node"
set ylabel "Average Queuing Time (ms)"
set key top right
#unset key
#set title "Average Queuing Time (16 nodes per cabinet)"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d-16.txt' using ($2*1000):xtic(1) title "sub,host(3d,4d)"with linespoints pointtype 4 linewidth 2 pointsize 2, '' using ($3*1000) title "sub,host(4d,4d)"with linespoints linewidth 2 pointsize 2, '' using ($4*1000) title "sub,host(3d,5d)"with linespoints linewidth 2 pointsize 2, '' using ($5*1000) title "sub,host(5d,5d)"with linespoints linewidth 2 pointsize 2

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d-16.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-sub3d-16.eps'  
replot
