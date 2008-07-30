load "general.gnu.inc"
set output FILE.'.pdf'
set ylabel "Microsegundos"
set xlabel "Tamaño del archivo"

plot FILE.'.dat' using 2, '' using 3:xticlabels(1)


