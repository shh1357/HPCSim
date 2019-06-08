set yrange [0.0:0.6]
#set xrange [0:10000]
set xlabel "Workloads"
set ylabel "Overall CPU Utilization"
set key top left
#unset key
#set title "Overall CPU Utilization"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\fat-tree-irs\overall-uti.txt' using 2:xtic(1) title "RS"with linespoints pointtype 2 linewidth 2 pointsize 3, '' using 3 title "IRS"with linespoints pointtype 4 linewidth 2 pointsize 3

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\fat-tree-irs\overall-uti.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
#set term post eps color 
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\fat-tree-irs\overall-uti.eps'  
replot
