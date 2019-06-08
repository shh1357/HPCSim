#set terminal png 18         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queue-rev.png'  

set term post eps color 20      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queue-rev.eps'  

set size 1,1
set origin 0,0
set multiplot

set size 0.5,1
set origin 0,0
set yrange [0:120]
set xlabel "FSO Links per Node"
#set ylabel "No. of Queued Jobs"
set ylabel "Average Number of Queued Jobs"
#set key top right
unset key
#set title "Average Number of Queued Jobs"
set xtics (0, 2, 5, 8, 10)

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queued-jobs.txt' using ($1):($2) with points pointtype 8 pointsize 2 

#plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queued-jobs.txt' using ($1):($2) with points pointtype 7 pointsize 2 

set size 0.5,1
set origin 0.5,0
set yrange [0:150]
set xlabel "FSO Links per Node"
#set ylabel "Avg. Queuing Time (s)"
set ylabel "Average Queuing Time (s)"
#set key top right
unset key
#set title "Average Queuing Time"
set xtics (0, 2, 5, 8, 10)

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\torus-constant-fso-links-per-node\5dtorus-avg-queue-time.txt' using ($1):($2) with points pointtype 8 pointsize 2 


unset multiplot
reset