set title "Crater H1B1: 5 km deep, 5 km base radius"
plot "processed_74_sum.txt" using 1:3:($3*$4/100.0):xtic(2) title 'Apex' with yerrorbars, \
     "processed_76_sum.txt" using 1:2:($2*$3/100.0) title 'Half-way up' with yerrorbars, \
     "processed_78_sum.txt" using 1:2:($2*$3/100.0) title 'Edge of base' with yerrorbars, \
     "processed_80_sum.txt" using 1:2:($2*$3/100.0) title 'Half the depth away from base' with yerrorbars
#set xtics ("pro" 1, "neu" 2, "elec" 3, "pos" 4, "mu" 5, "pi" 6, "pho" 7, "He-3" 8, "He-4" 9, "tri" 10, "deu" 11, "Cr-52" 12)
set grid ytics lc 8 lw 1 
set ylabel "particles/cm^3/primary"
set logscale y
set format y '10^{%3T}'
set yrange [1e-14: 1e-7]
set tics out
set terminal png 
unset output
set output "h1b1.png"
replot
