set yrange [0:100]
#set xrange [0:10000]
set xlabel "Workloads"
set ylabel "Improvement for Inter-CPU/SSD(GPU) Connections (%)" font ",15"
set key bottom left
#unset key
#set title "Overall System Utilization"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\fat-tree-irs\fso-irs-repeat.txt' using ($2*100):xtic(1) title "1 FSO/Rack"with linespoints pointtype 2 linewidth 2 pointsize 3, '' using ($3*100) title "2 FSOs/Rack"with linespoints pointtype 4 linewidth 2 pointsize 3, '' using ($4*100) title "3 FSOs/Rack"with linespoints pointtype 8 linewidth 2 pointsize 3, '' using ($5*100) title "4 FSOs/Rack"with linespoints pointtype 7 linewidth 2 pointsize 3

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\fat-tree-irs\fso-irs-repeat.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"
#set term post eps color       
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\fat-tree-irs\fso-irs-repeat.eps'  
replot
