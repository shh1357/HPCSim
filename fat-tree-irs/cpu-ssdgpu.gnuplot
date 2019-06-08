set yrange [0.0:8.0]
set key top left
set grid
set style data histograms
#set style fill solid 1.00 border -1
set style fill pattern 3 border -1
#set title "Average Queuing Time (16 nodes per cabinet)"
#set xtics rotate by -30 font "GothicBBB-Medium-RKSJ-H, 20"
set xtics font "GothicBBB-Medium-RKSJ-H, 20"
set xlabel "Workload Size (\# of Dispatched Jobs)" font "GothicBBB-Medium-RKSJ-H, 20"
set ylabel "Average Inter-CPU/SSD(GPU) Hop Count"

plot  '/Users/smallcat/gnuplot/cpu-ssdgpu.txt' using ($2):xtic(1) title "0 FSO/Rack", '' using ($3) title "1 FSO/Rack", '' using ($4) title "2 FSOs/Rack", '' using ($5) title "3 FSOs/Rack", '' using ($6) title "4 FSOs/Rack"

#set terminal png         # gnuplot recommends setting terminal before output
#set output '/Users/smallcat/gnuplot/cpu-ssdgpu.png'  

set terminal postscript eps color "GothicBBB-Medium-RKSJ-H, 20"
#set term post eps color      
set output '/Users/smallcat/gnuplot/cpu-ssdgpu.eps'  
replot
