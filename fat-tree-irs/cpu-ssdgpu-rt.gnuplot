set yrange [7.2:7.6]
set key top right
set grid
set style data histograms
#set style fill solid 1.00 border -1
set style fill pattern 3 border -1
#set title "Average Queuing Time (16 nodes per cabinet)"
#set xtics rotate by -30 font "GothicBBB-Medium-RKSJ-H, 20"
set xtics font "GothicBBB-Medium-RKSJ-H, 20"
set xlabel "Workloads" font "GothicBBB-Medium-RKSJ-H, 20"
set ylabel "Average Response Time (s)"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\fat-tree-irs\cpu-ssdgpu-rt.txt' using ($2):xtic(1) title "0 FSO/Rack", '' using ($3) title "1 FSO/Rack", '' using ($4) title "2 FSOs/Rack", '' using ($5) title "3 FSOs/Rack", '' using ($6) title "4 FSOs/Rack"

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\fat-tree-irs\cpu-ssdgpu-rt.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"  
#set term post eps color     
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\fat-tree-irs\cpu-ssdgpu-rt.eps'  
replot
