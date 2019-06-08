set yrange [0:150]
set xlabel "FSO Links per Node"
set ylabel "Average Queuing Time (s)"
#set key top right
unset key
#set title "Average Queuing Time"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queue-time.txt' using 2:xtic(1) with linespoints linewidth 2 pointtype 4 pointsize 2 

#set terminal png 18         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queue-time.png'  

set term post eps color 20      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queue-time.eps'  
replot
