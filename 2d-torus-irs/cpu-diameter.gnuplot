#set yrange [0.0:40.0]
#set xrange [0:10000]
#set xlabel "Workloads"
#set ylabel "Inter-CPU/SSD(GPU) Hops for IRS-REPEAT"
#set key top right
#unset key
#set title "Overall System Utilization"

#plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-irs\cpu-ssdgpu.txt' using 2:xtic(1) title "0 FSO per Rack"with linespoints pointtype 2 linewidth 2 pointsize 2, '' using 3 title "1 FSO per Rack"with linespoints pointtype 4 linewidth 2 pointsize 2, '' using 4 title "2 FSOs per Rack"with linespoints pointtype 8 linewidth 2 pointsize 2, '' using 5 title "3 FSOs per Rack"with linespoints pointtype 1 linewidth 2 pointsize 2, '' using 6 title "4 FSOs per Rack"with linespoints pointtype 6 linewidth 2 pointsize 2

set yrange [4.0:16.0]
set key top right
set grid
set style data histograms
#set style fill solid 1.00 border -1
set style fill pattern 3 border -1
#set title "Average Queuing Time (16 nodes per cabinet)"
#set xtics rotate by -30 font "GothicBBB-Medium-RKSJ-H, 20"
set xtics font "GothicBBB-Medium-RKSJ-H, 20"
set xlabel "Workloads" font "GothicBBB-Medium-RKSJ-H, 20"
set ylabel "Average Diameter of Inter-CPU Networks"

plot  'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-irs\cpu-diameter.txt' using ($2):xtic(1) title "RS", '' using ($3) title "IRS-REPEAT", '' using ($4) title "IRS-LOOP (0 FSO/Rack)", '' using ($5) title "IRS-LOOP (1 FSO/Rack)", '' using ($6) title "IRS-LOOP (2 FSOs/Rack)"

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-irs\cpu-diameter.png'  

set term post eps color "GothicBBB-Medium-RKSJ-H, 20"      
#set term post eps color 
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\2d-torus-irs\cpu-diameter.eps'  
replot
