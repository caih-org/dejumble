load "general.gnu.inc"
set output 'crearborrar.pdf'
set ylabel "Microsegundos"
set xlabel "Numero de archivos"

plot 'crearborrar.dat' using 2, '' using 3:xticlabels(1)


