set yrange [2000:3000]
set key top left
set grid
set style data histograms
#set style fill solid 1.00 border -1
set style fill pattern 3 border -1
#set title "Average Queuing Time (16 nodes per cabinet)"
#set xtics rotate by -30
set xlabel "Topology"
set ylabel "Average Queuing Time (ms)"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-16.txt' using ($2*1000):xtic(1) title "FSO-0%", '' using ($3*1000) title "FSO-20%", '' using ($4*1000) title "FSO-50%", '' using ($5*1000) title "FSO-100%"

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-16.png'  

set term post eps color #"GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\tor\queuingtime-16.eps'  

replot