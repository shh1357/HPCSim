set yrange [7.0:12.0]
set key top left font "GothicBBB-Medium-RKSJ-H, 11"
#set key c tm horizontal box font "GothicBBB-Medium-RKSJ-H, 13"
set grid
set style data histograms
#set style fill solid 1.00 border -1
set style fill pattern 3 border -1
#set title "Average Queuing Time (16 nodes per cabinet)"
#set xtics rotate by -5 font "GothicBBB-Medium-RKSJ-H, 20"
set xtics font "GothicBBB-Medium-RKSJ-H, 16"
set xlabel "Subtopology" font "GothicBBB-Medium-RKSJ-H, 16"
set ylabel "Inter-CPU Network Diameter" font ",16"

plot  'C:\Users\smallcat\Downloads\diameter-png.txt' using ($2):xtic(1) title "RS", '' using ($3) title "IRS-REPEAT, 0 FSO/rack, dilation=1", '' using ($4) title "IRS-REPEAT, 0 FSO/rack, dilation<=2", '' using ($5) title "IRS-REPEAT, 0 FSO/rack, dilation<=3", '' using ($6) title "IRS-REPEAT, 0 FSO/rack, dilation<=4", '' using ($7) title "IRS-LOOP, 0 FSO/rack, dilation=1", '' using ($8) title "IRS-LOOP, 1 FSO/rack, dilation=1", '' using ($9) title "IRS-LOOP, 2 FSOs/rack, dilation=1"
#, '' using ($10) title "IRS-LOOP, 2 FSOs/rack, dilation<=2", '' using ($11) title "IRS-LOOP, 2 FSOs/rack, dilation<=3", '' using ($12) title "IRS-LOOP, 2 FSOs/rack, dilation<=4"

set terminal png         # gnuplot recommends setting terminal before output
set output 'C:\Users\smallcat\Downloads\diameter-png.png'  

#set term post eps color "GothicBBB-Medium-RKSJ-H, 20"  
#set term post eps color     
#set output 'C:\Users\smallcat\Downloads\diameter-png.eps'  
replot
