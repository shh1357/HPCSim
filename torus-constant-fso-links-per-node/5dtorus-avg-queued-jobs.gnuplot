set yrange [0:120]
set xlabel "FSO Links per Node"
set ylabel "Average Number of Queued Jobs"
#set key top right
unset key
#set title "Average Number of Queued Jobs"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queued-jobs.txt' using 2:xtic(1) with linespoints linewidth 2 pointtype 4 pointsize 2 

#plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queued-jobs.txt' using 2:xtic(1) with linespoints linecolor 3 linewidth 2 pointtype 7 pointsize 2 

#set terminal png 18         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queued-jobs.png'  

set term post eps color 20      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queued-jobs.eps'  
replot
