set yrange [0.0:1.0]
set xlabel "Number of Requested CPUs (log2 N)"
set ylabel "CDF"
#set key top right
unset key
#set title "wired vs. FSO"
#set xtics ("0" 0, "1" 1, "2" 2, "4" 3, "8" 4, "16" 5, "32" 6, "64" 7, "128" 8, "256" 9, "512" 10, "1024" 11)

plot [0:8] 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\UniLu-Gaia-2014-2_jobs_cdf.txt' using 1:2  with linespoints linecolor 3 linewidth 2 pointtype 7 pointsize 2 

#set terminal png         # gnuplot recommends setting terminal before output
#set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\UniLu-Gaia-2014-2_jobs_cdf.png'  

set term post eps color #"GothicBBB-Medium-RKSJ-H, 20"      
set output 'C:\Users\smallcat\Dropbox\eclipse\common_workspace\HPCSim\UniLu-Gaia-2014-2_jobs_cdf.eps'  
replot
