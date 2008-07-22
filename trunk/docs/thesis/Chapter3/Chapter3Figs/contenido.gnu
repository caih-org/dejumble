load "general.gnu.inc"
set output 'contenido.pdf'
set ylabel "Microsegundos"
set xlabel "Tamaño del archivo"

plot 'contenido.dat' using 2, '' using 3:xticlabels(1)


