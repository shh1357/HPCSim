set yrange [0:250]
set key top right
set grid
set style data histograms
#set style fill solid 1.00 border -1
set style fill pattern 3 border -1
#set title "Queuing Time"
#set xtics rotate by -30
set xlabel "Topology"
set ylabel "Queuing Time (s)"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\queuingtime.txt' using 2:xtic(1) title "Wired", '' using 3 title "FSO-20%", '' using 4 title "FSO-50%", '' using 5 title "FSO-80%", '' using 6 title "Ideal FSO"

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\queuingtime.png'  

set term post eps color #"GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\queuingtime.eps'  

replot