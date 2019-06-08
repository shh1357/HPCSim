set yrange [0.0:1.0]
set key top right font "GothicBBB-Medium-RKSJ-H, 16"
#set key c tm horizontal box font "GothicBBB-Medium-RKSJ-H, 13"
set grid
set style data histograms
#set style fill solid 1.00 border -1
set style fill pattern 3 border -1
#set title "Average Queuing Time (16 nodes per cabinet)"
#set xtics rotate by -5 font "GothicBBB-Medium-RKSJ-H, 20"
set xtics font "GothicBBB-Medium-RKSJ-H, 20"
set xlabel "Subtopology" font "GothicBBB-Medium-RKSJ-H, 20"
set ylabel "Average Turnaround Time (s)" font ",20"

#set border 3
#number of columns to be plotted
N=8
#vertical offset
OFFSET=0
#gapwidth (set to gnuplot's default)
GW=2
xbox(x,i)=x+(i-N*0.5)/(N+GW)
set boxwidth 0.9
set tics nomirror out scale 0.75
set style fill solid 0.8

plot  '/Users/smallcat/gnuplot/tat.txt' using ($2):xtic(1) title "RS" fillstyle pattern 0, '' using ($3) title "IRS-REPEAT, 0 FSO/rack, dilation=1" fillstyle pattern 1, '' using ($4) title "IRS-REPEAT, 0 FSO/rack, dilation<=2" fillstyle pattern 2, '' using ($5) title "IRS-REPEAT, 0 FSO/rack, dilation<=3" fillstyle pattern 3, '' using ($6) title "IRS-REPEAT, 0 FSO/rack, dilation<=4" fillstyle pattern 4, '' using ($7) title "IRS-LOOP, 0 FSO/rack, dilation=1" fillstyle pattern 5, '' using ($8) title "IRS-LOOP, 1 FSO/rack, dilation=1" fillstyle pattern 6, '' using ($9) title "IRS-LOOP, 2 FSOs/rack, dilation=1" fillstyle pattern 7, '/Users/smallcat/gnuplot/queue.txt' using (xbox($0,1)):($2+OFFSET) title "queuing time" with points pt 9 lc rgb"black", '' using (xbox($0,2)):($3+OFFSET) notitle with points pt 9 lc rgb"black", '' using (xbox($0,3)):($4+OFFSET) notitle with points pt 9 lc rgb"black", '' using (xbox($0,4)):($5+OFFSET) notitle with points pt 9 lc rgb"black", '' using (xbox($0,5)):($6+OFFSET) notitle with points pt 9 lc rgb"black", '' using (xbox($0,6)):($7+OFFSET) notitle with points pt 9 lc rgb"black", '' using (xbox($0,7)):($8+OFFSET) notitle with points pt 9 lc rgb"black", '' using (xbox($0,8)):($9+OFFSET) notitle with points pt 9 lc rgb"black"
#, '' using ($10) title "IRS-LOOP, 2 FSOs/rack, dilation<=2", '' using ($11) title "IRS-LOOP, 2 FSOs/rack, dilation<=3", '' using ($12) title "IRS-LOOP, 2 FSOs/rack, dilation<=4"

#plot  '/Users/smallcat/gnuplot/queue.txt' using ($2):xtic(1) notitle with linespoints, '' using ($3) notitle with linespoints, '' using ($4) notitle with linespoints, '' using ($5) notitle with linespoints, '' using ($6) notitle with linespoints, '' using ($7) notitle with linespoints, '' using ($8) notitle with linespoints, '' using ($9) notitle with linespoints

#set terminal png         # gnuplot recommends setting terminal before output
#set output '/Users/smallcat/gnuplot/tat-queue.png'  

#set term post eps color "GothicBBB-Medium-RKSJ-H, 20"  
#set term post eps color  
set terminal postscript eps 20   
set output '/Users/smallcat/gnuplot/tat-queue.eps'  
replot
